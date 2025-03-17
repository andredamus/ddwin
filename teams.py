import ssl
import time
import pandas as pd
import os
import requests
from datetime import datetime

# Ignorar verificação SSL
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURAÇÕES TELEGRAM ---
TELEGRAM_TOKEN = '7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM'
CHAT_ID = '1700880989'

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem no Telegram: {response.text}")
    except Exception as e:
        print(f"Falha ao tentar enviar mensagem Telegram: {e}")

# Lista com as siglas corretas dos 30 times da NBA
times_nba = [
    "ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
    "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
    "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
]

# Caminho para salvar os arquivos CSV no repositório
BASE_DIR = "/home/andredamus/ddwin"
CAMINHO_PASTA = f"{BASE_DIR}/data/teams"
os.makedirs(CAMINHO_PASTA, exist_ok=True)

def baixar_gamelogs():
    logs = []
    logs.append("==============================")
    logs.append(f"🕓 Início da execução: {datetime.now()}")

    for i, team in enumerate(times_nba):
        url = f"https://www.basketball-reference.com/teams/{team}/2025/gamelog/"

        try:
            logs.append(f"🔗 Acessando: {url}")
            tabelas = pd.read_html(url)
            game_log = tabelas[0]

            nome_arquivo = os.path.join(CAMINHO_PASTA, f"{team}_gamelog.csv")
            game_log.to_csv(nome_arquivo, index=False)

            mensagem = f"✅ {team} salvo com sucesso!"
            print(mensagem)
            logs.append(mensagem)

            # Aguardar entre 10 e 20 segundos
            time.sleep(1 + (2 * (i % 2)))

        except Exception as e:
            mensagem = f"❌ Erro ao baixar {team}: {e}"
            print(mensagem)
            logs.append(mensagem)

    logs.append(f"✅ Fim da execução: {datetime.now()}")
    logs.append("==============================")

    # Enviar log completo para o Telegram
    mensagem_final = "\n".join(logs)
    enviar_telegram(f"🏀 Teams Atualização\n\n{mensagem_final}")

if __name__ == "__main__":
    baixar_gamelogs()
