#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/teams_cron.log"

# Garantir que a pasta de logs existe
mkdir -p "$LOG_DIR"

# Início do log
echo "=============================" >> "$LOG_FILE"
echo "🕓 Início da execução: $(date)" >> "$LOG_FILE"

# Corrigindo permissões dos arquivos de importação de jogadores
echo "🔧 Corrigindo permissões dos arquivos importados..." >> "$LOG_FILE"
find "$PROJETO_DIR/data/players" -type f -exec chmod 644 {} \; -exec echo "✔ Permissão corrigida: {}" >> "$LOG_FILE" \;

# Ativar o ambiente virtual
source "$PROJETO_DIR/venv/bin/activate"

# Executar o script Python e capturar a saída no log
echo "🚀 Rodando teams.py... $(date)" >> "$LOG_FILE"
python3 "$PROJETO_DIR/teams.py" >> "$LOG_FILE" 2>&1

# Desativar o ambiente virtual após a execução
deactivate

# Fim do log
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
