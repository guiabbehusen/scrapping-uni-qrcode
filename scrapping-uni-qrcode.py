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
    sb.solve_captcha()
    sb.assert_element("img#captcha-success")
    sb.set_messenger_theme(location="bottom_right")
    sb.post_message("SeleniumBase wasn't detected", duration=3)


    sb.sleep(3)
    sb.quit()



def login_ceub(url):
    
    with SB(uc=True, headless=True) as sb:
        sb.goto(url)
        sb.type('#coAcesso', ra_espaco_aluno)
        sb.type('#coSenha', senha_espaco_aluno)
        sb.click('#btn-login')
        

        sb.solve_captcha()
        sb.sleep(10)
        
        sb.click('#masterfab')
        print("Esperando o servidor gerar o QR Code...")
        sb.sleep(10)
        sb.execute_script("ShowQrCode();")
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

