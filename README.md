# 🎓 Student ID Automation | Automação de Carteirinha

![Widget Preview](preview.jpg)

*(Scroll down for the English version)*

## 🇧🇷 Português

Este projeto automatiza a extração do QR Code da carteirinha estudantil do portal do CEUB e o exibe diretamente na tela inicial do iPhone através de um widget. A arquitetura foi desenhada para manter o código-fonte público para fins de portfólio, enquanto protege os dados pessoais (a imagem do QR Code) em um repositório privado.

### ⚙️ Como Funciona (Arquitetura)

1. **Scraping Invisível:** Um script em Python utiliza a biblioteca `seleniumbase` (com Undetected ChromeDriver) para contornar as proteções anti-bot (Cloudflare/CAPTCHA) do portal da universidade. Ele faz o login, aguarda o carregamento dinâmico e decodifica a imagem gerada em base64.
2. **CI/CD & Automação:** O GitHub Actions executa o script automaticamente de segunda a sexta-feira.
3. **Segurança de Dados (O Cofre):** Para evitar o vazamento do QR Code no repositório público, o GitHub Actions transfere a imagem gerada e faz o *push* diretamente para um segundo repositório privado usando um Personal Access Token (PAT).
4. **Integração iOS:** O aplicativo **Scriptable** no iPhone utiliza um script JavaScript para acessar o repositório privado, baixar a imagem mais recente via API do GitHub e atualizá-la no widget da tela inicial.

### 🛠 Tecnologias Utilizadas
* **Python** (Automação e processamento de imagem)
* **SeleniumBase** (Bypass de WAF e interação web)
* **GitHub Actions** (Agendamento e CI/CD)
* **JavaScript / Scriptable** (Desenvolvimento do widget iOS)

---

## 🇺🇸 English

This project automates the extraction of the student ID QR Code from the CEUB university portal and displays it directly on the iPhone home screen via a custom widget. The architecture is designed to keep the source code public for portfolio purposes while securing personal data (the QR Code image) in a private repository.

### ⚙️ How It Works (Architecture)

1. **Stealth Scraping:** A Python script uses the `seleniumbase` library (Undetected ChromeDriver) to bypass the university's anti-bot protections (Cloudflare/CAPTCHA). It logs in, waits for the dynamic rendering, and decodes the base64 image.
2. **CI/CD & Automation:** GitHub Actions is scheduled to run the script automatically every weekday.
3. **Data Security (The Vault):** To prevent leaking the QR Code in the public repository, GitHub Actions securely transfers and pushes the generated image to a separate private repository using a Personal Access Token (PAT).
4. **iOS Integration:** The **Scriptable** app on the iPhone runs a JavaScript snippet to authenticate with the private repository via the GitHub API, fetches the latest image, and renders it on a home screen widget.

### 🛠 Technologies Used
* **Python** (Automation and image processing)
* **SeleniumBase** (WAF bypass and web interaction)
* **GitHub Actions** (Cron scheduling and CI/CD)
* **JavaScript / Scriptable** (iOS widget development)
