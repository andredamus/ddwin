import os
import pandas as pd
import requests

# ========== CONFIGURAÇÕES ==========
DIRETORIO_RANKINGS = "/home/andredamus/ddwin/data/rankings"
ARQUIVO_ENTRADA = os.path.join(DIRETORIO_RANKINGS, "rankings.csv")

# Configuração do Telegram
TELEGRAM_BOT_TOKEN = "7711386411:AAEZc_cIeYW33PsgJlNvWZb8V4nc7YhmcGM"
TELEGRAM_CHAT_ID = "1700880989"

# ========== FUNÇÃO PARA ENVIAR MENSAGEM NO TELEGRAM ==========
def enviar_mensagem_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensagem
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso para o Telegram!")
        else:
            print(f"⚠️ Erro ao enviar mensagem para o Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Exceção ao enviar mensagem para o Telegram: {e}")

# ========== FUNÇÃO PRINCIPAL ==========
def processar_rankings(caminho_arquivo):
    try:
        print("🚀 Iniciando processamento dos rankings...")
        
        # Lê o arquivo principal
        df = pd.read_csv(caminho_arquivo)

        # Define colunas para as duas tabelas
        colunas_tabela1 = ["TEAM", "dEFF"]
        colunas_tabela2 = ["TEAM_2", "dEFF_2"]

        # Filtra os DataFrames
        df_tabela1 = df[colunas_tabela1]
        df_tabela2 = df[colunas_tabela2]

        # Ordena e cria o ranking
        df_tabela1_ordenado = df_tabela1.sort_values(by="dEFF", ascending=True)
        df_tabela1_ordenado["Ranking"] = range(1, len(df_tabela1_ordenado) + 1)

        df_tabela2_ordenado = df_tabela2.sort_values(by="dEFF_2", ascending=True)
        df_tabela2_ordenado["Ranking"] = range(1, len(df_tabela2_ordenado) + 1)

        # Confirma se o diretório existe
        if not os.path.exists(DIRETORIO_RANKINGS):
            os.makedirs(DIRETORIO_RANKINGS)

        # Caminhos de saída
        caminho_saida_tabela1 = os.path.join(DIRETORIO_RANKINGS, "ranking_tabela1.csv")
        caminho_saida_tabela2 = os.path.join(DIRETORIO_RANKINGS, "ranking_tabela2.csv")

        # Salva os arquivos
        df_tabela1_ordenado.to_csv(caminho_saida_tabela1, index=False)
        df_tabela2_ordenado.to_csv(caminho_saida_tabela2, index=False)

        print(f"✅ Tabela 1 salva em {caminho_saida_tabela1}")
        print(f"✅ Tabela 2 salva em {caminho_saida_tabela2}")

        # Exibe no terminal (opcional)
        print("\n🏀 Ranking Tabela 1:")
        print(df_tabela1_ordenado)

        print("\n🏀 Ranking Tabela 2:")
        print(df_tabela2_ordenado)

        # Mensagem de sucesso para Telegram
        mensagem = (
            "✅ Processamento de rankings concluído!\n\n"
            f"- Ranking Tabela 1 salvo: ranking_tabela1.csv\n"
            f"- Ranking Tabela 2 salvo: ranking_tabela2.csv\n"
            f"🕒 Horário: {pd.Timestamp.now()}"
        )
        enviar_mensagem_telegram(mensagem)

    except Exception as e:
        mensagem_erro = f"❌ Erro ao processar rankings: {e}"
        print(mensagem_erro)
        enviar_mensagem_telegram(mensagem_erro)

# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    processar_rankings(ARQUIVO_ENTRADA)
