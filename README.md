# feriadosbot

Esse repositório é um **site automatizado** que possui:

- Robô do Telegram
- Integração com o Google Sheets
- Site em Flask

## Configuração inicial
- *Service account* no Google Cloud
- *Token* do robô no Telegram
- `setWebhook` do Telegram

### Configurando o webhook do Telegram

Execute o seguinte código:
```
import requests
token = "SEU TOKEN"
url = "https://site-teste-turicas.onrender.com/telegram-bot"
response = requests.post(f"https://api.telegram.org/bot{token}/setWebhook", data={"url": url})
print(response.text)
