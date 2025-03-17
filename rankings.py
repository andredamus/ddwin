import ssl
import pandas as pd
import os
from datetime import datetime

# Ignorar verificação SSL (para casos de certificados problemáticos)
ssl._create_default_https_context = ssl._create_unverified_context

# Diretórios e arquivos
BASE_DIR = "/home/andredamus/ddwin"
RANKINGS_DIR = f"{BASE_DIR}/data/rankings"
LOGS_DIR = f"{BASE_DIR}/logs"
os.makedirs(RANKINGS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Nome do arquivo CSV para salvar os rankings
nome_arquivo = os.path.join(RANKINGS_DIR, "rankings.csv")
log_file = os.path.join(LOGS_DIR, "rankings_cron.log")

# URL da página com as tabelas de estatísticas
url = "https://www.nbastuffer.com/2024-2025-nba-team-stats/"

def baixar_estatisticas():
    with open(log_file, "a") as log:
        log.write(f"\n==============================\n")
        log.write(f"🕓 Início da execução: {datetime.now()}\n")
        log.write(f"Acessando URL: {url}\n")

        try:
            # Lê todas as tabelas da página
            tabelas = pd.read_html(url)

            # Verifica se há pelo menos duas tabelas na página
            if len(tabelas) < 2:
                mensagem = "❌ Menos de duas tabelas encontradas na página.\n"
                print(mensagem)
                log.write(mensagem)
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

            mensagem = f"✅ Estatísticas salvas com sucesso em {nome_arquivo}!\n"
            print(mensagem)
            log.write(mensagem)

        except Exception as e:
            mensagem = f"❌ Erro ao baixar estatísticas: {e}\n"
            print(mensagem)
            log.write(mensagem)

        log.write(f"✅ Fim da execução: {datetime.now()}\n")
        log.write(f"==============================\n")

if __name__ == "__main__":
    baixar_estatisticas()
