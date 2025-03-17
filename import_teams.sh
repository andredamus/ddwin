#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/teams_cron.log"

# Garantir que a pasta de logs existe
mkdir -p "$LOG_DIR"

# Ativar ambiente virtual (caso necessário)
# source "$PROJETO_DIR/venv/bin/activate"

# Log de início (opcional)
echo "🚀 Rodando teams.py... $(date)" >> "$LOG_FILE"

# Executar o script Python
python3 "$PROJETO_DIR/teams.py" >> "$LOG_FILE" 2>&1

# Log de finalização (opcional)
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
