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

from sugestoessp import sugestao_aleatoria_sp
from sugestoesrj import sugestao_aleatoria_rj
from sugestoespr import sugestao_aleatoria_pr
from sugestoespe import sugestao_aleatoria_pe
from sugestoesmg import sugestao_aleatoria_mg
from sugestoesgo import sugestao_aleatoria_go
from sugestoesdf import sugestao_aleatoria_df
from sugestoesce import sugestao_aleatoria_ce
from sugestoesba import sugestao_aleatoria_ba
from sugestoesam import sugestao_aleatoria_am

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
    message = update["message"]["text"].upper()

    if message == "/START":
        texto_resposta = "Olá! Seja bem-vindo(a)! \nVocê quer saber quando é o próximo feriado em São Paulo? Digite SIM, caso queira."
    elif message == "SIM":
        texto_resposta = f"""
        O próximo feriado é {descricao_feriado_sp}, no dia {prox_feriado_formatado_sp}. Aproveite para {sugestao_aleatoria_sp}, {sugestao_aleatoria_sp} e {sugestao_aleatoria_sp}."
        """
    else:
        texto_resposta = "Não consegui processar sua mensagem. Ainda estou aprendendo :("

    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    return "ok"
