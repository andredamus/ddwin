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

def verificar_permissao_pasta():
    """Verifica se o script tem permissão para escrever na pasta."""
    try:
        teste_arquivo = os.path.join(CAMINHO_PASTA, "teste_permissao.txt")
        with open(teste_arquivo, "w") as f:
            f.write("Teste de permissão")
        os.remove(teste_arquivo)
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar permissão na pasta {CAMINHO_PASTA}: {e}")
        return False

def baixar_gamelogs():
    logs = []
    logs.append(f"Atualização de times: Início da execução {datetime.now()}")
    
    # Verifica permissão na pasta
    if not verificar_permissao_pasta():
        logs.append("❌ Sem permissão para escrever na pasta. Verifique as permissões.")
        enviar_telegram("\n".join(logs))
        return

    for i, team in enumerate(times_nba):
        nome_arquivo = os.path.join(CAMINHO_PASTA, f"{team}_gamelog.csv")
        url = f"https://www.basketball-reference.com/teams/{team}/2025/gamelog/"

        try:
            print(f"🔗 Acessando: {url}")
            tabelas = pd.read_html(url)
            game_log = tabelas[0]

            # Adicionando logs para depuração
            print(f"💾 Tentando salvar arquivo: {nome_arquivo}")
            logs.append(f"💾 Tentando salvar arquivo: {nome_arquivo}")
            print(game_log.head())  # Mostrar as primeiras linhas do DataFrame
            print(game_log.info())  # Mostrar informações do DataFrame
            if not os.access(CAMINHO_PASTA, os.W_OK):
                erro_permissao = f"❌ Sem permissão de escrita na pasta {CAMINHO_PASTA} antes de salvar {nome_arquivo}"
                print(erro_permissao)
                logs.append(erro_permissao)

            game_log.to_csv(nome_arquivo, index=False)

            mensagem = f"✅ {team}_gamelog.csv salvo com sucesso!"
            print(mensagem)
            logs.append(mensagem)

            # Aguardar entre 10 e 20 segundos
            time.sleep(1 + (2 * (i % 2)))

        except Exception as e:
            mensagem = f"❌ Erro ao baixar {team}: {e}"
            print(mensagem)
            logs.append(mensagem)

    logs.append(f"Fim da execução: {datetime.now()}")

    # Enviar log completo para o Telegram
    mensagem_final = "\n".join(logs)
    enviar_telegram(mensagem_final)

if __name__ == "__main__":
    baixar_gamelogs()