#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/rankings_cron.log"
EMAIL_DESTINO="andredamus@gmail.com"

# Garantir que a pasta de logs existe
mkdir -p "$LOG_DIR"

# Ativar ambiente virtual
source "$PROJETO_DIR/venv/bin/activate"

# Executar o script Python e capturar a saída no log
echo "🚀 Rodando rankings.py..." >> "$LOG_FILE"
python3 "$PROJETO_DIR/rankings.py" >> "$LOG_FILE" 2>&1

# Final do log
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Enviar log por e-mail
mail -s "📝 LOG rankings.py - $(date '+%d/%m/%Y %H:%M')" "$EMAIL_DESTINO" < "$LOG_FILE"
