"""
Demonstração específica do comando /myinfo
"""

def demonstrate_myinfo_command():
    """Demonstra como o comando /myinfo funciona"""
    
    print("📱 DEMONSTRAÇÃO - Comando /myinfo")
    print("=" * 50)
    
    print("\n👤 O que o comando /myinfo mostra:")
    print("✅ ID único do usuário no Telegram")
    print("✅ Username (@usuario)")
    print("✅ Nome completo (primeiro e último nome)")
    print("✅ Código do idioma (pt, en, es, etc.)")
    print("✅ Se a conta é bot ou usuário normal")
    print("✅ Se tem Telegram Premium")
    print("✅ ID do chat atual")
    print("✅ Tipo do chat (private, group, etc.)")
    
    print("\n📋 Exemplo de resposta do bot:")
    print("-" * 30)
    
    example_response = """👤 *Suas Informações de Conta*

📋 **Dados Pessoais:**
• 🆔 **ID:** `123456789`
• 👤 **Username:** @joao_silva
• 📝 **Nome:** João Silva
• 🌍 **Idioma:** pt
• 🤖 **É Bot:** Não
• 💎 **Premium:** Sim

💬 **Informações do Chat:**
• 🆔 **Chat ID:** `123456789`
• 📱 **Tipo:** private

ℹ️ *Essas informações são obtidas diretamente do Telegram*"""
    
    print(example_response)
    
    print("\n" + "-" * 30)
    print("\n🔒 PRIVACIDADE:")
    print("• As informações são obtidas diretamente do Telegram")
    print("• Nada é armazenado pelo bot")
    print("• Dados são mostrados apenas para você")
    print("• Funciona em chats privados e grupos")
    
    print("\n💡 USO PRÁTICO:")
    print("• Descobrir seu ID do Telegram")
    print("• Verificar configurações da conta")
    print("• Debugar problemas com o bot")
    print("• Confirmar username atual")

if __name__ == "__main__":
    demonstrate_myinfo_command()
