import os

import datetime
import gspread
import pandas as pd
import requests

from bs4 import BeautifulSoup
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

from feriadossp import prox_feriado_formatado

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1zI16LZUgnR-1Xr3MqsjdV6wtyYNMiPpVuxdUVoXYuA4")
sheet = planilha.worksheet("Resultados")

app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é um site de automação"

@app.route("/sobre")
def sobre():
   return menu + "Este site foi criado para o trabalho final da disciplina de Algoritmos de Automação, ministrada por Álvaro Justen, no Insper"

@app.route("/contato")
def contato():
   return menu + """
   Você pode encontrar em contato comigo pelo @viniciusdmelo nas redes sociais <br>
   <a href="https://www.linkedin.com/in/viniciusdmelo/">LinkedIn</a> | 
   <a href="https://www.facebook.com/viniciusdmelo">Facebook</a> | 
   <a href="http://instagram.com/viniciusdmelo">Instagram</a> | 
   <a href="https://twitter.com/viniciusdmelo">Twitter</a>
   """

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]

  mensagens = []
  for update in dados:
    lastupdate_id = update["update_id"]
    first_name = update["message"]["from"]["first_name"]
    sender_id = update["message"]["from"]["id"]
    if "text" not in update["message"]:
      continue
    message = update["message"]["text"].upper()
    chat_id = update["message"]["chat"]["id"]
    datahora = datetime.datetime.fromtimestamp(update["message"]["date"])
    if "username" in update["message"]["from"]:
      username = f'@{update["message"]["from"]["username"]}'
    else:
      username = ""
    print(f"[{datahora}] Nova mensagem de {first_name} @{username} ({chat_id}): {message}")
    mensagens.append([str(datahora), "recebida", username, first_name, chat_id, message])

  #APÓS RECEBER AS RESPOSTAS E ARMAZENÁ-LAS, O BOT RESPONDE CONFORME A MENSAGEM ENVIADA

    if message == "/START":
      texto_resposta = "Olá! Seja bem-vindo(a)! \nVocê quer saber quando é o próximo feriado em São Paulo? Digite SIM, caso queira."
    elif message == "SIM":
      texto_resposta = f"O próximo feriado é dia {prox_feriado_formatado}. Aproveite para ir a lugares como o Parque Ibirapuera, o museu da Pinacoteca ou passear pela Liberdade."
    else:
      texto_resposta = "Não consegui processar sua mensagem. Ainda estou aprendendo :("
    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=nova_mensagem)
    mensagens.append([str(datahora), "enviada", username, first_name, chat_id, texto_resposta])
    
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  print(resposta.text)
  return "ok"

  #ADICIONA TODAS AS MENSAGENS ENVIADAS NA PLANILHA E ATUALIZADA O ID DO ÚLTIMO UPDATE

  sheet.append_rows(mensagens)
  sheet.update("A1", lastupdate_id)
