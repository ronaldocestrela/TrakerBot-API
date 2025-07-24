"""
Bot do Telegram para verificar casas de apostas - Versão Modular
"""

import asyncio
import logging
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import BotConfig, BOT_MESSAGES
from api_client import BettingHouseAPI
from domain_extractor import DomainExtractor

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBetBot:
    """Bot do Telegram para verificação de casas de apostas"""
    
    def __init__(self):
        # Carregar configurações
        self.config = BotConfig.from_env()
        
        # Inicializar componentes
        self.api_client = BettingHouseAPI(
            base_url=self.config.api_base_url,
            api_key=self.config.api_key
        )
        self.domain_extractor = DomainExtractor()
        
        logger.info("Bot inicializado com sucesso")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /start"""
        await update.message.reply_text(
            BOT_MESSAGES['welcome'],
            parse_mode='Markdown'
        )
        
        # Log da interação
        user = update.effective_user
        logger.info(f"Comando /start executado por {user.username} (ID: {user.id})")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /help"""
        await update.message.reply_text(
            BOT_MESSAGES['help'],
            parse_mode='Markdown'
        )
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /info"""
        await update.message.reply_text(
            BOT_MESSAGES['info'],
            parse_mode='Markdown'
        )
    
    async def myinfo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /myinfo - mostra informações da conta do usuário"""
        try:
            user = update.effective_user
            chat = update.effective_chat
            
            # Coletar informações do usuário
            user_info = {
                'id': user.id,
                'username': user.username or 'Não definido',
                'first_name': user.first_name or 'Não informado',
                'last_name': user.last_name or '',
                'language_code': user.language_code or 'Não definido',
                'is_bot': user.is_bot,
                'is_premium': getattr(user, 'is_premium', False)
            }
            
            # Informações do chat
            chat_info = {
                'chat_id': chat.id,
                'chat_type': chat.type
            }
            
            # Montar mensagem de resposta
            response = f"""👤 *Suas Informações de Conta*

📋 **Dados Pessoais:**
• 🆔 **ID:** `{user_info['id']}`
• 👤 **Username:** @{user_info['username']} 
• 📝 **Nome:** {user_info['first_name']} {user_info['last_name']}
• 🌍 **Idioma:** {user_info['language_code']}
• 🤖 **É Bot:** {'Sim' if user_info['is_bot'] else 'Não'}
• 💎 **Premium:** {'Sim' if user_info['is_premium'] else 'Não'}

💬 **Informações do Chat:**
• 🆔 **Chat ID:** `{chat_info['chat_id']}`
• 📱 **Tipo:** {chat_info['chat_type']}

ℹ️ *Essas informações são obtidas diretamente do Telegram*"""
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Log da interação
            logger.info(f"Comando /myinfo executado por {user_info['username']} (ID: {user_info['id']})")
            
        except Exception as e:
            logger.error(f"Erro no comando /myinfo: {e}")
            await update.message.reply_text("🚫 Erro ao obter informações da conta.")
    
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /list - lista casas de apostas disponíveis"""
        try:
            processing_msg = await update.message.reply_text("🔍 Buscando casas de apostas disponíveis...")
            
            result = await self.api_client.list_all_betting_houses()
            
            await processing_msg.delete()
            
            if result['success'] and result['data']:
                houses = result['data']
                if isinstance(houses, list) and len(houses) > 0:
                    # Limitar a 20 primeiras para não sobrecarregar
                    limited_houses = houses[:20]
                    house_names = [house.get('name', 'N/A') if isinstance(house, dict) else str(house) 
                                 for house in limited_houses]
                    
                    response = f"📋 *Casas de Apostas Disponíveis* ({len(houses)} total):\n\n"
                    response += "\n".join([f"• {name}" for name in house_names])
                    
                    if len(houses) > 20:
                        response += f"\n\n... e mais {len(houses) - 20} casas de apostas."
                else:
                    response = "📋 Nenhuma casa de apostas encontrada na base de dados."
            else:
                response = "❌ Erro ao buscar lista de casas de apostas."
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erro no comando /list: {e}")
            await update.message.reply_text("🚫 Erro ao buscar lista de casas de apostas.")
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /search - busca casas de apostas por termo"""
        try:
            # Obter termo de busca
            if context.args:
                query = ' '.join(context.args)
            else:
                await update.message.reply_text(
                    "🔍 Use: `/search <termo>`\n\nExemplo: `/search bet365`",
                    parse_mode='Markdown'
                )
                return
            
            processing_msg = await update.message.reply_text(f"🔍 Buscando por '{query}'...")
            
            result = await self.api_client.search_betting_houses(query)
            
            await processing_msg.delete()
            
            if result['success'] and result['data']:
                houses = result['data']
                if isinstance(houses, list) and len(houses) > 0:
                    response = f"🔍 *Resultados para '{query}'* ({len(houses)} encontrados):\n\n"
                    
                    for house in houses[:10]:  # Limitar a 10 resultados
                        if isinstance(house, dict):
                            name = house.get('name', 'N/A')
                            domain = house.get('domain', 'N/A')
                            status = house.get('status', 'N/A')
                            response += f"• *{name}*\n  📍 {domain}\n  📊 {status}\n\n"
                        else:
                            response += f"• {str(house)}\n"
                else:
                    response = f"❌ Nenhum resultado encontrado para '{query}'."
            else:
                response = f"❌ Erro ao buscar por '{query}'."
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erro no comando /search: {e}")
            await update.message.reply_text("🚫 Erro ao realizar busca.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Processa mensagens de texto recebidas"""
        try:
            message_text = update.message.text
            user = update.effective_user
            
            logger.info(f"Mensagem recebida de {user.username or 'Unknown'} (ID: {user.id}): {message_text}")
            
            # Extrair domínios da mensagem
            domains = self.domain_extractor.find_domains_in_message(message_text)
            
            if not domains:
                await update.message.reply_text(BOT_MESSAGES['no_domain_found'])
                return
            
            # Enviar mensagem de processamento
            processing_msg = await update.message.reply_text(
                BOT_MESSAGES['processing'].format(count=len(domains))
            )
            
            # Verificar cada domínio
            results = await self._check_multiple_domains(domains)
            
            # Deletar mensagem de processamento
            await processing_msg.delete()
            
            # Enviar resposta
            response = self._format_results(results)
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            await update.message.reply_text(BOT_MESSAGES['error_general'])
    
    async def _check_multiple_domains(self, domains: List[str]) -> List[Dict[str, Any]]:
        """
        Verifica múltiplos domínios na API
        
        Args:
            domains: Lista de nomes de domínios
            
        Returns:
            Lista com resultados das verificações
        """
        results = []
        
        for domain in domains:
            try:
                result = await self.api_client.check_betting_house(domain)
                results.append({
                    'domain': domain,
                    'result': result
                })
            except Exception as e:
                logger.error(f"Erro ao verificar domínio {domain}: {e}")
                results.append({
                    'domain': domain,
                    'result': {
                        'found': False,
                        'data': None,
                        'message': f"🚫 Erro ao verificar '{domain}'",
                        'status_code': None
                    }
                })
        
        return results
    
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formata os resultados das verificações
        
        Args:
            results: Lista com resultados das verificações
            
        Returns:
            String formatada com os resultados
        """
        response_parts = [BOT_MESSAGES['results_header']]
        
        for item in results:
            domain = item['domain']
            result = item['result']
            
            response_parts.append(f"🏠 *{domain.title()}*")
            response_parts.append(result['message'])
            
            # Adicionar informações extras se disponíveis
            if result['found'] and result.get('data'):
                data = result['data']
                if isinstance(data, dict):
                    extra_info = []
                    
                    if 'license' in data:
                        extra_info.append(f"📜 Licença: {data['license']}")
                    if 'country' in data:
                        extra_info.append(f"🌍 País: {data['country']}")
                    if 'status' in data:
                        extra_info.append(f"📊 Status: {data['status']}")
                    if 'website' in data:
                        extra_info.append(f"🌐 Site: {data['website']}")
                    if 'founded' in data:
                        extra_info.append(f"📅 Fundado: {data['founded']}")
                    
                    if extra_info:
                        response_parts.extend(extra_info)
            
            response_parts.append("")  # Linha em branco
        
        return "\n".join(response_parts)
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler para erros do bot"""
        logger.error(f"Exception while handling an update: {context.error}")
    
    def run(self):
        """Iniciar o bot"""
        try:
            # Criar aplicação do Telegram
            application = Application.builder().token(self.config.telegram_token).build()
            
            # Adicionar handlers de comandos
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("info", self.info_command))
            application.add_handler(CommandHandler("myinfo", self.myinfo_command))
            application.add_handler(CommandHandler("list", self.list_command))
            application.add_handler(CommandHandler("search", self.search_command))
            
            # Handler para mensagens de texto
            application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            # Handler de erro
            application.add_error_handler(self.error_handler)
            
            logger.info("🤖 Bot iniciado com sucesso!")
            print("🤖 Bot do Telegram iniciado. Pressione Ctrl+C para parar.")
            print(f"🔧 Debug mode: {'ON' if self.config.debug else 'OFF'}")
            print(f"🌐 API URL: {self.config.api_base_url}")
            
            # Iniciar o bot
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
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
        logger.error(f"Erro fatal: {e}")
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()
