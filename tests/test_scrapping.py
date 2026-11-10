import base64
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch


# A unidade testada é o tratamento dos resultados; nenhum teste acessa o portal.
spec = importlib.util.spec_from_file_location(
    "scrapping", Path(__file__).resolve().parents[1] / "scrapping-uni-qrcode.py"
)
scrapping = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"seleniumbase": types.SimpleNamespace(SB=MagicMock())}):
    spec.loader.exec_module(scrapping)


class ScrappingTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.output = Path(directory.name) / "imagem_convertida.jpg"
        self.output.write_bytes(b"old-image")
        output_patch = patch.object(scrapping, "OUTPUT", self.output)
        output_patch.start()
        self.addCleanup(output_patch.stop)
        env_patch = patch.dict(
            os.environ, {"RA_ESPACO_ALUNO": "test-ra", "SENHA_ESPACO_ALUNO": "test-password"}
        )
        env_patch.start()
        self.addCleanup(env_patch.stop)
        browser_patch = patch.object(scrapping, "SB")
        self.factory = browser_patch.start()
        self.addCleanup(browser_patch.stop)
        self.sb = self.factory.return_value.__enter__.return_value

    def test_missing_credentials_removes_old_image_and_fails(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "secrets"):
                scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())
        self.factory.assert_not_called()

    def test_login_failure_is_not_reported_as_success(self):
        self.sb.wait_for_element.side_effect = TimeoutError("login timeout")
        with self.assertRaisesRegex(RuntimeError, "Login não concluído"):
            scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())
        self.sb.save_screenshot.assert_called_once_with("tela_do_erro.png")
        self.sb.execute_script.assert_not_called()

    def test_navigation_failure_also_saves_debug_screenshot(self):
        self.sb.goto.side_effect = RuntimeError("navigation failure")
        with self.assertRaisesRegex(RuntimeError, "navigation failure"):
            scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())
        self.sb.save_screenshot.assert_called_once()

    def test_screenshot_failure_does_not_hide_login_failure(self):
        self.sb.wait_for_element.side_effect = TimeoutError("login timeout")
        self.sb.save_screenshot.side_effect = OSError("screenshot failure")
        with self.assertRaisesRegex(RuntimeError, "Login não concluído"):
            scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())

    def test_missing_qr_code_fails_without_reusing_old_image(self):
        self.sb.get_attribute.return_value = None
        with self.assertRaisesRegex(RuntimeError, "15 tentativas"):
            scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())
        self.assertEqual(self.sb.get_attribute.call_count, 15)
        self.sb.save_screenshot.assert_called_once()

    def test_invalid_payloads_fail(self):
        for src in (None, "https://example.test/image.png", "data:image/png;base64,", "data:image/png;base64,!"):
            with self.subTest(src=src):
                with self.assertRaises(ValueError):
                    scrapping.decode_qr_image(src)

    def test_invalid_base64_leaves_no_output(self):
        self.sb.get_attribute.return_value = "data:image/png;base64,!"
        with self.assertRaisesRegex(ValueError, "base64 inválido"):
            scrapping.login_ceub("https://example.test")
        self.assertFalse(self.output.exists())
        self.sb.save_screenshot.assert_called_once()

    def test_success_writes_new_image_after_waiting_for_src(self):
        image = b"new-image"
        src = "data:image/png;base64," + base64.b64encode(image).decode("ascii")
        self.sb.get_attribute.side_effect = [None, src]
        scrapping.login_ceub("https://example.test")
        self.assertEqual(self.output.read_bytes(), image)
        self.sb.save_screenshot.assert_not_called()
        self.sb.execute_script.assert_called_once_with("ShowQrCode();")


if __name__ == "__main__":
    unittest.main()
