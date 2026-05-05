# 2026-1-Squad11

Resumo
- Projeto: repositório do grupo Squad11 (semestre 2026-1).
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
cp .env.example .env
# Edite .env conforme necessário
```

2) Subir com Docker Compose (recomendado)

```bash
docker compose -f compose.yml up --build -d
# Ver logs:
docker compose -f compose.yml logs -f
# Parar e remover containers:
docker compose -f compose.yml down
```

3) Build e run com Docker (sem Compose)

```bash
docker build -t squad11 .
docker run -p 8000:8000 --env-file .env squad11
```

Notas sobre o container
- O container espera ouvir a porta `8000` (exponha essa porta ao executar).
- Se o `compose.yml` define serviços (DB, redis, etc.), o Compose cuidará da rede e volumes.

Comandos locais rápidos (alternativa)
- Ativar venv e instalar deps (se preferir rodar sem Docker):

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Observações
- As configurações do Django estão em [src/config/settings.py](src/config/settings.py).
- Documentação de sprints e backlog em `docs/`.

Execução com Docker (opção rápida)
- Se preferir isolar o ambiente, use Docker. Exemplos mínimos:

Build da imagem:

```bash
docker build -t squad11 .
```

Rodar container:

```bash
docker run -p 8000:8000 --env-file .env squad11
```

Usando Docker Compose (se aplicável):

```bash
docker compose -f compose.yml up --build
```

Comandos úteis
- Ativar ambiente: `source venv/bin/activate`
- Instalar deps: `pip install -r requirements.txt`
- Migrar DB: `python manage.py migrate`
- Criar superuser: `python manage.py createsuperuser`
- Rodar servidor: `python manage.py runserver`

Depuração e problemas comuns
- Erro: "Couldn't import Django" — verifique se o venv está ativado e `django` está instalado.
- Permissões de porta (Linux) — use portas acima de 1024 ou `sudo` para portas baixas.

Referências
- Configurações principais: [src/config/settings.py](src/config/settings.py)
- Documentação de sprints e backlog: `docs/`

Licença
- Consulte o arquivo `LICENSE`.

---
_Atualizar este arquivo conforme o projeto evolui._