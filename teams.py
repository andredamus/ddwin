import os
import requests
from tqdm import tqdm

# Função para enviar mensagem para o Telegram
def enviar_mensagem_telegram(mensagem):
    bot_token = "7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM"
    chat_id = "1700880989"
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': mensagem,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta um erro para status de resposta diferente de 2xx
        if response.status_code == 200:
            print("✅ Mensagem enviada no Telegram com sucesso!")
        else:
            print(f"Erro ao enviar mensagem no Telegram: Status {response.status_code}, Detalhes: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")

# Função para verificar se o arquivo já existe
def verificar_arquivo_existente(caminho_arquivo):
    return os.path.exists(caminho_arquivo)

# Função para fazer o download do arquivo
def baixar_arquivo(url, caminho_arquivo):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(caminho_arquivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"📥 Arquivo baixado com sucesso: {caminho_arquivo}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return False

# Lista de siglas dos times da NBA
times_nba = [
    'ATL', 'BOS', 'BRK', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU',
    'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC',
    'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]

# URL base para o download dos gamelogs
url_base = "https://www.basketball-reference.com/teams/{team_abbr}/gamelog/"

# Diretório onde os arquivos serão salvos
diretorio_arquivos = '/home/andredamus/ddwin/data/teams/'

# Loop para baixar os gamelogs de cada time
for time in tqdm(times_nba, desc="Baixando gamelogs"):
    nome_arquivo = f"{time}_gamelog.csv"
    caminho_arquivo = os.path.join(diretorio_arquivos, nome_arquivo)
    
    # Verifica se o arquivo já existe
    if verificar_arquivo_existente(caminho_arquivo):
        print(f"⚠️ O arquivo {caminho_arquivo} já existe. Pulando o download.")
    else:
        # Monta a URL para o time
        url = url_base.format(team_abbr=time)
        print(f"Baixando o arquivo de {time}...")

        # Faz o download do arquivo e verifica se foi bem-sucedido
        if baixar_arquivo(url, caminho_arquivo):
            # Envia mensagem no Telegram somente após o download bem-sucedido
            enviar_mensagem_telegram(f"✅ {time}_gamelog.csv baixado com sucesso.")
