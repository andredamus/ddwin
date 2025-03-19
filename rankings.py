import ssl
import pandas as pd
import os
from datetime import datetime
import requests

# Ignorar verificação SSL (para casos de certificados problemáticos)
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

# Diretórios e arquivos
BASE_DIR = "/home/andredamus/ddwin"
RANKINGS_DIR = f"{BASE_DIR}/data/rankings"
os.makedirs(RANKINGS_DIR, exist_ok=True)

# Nome do arquivo CSV para salvar os rankings
nome_arquivo = os.path.join(RANKINGS_DIR, "rankings.csv")

# URL da página com as tabelas de estatísticas
url = "https://www.nbastuffer.com/2024-2025-nba-team-stats/"

def baixar_estatisticas():
    logs = []
    logs.append(f"🕓 Início da execução: {datetime.now()}")
    print(f"Acessando URL: {url}")

    try:
        # Lê todas as tabelas da página
        tabelas = pd.read_html(url)

        # Verifica se há pelo menos duas tabelas na página
        if len(tabelas) < 2:
            mensagem = "❌ Menos de duas tabelas encontradas na página."
            print(mensagem)
            logs.append(mensagem)
            
            # Envia o log parcial e finaliza
            mensagem_final = "\n".join(logs)
            enviar_telegram(f"Atualização de Rankings \n\n{mensagem_final}")
            return

        # Primeira tabela: Estatísticas principais
        primeira_tabela = tabelas[0]

        # Segunda tabela: Estatísticas adicionais
        segunda_tabela = tabelas[1]

        # Renomear as colunas da segunda tabela
        segunda_tabela.columns = [f"{col}_2" for col in segunda_tabela.columns]

        # Juntar as duas tabelas horizontalmente
        tabela_completa = pd.concat([primeira_tabela, segunda_tabela], axis=1)

        # Salvar o arquivo CSV
        tabela_completa.to_csv(nome_arquivo, index=False)

        mensagem = f"✅ {nome_arquivo}"
        print(mensagem)
        logs.append(mensagem)

    except Exception as e:
        mensagem = f"❌ Erro ao baixar estatísticas: {e}"
        print(mensagem)
        logs.append(mensagem)

    logs.append(f"Fim da execução: {datetime.now()}")

    # Envia o log completo no Telegram
    mensagem_final = "\n".join(logs)
    enviar_telegram(f"Atualização de Rankings \n\n{mensagem_final}")

if __name__ == "__main__":
    baixar_estatisticas()
