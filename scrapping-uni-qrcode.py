import base64
import binascii
import os
from pathlib import Path

from seleniumbase import SB


OUTPUT = Path("imagem_convertida.jpg")


def decode_qr_image(src):
    header, separator, payload = (src or "").partition(",")
    if not separator or not header.startswith("data:image/") or not header.endswith(";base64"):
        raise ValueError("O portal não retornou uma imagem do QR Code em base64.")
    try:
        image = base64.b64decode(payload, validate=True)
    except binascii.Error as error:
        raise ValueError("A imagem do QR Code contém base64 inválido.") from error
    if not image:
        raise ValueError("A imagem do QR Code está vazia.")
    return image


def login_ceub(url):
    # O checkout pode trazer uma imagem antiga. Ela nunca comprova uma coleta nova.
    OUTPUT.unlink(missing_ok=True)
    ra = os.environ.get("RA_ESPACO_ALUNO")
    senha = os.environ.get("SENHA_ESPACO_ALUNO")
    if not ra or not senha:
        raise RuntimeError("Configure os secrets RA_ESPACO_ALUNO e SENHA_ESPACO_ALUNO.")

    with SB(uc=True, headless=True) as sb:
        try:
            sb.goto(url)
            sb.type("#coAcesso", ra)
            sb.type("#coSenha", senha)
            sb.click("#btn-login")
            try:
                sb.wait_for_element("#masterfab", timeout=20)
            except Exception as error:
                raise RuntimeError(
                    "Login não concluído. Verifique a captura de tela: o portal pode "
                    "exigir CAPTCHA, rejeitar as credenciais ou estar indisponível."
                ) from error

            print("Login concluído. Esperando o servidor gerar o QR Code...")
            sb.sleep(10)
            sb.execute_script("ShowQrCode();")
            sb.wait_for_element("#imgQRCode", timeout=20)
            for _ in range(15):
                sb.sleep(1)
                src = sb.get_attribute("#imgQRCode", "src") or ""
                if src.startswith("data:image/") and ";base64," in src:
                    image = decode_qr_image(src)
                    OUTPUT.write_bytes(image)
                    print("QR Code obtido nesta execução e salvo em imagem_convertida.jpg.")
                    return
            raise RuntimeError("O portal não gerou uma imagem base64 do QR Code em 15 tentativas.")
        except Exception:
            # Inclui erros anteriores ao clique de login e durante a geração da imagem.
            OUTPUT.unlink(missing_ok=True)
            try:
                sb.save_screenshot("tela_do_erro.png")
                print("Captura do erro salva como tela_do_erro.png.")
            except Exception:
                print("Não foi possível salvar a captura do erro.")
            raise


if __name__ == "__main__":
    login_ceub("https://ea.uniceub.br/")

