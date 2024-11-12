FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build

WORKDIR /src

COPY Servicios.sln .
COPY Servicios.Fachada/Servicios.Fachada.csproj Servicios.Fachada/
COPY Servicios.Datos/Servicios.Datos.csproj Servicios.Datos/
COPY Servicios.Dominio/Servicios.Dominio/Servicios.Dominio.csproj Servicios.Dominio/Servicios.Dominio/
COPY Servicios.Dominio/Servicios.Entidad/Servicios.Entidad.csproj Servicios.Dominio/Servicios.Entidad/
COPY Security/Security.csproj Security/

RUN dotnet restore

COPY . .

WORKDIR /src/Servicios.Fachada

RUN dotnet publish -c Release -o /app/out

FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /app

COPY --from=build /app/out .

COPY Servicios.Fachada/RCA.p12 .

EXPOSE 5030

ENTRYPOINT ["dotnet", "Servicios.Fachada.dll"]
