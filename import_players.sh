#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/players_cron.log"
EMAIL_DESTINO="andredamus@gmail.com"   # <-- Coloca seu e-mail aqui!

# Criar pasta de logs caso não exista
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
echo "🚀 Rodando players.py..." >> "$LOG_FILE"
python3 "$PROJETO_DIR/players.py" >> "$LOG_FILE" 2>&1

# Desativar o ambiente virtual após a execução
deactivate

# Fim do log
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
