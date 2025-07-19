# TrakerBot 🔗📊

[![.NET](https://img.shields.io/badge/.NET-9.0-purple.svg)](https://dotnet.microsoft.com/download)
[![API](https://img.shields.io/badge/API-REST-blue.svg)](https://restfulapi.net/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

*[Português](#português) | [English](#english)*

---

## English

### 🚀 Overview

TrakerBot is a comprehensive link tracking and management system built with .NET 9. It combines a powerful REST API with an intelligent Telegram bot to provide link shortening, click tracking, and affiliate marketing analytics.

### ✨ Features

- **🔗 Link Shortening**: Create short, trackable URLs for better sharing
- **📈 Click Analytics**: Real-time click counting and engagement tracking
- **📊 Detailed Reports**: Generate comprehensive engagement and performance reports
- **🤖 Telegram Bot Integration**: Smart bot that responds to link queries
- **👥 User Management**: Complete user authentication and authorization system
- **🏢 Affiliate Management**: Track affiliate codes and commissions
- **🎯 House/Platform Registration**: Manage multiple betting platforms and houses

### 🏗️ Architecture

The project follows Clean Architecture principles with the following layers:

- **TrakerBot.API** - Web API layer with controllers and endpoints
- **TrakerBot.Application** - Business logic and use cases
- **TrakerBot.Core** - Domain entities and business rules
- **TrakerBot.Infrastructure** - External services and integrations
- **TrakerBot.Persistence** - Data access and database context
- **Bot** - Telegram bot service for automated interactions

### 🛠️ Technologies

- **.NET 9** - Modern framework for high-performance applications
- **ASP.NET Core** - Web API framework
- **Entity Framework Core** - ORM for database operations
- **AutoMapper** - Object mapping
- **FluentValidation** - Input validation
- **MediatR** - CQRS pattern implementation
- **Telegram.Bot** - Telegram bot integration
- **Identity Framework** - Authentication and authorization

### 📋 Prerequisites

- .NET 9 SDK
- SQL Server (or your preferred database)
- Telegram Bot Token (for bot functionality)

### 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/ronaldocestrela/TrakerBot-API.git
   cd TrakerBot-API
   ```

2. **Configure the database**
   ```bash
   cd TrakerBot.API
   dotnet ef database update
   ```

3. **Configure settings**
   - Update `appsettings.json` with your database connection string
   - Add your Telegram bot token
   - Configure Cloudinary settings (if using image upload)

4. **Run the application**
   ```bash
   dotnet run
   ```

5. **Access the API**
   - API: `https://localhost:5001`
   - OpenAPI docs: `https://localhost:5001/openapi`

### 🤖 Telegram Bot Features

The integrated Telegram bot provides:

- **Link Verification**: Send a link to check if the house/platform is registered
- **Affiliate Code Lookup**: Automatically finds your affiliate codes for registered houses
- **Real-time Responses**: Instant feedback on link status and affiliate information

### 📊 API Endpoints

- `GET /api/links` - List all shortened links
- `POST /api/links` - Create a new shortened link
- `GET /api/links/{id}/analytics` - Get click analytics for a specific link
- `GET /api/houses` - List registered houses/platforms
- `GET /api/affiliates` - Manage affiliate relationships

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

This project is licensed under the MIT License.

---

## Português

### 🚀 Visão Geral

TrakerBot é um sistema abrangente de rastreamento e gerenciamento de links desenvolvido com .NET 9. Combina uma API REST poderosa com um bot inteligente do Telegram para fornecer encurtamento de links, rastreamento de cliques e análises de marketing de afiliados.

### ✨ Funcionalidades

- **🔗 Encurtamento de Links**: Crie URLs curtas e rastreáveis para melhor compartilhamento
- **📈 Análise de Cliques**: Contagem de cliques em tempo real e rastreamento de engajamento
- **📊 Relatórios Detalhados**: Gere relatórios abrangentes de engajamento e performance
- **🤖 Integração com Bot do Telegram**: Bot inteligente que responde a consultas de links
- **👥 Gerenciamento de Usuários**: Sistema completo de autenticação e autorização
- **🏢 Gestão de Afiliados**: Rastreie códigos de afiliados e comissões
- **🎯 Registro de Casas/Plataformas**: Gerencie múltiplas plataformas e casas de apostas

### 🏗️ Arquitetura

O projeto segue os princípios da Clean Architecture com as seguintes camadas:

- **TrakerBot.API** - Camada da Web API com controllers e endpoints
- **TrakerBot.Application** - Lógica de negócio e casos de uso
- **TrakerBot.Core** - Entidades de domínio e regras de negócio
- **TrakerBot.Infrastructure** - Serviços externos e integrações
- **TrakerBot.Persistence** - Acesso a dados e contexto do banco
- **Bot** - Serviço do bot do Telegram para interações automatizadas

### 🛠️ Tecnologias

- **.NET 9** - Framework moderno para aplicações de alta performance
- **ASP.NET Core** - Framework para Web API
- **Entity Framework Core** - ORM para operações de banco de dados
- **AutoMapper** - Mapeamento de objetos
- **FluentValidation** - Validação de entrada
- **MediatR** - Implementação do padrão CQRS
- **Telegram.Bot** - Integração com bot do Telegram
- **Identity Framework** - Autenticação e autorização

### 📋 Pré-requisitos

- .NET 9 SDK
- SQL Server (ou seu banco de dados preferido)
- Token do Bot do Telegram (para funcionalidade do bot)

### 🚀 Como Começar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/ronaldocestrela/TrakerBot-API.git
   cd TrakerBot-API
   ```

2. **Configure o banco de dados**
   ```bash
   cd TrakerBot.API
   dotnet ef database update
   ```

3. **Configure as definições**
   - Atualize `appsettings.json` com sua string de conexão do banco
   - Adicione seu token do bot do Telegram
   - Configure as definições do Cloudinary (se usar upload de imagem)

4. **Execute a aplicação**
   ```bash
   dotnet run
   ```

5. **Acesse a API**
   - API: `https://localhost:5001`
   - Documentação OpenAPI: `https://localhost:5001/openapi`

### 🤖 Funcionalidades do Bot do Telegram

O bot integrado do Telegram oferece:

- **Verificação de Links**: Envie um link para verificar se a casa/plataforma está registrada
- **Busca de Código de Afiliado**: Encontra automaticamente seus códigos de afiliados para casas registradas
- **Respostas em Tempo Real**: Feedback instantâneo sobre status do link e informações de afiliados

### 📊 Endpoints da API

- `GET /api/links` - Lista todos os links encurtados
- `POST /api/links` - Cria um novo link encurtado
- `GET /api/links/{id}/analytics` - Obtém análises de cliques para um link específico
- `GET /api/houses` - Lista casas/plataformas registradas
- `GET /api/affiliates` - Gerencia relacionamentos de afiliados

### 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

### 📄 Licença

Este projeto está licenciado sob a Licença MIT.