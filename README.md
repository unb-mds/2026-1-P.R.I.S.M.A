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
# Copiar variáveis de ambiente
cp .env.example .env

# Editar .env se necessário (geralmente mantém o padrão para testes)
nano .env  # ou use qualquer editor
```

2) Subir com Docker Compose (recomendado)

```bash
docker compose -f compose.yml up --build -d
# Ver logs:
docker compose -f compose.yml logs -f

# O projeto estará disponível em: http://localhost:8000

#Verificar se ambos containers estão rodando :
docker ps

# Aplicar as migrations pendentes (teste)
docker compose -f compose.yml exec django-web python src/manage.py migrate

# Verificar se as migrações foram aplicadas
docker compose -f compose.yml exec django-web python src/manage.py showmigrations

# Parar e remover containers:
docker compose -f compose.yml down



```
O warning sobre DJANGO_LOGLEVEL não afeta o funcionamento é apenas uma variavel opcional não configurada.
A porta 5432 do PostgreSQL não precisa ter interface exposta publicamente.

Se no docker ps, apareceu 0.0.0.0:5432->5432/tcp, mas isso é uma configuração do compose.yml que expôs a porta para facilitar debug. Em produção, não deveria ser exposta.


3) Build e run com Docker (sem Compose)

 Importante: Sem Compose = Sem Banco de Dados
Rodar apenas o container Django sem o Compose significa que não haverá PostgreSQL. Para funcionar, você precisa ajustar o .env para usar SQLite (banco local).

```bash

# Editar o arquivo .env
nano .env
# ou
notepad .env  # No Windows

Altere para usar SQLite (banco de dados local, sem necessidade de PostgreSQL):

DEBUG=1
SECRET_KEY=teste-key-123456789
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

Caso esteja com problemas há outra opção  

# Apagar o arquivo confuso
rm .env

# Criar um novo .env limpo
cat > .env << 'EOF'
# Django Settings
DEBUG=1
SECRET_KEY=django-insecure-test-key-123456789
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite (para rodar sem Docker Compose)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=/src/db.sqlite3

# Porta
PORT=8000
EOF

Verificar se corrigiu:

cat .env

##build da imagem
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
