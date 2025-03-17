#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/rankings_cron.log"

# Garantir que a pasta de logs existe
mkdir -p "$LOG_DIR"

# Ativar ambiente virtual
source "$PROJETO_DIR/venv/bin/activate"

# Log de início (opcional)
echo "🚀 Rodando rankings.py... $(date)" >> "$LOG_FILE"

# Executar o script Python
python3 "$PROJETO_DIR/rankings.py" >> "$LOG_FILE" 2>&1

# Log de finalização (opcional)
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
