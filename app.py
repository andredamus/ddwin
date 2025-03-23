from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback
import os
import pandas as pd

app = Flask(__name__)

# <<CONFIGURAÇÕES GERAIS>>

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Agora, usando o caminho relativo para as pastas
DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "teams")
PLAYERS_FOLDER = os.path.join(BASE_FOLDER, "data", "players")
RANKINGS_FOLDER = os.path.join(BASE_FOLDER, "data", "rankings")


# <<LÓGICA PARA TIMES>>

nba_teams = [
    {"id": "ATL", "full_name": "Atlanta Hawks"},
    {"id": "BOS", "full_name": "Boston Celtics"},
    {"id": "BRK", "full_name": "Brooklyn Nets"},
    {"id": "CHO", "full_name": "Charlotte Hornets"},
    {"id": "CHI", "full_name": "Chicago Bulls"},
    {"id": "CLE", "full_name": "Cleveland Cavaliers"},
    {"id": "DAL", "full_name": "Dallas Mavericks"},
    {"id": "DEN", "full_name": "Denver Nuggets"},
    {"id": "DET", "full_name": "Detroit Pistons"},
    {"id": "GSW", "full_name": "Golden State Warriors"},
    {"id": "HOU", "full_name": "Houston Rockets"},
    {"id": "IND", "full_name": "Indiana Pacers"},
    {"id": "LAC", "full_name": "Los Angeles Clippers"},
    {"id": "LAL", "full_name": "Los Angeles Lakers"},
    {"id": "MEM", "full_name": "Memphis Grizzlies"},
    {"id": "MIA", "full_name": "Miami Heat"},
    {"id": "MIL", "full_name": "Milwaukee Bucks"},
    {"id": "MIN", "full_name": "Minnesota Timberwolves"},
    {"id": "NOP", "full_name": "New Orleans Pelicans"},
    {"id": "NYK", "full_name": "New York Knicks"},
    {"id": "OKC", "full_name": "Oklahoma City Thunder"},
    {"id": "ORL", "full_name": "Orlando Magic"},
    {"id": "PHI", "full_name": "Philadelphia 76ers"},
    {"id": "PHO", "full_name": "Phoenix Suns"},
    {"id": "POR", "full_name": "Portland Trail Blazers"},
    {"id": "SAC", "full_name": "Sacramento Kings"},
    {"id": "SAS", "full_name": "San Antonio Spurs"},
    {"id": "TOR", "full_name": "Toronto Raptors"},
    {"id": "UTA", "full_name": "Utah Jazz"},
    {"id": "WAS", "full_name": "Washington Wizards"}
]

def processar_dados(arquivo):
    df = pd.read_csv(arquivo, skiprows=1)  # Pula a primeira linha
    df = df[df.iloc[:, 0] != 'Rk'].iloc[:-1]  # Remove cabeçalhos repetidos e a última linha (totais)

    colunas = {
        6: 'Tm', 7: 'Opp', 24: 'Trb', 44: 'Trbc', 25: 'Ast', 46: 'Astp',
        12: '3pt', 33: '3ptp', 26: 'Stl', 47: 'Stlp', 27: 'Blk', 48: 'Blkp'
    }

    df = df.assign(**{nome: pd.to_numeric(df.iloc[:, idx], errors='coerce') for idx, nome in colunas.items()}) # Converte as colunas desejadas para numérico

    df['Rk'] = pd.to_numeric(df['Rk'], errors='coerce') # Converte 'Rk' para numérico e ordena decrescentemente
    return df.sort_values(by='Rk', ascending=False)

def carregar_e_limpar_dados(time):
    arquivo = os.path.join(DATA_FOLDER, f"{time}_gamelog.csv")
    print(f"Tentando carregar o arquivo: {arquivo}")
    
    if not os.path.exists(arquivo):
        print(f"Arquivo {arquivo} não encontrado!")
        return None

    return processar_dados(arquivo)

