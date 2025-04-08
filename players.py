import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os
from datetime import datetime
import time
from random import randint

# --- CONFIGURAÇÕES TELEGRAM ---
TELEGRAM_TOKEN = '7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM'
CHAT_ID = '1700880989'

# URLs e filtros
base_url = "https://basketball.realgm.com/nba/stats/2025/Averages/Qualified"
filtros = ["regular", "Last_10_Games", "Last_5_Games"]
criterios = ["points", "trb", "assists", "tpfgm", "steals", "blocks"]

# Cabeçalhos para a requisição
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Caminho para salvar os arquivos CSV
caminho_pasta = "/home/andredamus/ddwin/data/players/"

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

def baixar_tabela(filtro, criterio):
    url = f"{base_url}/{criterio}/All/desc/1/{filtro}"
    print(f"➡️ Acessando URL: {url}")
    logs.append(f"➡️ Acessando URL: {url}")
    
    try:
        # Delay aleatório entre requests
        time.sleep(randint(1, 3))
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Estratégias de busca em ordem de prioridade
        metodos_busca = [
            {"attrs": {"data-toggle": "table"}},
            {"class_": "table-striped"},
            {"class_": lambda x: x and "table" in x.split()},
            {"class_": "tablesaw"}  # Mantendo o método antigo como fallback
        ]

        for metodo in metodos_busca:
            tabela = soup.find("table", **metodo)
            if tabela:
                print(f"✅ Tabela encontrada usando método: {metodo}")
                logs.append(f"✅ Tabela encontrada para {filtro}/{criterio}")
                df = pd.read_html(StringIO(str(tabela)))[0]
                return df

        print(f"⚠️ Tabela não encontrada para {filtro} e {criterio}")
        logs.append(f"⚠️ Tabela não encontrada para {filtro}/{criterio}")
        print("HTML parcial:", soup.prettify()[:500])  # Debug
        return None

    except requests.exceptions.RequestException as e:
        erro_msg = f"❌ Erro na requisição para {filtro}/{criterio}: {str(e)}"
        print(erro_msg)
        logs.append(erro_msg)
        return None
    except Exception as e:
        erro_msg = f"❌ Erro inesperado em {filtro}/{criterio}: {str(e)}"
        print(erro_msg)
        logs.append(erro_msg)
        return None

# Criar diretório se não existir
os.makedirs(caminho_pasta, exist_ok=True)

# Início do processo
logs = []
inicio_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🚀 Início da execução: {inicio_execucao}")

for filtro in filtros:
    for criterio in criterios:
        nome_filtro = {
            "Last_5_Games": "Last_5",
            "Last_10_Games": "Last_10"
        }.get(filtro, filtro)  # Mantém "regular" se não for os casos acima
        
        nome_arquivo = os.path.join(caminho_pasta, f"tabela_{nome_filtro}_{criterio}.csv")
        
        tabela = baixar_tabela(filtro, criterio)
        if tabela is not None:
            try:
                tabela.to_csv(nome_arquivo, index=False)
                msg = f"💾 Arquivo salvo: {nome_arquivo}"
                print(msg)
                logs.append(msg)
            except Exception as e:
                erro_msg = f"❌ Falha ao salvar {nome_arquivo}: {str(e)}"
                print(erro_msg)
                logs.append(erro_msg)

fim_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🛑 Fim da execução: {fim_execucao}")
logs.append(f"⏳ Tempo total: {datetime.strptime(fim_execucao, '%d/%m/%Y %H:%M:%S') - datetime.strptime(inicio_execucao, '%d/%m/%Y %H:%M:%S')}")

# Enviar log completo para o Telegram
mensagem_final = "\n".join(logs)
enviar_telegram(mensagem_final)