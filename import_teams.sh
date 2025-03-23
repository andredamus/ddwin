#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/teams_cron.log"
VENV_DIR="$PROJETO_DIR/venv"
PYTHON_PATH="$VENV_DIR/bin/python3"
SCRIPT_PATH="$PROJETO_DIR/teams.py"
TEAMS_DATA_DIR="$PROJETO_DIR/data/teams"

# Garantir que a pasta de logs existe
mkdir -p "$LOG_DIR"

# Início do log
echo "=============================" >> "$LOG_FILE"
echo "🕓 Início da execução: $(date)" >> "$LOG_FILE"

# Verificar se o diretório de dados existe
if [ ! -d "$TEAMS_DATA_DIR" ]; then
    echo "❌ Erro: Diretório de dados não encontrado: $TEAMS_DATA_DIR" >> "$LOG_FILE"
    exit 1
fi

# Corrigindo permissões dos arquivos de importação de teams
echo "🔧 Corrigindo permissões dos arquivos importados..." >> "$LOG_FILE"
find "$TEAMS_DATA_DIR" -type f -exec chmod 644 {} \; -exec echo "✔ Permissão corrigida: {}" >> "$LOG_FILE" \;

# Verificar se o ambiente virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado em $VENV_DIR" >> "$LOG_FILE"
    exit 1
fi

# Ativar o ambiente virtual
echo "🔧 Ativando ambiente virtual..." >> "$LOG_FILE"
source "$VENV_DIR/bin/activate"

# Verificar se o Python está disponível no ambiente virtual
if ! command -v "$PYTHON_PATH" &> /dev/null; then
    echo "❌ Erro: Python não encontrado no ambiente virtual." >> "$LOG_FILE"
    deactivate
    exit 1
fi

# Executar o script Python e capturar a saída no log
echo "🚀 Rodando teams.py... $(date)" >> "$LOG_FILE"
"$PYTHON_PATH" "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1

# Verificar o status de saída do script Python
if [ $? -eq 0 ]; then
    echo "✅ Script teams.py executado com sucesso!" >> "$LOG_FILE"
else
    echo "❌ Erro durante a execução do script teams.py." >> "$LOG_FILE"
fi

# Desativar o ambiente virtual após a execução
deactivate

# Fim do log
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"