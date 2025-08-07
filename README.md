# weather_api_DRF
Desafio hubxp

# 🌦️ Weather API Gateway

Uma API intermediária em Django REST Framework que consome dados da [OpenWeatherMap API](https://openweathermap.org/api), com cache, limite de requisições, histórico e documentação via Swagger.

---

##  Funcionalidades

- Consulta do clima de uma cidade via OpenWeatherMap
- Cache de 10 minutos (Redis)
- Histórico das últimas 10 buscas por IP (PostgreSQL + Celery)
- Rate limiting por IP (limite de requisições)
- Documentação Swagger
- Docker + Docker Compose
- Testes unitários e de integração
- Logs estruturados

---

## Tecnologias

- Python 3.11
- Django 4
- Django REST Framework
- Redis
- Celery + Redis Broker
- PostgreSQL

---


## 🚀 Como rodar o projeto

1. Clone o repositório

```bash
cd weather-api
```

2. Crie um arquivo .env com as variáveis:

```env
DJANGO_SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

OPENWEATHER_API_KEY=

POSTGRES_DB=weather_db
POSTGRES_USER=
POSTGRES_PASSWORD=
DEBUG=True
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

#API
CACHE_TIMEOUT=600

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
3. Suba os containers

```bash
docker compose up --build
```

4. Acesse:

API: http://localhost:8000/api/

Swagger UI: http://localhost:8000/api/docs/

---

## Como funciona
- O endpoint /api/weather/?city=Brasilia retorna o clima atual da cidade.
- A resposta é armazenada em cache Redis por 10 minutos.
- Um histórico da busca é salvo de forma assíncrona via Celery (tempo, cidade, IP).
- Um rate limit de 5 chamadas/minuto.

---

## Testes

```bash
docker compose exec web pytest
```
---

## Para o futuro
- Adicionar autenticação na API
- Realizar deploy automático
- Salvar logs estruturados
- Adicionar parâmetros e body nas requisições para informações específicas
- Fazer um dashboard usando Grafana/Kibana, com as informações de tempo em determinadas cidades
- Adicionar esquemas mais complexos na documentação do Swagger
