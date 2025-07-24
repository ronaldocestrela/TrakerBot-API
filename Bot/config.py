"""
Configurações do Bot
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class BotConfig:
    """Configurações do bot"""
    telegram_token: str
    api_base_url: str
    api_key: Optional[str] = None
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """Carrega configurações das variáveis de ambiente"""
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        api_base_url = os.getenv('API_BASE_URL')
        api_key = os.getenv('API_KEY')
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        if not telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN é obrigatório")
        
        if not api_base_url:
            raise ValueError("API_BASE_URL é obrigatório")
        
        return cls(
            telegram_token=telegram_token,
            api_base_url=api_base_url,
            api_key=api_key,
            debug=debug
        )

# Endpoints da API
API_ENDPOINTS = {
    'check_betting_house': '/betting-houses/{house_name}',
    'list_betting_houses': '/betting-houses',
    'search_betting_houses': '/betting-houses/search?q={query}'
}

# Mensagens do bot
BOT_MESSAGES = {
    'welcome': """
🎰 *Bot Verificador de Casas de Apostas*

Olá! Envie uma mensagem com um domínio ou URL de uma casa de apostas e eu verificarei se ela está registrada em nossa base de dados.

*Exemplos:*
• bet365.com
• https://www.sportingbet.com
• Betfair
• https://betano.com/br

*Comandos disponíveis:*
/start - Mostrar esta mensagem
/help - Ajuda
/info - Informações sobre o bot
/myinfo - Suas informações de conta
    """,
    
    'help': """
🆘 *Ajuda*

*Como usar:*
1. Envie uma mensagem com o domínio da casa de apostas
2. O bot extrairá automaticamente o nome da casa de apostas
3. Verificará se existe na base de dados
4. Retornará o resultado

*Formatos aceitos:*
• bet365.com
• www.betfair.com
• https://sportingbet.com
• betano

*Nota:* O bot pode processar múltiplos domínios em uma única mensagem.
    """,
    
    'info': """
ℹ️ *Informações do Bot*

Este bot verifica se casas de apostas estão registradas em nossa base de dados.

*Funcionalidades:*
• Traqueamento automatico de links de afiliados
• Controle de clicks e conversões
• UTMs personalizadas

*Desenvolvido por:* Ronaldo
*Versão:* 1.0
    """,
    
    'no_domain_found': """
❓ Não encontrei nenhum domínio válido na sua mensagem.

Envie um domínio como:
• bet365.com
• https://www.betfair.com
• sportingbet
    """,
    
    'processing': "🔍 Verificando {count} casa(s) de apostas...",
    'results_header': "📊 *Resultados da Verificação:*\n",
    'error_general': "🚫 Ocorreu um erro ao processar sua mensagem. Tente novamente."
}
