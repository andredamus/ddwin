import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os

# URLs e filtros
base_url = "https://basketball.realgm.com/nba/stats/2025/Averages/Qualified"
filtros = ["regular", "Last_10_Games", "Last_5_Games"]
criterios = ["points", "trb", "assists", "tpfgm", "steals", "blocks"]

# Cabeçalhos para a requisição
headers = {"User-Agent": "Mozilla/5.0"}

# Caminho para salvar os arquivos CSV
caminho_pasta = "Data/Players/"

# Função para baixar as tabelas
def baixar_tabela(filtro, criterio):
    # Monta a URL correta com o filtro e o critério
    url = f"{base_url}/{criterio}/All/desc/1/{filtro}"
    print(f"Acessando URL: {url}")  # Para depuração
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Procura pela tabela correta usando uma classe ou ID específica
        # Inspecione o HTML da página para encontrar a classe ou ID correta
        tabela_certa = soup.find("table", class_="tablesaw")  # Exemplo: classe "tablesaw"
        
        if tabela_certa:
            # Usa StringIO para evitar o FutureWarning
            df = pd.read_html(StringIO(str(tabela_certa)))[0]
            return df
        else:
            print(f"Tabela não encontrada para {filtro} e {criterio}")
            return None
    else:
        print(f"Erro ao acessar o site: {response.status_code}")
        return None

# Iterar sobre filtros e critérios para salvar as 18 tabelas
for filtro in filtros:
    for criterio in criterios:
        tabela = baixar_tabela(filtro, criterio)
        if tabela is not None:
            # Ajusta o nome do arquivo para Last_5 e Last_10
            if filtro == "Last_5_Games":
                nome_filtro = "Last_5"
            elif filtro == "Last_10_Games":
                nome_filtro = "Last_10"
            else:
                nome_filtro = filtro  # Mantém "regular" sem alteração

            nome_arquivo = f"{caminho_pasta}tabela_{nome_filtro}_{criterio}.csv"
            tabela.to_csv(nome_arquivo, index=False)
            print(f"✅ Arquivo salvo como {nome_arquivo}")
            print(tabela.head())  # Para conferir as primeiras linhas