#!/bin/bash

# Script de início rápido para o Bot Telegram

echo "🤖 Bot Telegram - Verificador de Casas de Apostas"
echo "=================================================="

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "⚙️  Criando arquivo .env..."
    cp .env.example .env
    echo "📝 Configure o arquivo .env com suas credenciais antes de continuar."
    echo "   - TELEGRAM_BOT_TOKEN: Token do seu bot (obtenha com @BotFather)"
    echo "   - API_BASE_URL: URL da sua API de casas de apostas"
    echo "   - API_KEY: Chave da API (se necessário)"
    read -p "🔑 Pressione Enter após configurar o .env..."
fi

# Verificar configuração
echo "🧪 Testando configuração..."
python test_bot.py

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "🚀 Para iniciar o bot:"
echo "   python bot.py"
echo ""
echo "🧪 Para testar com API mock local:"
echo "   1. Em um terminal: python mock_api.py"
echo "   2. Configure API_BASE_URL=http://localhost:5000 no .env"
echo "   3. Em outro terminal: python bot.py"
