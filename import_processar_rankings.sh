#!/bin/bash

# ===== CONFIGURAÇÕES =====
DATA=$(date '+%Y-%m-%d %H:%M:%S')
PROJETO_DIR="/home/andredamus/ddwin"
LOG_DIR="$PROJETO_DIR/logs"
LOG_FILE="$LOG_DIR/import_processar_rankings.log"

# Criar pasta de logs caso não exista
mkdir -p "$LOG_DIR"

# Início do log
echo "=============================" >> "$LOG_FILE"
echo "🕓 Início da execução: $(date)" >> "$LOG_FILE"

# Corrigindo permissões dos arquivos de importação de jogadores
echo "🔧 Corrigindo permissões dos arquivos importados..." >> "$LOG_FILE"
find "$PROJETO_DIR/data/rankings" -type f -exec chmod 644 {} \; -exec echo "✔ Permissão corrigida: {}" >> "$LOG_FILE" \;

# Ativar o ambiente virtual
source "$PROJETO_DIR/venv/bin/activate"

# Executar o script Python e capturar a saída no log
echo "🚀 Rodando processar_rankings.py..." >> "$LOG_FILE"
python3 "$PROJETO_DIR/processar_rankings.py" >> "$LOG_FILE" 2>&1

# Desativar o ambiente virtual após a execução
deactivate

# Fim do log
if [ $? -eq 0 ]; then
    echo "✅ [$DATA] import_processar_rankings.sh finalizado com sucesso!" >> "$LOG_FILE"
else
    echo "❌ [$DATA] Erro ao executar import_processar_rankings.sh" >> "$LOG_FILE"
fi
