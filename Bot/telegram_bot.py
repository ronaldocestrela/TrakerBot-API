"""
Bot do Telegram para verificar casas de apostas
Recebe uma mensagem com domínio e verifica se a casa de apostas está registrada na API
"""

import asyncio
import logging
import os
import re
import requests
import tldextract
from typing import Optional
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBetBot:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.api_base_url = os.getenv('API_BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente")
        
        if not self.api_base_url:
            raise ValueError("API_BASE_URL não encontrado nas variáveis de ambiente")

    def extract_domain_name(self, url_or_domain: str) -> Optional[str]:
        """
        Extrai o nome da casa de apostas do domínio
        
        Args:
            url_or_domain: URL ou domínio para extrair o nome
            
        Returns:
            Nome da casa de apostas extraído do domínio
        """
        try:
            # Remove protocolos se existirem
            if url_or_domain.startswith(('http://', 'https://')):
                domain = url_or_domain.replace('http://', '').replace('https://', '')
            else:
                domain = url_or_domain
            
            # Remove paths e parâmetros
            domain = domain.split('/')[0].split('?')[0]
            
            # Usar tldextract para obter o domínio principal
            extracted = tldextract.extract(domain)
            
            # Retorna o domínio principal (sem subdomínio e TLD)
            if extracted.domain:
                return extracted.domain.lower()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair domínio de '{url_or_domain}': {e}")
            return None

    def find_domains_in_message(self, message: str) -> list:
        """
        Encontra domínios/URLs na mensagem
        
        Args:
            message: Texto da mensagem
            
        Returns:
            Lista de domínios encontrados
        """
        # Regex para encontrar URLs e domínios
        url_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+(?:\.[a-zA-Z]{2,})?)'
        
        domains = []
        matches = re.findall(url_pattern, message)
        
        for match in matches:
            domain_name = self.extract_domain_name(match)
            if domain_name and domain_name not in domains:
                domains.append(domain_name)
        
        return domains

    async def check_betting_house_api(self, house_name: str) -> dict:
        """
        Verifica se a casa de apostas existe na API
        
        Args:
            house_name: Nome da casa de apostas
            
        Returns:
            Dicionário com resultado da verificação
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
                # ou headers['X-API-Key'] = self.api_key, dependendo da API
            
            # Endpoint da API - ajuste conforme sua API
            url = f"{self.api_base_url}/betting-houses/{house_name}"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': True,
                    'data': data,
                    'message': f"✅ Casa de apostas '{house_name}' encontrada!"
                }
            elif response.status_code == 404:
                return {
                    'found': False,
                    'data': None,
                    'message': f"❌ Casa de apostas '{house_name}' não encontrada na base de dados."
                }
            else:
                return {
                    'found': False,
                    'data': None,
                    'message': f"⚠️ Erro ao consultar API para '{house_name}'. Status: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'found': False,
                'data': None,
                'message': f"⏱️ Timeout ao consultar API para '{house_name}'"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para {house_name}: {e}")
            return {
                'found': False,
                'data': None,
                'message': f"🚫 Erro de conexão ao consultar '{house_name}'"
            }

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /start"""
        welcome_message = """
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
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /help"""
        help_message = """
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
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /info"""
        info_message = """
ℹ️ *Informações do Bot*

Este bot verifica se casas de apostas estão registradas em nossa base de dados.

*Funcionalidades:*
• Traqueamento automatico de links de afiliados
• Controle de clicks e conversões
• UTMs personalizadas

*Desenvolvido por:* Ronaldo
*Versão:* 1.0
        """
        await update.message.reply_text(info_message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Processa mensagens recebidas"""
        try:
            message_text = update.message.text
            user_id = update.effective_user.id
            username = update.effective_user.username or "Usuário"
            
            logger.info(f"Mensagem recebida de {username} (ID: {user_id}): {message_text}")
            
            # Buscar domínios na mensagem
            domains = self.find_domains_in_message(message_text)
            
            if not domains:
                await update.message.reply_text(
                    "❓ Não encontrei nenhum domínio válido na sua mensagem.\n\n"
                    "Envie um domínio como:\n"
                    "• bet365.com\n"
                    "• https://www.betfair.com\n"
                    "• sportingbet"
                )
                return
            
            # Enviar mensagem de processamento
            processing_msg = await update.message.reply_text(
                f"🔍 Verificando {len(domains)} casa(s) de apostas..."
            )
            
            results = []
            
            # Verificar cada domínio
            for domain in domains:
                result = await self.check_betting_house_api(domain)
                results.append({
                    'domain': domain,
                    'result': result
                })
            
            # Montar resposta
            response_parts = ["📊 *Resultados da Verificação:*\n"]
            
            for item in results:
                domain = item['domain']
                result = item['result']
                
                response_parts.append(f"🏠 *{domain.title()}*")
                response_parts.append(result['message'])
                
                if result['found'] and result['data']:
                    # Adicionar informações extras se disponíveis
                    data = result['data']
                    if isinstance(data, dict):
                        if 'license' in data:
                            response_parts.append(f"📜 Licença: {data['license']}")
                        if 'country' in data:
                            response_parts.append(f"🌍 País: {data['country']}")
                        if 'status' in data:
                            response_parts.append(f"📊 Status: {data['status']}")
                
                response_parts.append("")  # Linha em branco
            
            # Deletar mensagem de processamento
            await processing_msg.delete()
            
            # Enviar resposta final
            final_response = "\n".join(response_parts)
            await update.message.reply_text(final_response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            await update.message.reply_text(
                "🚫 Ocorreu um erro ao processar sua mensagem. Tente novamente."
            )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log erros"""
        logger.error(f"Exception while handling an update: {context.error}")

    def run(self):
        """Iniciar o bot"""
        try:
            # Criar aplicação
            application = Application.builder().token(self.telegram_token).build()
            
            # Adicionar handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("info", self.info_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Adicionar handler de erro
            application.add_error_handler(self.error_handler)
            
            logger.info("🤖 Bot iniciado com sucesso!")
            print("🤖 Bot do Telegram iniciado. Pressione Ctrl+C para parar.")
            
            # Iniciar o bot
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Erro ao iniciar bot: {e}")
            print(f"❌ Erro ao iniciar bot: {e}")

def main():
    """Função principal"""
    try:
        bot = TelegramBetBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot finalizado pelo usuário.")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()
