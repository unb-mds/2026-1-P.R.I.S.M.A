# 2026-1-P.R.I.S.M.A

## Sobre

P.R.I.S.M.A é uma aplicação Django para monitoramento de processos e proposições legislativas. O sistema permite buscar e filtrar processos, acompanhar favoritos, receber alertas de estagnação e novas movimentações, e sincronizar dados com APIs públicas da Câmara e do Senado.

## Principais funcionalidades

- Dashboard com indicadores de processos em andamento, estagnados e tempo médio de tramitação.
- Página de processos com filtros por ano, número, tipo de proposição, status e pesquisa livre.
- Favoritos / acompanhar proposições com visão de estado e urgência.
- Alertas de estagnação e atualizações de movimentações para usuários autenticados.
- Integração com APIs da Câmara e do Senado para sincronização de dados legislativos.
- Perfil de usuário com preferências de notificações.

## Links úteis

- Gitpage: https://unb-mds.github.io/2026-1-P.R.I.S.M.A/
- Documentação do projeto: `docs/`
- Contribuição: `docs/CONTRIBUTING.md`
- Código de conduta: `docs/CODE_OF_CONDUCT.md`
- Release notes: `docs/releases/`

## Requisitos

- Docker Engine e Docker Compose (recomendado)
- Python 3.12+ (para execução local)
- PostgreSQL (para execução local sem Docker)

## Rodar com Docker (recomendado)

O ambiente Docker isola dependências e usa PostgreSQL em container.

### 1) Preparar arquivo de variáveis de ambiente

Copie o exemplo e ajuste os valores conforme necessário:

```bash
cp .env_docker.exemplo .env
```

### 2) Subir o ambiente

```bash
docker compose -f compose.yml up --build -d
```

### 3) Aplicar migrations

```bash
docker compose -f compose.yml exec django-web python src/manage.py migrate
```

### 4) Criar superuser (opcional)

```bash
docker compose -f compose.yml exec django-web python src/manage.py createsuperuser
```

### 5) Acessar a aplicação

Abra em:

```
http://localhost:8000
```

### 6) Parar o ambiente

```bash
docker compose -f compose.yml down
```

## Rodar local sem Docker

As instruções abaixo usam `uv` para sincronizar dependências e ambiente local. Caso não use `uv`, crie um virtualenv manual e instale `requirements.txt`.

### 1) Instalar `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 2) Sincronizar dependências

```bash
uv sync
```

### 3) Preparar PostgreSQL local

Instale e inicie o PostgreSQL. Se estiver usando o `.env_local.exemplo`, a configuração padrão é:

- `DATABASE_HOST=127.0.0.1`
- `DATABASE_PORT=5433`
- `DATABASE_NAME=polls`
- `DATABASE_USERNAME=myprojectuser`
- `DATABASE_PASSWORD=password`

Crie o banco e o usuário local usando comandos do PostgreSQL:

```bash
sudo -u postgres psql -c "CREATE USER myprojectuser WITH PASSWORD 'password';"
sudo -u postgres psql -c "CREATE DATABASE polls OWNER myprojectuser;"
```

### 4) Copiar arquivo de ambiente

```bash
cp .env_local.exemplo .env
```

### 5) Aplicar migrations

```bash
uv run src/manage.py migrate
```

### 6) Criar superuser

```bash
uv run src/manage.py createsuperuser
```

### 7) Executar o servidor

```bash
uv run src/manage.py runserver 0.0.0.0:8000
```

## Dependências principais

- Django 6.0.4
- django-crontab
- django-jazzmin
- django-filter
- dotenv
- psycopg[binary]
- requests

Dependências de desenvolvimento estão em `pyproject.toml` no grupo `dev`, incluindo `pytest`, `pytest-django`, `playwright` e `pytest-playwright`.

## Executar testes

```bash
uv run pytest
```

Se não estiver usando `uv`:

```bash
pytest
```

O arquivo `pytest.ini` já define `DJANGO_SETTINGS_MODULE=config.settings` e `pythonpath=src`.

## Estrutura do repositório

- `src/manage.py` — entrypoint Django
- `src/config/` — configurações, URLs e ASGI/WGI
- `src/home/` — views, formulários, templates e páginas principais
- `src/Processos/` — modelos, serviços de sincronização com APIs e filtros
- `src/Usuarios/` — usuário customizado, notificações e perfil
- `docs/` — documentação, padrões, releases e sprint notes
- `compose.yml` — definição dos containers Docker
- `dockerfile` — imagem do container Django
- `entrypoint.sh` — script de inicialização do container
- `.env_docker.exemplo` / `.env_local.exemplo` — exemplos de variáveis de ambiente

## Como contribuir

- Leia `docs/CONTRIBUTING.md` e `docs/CODE_OF_CONDUCT.md`.
- Abra uma issue antes de iniciar mudanças relevantes.
- Crie uma branch de trabalho clara com nome descritivo.
- Faça commits pequenos e significativos.
- Abra um pull request explicando o propósito e referencie a issue relacionada.

## Observações

- Não compartilhe valores secretos ou credenciais no repositório.
- Use `DEBUG=True` apenas em ambientes de desenvolvimento.
- O `entrypoint.sh` configura o cronjob de `django-crontab` e inicializa o serviço `cron` dentro do container.
