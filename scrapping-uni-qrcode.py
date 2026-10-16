from seleniumbase import SB
import base64
import os

ra_espaco_aluno = os.environ.get('RA_ESPACO_ALUNO')
senha_espaco_aluno = os.environ.get('SENHA_ESPACO_ALUNO')

def login_ceub(url):
    print("Iniciando navegador...")
    with SB(uc=True, headless=True) as sb:
        sb.goto(url)
        
        print("Preenchendo credenciais...")
        sb.type('#coAcesso', ra_espaco_aluno)
        sb.type('#coSenha', senha_espaco_aluno)
        sb.click('#btn-login')
        
        print("Aguardando carregamento da área do aluno...")
        try:
            # Espera 20 segundos para ver se consegue passar do login
            sb.wait_for_element('#masterfab', timeout=20)
            print("Passou do login!")
        except Exception:
            print("ERRO: O robô não conseguiu logar (provavelmente preso no CAPTCHA).")
            sb.save_screenshot("erro_login.png")
            print("Print salvo como erro_login.png")
            return # Para o código aqui
        
        sb.sleep(2)
        sb.execute_script("ShowQrCode();")
        
        print("Aguardando imagem...")
        qr_code_base64_raw = ""
        
        # Espera a imagem carregar
        for tentativa in range(15):
            sb.sleep(1)
            src_atual = sb.get_attribute('#imgQRCode', 'src')
            if src_atual and "base64" in src_atual:
                qr_code_base64_raw = src_atual
                break
                
        if "," in qr_code_base64_raw:
            qr_code_base64 = qr_code_base64_raw.split(",")[1]
            imagem_bytes = base64.b64decode(qr_code_base64)
            with open("imagem_convertida.jpg", "wb") as arquivo_jpg:
                arquivo_jpg.write(imagem_bytes)
            print("SUCESSO: Imagem JPG salva!")
            sb.save_screenshot("sucesso.png")
        else:
            print("ERRO: A imagem não carregou a tempo.")

if __name__ == "__main__":
    login_ceub("https://ea.uniceub.br/")