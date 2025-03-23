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
    print(f"➡️ Acessando URL: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tabela_certa = soup.find("table", class_="tablesaw")
        
        if tabela_certa:
            df = pd.read_html(StringIO(str(tabela_certa)))[0]
            print(f"✅ Tabela encontrada para {filtro} e {criterio}")
            return df
        else:
            print(f"⚠️ Tabela **não** encontrada para {filtro} e {criterio}")
            logs.append(f"⚠️ Tabela não encontrada para {filtro} e {criterio}")
            return None
    else:
        print(f"❌ Erro ao acessar {url}: Código {response.status_code}")
        logs.append(f"❌ Erro ao acessar {url}: Código {response.status_code}")
        return None

# Início do processo
logs = []
inicio_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🚀 Atualização de Jogadores: Início da execução: {inicio_execucao}\n")

for filtro in filtros:
    for criterio in criterios:
        if filtro == "Last_5_Games":
            nome_filtro = "Last_5"
        elif filtro == "Last_10_Games":
            nome_filtro = "Last_10"
        else:
            nome_filtro = filtro
        
        nome_arquivo = f"{caminho_pasta}tabela_{nome_filtro}_{criterio}.csv"
        
        # TIRANDO A VERIFICAÇÃO DE ARQUIVO JÁ EXISTENTE para sempre baixar como no seu ambiente de teste
        print(f"➡️ Baixando tabela para filtro {filtro} e critério {criterio}...")
        tabela = baixar_tabela(filtro, criterio)
        
        if tabela is not None:
            tabela.to_csv(nome_arquivo, index=False)
            print(f"✅ Arquivo salvo em {nome_arquivo}")
            logs.append(f"✅ {nome_arquivo} salvo com sucesso.")
        else:
            print(f"❌ Falha ao salvar {nome_arquivo}")
            logs.append(f"❌ Falha ao salvar {nome_arquivo}. Tabela não encontrada ou erro de rede.")

fim_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
logs.append(f"🕒 Fim da execução: {fim_execucao}")

# Enviar o log completo no Telegram
mensagem_final = "\n".join(logs)
enviar_mensagem_telegram(mensagem_final)