def calcular_medias(team_abbr, damus_sports=False, filtro="regular"):
    df = carregar_e_limpar_dados(team_abbr)
    if df is None:
        return None

    ultimos_10 = df.head(10) # Criar subconjuntos para reduzir chamadas redundantes
    ultimos_9 = df.head(9)
    ultimos_8 = df.head(8)
    ultimos_7 = df.head(7)
    ultimos_6 = df.head(6)
    ultimos_5 = df.head(5)
    ultimos_4 = df.head(4)
    ultimos_3 = df.head(3)
    ultimos_2 = df.head(2)

    if damus_sports:
        medias = df[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean()
        medias_10 = ultimos_10[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean()
        medias_7 = ultimos_7[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean()
        medias_4 = ultimos_4[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean()

        resultado = (medias + medias_10 + medias_7 + medias_4) / 4
        return resultado.round(2).to_dict()

    filtros = {
        "regular": df[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_10": ultimos_10[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_9": ultimos_9[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_8": ultimos_8[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_7": ultimos_7[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_6": ultimos_6[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_5": ultimos_5[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_4": ultimos_4[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_3": ultimos_3[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
        "last_2": ultimos_2[['Tm', 'Opp', 'Trb', 'Trbc', 'Ast', 'Astp', '3pt', '3ptp', 'Stl', 'Stlp', 'Blk', 'Blkp']].mean(),
    }
    
    return filtros.get(filtro, filtros["regular"]).round(2).to_dict()

def calcular_frequencia(df, valor_digitado, tipo_analise="over"):
    """
    Calcula a frequência dos últimos 10 jogos com base no valor digitado e no tipo de análise (Over ou Under).

    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados dos jogos.
        valor_digitado (float): Valor digitado pelo usuário.
        tipo_analise (str): Tipo de análise ("over" ou "under").

    Retorna:
        str: Frequência no formato "X/10".
    """
    if df is None or 'Tm' not in df.columns:
        return "0/10"
    
    # Pega os últimos 10 jogos
    pontos_ultimos_10_jogos = df['Tm'].head(10).tolist()
    
    # Calcula a frequência com base no tipo de análise
    if tipo_analise.lower() == "over":
        contagem = sum(1 for pontos in pontos_ultimos_10_jogos if pontos >= valor_digitado)
    elif tipo_analise.lower() == "under":
        contagem = sum(1 for pontos in pontos_ultimos_10_jogos if pontos <= valor_digitado)
    else:
        return "0/10"  # Tipo de análise inválido
    
    return f"{contagem}/10"


# <<LÓGICA PARA JOGADORES>>

SIGLAS_TIMES = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GOS",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHL",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
}

SIGLAS_EQUIVALENTES = {
    "BRK": "BRK",  # Correto
    "BRN": "BRK",  # Alternativa do site
    "CHA": "CHA",
    "CHO": "CHA",
    "GOS": "GOS",
    "GSW": "GOS",
    "PHL": "PHL",
    "PHI": "PHL",
    "PHX": "PHX",
    "PHO": "PHX",
}


SIGLAS_TIMES_REVERSE = {v: k for k, v in SIGLAS_TIMES.items()}


# <<LÓGICA PARA ROTA FREQUÊNCIA>>

@app.route('/calcular-frequencia', methods=['GET'])
def calcular_frequencia_rota():
    time = request.args.get('time')
    valor_digitado = request.args.get('valor')
    tipo_analise = request.args.get('tipo_analise', 'over')  # Padrão é "over"

    # Verifica se o valor foi passado e é um número válido
    if valor_digitado is None or valor_digitado.strip() == "":
        print("Valor não foi fornecido ou está vazio.")
        return jsonify({"resultado": "-"})
    
    try:
        valor_digitado = float(valor_digitado)
        if valor_digitado < 0:
            print("Valor digitado é negativo. Pontuações não podem ser negativas.")
            return jsonify({"resultado": "-"})
    except ValueError:
        print(f"Valor digitado inválido: {valor_digitado}")
        return jsonify({"resultado": "-"})
    
    # Converte o nome completo do time para o ID correspondente
    time_id = None
    for team in nba_teams:
        if team["full_name"] == time:
            time_id = team["id"]
            break
    
    if time_id is None:
        print(f"Time não encontrado: {time}")
        return jsonify({"resultado": "-"})
    
    # Carrega os dados do time
    df = carregar_e_limpar_dados(time_id)
    if df is None:
        print(f"Erro ao carregar dados para o time: {time} (ID: {time_id})")
        return jsonify({"resultado": "-"})
    
    # Verifica se a coluna 'Tm' existe no DataFrame
    if 'Tm' not in df.columns:
        print(f"Coluna 'Tm' não encontrada no DataFrame do time: {time} (ID: {time_id})")
        return jsonify({"resultado": "-"})
    
    # Calcula a frequência com base no tipo de análise
    resultado = calcular_frequencia(df, valor_digitado, tipo_analise)
    print(f"Resultado calculado para {time} (ID: {time_id}) com valor {valor_digitado} e tipo {tipo_analise}: {resultado}")
    return jsonify({"resultado": resultado})


# <<LÓGICA PARA ROTA PARA RANKINGS>>

@app.route("/rankings", methods=["GET"])
def obter_rankings():
    caminho_arquivo_rankings = os.path.join(RANKINGS_FOLDER, "rankings.csv")
    
    try:
        # Processar os rankings
        df = pd.read_csv(caminho_arquivo_rankings)

        colunas_tabela1 = ["TEAM", "dEFF"]  # Primeira tabela
        colunas_tabela2 = ["TEAM_2", "dEFF_2"]  # Segunda tabela

        df_tabela1 = df[colunas_tabela1]
        df_tabela2 = df[colunas_tabela2]

        df_tabela1_ordenado = df_tabela1.sort_values(by="dEFF", ascending=True)
        df_tabela1_ordenado["Ranking"] = range(1, len(df_tabela1_ordenado) + 1)

        df_tabela2_ordenado = df_tabela2.sort_values(by="dEFF_2", ascending=True)
        df_tabela2_ordenado["Ranking"] = range(1, len(df_tabela2_ordenado) + 1)

        # Converter os DataFrames para dicionários
        rankings_tabela1 = df_tabela1_ordenado.to_dict(orient="records")
        rankings_tabela2 = df_tabela2_ordenado.to_dict(orient="records")

        # Retornar os rankings em formato JSON
        return jsonify({
            "tabela1": rankings_tabela1,
            "tabela2": rankings_tabela2
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# <<LÓGICA PARA ROTA DE TIMES E JOGADORES>>

@app.route('/', methods=['GET', 'POST'])
def index_view():
    time_visitante = time_mandante = None
    media_visitante = media_mandante = None
    nome_mandante = nome_visitante = ""
    filtro = request.form.get('filter', 'regular')
    filtro_jogadores = request.form.get('filter_jogadores', 'regular')

    print(f"Tentando acessar: {filtro_jogadores}")

    # Critérios disponíveis e valores predefinidos
    criterios = ["Pontos", "Rebotes", "Assistências", "Três Pontos", "Roubos", "Bloqueios"]
    valores_criterios = [-10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0,
                         -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0,
                         1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5,
                         8.0, 8.5, 9.0, 9.5, 10.0]

    # Inicializa critérios com valores padrão
    criterio_pontos = 0.0
    criterio_rebotes = 0.0
    criterio_assistencias = 0.0
    criterio_trespontos = 0.0
    criterio_roubos = 0.0
    criterio_bloqueios = 0.0

    # Dicionário para armazenar resultados do matchup
    resultado_matchup = {"visitante_pontos": 0, "visitante_rebotes": 0, "visitante_assistencias": 0, "visitante_trespontos": 0, "visitante_roubos": 0, "visitante_bloqueios": 0, 
                         "mandante_pontos": 0, "mandante_rebotes": 0, "mandante_assistencias": 0, "mandante_trespontos": 0, "mandante_roubos": 0, "mandante_bloqueios": 0}

    if request.method == 'POST':
        time_visitante = request.form.get('away_team')
        time_mandante = request.form.get('home_team')
        filtro = request.form.get('filter', 'regular')
        criterio = request.form.get('criterio', "0.0")

        damus_sports = (criterio == "damus_sports")

    # Inicializa criterios_selecionados para evitar erro de variável não definida
    criterios_selecionados = {
        "Pontos": 0.0,
        "Rebotes": 0.0,
        "Assistências": 0.0,
        "Três Pontos": 0.0,
        "Roubos": 0.0,
        "Bloqueios": 0.0
    }

    criterio = "Clique aqui para definir o critério"  # Valor padrão

    criterios_damus_sports = {
        "Pontos": 2,
        "Rebotes": 1,
        "Assistências": 1,
        "Três Pontos": 1,
        "Roubos": 1,
        "Bloqueios": 1
    }

    # Tradução das chaves para corresponder ao dicionário criterios_selecionados
    criterios_traduzidos = {
        "pontos": "Pontos",
        "rebotes": "Rebotes",
        "assistencias": "Assistências",
        "trespontos": "Três Pontos",
        "roubos": "Roubos",
        "bloqueios": "Bloqueios"
    }

    # Listas para armazenar os dados dos jogadores
    dados_jogadores_visitante = []
    dados_jogadores_mandante = []

    if request.method == "POST":
        criterio = request.form.get("criterio", "Clique aqui para definir o critério")
        
        # Verifica se o critério Damus Sports foi selecionado
        damus_sports = criterio == "damus_sports"

        if damus_sports:
            # Se o critério for Damus Sports, preenche com os valores predefinidos
            criterios_selecionados = criterios_damus_sports.copy()
        else:
            criterios_selecionados = {
                "Pontos": float(request.form.get("criterio_pontos") or 0.0),
                "Rebotes": float(request.form.get("criterio_rebotes") or 0.0),
                "Assistências": float(request.form.get("criterio_assistencias") or 0.0),
                "Três Pontos": float(request.form.get("criterio_trespontos") or 0.0),
                "Roubos": float(request.form.get("criterio_roubos") or 0.0),
                "Bloqueios": float(request.form.get("criterio_bloqueios") or 0.0)
            }

        # Atualiza valores individuais
        criterio_pontos = criterios_selecionados["Pontos"]
        criterio_rebotes = criterios_selecionados["Rebotes"]
        criterio_assistencias = criterios_selecionados["Assistências"]
        criterio_trespontos = criterios_selecionados["Três Pontos"]
        criterio_roubos = criterios_selecionados["Roubos"]
        criterio_bloqueios = criterios_selecionados["Bloqueios"]

        # Obtém médias das equipes
        media_visitante = calcular_medias(time_visitante, damus_sports, filtro) or {}
        media_mandante = calcular_medias(time_mandante, damus_sports, filtro) or {}

        # Busca nomes dos times
        nome_mandante = next((team["full_name"] for team in nba_teams if team["id"] == time_mandante), "")
        nome_visitante = next((team["full_name"] for team in nba_teams if team["id"] == time_visitante), "")

        # Calcula resultados do matchup
        if media_visitante and media_mandante:
            resultado_matchup["visitante_pontos"] = round(((media_visitante["Tm"] + media_mandante["Opp"]) / 2) - media_visitante["Tm"], 2)
            resultado_matchup["mandante_pontos"] = round(((media_mandante["Tm"] + media_visitante["Opp"]) / 2) - media_mandante["Tm"], 2)
            resultado_matchup["visitante_rebotes"] = round(((media_visitante["Trb"] + media_mandante["Trbc"]) / 2) - media_visitante["Trb"], 2)
            resultado_matchup["mandante_rebotes"] = round(((media_mandante["Trb"] + media_visitante["Trbc"]) / 2) - media_mandante["Trb"], 2)
            resultado_matchup["visitante_assistencias"] = round(((media_visitante["Ast"] + media_mandante["Astp"]) / 2) - media_visitante["Ast"], 2)
            resultado_matchup["mandante_assistencias"] = round(((media_mandante["Ast"] + media_visitante["Astp"]) / 2) - media_mandante["Ast"], 2)
            resultado_matchup["visitante_trespontos"] = round(((media_visitante["3pt"] + media_mandante["3ptp"]) / 2) - media_visitante["3pt"], 2)
            resultado_matchup["mandante_trespontos"] = round(((media_mandante["3pt"] + media_visitante["3ptp"]) / 2) - media_mandante["3pt"], 2)
            resultado_matchup["visitante_roubos"] = round(((media_visitante["Stl"] + media_mandante["Stlp"]) / 2) - media_visitante["Stl"], 2)
            resultado_matchup["mandante_roubos"] = round(((media_mandante["Stl"] + media_visitante["Stlp"]) / 2) - media_mandante["Stl"], 2)
            resultado_matchup["visitante_bloqueios"] = round(((media_visitante["Blk"] + media_mandante["Blkp"]) / 2) - media_visitante["Blk"], 2)
            resultado_matchup["mandante_bloqueios"] = round(((media_mandante["Blk"] + media_visitante["Blkp"]) / 2) - media_mandante["Blk"], 2)

        # Função para carregar os arquivos de jogadores
        def carregar_arquivo_jogadores(filtro_jogadores, resultado_matchup, criterios_selecionados, time_visitante, time_mandante):
            # Mapeamento dos critérios e colunas correspondentes
            criterios_map = {
                "pontos": {"arquivo": "points", "coluna_media": 5},
                "rebotes": {"arquivo": "trb", "coluna_media": 17},
                "assistencias": {"arquivo": "assists", "coluna_media": 18},
                "trespontos": {"arquivo": "tpfgm", "coluna_media": 9},
                "roubos": {"arquivo": "steals", "coluna_media": 19},
                "bloqueios": {"arquivo": "blocks", "coluna_media": 20}
            }

            # Dicionários para armazenar os dados agrupados por critério
            dados_jogadores_visitante = {}
            dados_jogadores_mandante = {}

            print(f"Dados Visitante: {dados_jogadores_visitante}")
            print(f"Dados Mandante: {dados_jogadores_mandante}")

            # Obtém as siglas dos times (PADRÃO)
            sigla_visitante = SIGLAS_TIMES.get(time_visitante, "")
            sigla_mandante = SIGLAS_TIMES.get(time_mandante, "")

            for criterio, info in criterios_map.items():
                # Acessa o valor do critério com a chave traduzida
                valor_criterio = criterios_selecionados.get(criterios_traduzidos.get(criterio, ""), 0.0)

                # Verifica a condição para o visitante e o mandante
                visitante_criterio = resultado_matchup.get(f'visitante_{criterio}', 0.0)
                mandante_criterio = resultado_matchup.get(f'mandante_{criterio}', 0.0)
                
                # Nome do critério traduzido (vai servir como chave)
                nome_criterio = criterios_traduzidos[criterio]

                # ------- VISITANTE -------
                if visitante_criterio >= valor_criterio:
                    nome_arquivo = f"tabela_{filtro_jogadores}_{info['arquivo']}.csv"
                    caminho_completo = os.path.join(PLAYERS_FOLDER, nome_arquivo)
                    
                    if os.path.exists(caminho_completo):
                        df = pd.read_csv(caminho_completo)

                        if nome_criterio not in dados_jogadores_visitante:
                            dados_jogadores_visitante[nome_criterio] = []

                        for _, row in df.iterrows():
                            # Normaliza a sigla do CSV para a sigla padrão
                            sigla_csv = row.iloc[2]
                            sigla_normalizada = SIGLAS_EQUIVALENTES.get(sigla_csv, sigla_csv)

                            # Compara com a sigla padronizada do visitante
                            if sigla_normalizada == sigla_visitante:
                                dados_jogadores_visitante[nome_criterio].append({
                                    "Player": row.iloc[1],
                                    "Media": row.iloc[info['coluna_media']]
                                })

                # ------- MANDANTE -------
                if mandante_criterio >= valor_criterio:
                    nome_arquivo = f"tabela_{filtro_jogadores}_{info['arquivo']}.csv"
                    caminho_completo = os.path.join(PLAYERS_FOLDER, nome_arquivo)

                    if os.path.exists(caminho_completo):
                        df = pd.read_csv(caminho_completo)

                        if nome_criterio not in dados_jogadores_mandante:
                            dados_jogadores_mandante[nome_criterio] = []

                        for _, row in df.iterrows():
                            # Normaliza a sigla do CSV para a sigla padrão
                            sigla_csv = row.iloc[2]
                            sigla_normalizada = SIGLAS_EQUIVALENTES.get(sigla_csv, sigla_csv)

                            # Compara com a sigla padronizada do mandante
                            if sigla_normalizada == sigla_mandante:
                                dados_jogadores_mandante[nome_criterio].append({
                                    "Player": row.iloc[1],
                                    "Media": row.iloc[info['coluna_media']]
                                })

            return dados_jogadores_visitante, dados_jogadores_mandante

        # Carregar os dados dos jogadores
        dados_jogadores_visitante, dados_jogadores_mandante = carregar_arquivo_jogadores(
            filtro_jogadores,
            resultado_matchup,
            criterios_selecionados,
            nome_visitante,
            nome_mandante
        )

    return render_template(
        "index.html",
        nba_teams=nba_teams,
        nome_mandante=nome_mandante,
        nome_visitante=nome_visitante,
        time_mandante=time_mandante, 
        time_visitante=time_visitante, 
        filtro=filtro,
        filtro_jogadores=filtro_jogadores,
        media_mandante=media_mandante, 
        media_visitante=media_visitante,
        criterio=criterio,
        criterios=criterios,
        criterios_traduzidos=criterios_traduzidos,
        valores_criterios=valores_criterios, 
        criterios_selecionados=criterios_selecionados,
        resultado_matchup=resultado_matchup,
        resultado_matchup_visitante_pontos=resultado_matchup["visitante_pontos"],
        resultado_matchup_visitante_rebotes=resultado_matchup["visitante_rebotes"],
        resultado_matchup_visitante_assistencias=resultado_matchup["visitante_assistencias"],
        resultado_matchup_visitante_trespontos=resultado_matchup.setdefault("visitante_trespontos", 0),
        resultado_matchup_visitante_roubos=resultado_matchup.setdefault("visitante_roubos", 0),
        resultado_matchup_visitante_bloqueios=resultado_matchup.setdefault("visitante_bloqueios", 0),
        resultado_matchup_mandante_pontos=resultado_matchup["mandante_pontos"],
        resultado_matchup_mandante_rebotes=resultado_matchup["mandante_rebotes"],
        resultado_matchup_mandante_assistencias=resultado_matchup["mandante_assistencias"],
        resultado_matchup_mandante_trespontos=resultado_matchup.setdefault("mandante_trespontos", 0),
        resultado_matchup_mandante_roubos=resultado_matchup.setdefault("mandante_roubos", 0),
        resultado_matchup_mandante_bloqueios=resultado_matchup.setdefault("mandante_bloqueios", 0),
        valores_criterio={  # Dicionário com os valores
            "criterio_pontos": criterio_pontos,
            "criterio_rebotes": criterio_rebotes,
            "criterio_assistencias": criterio_assistencias,
            "criterio_trespontos": criterio_trespontos,
            "criterio_roubos": criterio_roubos,
            "criterio_bloqueios": criterio_bloqueios,
        },
        dados_jogadores_visitante=dados_jogadores_visitante,  # Passa os dados dos jogadores do visitante
        dados_jogadores_mandante=dados_jogadores_mandante
    )


# <<EXECUÇÃO PRINCIPAL>>

if __name__ == "__main__":

    # Ajuste o caminho para o arquivo rankings.csv com base na estrutura de pastas
    caminho_arquivo_rankings = os.path.join(RANKINGS_FOLDER, "rankings.csv")
    
    # Iniciar o servidor da aplicação
    app.run(host='0.0.0.0', port=5001)

