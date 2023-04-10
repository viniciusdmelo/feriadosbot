import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from oauth2client.service_account import ServiceAccountCredentials

#FAZENDO O SCRAPPING DOS DADOS DO SITE FERIADOS.COM.BR
url_ano_atual = 'https://www.feriados.com.br/feriados-sao_paulo-sp.php'
site_ano_atual = requests.get(url_ano_atual)
conteudo_ano_atual = site_ano_atual.content
html_feriados_ano_atual = BeautifulSoup(conteudo_ano_atual, "html.parser")
feriados_ano_atual = html_feriados_ano_atual.findAll('span', {'class':'style_lista_feriados'})
feriados_sp_ano_atual = []
for data in feriados_ano_atual:
    feriado = data.text
    feriados_sp_ano_atual.append(feriado)

facultativos_ano_atual = html_feriados_ano_atual.findAll('span', {'class':'style_lista_facultativos'})
facultativos_sp_ano_atual = []
for data in facultativos_ano_atual:
    facultativo = data.text
    facultativos_sp_ano_atual.append(facultativo)

datas_comemorativas_ano_atual = feriados_sp_ano_atual + facultativos_sp_ano_atual
ajuste_feriados_ano_atual = []
for linha in datas_comemorativas_ano_atual:
    ajuste = linha.split(' - ')
    ajuste_feriados_ano_atual.append(ajuste)

#CRIAÇÃO DE UM DATAFRAME COM AS DATAS COMEMORATIVAS
tabela_datas_comemorativas_ano_atual = pd.DataFrame(ajuste_feriados_ano_atual, columns=['Data', 'Comemoração'])
tabela_final = tabela_datas_comemorativas_ano_atual.drop_duplicates(subset='Data', keep='first').sort_values('Data')

#DESCOBRINDO QUE DIA É HOJE
today = datetime.date.today().strftime('%d/%m/%Y')

#DESCOBRINDO QUANDO É O PRÓXIMO FERIADO
prox_feriado = tabela_final.loc[tabela_final['Data'] > today, 'Data'].iloc[0]
descricao_feriado = tabela_final.loc[tabela_final['Data'] == prox_feriado, 'Comemoração'].iloc[0]
prox_feriado_formatado = datetime.datetime.strptime(prox_feriado, '%d/%m/%Y').strftime('%d/%m/%Y')

print(f'O próximo feriado é {descricao_feriado}, em {prox_feriado_formatado}.')


GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1zI16LZUgnR-1Xr3MqsjdV6wtyYNMiPpVuxdUVoXYuA4")
sheet = planilha.worksheet("Pandas")

lista = tabela_final.values.tolist()
sheet.insert_rows(lista)
