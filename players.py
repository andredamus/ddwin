import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os
from datetime import datetime

# Configuração do Telegram
TELEGRAM_BOT_TOKEN = "7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM"
TELEGRAM_CHAT_ID = "1700880989"

# URLs e filtros
base_url = "https://basketball.realgm.com/nba/stats/2025/Averages/Qualified"
filtros = ["regular", "Last_10_Games", "Last_5_Games"]
criterios = ["points", "trb", "assists", "tpfgm", "steals", "blocks"]

# Cabeçalhos para a requisição
headers = {"User-Agent": "Mozilla/5.0"}

# Caminho para salvar os arquivos CSV
caminho_pasta = "/home/andredamus/ddwin/data/players/"

def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    requests.post(url, data=payload)

def baixar_tabela(filtro, criterio):
    url = f"{base_url}/{criterio}/All/desc/1/{filtro}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tabela_certa = soup.find("table", class_="tablesaw")
        if tabela_certa:
            df = pd.read_html(StringIO(str(tabela_certa)))[0]
            return df
        else:
            logs.append(f"⚠️ Tabela não encontrada para {filtro} e {criterio}")
            return None
    else:
        logs.append(f"❌ Erro ao acessar {url}: Código {response.status_code}")
        return None

# Início do processo
logs = []
inicio_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🚀 Atualização de Jogadores: Início da execução: {inicio_execucao}\n")

for filtro in filtros:
    for criterio in criterios:
        tabela = baixar_tabela(filtro, criterio)
        if tabela is not None:
            nome_filtro = "Last_5" if filtro == "Last_5_Games" else "Last_10" if filtro == "Last_10_Games" else filtro
            nome_arquivo = f"{caminho_pasta}tabela_{nome_filtro}_{criterio}.csv"
            tabela.to_csv(nome_arquivo, index=False)
            logs.append(f"✅ {nome_arquivo}")

fim_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🕒 Fim da execução: {fim_execucao}")

# Enviar o log completo no Telegram
mensagem_final = "\n".join(logs)
enviar_mensagem_telegram(mensagem_final)
