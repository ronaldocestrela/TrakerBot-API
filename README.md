# TrakerBot API

TrakerBot API é uma aplicação desenvolvida em .NET 9 que fornece uma interface para gerenciamento e traqueamento de links. O objetivo principal é permitir a criação de encurtadores de links e contabilizar a quantidade de cliques em cada link, possibilitando a geração de relatórios de engajamento.

## Funcionalidades

- **Criação de encurtadores de link**: Gere URLs curtas para facilitar o compartilhamento.
- **Contagem de cliques**: Monitore quantas vezes cada link foi acessado.
- **Relatórios de engajamento**: Gere relatórios detalhados sobre o desempenho dos links encurtados.
- **API RESTful**: Interface moderna e fácil de integrar com outros sistemas.

## Tecnologias Utilizadas

- .NET 9
- ASP.NET Core
- C#

## Como Executar o Projeto

1. **Pré-requisitos**:
   - .NET 9 SDK instalado

2. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   ```

3. **Acesse a pasta do projeto**:
   ```bash
   cd TrakerBot.API
   ```

4. **Restaure as dependências**:
   ```bash
   dotnet restore
   ```

5. **Execute a aplicação**:
   ```bash
   dotnet run
   ```

6. **Acesse a API**:
   - Por padrão, a API estará disponível em `http://localhost:5000` ou `https://localhost:5001`.

## Estrutura do Projeto

- `TrakerBot.API/` - Projeto principal da API
- `TrakerBot.Application/` - Lógica de aplicação
- `TrakerBot.Core/` - Entidades e regras de negócio
- `TrakerBot.Infrastructure/` - Infraestrutura e integrações
- `TrakerBot.Persistance/` - Persistência de dados

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob os termos da licença MIT.
