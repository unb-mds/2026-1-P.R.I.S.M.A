# 2026-1-P.R.I.S.M.A

## Resumo

- Projeto: P.R.I.S.M.A
- Objetivo: código e material referente às entregas do time (aplicação Django).

## Foco deste README

- Prioriza instruções para rodar o projeto com Docker (recomendado). Inclui também comandos rápidos locais.

## Requisitos mínimos (para esta seção)

- Docker (Engine) e Docker Compose instalados

## Rodando com Docker (recomendado)

Usar Docker isola dependências e facilita a configuração. Preferimos `docker compose` quando possível.

### 1) Preparar arquivo de variáveis de ambiente

Copie o exemplo e ajuste valores sensíveis:

```bash
# Copiar variáveis de ambiente
cp .env_docker.exemplo .env
```

### 2) Subir com Docker Compose (recomendado)

```bash
docker compose -f compose.yml up --build -d

# O projeto estará disponível em: http://localhost:8000

# Aplicar as migrations pendentes (teste)
docker compose -f compose.yml exec django-web python src/manage.py migrate

# Parar e remover containers:
docker compose -f compose.yml down
```

## Rodando sem Docker (PostgreSQL local, usando `uv`)

As instruções abaixo mostram como executar o projeto localmente sem Docker, usando um PostgreSQL local e `uv` para gerenciar dependências e ambiente.

1) Instalar e preparar `uv`

```bash
# Instalar `uv` (se ainda não tiver):
curl -LsSf https://astral.sh/uv/install.sh | sh

# Carregar o helper do `uv` no shell (bash):
source $HOME/.local/bin/env

# Sincronizar dependências e ambiente definido em uv
uv sync
```

2) Preparar PostgreSQL local

Assegure que o PostgreSQL esteja instalado e em execução. Neste ambiente local, ele está disponível na porta `5433`. Em muitas distros Linux você pode usar:

```bash
# Debian/Ubuntu (exemplo):
sudo apt update && sudo apt install -y postgresql postgresql-contrib

# Criar usuário e banco com os valores padrão do .env_local.exemplo:
sudo -u postgres psql -c "CREATE USER myprojectuser WITH PASSWORD 'password';"
sudo -u postgres psql -c "CREATE DATABASE polls OWNER myprojectuser;"
```

Se já tiver um superuser PostgreSQL (ex.: `postgres`) use esse usuário para criar o DB.

3) Copiar o arquivo de ambiente pronto

Copie o arquivo de exemplo para `.env`:

```bash
cp .env_local.exemplo .env
```

4) Aplicar migrations e criar superuser (usando `uv`)

```bash
uv run src/manage.py migrate
uv run src/manage.py createsuperuser
```

5) Executar o servidor (usando `uv`)

```bash
uv run src/manage.py runserver 0.0.0.0:8000
```

Observações

- Nos passos acima assumimos que `src/manage.py` é o comando de gerenciamento do Django (arquivo presente no repositório). Ajuste caminhos se necessário.
- Para desenvolvimento local, mantenha `DEBUG=True` apenas em ambientes seguros.

