"""
Script de teste para a API de casas de apostas
Execute este script para testar se sua API está funcionando corretamente
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from api_client import BettingHouseAPI
from domain_extractor import DomainExtractor

# Carregar variáveis de ambiente
load_dotenv()

async def test_domain_extraction():
    """Testa a extração de domínios"""
    print("🧪 Testando extração de domínios...")
    
    extractor = DomainExtractor()
    
    test_messages = [
        "Verifique bet365.com",
        "https://www.betfair.com é confiável?",
        "O que acha de sportingbet e betano.com?",
        "www.poker.com",
        "https://casino.betway.com/games",
        "site sem domínio"
    ]
    
    for message in test_messages:
        domains = extractor.find_domains_in_message(message)
        print(f"Mensagem: '{message}'")
        print(f"Domínios: {domains}")
        print("-" * 50)

async def test_api_connection():
    """Testa a conexão com a API"""
    print("\n🌐 Testando conexão com a API...")
    
    api_base_url = os.getenv('API_BASE_URL')
    api_key = os.getenv('API_KEY')
    
    if not api_base_url:
        print("❌ API_BASE_URL não configurada no .env")
        return False
    
    print(f"URL da API: {api_base_url}")
    print(f"API Key: {'Configurada' if api_key else 'Não configurada'}")
    
    api_client = BettingHouseAPI(api_base_url, api_key)
    
    # Testar com alguns nomes comuns
    test_houses = ['bet365', 'betfair', 'sportingbet', 'inexistente']
    
    for house in test_houses:
        print(f"\nTestando: {house}")
        result = await api_client.check_betting_house(house)
        print(f"Resultado: {result['message']}")
        if result['found']:
            print(f"Dados: {result['data']}")
    
    return True

async def test_full_workflow():
    """Testa o fluxo completo"""
    print("\n🔄 Testando fluxo completo...")
    
    extractor = DomainExtractor()
    
    api_base_url = os.getenv('API_BASE_URL')
    api_key = os.getenv('API_KEY')
    
    if not api_base_url:
        print("❌ Configure API_BASE_URL no .env para testar o fluxo completo")
        return
    
    api_client = BettingHouseAPI(api_base_url, api_key)
    
    test_message = "Gostaria de verificar bet365.com e betfair.com"
    
    print(f"Mensagem de teste: '{test_message}'")
    
    # Extrair domínios
    domains = extractor.find_domains_in_message(test_message)
    print(f"Domínios extraídos: {domains}")
    
    # Verificar cada domínio
    for domain in domains:
        result = await api_client.check_betting_house(domain)
        print(f"\n{domain}: {result['message']}")

def test_telegram_token():
    """Testa se o token do Telegram está configurado"""
    print("🤖 Testando configuração do Telegram...")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if token:
        print("✅ Token do Telegram configurado")
        # Não mostrar o token completo por segurança
        print(f"Token: {token[:10]}...{token[-10:]}")
        return True
    else:
        print("❌ Token do Telegram não configurado")
        print("Configure TELEGRAM_BOT_TOKEN no arquivo .env")
        return False

async def main():
    """Função principal do teste"""
    print("🧪 SCRIPT DE TESTE - Bot Telegram Casas de Apostas")
    print("=" * 60)
    
    # Verificar arquivo .env
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        print("Copie .env.example para .env e configure as variáveis")
        return
    
    print("✅ Arquivo .env encontrado")
    
    # Testar configurações
    token_ok = test_telegram_token()
    
    # Testar extração de domínios
    await test_domain_extraction()
    
    # Testar API (se configurada)
    api_ok = await test_api_connection()
    
    # Testar fluxo completo
    if token_ok and api_ok:
        await test_full_workflow()
    
    print("\n" + "=" * 60)
    print("🏁 Teste concluído!")
    
    if token_ok and api_ok:
        print("✅ Tudo configurado! Você pode executar o bot com: python bot.py")
    else:
        print("⚠️  Configure as variáveis faltantes no .env antes de executar o bot")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        sys.exit(1)
