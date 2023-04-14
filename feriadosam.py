import os

import requests
import gspread
import pandas as pd
import datetime
import gspread_dataframe as gsdf
import pytz

from datetime import datetime
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# FAZENDO O SCRAPPING DOS DADOS DO SITE FERIADOS.COM.BR
url_ano_atual = 'https://www.feriados.com.br/feriados-manaus-am.php'
site_ano_atual = requests.get(url_ano_atual)
conteudo_ano_atual = site_ano_atual.content
html_feriados_ano_atual = BeautifulSoup(conteudo_ano_atual, "html.parser")
feriados_ano_atual = html_feriados_ano_atual.findAll('span', {'class':'style_lista_feriados'})
feriados_am_ano_atual = []
for data in feriados_ano_atual:
    feriado = data.text
    feriados_am_ano_atual.append(feriado)

facultativos_ano_atual = html_feriados_ano_atual.findAll('span', {'class':'style_lista_facultativos'})
facultativos_am_ano_atual = []
for data in facultativos_ano_atual:
    facultativo = data.text
    facultativos_am_ano_atual.append(facultativo)

datas_comemorativas_ano_atual = feriados_am_ano_atual + facultativos_am_ano_atual
ajuste_feriados_ano_atual = []
for linha in datas_comemorativas_ano_atual:
    ajuste = linha.split(' - ')
    ajuste_feriados_ano_atual.append(ajuste)

# CRIAÇÃO DE UM DATAFRAME COM AS DATAS COMEMORATIVAS
tabela_datas_comemorativas_ano_atual = pd.DataFrame(ajuste_feriados_ano_atual, columns=['Data', 'Comemoração'])
tabela_final = tabela_datas_comemorativas_ano_atual.drop_duplicates(subset='Data', keep='first').sort_values('Data')
tabela_final['Data'] = pd.to_datetime(tabela_final['Data'], format='%d/%m/%Y')

# AJUSTANDO O FUSO HORÁRIO
fuso = pytz.timezone('America/Sao_Paulo')
hoje = pd.Timestamp.now(tz=fuso)

# DESCOBRINDO QUANDO É O PRÓXIMO FERIADO
prox_feriado = tabela_final.loc[tabela_final['Data'] > pd.Timestamp.now(), 'Data'].sort_values().iloc[0]
descricao_feriado_am = tabela_final.loc[tabela_final['Data'] == prox_feriado, 'Comemoração'].iloc[0]
prox_feriado_formatado_am = prox_feriado.strftime('%d/%m/%Y')

#AUTORIZANDO GRAVAR OS DADOS EM UMA PLANILHA NO GOOGLE SHEETS
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1zI16LZUgnR-1Xr3MqsjdV6wtyYNMiPpVuxdUVoXYuA4")
sheet = planilha.worksheet("AM")

#GRAVANDO OS DADOS NA PLANILHA)
sheet.clear()
gsdf.set_with_dataframe(sheet, tabela_final)
