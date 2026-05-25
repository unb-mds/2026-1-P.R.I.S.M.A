# 2026-1-P.R.I.S.M.A

Resumo
- Projeto: P.R.I.S.M.A
- Objetivo: código e material referente às entregas do time (aplicação Django).


Foco deste README
- Prioriza instruções para rodar o projeto com Docker (recomendado). Inclui também comandos rápidos locais.

Requisitos mínimos (para esta seção)
- Docker (Engine) e Docker Compose instalados

Rodando com Docker (recomendado)
- Usar Docker isola dependências e facilita a configuração. Preferimos `docker compose` quando possível.

1) Preparar arquivo de variáveis de ambiente
- Copie o exemplo e ajuste valores sensíveis:

```bash
# Copiar variáveis de ambiente
cp .env_docker.exemplo .env
```

2) Subir com Docker Compose (recomendado)

```bash
docker compose -f compose.yml up --build -d

# O projeto estará disponível em: http://localhost:8000

# Aplicar as migrations pendentes (teste)
docker compose -f compose.yml exec django-web python src/manage.py migrate

# Parar e remover containers:
docker compose -f compose.yml down
```

