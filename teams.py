import ssl
import time
import pandas as pd
import os

# Ignorar verificação SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Lista com as siglas corretas dos 30 times da NBA
times_nba = [
    "ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
    "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
    "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
]

# Caminho para salvar os arquivos CSV no repositório
caminho_pasta = "Data/Teams/"

# Função para baixar e salvar os game logs de cada time
def baixar_gamelogs():
    for i, team in enumerate(times_nba):  # Renomeando "time" para "team"
        url = f"https://www.basketball-reference.com/teams/{team}/2025/gamelog/"
        try:
            tabelas = pd.read_html(url)
            game_log = tabelas[0]  # Pegando a primeira tabela da página

            # Salvar o arquivo na pasta correta
            nome_arquivo = os.path.join(caminho_pasta, f"{team}_gamelog.csv")
            game_log.to_csv(nome_arquivo, index=False)
            print(f"✅ {team} salvo com sucesso!")

            # Aguarda entre 10 e 20 segundos antes de fazer a próxima requisição
            time.sleep(1 + (2 * (i % 2)))  # Agora "time" é o módulo correto

        except Exception as e:
            print(f"❌ Erro ao baixar {team}: {e}")

# Executar a função
baixar_gamelogs()
