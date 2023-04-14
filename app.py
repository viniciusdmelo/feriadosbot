#IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS

import os

import datetime
import gspread
import pandas as pd
import requests
import random

from bs4 import BeautifulSoup
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

#IMPORTANDO AS INFORMAÇÕES DE FERIADOS

from feriadossp import prox_feriado_formatado_sp, descricao_feriado_sp
from feriadosrj import prox_feriado_formatado_rj, descricao_feriado_rj
from feriadospr import prox_feriado_formatado_pr, descricao_feriado_pr
from feriadospe import prox_feriado_formatado_pe, descricao_feriado_pe
from feriadosmg import prox_feriado_formatado_mg, descricao_feriado_mg
from feriadosgo import prox_feriado_formatado_go, descricao_feriado_go
from feriadosdf import prox_feriado_formatado_df, descricao_feriado_df
from feriadosce import prox_feriado_formatado_ce, descricao_feriado_ce
from feriadosba import prox_feriado_formatado_ba, descricao_feriado_ba
from feriadosam import prox_feriado_formatado_am, descricao_feriado_am

#IMPORTANDO AS SUGESTÕES DE ATIVIDADES

from sugestoessp import sugestoes_sp
from sugestoesrj import sugestoes_rj
from sugestoespr import sugestoes_pr
from sugestoespe import sugestoes_pe
from sugestoesmg import sugestoes_mg
from sugestoesgo import sugestoes_go
from sugestoesdf import sugestoes_df
from sugestoesce import sugestoes_ce
from sugestoesba import sugestoes_ba
from sugestoesam import sugestoes_am

#IMPORTANDO AS VARIÁVEIS DE AMBIENTE

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

#CRIANDO O SITE COM MENU PRINCIPAL

app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

#CRIANDO A PÁGINA INICIAL

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é um site de automação"

#CRIANDO A PÁGINA SOBRE

@app.route("/sobre")
def sobre():
   return menu + "Este site foi criado para o trabalho final da disciplina de Algoritmos de Automação, ministrada por Álvaro Justen, no Insper"

#CRIANDO A PÁGINA DE CONTATO

@app.route("/contato")
def contato():
   return menu + """
   Você pode encontrar em contato comigo pelo @viniciusdmelo nas redes sociais <br>
   <a href="https://www.linkedin.com/in/viniciusdmelo/">LinkedIn</a> | 
   <a href="https://www.facebook.com/viniciusdmelo">Facebook</a> | 
   <a href="http://instagram.com/viniciusdmelo">Instagram</a> | 
   <a href="https://twitter.com/viniciusdmelo">Twitter</a>
   """

#CRIANDO O BOT DO TELEGRAM

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"].lower()

    if message == "/start":
        texto_resposta = "Olá! Seja bem-vindo(a)! \nPara saber quando é o próximo feriado em sua cidade, digite a cidade desejada, como por exemplo: /SaoPaulo, /RioDeJaneiro, /Curitiba, /Recife, /BeloHorizonte, /Goiania, /Brasilia, /Fortaleza, /Salvador ou /Manaus."
    elif message.startswith("/"):
        cidade = message[1:].replace(" ", "").replace("-", "").replace(".", "").replace(",", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("â", "a").replace("ê", "e").replace("ô", "o").replace("ã", "a").replace("õ", "o").replace("/", "").lower()
        if cidade == "saopaulo":
            texto_resposta = f"O próximo feriado em São Paulo é {descricao_feriado_sp}, no dia {prox_feriado_formatado_sp}. Aproveite para {random.choice(sugestoes_sp)}, {random.choice(sugestoes_sp)} ou {random.choice(sugestoes_sp)}."
        elif cidade == "riodejaneiro":
            texto_resposta = f"O próximo feriado no Rio de Janeiro é {descricao_feriado_rj}, no dia {prox_feriado_formatado_rj}. Aproveite para {random.choice(sugestoes_rj)}, {random.choice(sugestoes_rj)} ou {random.choice(sugestoes_rj)}."
        elif cidade == "curitiba":
            texto_resposta = f"O próximo feriado em Curitiba é {descricao_feriado_pr}, no dia {prox_feriado_formatado_pr}. Aproveite para {random.choice(sugestoes_pr)}, {random.choice(sugestoes_pr)} ou {random.choice(sugestoes_pr)}."
        elif cidade == "recife":
            texto_resposta = f"O próximo feriado em Recife é {descricao_feriado_pe}, no dia {prox_feriado_formatado_pe}. Aproveite para {random.choice(sugestoes_pe)}, {random.choice(sugestoes_pe)} ou {random.choice(sugestoes_pe)}."
        elif cidade == "belohorizonte":
            texto_resposta = f"O próximo feriado em Belo Horizonte é {descricao_feriado_mg}, no dia {prox_feriado_formatado_mg}. Aproveite para {random.choice(sugestoes_mg)}, {random.choice(sugestoes_mg)} ou {random.choice(sugestoes_mg)}."
        elif cidade == "goiania":
            texto_resposta = f"O próximo feriado em Goiânia é {descricao_feriado_go}, no dia {prox_feriado_formatado_go}. Aproveite para {random.choice(sugestoes_go)}, {random.choice(sugestoes_go)} ou {random.choice(sugestoes_go)}."
        elif cidade in ["brasilia", "brasília"]:
            texto_resposta = f"Em Brasília, o próximo feriado é {descricao_feriado_df}, no dia {prox_feriado_formatado_df}. Aproveite para {random.choice(sugestoes_df)}, {random.choice(sugestoes_df)} ou {random.choice(sugestoes_df)}."
        elif cidade == "fortaleza":
            texto_resposta = f"Em Fortaleza, o próximo feriado é {descricao_feriado_ce}, no dia {prox_feriado_formatado_ce}. Aproveite para {random.choice(sugestoes_ce)}, {random.choice(sugestoes_ce)} ou {random.choice(sugestoes_ce)}."
        elif cidade == "salvador":
            texto_resposta = f"Em Salvador, o próximo feriado é {descricao_feriado_ba}, no dia {prox_feriado_formatado_ba}. Aproveite para {random.choice(sugestoes_ba)}, {random.choice(sugestoes_ba)} ou {random.choice(sugestoes_ba)}."
        elif cidade == "manaus":
            texto_resposta = f"Em Manaus, o próximo feriado é {descricao_feriado_am}, no dia {prox_feriado_formatado_am}. Aproveite para {random.choice(sugestoes_am)}, {random.choice(sugestoes_am)} ou {random.choice(sugestoes_am)}."
    else:
        texto_resposta = "Não consegui processar sua mensagem. Ainda estou aprendendo :("

    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    return "ok"
