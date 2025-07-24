"""
Demonstração do Bot Telegram - Casas de Apostas
Execute este arquivo para ver exemplos de funcionamento
"""

from domain_extractor import DomainExtractor

def demonstrate_domain_extraction():
    """Demonstra a extração de domínios"""
    print("🎯 DEMONSTRAÇÃO - Extração de Domínios")
    print("=" * 50)
    
    extractor = DomainExtractor()
    
    examples = [
        # URLs completas
        "https://www.bet365.com",
        "http://betfair.com",
        "https://casino.betway.com/br/games",
        
        # Domínios simples
        "bet365.com",
        "www.sportingbet.com",
        "betano.br",
        
        # Múltiplos domínios
        "Verifique bet365.com e betfair.com",
        "Sites: pokerstars.com, bet365.com, rivalo.com",
        
        # Mensagens naturais
        "O bet365 é confiável?",
        "Jogo no betfair há anos",
        "sportingbet está funcionando?",
        
        # Casos especiais
        "Não encontrei nenhum domínio aqui",
        "email@bet365.com não é domínio",
        "sub.dominio.bet365.com.br",
    ]
    
    for i, message in enumerate(examples, 1):
        print(f"\n{i:2d}. Mensagem: '{message}'")
        
        domains = extractor.find_domains_in_message(message)
        
        if domains:
            print(f"    ✅ Domínios encontrados: {', '.join(domains)}")
            
            # Mostrar informações detalhadas do primeiro domínio
            if len(domains) > 0:
                info = extractor.get_domain_info(message)
                if info.get('is_valid'):
                    print(f"    📋 Detalhes: {info['domain']}.{info['suffix']}")
        else:
            print("    ❌ Nenhum domínio encontrado")

def demonstrate_api_responses():
    """Demonstra respostas típicas da API"""
    print("\n\n🌐 DEMONSTRAÇÃO - Respostas da API")
    print("=" * 50)
    
    # Exemplos de respostas que a API poderia retornar
    api_responses = [
        {
            'house': 'bet365',
            'found': True,
            'data': {
                'name': 'Bet365',
                'domain': 'bet365.com',
                'license': 'Malta Gaming Authority',
                'country': 'Malta',
                'status': 'Ativo',
                'founded': '2000'
            }
        },
        {
            'house': 'casadesconhecida',
            'found': False,
            'data': None
        },
        {
            'house': 'betfair',
            'found': True,
            'data': {
                'name': 'Betfair',
                'domain': 'betfair.com',
                'license': 'UK Gambling Commission',
                'country': 'Reino Unido',
                'status': 'Ativo',
                'founded': '1999'
            }
        }
    ]
    
    for response in api_responses:
        house = response['house']
        print(f"\n🏠 {house.title()}")
        
        if response['found']:
            print(f"✅ Casa de apostas '{house}' encontrada!")
            data = response['data']
            print(f"📜 Licença: {data['license']}")
            print(f"🌍 País: {data['country']}")
            print(f"📊 Status: {data['status']}")
            print(f"📅 Fundado: {data['founded']}")
        else:
            print(f"❌ Casa de apostas '{house}' não encontrada na base de dados.")

