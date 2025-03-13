import ssl
import pandas as pd
import os

# Ignorar verificação SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Caminho para salvar o arquivo CSV
caminho_pasta = "/Users/andredamus/Documents/APP/Gamelog/Rankings/"
nome_arquivo = os.path.join(caminho_pasta, "rankings.csv")

# URL da página com as tabelas de estatísticas
url = "https://www.nbastuffer.com/2024-2025-nba-team-stats/"

def baixar_estatisticas():
    try:
        # Lê todas as tabelas da página
        tabelas = pd.read_html(url)

        # Verifica se há pelo menos duas tabelas na página
        if len(tabelas) < 2:
            print("❌ Menos de duas tabelas encontradas na página.")
            return

        # Primeira tabela: Estatísticas principais
        primeira_tabela = tabelas[0]

        # Segunda tabela: Estatísticas adicionais
        segunda_tabela = tabelas[1]

        # Renomear as colunas da segunda tabela
        segunda_tabela.columns = [f"{col}_2" for col in segunda_tabela.columns]

        # Juntar as duas tabelas horizontalmente
        tabela_completa = pd.concat([primeira_tabela, segunda_tabela], axis=1)

        # Salvar o arquivo na pasta correta
        tabela_completa.to_csv(nome_arquivo, index=False)
        print(f"✅ Estatísticas salvas com sucesso em {nome_arquivo}!")

    except Exception as e:
        print(f"❌ Erro ao baixar estatísticas: {e}")

# Executar a função
baixar_estatisticas()