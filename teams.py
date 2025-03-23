import os
import requests
from datetime import datetime

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = "7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM"
TELEGRAM_CHAT_ID = "1700880989"

# Diretório onde ficam os arquivos dos times
DATA_DIR = '/home/andredamus/ddwin/data/teams'

# Lista das siglas dos times da NBA
nba_teams_abbr = [
    "ATL", "BOS", "BRK", "CHI", "CLE", "DAL", "DEN", "DET",
    "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL",
    "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR",
    "SAC", "SAS", "TOR", "UTA", "WAS"
]

# Função para enviar mensagem no Telegram
def send_telegram_message(chat_id, message, token):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)

    if not response.ok:
        print("Erro ao enviar mensagem no Telegram:", response.text)

def main():
    skipped_files = []

    for team in nba_teams_abbr:
        file_name = f"{team}_gamelog.csv"
        file_path = os.path.join(DATA_DIR, file_name)

        if os.path.exists(file_path):
            print(f"⚠️ O arquivo {file_path} já existe. Pulando o download.")
            skipped_files.append(file_name)
        else:
            # Simulação do download do arquivo
            print(f"⬇️ Baixando o arquivo {file_name}...")

            # Simulando um conteúdo baixado
            content = f"Dados fictícios do time {team}"

            # Salvando o conteúdo no arquivo
            with open(file_path, 'w') as f:
                f.write(content)

            print(f"✅ Download concluído e salvo em {file_path}")

    # Montando a mensagem para o Telegram
    if skipped_files:
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        mensagem = f"🕒 Atualização de times em {now}:\n\n"
        mensagem += "\n".join([f"✅ {arquivo}" for arquivo in skipped_files])

        # Enviando a mensagem
        send_telegram_message(TELEGRAM_CHAT_ID, mensagem, TELEGRAM_BOT_TOKEN)

        print("✅ Mensagem enviada no Telegram com sucesso!")
    else:
        print("Nenhum arquivo foi pulado. Todos os downloads foram feitos.")

if __name__ == "__main__":
    main()