def demonstrate_bot_messages():
    """Demonstra mensagens do bot"""
    print("\n\n💬 DEMONSTRAÇÃO - Mensagens do Bot")
    print("=" * 50)
    
    scenarios = [
        {
            'user_message': 'bet365.com',
            'bot_response': '''📊 *Resultados da Verificação:*

🏠 *Bet365*
✅ Casa de apostas 'bet365' encontrada!
📜 Licença: Malta Gaming Authority
🌍 País: Malta
📊 Status: Ativo'''
        },
        {
            'user_message': 'Verifique bet365.com e betfair.com',
            'bot_response': '''📊 *Resultados da Verificação:*

🏠 *Bet365*
✅ Casa de apostas 'bet365' encontrada!
📜 Licença: Malta Gaming Authority
🌍 País: Malta

🏠 *Betfair*
✅ Casa de apostas 'betfair' encontrada!
📜 Licença: UK Gambling Commission
🌍 País: Reino Unido'''
        },
        {
            'user_message': 'casadesconhecida.com',
            'bot_response': '''📊 *Resultados da Verificação:*

🏠 *Casadesconhecida*
❌ Casa de apostas 'casadesconhecida' não encontrada na base de dados.'''
        },
        {
            'user_message': 'mensagem sem domínio',
            'bot_response': '''❓ Não encontrei nenhum domínio válido na sua mensagem.

Envie um domínio como:
• bet365.com
• https://www.betfair.com
• sportingbet'''
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Cenário {i} ---")
        print(f"👤 Usuário: {scenario['user_message']}")
        print(f"🤖 Bot:")
        print(scenario['bot_response'])

def demonstrate_commands():
    """Demonstra comandos do bot"""
    print("\n\n⚡ DEMONSTRAÇÃO - Comandos do Bot")
    print("=" * 50)
    
    commands = [
        {
            'command': '/start',
            'description': 'Mensagem de boas-vindas com instruções',
            'example': '''🎰 *Bot Verificador de Casas de Apostas*

Olá! Envie uma mensagem com um domínio ou URL de uma casa de apostas...'''
        },
        {
            'command': '/help',
            'description': 'Ajuda sobre como usar o bot',
            'example': '''🆘 *Ajuda*

*Como usar:*
1. Envie uma mensagem com o domínio da casa de apostas...'''
        },
        {
            'command': '/myinfo',
            'description': 'Mostra informações da sua conta',
            'example': '''👤 *Suas Informações de Conta*

📋 **Dados Pessoais:**
• 🆔 **ID:** `123456789`
• 👤 **Username:** @usuario
• 📝 **Nome:** João Silva
• 🌍 **Idioma:** pt'''
        },
        {
            'command': '/list',
            'description': 'Lista casas de apostas disponíveis',
            'example': '''📋 *Casas de Apostas Disponíveis* (7 total):

• Bet365
• Betfair
• Sportingbet
• Betano
• Rivalo'''
        },
        {
            'command': '/search bet365',
            'description': 'Busca casas de apostas por termo',
            'example': '''🔍 *Resultados para 'bet365'* (1 encontrados):

• *Bet365*
  📍 bet365.com
  📊 Ativo'''
        }
    ]
    
    for cmd in commands:
        print(f"\n{cmd['command']}")
        print(f"📝 {cmd['description']}")
        print(f"📄 Exemplo de resposta:")
        print(f"   {cmd['example'][:100]}...")

def main():
    """Função principal da demonstração"""
    print("🎭 DEMONSTRAÇÃO COMPLETA")
    print("Bot Telegram - Verificador de Casas de Apostas")
    print("=" * 60)
    
    demonstrate_domain_extraction()
    demonstrate_api_responses()
    demonstrate_bot_messages()
    demonstrate_commands()
    
    print("\n\n" + "=" * 60)
    print("🎯 RESUMO DAS FUNCIONALIDADES")
    print("=" * 60)
    
    features = [
        "✅ Extrai nomes de casas de apostas de URLs e domínios",
        "✅ Suporta múltiplos formatos (http/https, www, domínio simples)",
        "✅ Processa múltiplos domínios em uma única mensagem",
        "✅ Integra com API externa para verificação",
        "✅ Interface amigável via Telegram",
        "✅ Comandos adicionais (/list, /search, /help)",
        "✅ Tratamento de erros e timeouts",
        "✅ Logs detalhados para debugging",
        "✅ API mock incluída para testes",
        "✅ Configuração via variáveis de ambiente"
    ]
    
    for feature in features:
        print(feature)
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Configure TELEGRAM_BOT_TOKEN no .env")
    print("2. Configure API_BASE_URL no .env")
    print("3. Execute: python bot.py")
    print("4. Teste no Telegram enviando domínios")
    
    print("\n🧪 PARA TESTAR LOCALMENTE:")
    print("1. Terminal 1: python mock_api.py")
    print("2. Configure API_BASE_URL=http://localhost:5000")
    print("3. Terminal 2: python bot.py")

if __name__ == "__main__":
    main()
