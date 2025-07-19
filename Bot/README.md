# Bot Telegram - Verificador de Casas de Apostas

Um bot do Telegram em Python que recebe mensagens com domínios de casas de apostas e verifica se estão registradas em uma API.

## Funcionalidades

- 📈 Traqueamento automatico de links de afiliados
- 🔍 Controle de clicks e conversões
- 📱 Interface amigável via Telegram
- 🌐 UTMs personalizadas
- 📊 Comandos adicionais para busca e listagem

## Comandos Disponíveis

- `/start` - Mensagem de boas-vindas
- `/help` - Ajuda sobre como usar o bot
- `/info` - Informações sobre o bot
- `/list` - Lista casas de apostas disponíveis
- `/search <termo>` - Busca casas de apostas por termo

## Configuração

### 1. Requisitos

- Python 3.8+
- Token do Bot do Telegram
- API de casas de apostas

### 2. Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd Bot

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração das Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Token do Bot do Telegram (obtenha com @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# URL base da sua API
API_BASE_URL=https://api.example.com

# Chave da API (opcional)
API_KEY=your_api_key_here

# Debug mode (opcional)
DEBUG=True
```

### 4. Como obter o Token do Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Digite `/newbot` para criar um novo bot
3. Siga as instruções para escolher nome e username
4. Copie o token fornecido para o arquivo `.env`

## Estrutura da API

O bot espera que sua API tenha os seguintes endpoints:

### Verificar Casa de Apostas
```
GET /betting-houses/{house_name}
```

**Resposta 200 (Encontrado):**
```json
{
  "name": "Bet365",
  "domain": "bet365.com",
  "license": "Malta Gaming Authority",
  "country": "Malta",
  "status": "Ativo",
  "website": "https://www.bet365.com",
  "founded": "2000"
}
```

**Resposta 404 (Não encontrado):**
```json
{
  "error": "Casa de apostas não encontrada"
}
```

### Listar Casas de Apostas (Opcional)
```
GET /betting-houses
```

### Buscar Casas de Apostas (Opcional)
```
GET /betting-houses/search?q={query}
```

## Uso

### 1. Executar o Bot

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar o bot
python bot.py
```

### 2. Testar no Telegram

Envie mensagens para o bot com domínios:

- `bet365.com`
- `https://www.betfair.com`
- `Verifique sportingbet.com e betano.com`

## Estrutura do Projeto

```
Bot/
├── bot.py                 # Bot principal (versão modular)
├── telegram_bot.py        # Bot original (versão completa)
├── config.py             # Configurações e mensagens
├── api_client.py         # Cliente para API
├── domain_extractor.py   # Extrator de domínios
├── requirements.txt      # Dependências
├── .env.example         # Exemplo de configuração
└── README.md            # Este arquivo
```

## Exemplos de Uso

### Verificação Simples
```
Usuário: bet365.com
Bot: ✅ Casa de apostas 'bet365' encontrada!
     📜 Licença: Malta Gaming Authority
     🌍 País: Malta
     📊 Status: Ativo
```

### Múltiplos Domínios
```
Usuário: Verifique bet365.com e betfair.com
Bot: 📊 Resultados da Verificação:

     🏠 Bet365
     ✅ Casa de apostas 'bet365' encontrada!
     📜 Licença: Malta Gaming Authority

     🏠 Betfair
     ✅ Casa de apostas 'betfair' encontrada!
     📜 Licença: UK Gambling Commission
```

### Domínio Não Encontrado
```
Usuário: casadesconhecida.com
Bot: ❌ Casa de apostas 'casadesconhecida' não encontrada na base de dados.
```

## Personalização

### Modificar Mensagens

Edite o arquivo `config.py` na seção `BOT_MESSAGES`:

```python
BOT_MESSAGES = {
    'welcome': "Sua mensagem personalizada...",
    'help': "Sua ajuda personalizada...",
    # ...
}
```

### Modificar Endpoints da API

Edite o arquivo `config.py` na seção `API_ENDPOINTS`:

```python
API_ENDPOINTS = {
    'check_betting_house': '/seu-endpoint/{house_name}',
    # ...
}
```

### Adicionar Headers de Autenticação

Modifique o arquivo `api_client.py` no método `__init__`:

```python
if self.api_key:
    self.session.headers.update({
        'Authorization': f'Bearer {self.api_key}'
        # ou 'X-API-Key': self.api_key
        # ou outro formato que sua API espera
    })
```

## Logs e Debug

O bot gera logs detalhados. Para ativar o modo debug, defina `DEBUG=True` no arquivo `.env`.

Os logs incluem:
- Mensagens recebidas
- Domínios extraídos
- Chamadas para a API
- Erros e exceções

## Troubleshooting

### Erro: "TELEGRAM_BOT_TOKEN não encontrado"
- Verifique se o arquivo `.env` existe e contém o token correto

### Erro: "Timeout ao consultar API"
- Verifique se a URL da API está correta
- Verifique a conectividade com a internet
- Aumente o timeout na função `check_betting_house`

### Bot não responde
- Verifique se o token do Telegram está correto
- Verifique os logs para erros
- Teste com `/start` primeiro

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.
