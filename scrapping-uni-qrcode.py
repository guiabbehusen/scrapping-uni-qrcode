from seleniumbase import sb_cdp
from seleniumbase import SB
import base64
import os

ra_espaco_aluno = os.environ.get('RA_ESPACO_ALUNO')
senha_espaco_aluno = os.environ.get('SENHA_ESPACO_ALUNO')

def bypass_captcha_on_url(url):
    sb = sb_cdp.Chrome()
    sb.goto(url)


    sb.type('#coAcesso', ra_espaco_aluno)
    sb.type('#coSenha', senha_espaco_aluno)
    sb.click('#btn-login')

    sb.sleep(3)
    sb.quit()



def login_ceub(url):
    
    with SB(uc=True, headless=True) as sb:
        sb.goto(url)
        sb.type('#coAcesso', ra_espaco_aluno)
        sb.type('#coSenha', senha_espaco_aluno)
        sb.click('#btn-login')
        
        try:
                    # TRY: O robô "tenta" esperar o botão da carteirinha aparecer na tela.
                    # timeout=20 dá a ele 20 segundos de paciência antes de desistir.
                    sb.wait_for_element('#masterfab', timeout=20)
                    print("Sucesso! Passou do login e achou o botão.")
                    
        except Exception as erro:
            print("ERRO: O robô travou na tela de login (provavelmente bloqueio de CAPTCHA).")

            sb.save_screenshot("tela_do_erro.png")
            print("Uma foto da tela foi salva como 'tela_do_erro.png'")

            return
        
        print("Esperando o servidor gerar o QR Code...")
        sb.sleep(10)
        sb.execute_script("ShowQrCode();")

        qr_code_base64_raw = ""
        for tentativa in range(15):
            sb.sleep(1)
            qr_code_base64_raw = sb.get_attribute('#imgQRCode', 'src') or ""
            
            if "base64" in qr_code_base64_raw:
                break

        qr_code_base64_raw = sb.get_attribute('#imgQRCode', 'src')
        
        if "," in qr_code_base64_raw:
            qr_code_base64 = qr_code_base64_raw.split(",")[1]

            imagem_bytes = base64.b64decode(qr_code_base64)
            with open("imagem_convertida.jpg", "wb") as arquivo_jpg:
                arquivo_jpg.write(imagem_bytes)
            print("O format esta correto")
        else:
            print ("o formato nao é base 64")
            print(qr_code_base64_raw)
        print("Imagem JPG salva com sucesso!")
            


if __name__ == "__main__":
    login_ceub("https://ea.uniceub.br/")

