Esse repositório é um site que possui:

Robô do Telegram
Integração com o Google Sheets
Site em Flask

Configuração inicial
Service account no Google Cloud
Token do robô no Telegram
tWebhook do Telegram

Configurando o webhook do Telegram
import requests
token = "SEU TOKEN"
url = "https://site-teste-turicas.onrender.com/telegram-bot"
response = requests.post(f"https://api.telegram.org/bot{token}/setWebhook", data={"url": url})
print(response.text)
