#!/bin/bash

# Variáveis (mantenha as suas)
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/teams_cron.log"
VENV_DIR="$PROJETO_DIR/venv"
PYTHON_PATH="$VENV_DIR/bin/python3"
SCRIPT_PATH="$PROJETO_DIR/teams.py"
TEAMS_DATA_DIR="$PROJETO_DIR/data/teams"

# Garantir que a pasta de logs existe (mantenha)
mkdir -p "$LOG_DIR"

# Início do log (mantenha)
echo "=============================" >> "$LOG_FILE"
echo "🕓 Início da execução: $(date)" >> "$LOG_FILE"

# Verificar se o diretório de dados existe (mantenha)
if [ ! -d "$TEAMS_DATA_DIR" ]; then
    echo "❌ Erro: Diretório de dados não encontrado: $TEAMS_DATA_DIR" >> "$LOG_FILE"
    exit 1
fi

# Corrigindo permissões (mantenha)
echo "🔧 Corrigindo permissões dos arquivos importados..." >> "$LOG_FILE"
find "$TEAMS_DATA_DIR" -type f -exec chmod 644 {} \; -exec echo "✔ Permissão corrigida: {}" >> "$LOG_FILE" \;

# Executar o script Python diretamente com o interpretador do venv (MODIFICADO)
echo "🚀 Rodando teams.py... $(date)" >> "$LOG_FILE"
"$VENV_DIR/bin/python3" "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1

# Verificar o status de saída do script Python (mantenha)
if [ $? -eq 0 ]; then
    echo "✅ Script teams.py executado com sucesso!" >> "$LOG_FILE"
else
    echo "❌ Erro durante a execução do script teams.py." >> "$LOG_FILE"
fi

# Fim do log (mantenha)
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"