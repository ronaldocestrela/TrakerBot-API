FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build-env
WORKDIR /app

# copy .csproj and restore as distinct layers
COPY "TrakerBot.sln" "TrakerBot.sln"
COPY "TrakerBot.API/TrakerBot.API.csproj" "TrakerBot.API/TrakerBot.API.csproj"
COPY "TrakerBot.Application/TrakerBot.Application.csproj" "TrakerBot.Application/TrakerBot.Application.csproj"
COPY "TrakerBot.Persistance/TrakerBot.Persistance.csproj" "TrakerBot.Persistance/TrakerBot.Persistance.csproj"
COPY "TrakerBot.Core/TrakerBot.Core.csproj" "TrakerBot.Core/TrakerBot.Core.csproj"
COPY "TrakerBot.Infrastructure/TrakerBot.Infrastructure.csproj" "TrakerBot.Infrastructure/TrakerBot.Infrastructure.csproj"

RUN dotnet restore "TrakerBot.sln"

# copy everything else and build
COPY . .
WORKDIR /app
RUN dotnet publish -c Release -o out

# build a runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build-env /app/out .
EXPOSE 8080
EXPOSE 8081
ENTRYPOINT [ "dotnet", "TrakerBot.API.dll" ]
