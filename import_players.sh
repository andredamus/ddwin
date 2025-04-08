#!/bin/bash

# Variáveis
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/players_cron.log"
VENV_DIR="$PROJETO_DIR/venv"
PYTHON_PATH="$VENV_DIR/bin/python3" # Adicione esta variável para clareza
SCRIPT_PATH="$PROJETO_DIR/players.py" # Adicione esta variável para clareza

# Criar pasta de logs caso não exista
mkdir -p "$LOG_DIR"

# Início do log
echo "=============================" >> "$LOG_FILE"
echo "🕓 Início da execução: $(date)" >> "$LOG_FILE"

# Executar o script Python diretamente com o interpretador do venv (MODIFICADO)
echo "🚀 Rodando players.py... $(date)" >> "$LOG_FILE"
"$VENV_DIR/bin/python3" "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1

# Corrigir permissões dos arquivos gerados APÓS rodar o script (mantenha)
echo "🔧 Corrigindo permissões dos arquivos importados..." >> "$LOG_FILE"
find "$PROJETO_DIR/data/players" -type f -exec chmod 644 {} \; -exec echo "✔ Permissão corrigida: {}" >> "$LOG_FILE" \;

# Fim do log (mantenha)
echo "✅ Fim da execução: $(date)" >> "$LOG_FILE"
echo "=============================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"