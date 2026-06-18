# Arquitetura Interna — P.R.I.S.M.A

---

## 1. Estrutura de Pastas (ATUAL)

2026-1-SQUAD11/
├── .github/ # GitHub Actions workflows
├── docs/ # Documentação do projeto (MkDocs)
├── estudo/ # Estudos e pesquisas da equipe
├── figma/ # Assets exportados do Figma
├── src/ # Código fonte principal
│ ├── config/ # Configurações Django
│ │ ├── settings.py # Configurações (ambiente, apps, banco)
│ │ ├── urls.py # Rotas principais do projeto
│ │ ├── asgi.py # Entrada para servidores ASGI
│ │ └── wsgi.py # Entrada para servidores WSGI
│ ├── home/ # App inicial (página home)
│ │ ├── views.py # Lógica da view home
│ │ ├── models.py # Modelos do app home
│ │ ├── admin.py # Configuração do admin
│ │ ├── apps.py # Configuração do app
│ │ └── tests.py # Testes unitários
│ ├── migrations/ # Migrações de banco de dados
│ ├── templates/ # Templates HTML
│ │ └── exemplo.html
│ └── manage.py # Script de gerenciamento Django
├── .env # Variáveis de ambiente (não versionado)
├── .env_docker_exemplo # Exemplo de .env para Docker
├── .env_local_exemplo # Exemplo de .env para desenvolvimento local
├── .gitignore
├── .python-version # Versão do Python (via pyenv)
├── compose.yml # Docker Compose (serviços)
├── dockerfile # Dockerfile para a aplicação
├── LICENSE
├── manage.py # Gerenciador (symlink ou arquivo)
├── pyproject.toml # Projeto Python e dependências
├── README.md
├── requirements.txt # Dependências Python
└── uv.lock # Lock file do UV (fast package manager)

---

## 2. Tecnologias por Camada

| Camada             | Localização                  | Tecnologia                      | Responsabilidade      |
| ------------------ | ---------------------------- | ------------------------------- | --------------------- |
| **Templates**      | `src/templates/`             | HTML + Django Template Language | Interface visual      |
| **Views**          | `src/*/views.py`             | Python + Django                 | Lógica de negócio     |
| **Models**         | `src/*/models.py`            | Python + Django ORM             | Estrutura de dados    |
| **Config/URLs**    | `src/config/`                | Python                          | Rotas e configurações |
| **Banco de Dados** | PostgreSQL (via Docker)      | SQL                             | Armazenamento         |
| **Container**      | `compose.yml` + `dockerfile` | Docker                          | Ambiente isolado      |

---

## 3. Fluxo de Dados (Requisição HTTP → Resposta)

Com base na estrutura atual:

Requisição chega → src/config/urls.py roteia
↓

View correspondente (ex: src/home/views.py) processa
↓

View consulta Model (src/home/models.py)
↓

Model acessa PostgreSQL (ORM)
↓

View renderiza template (src/templates/)
↓

Resposta HTTP retorna ao navegador

---

## 4. Configuração de Ambiente (Docker)

Com base nos arquivos `.env_docker_exemplo` e `compose.yml`:

```bash
# Subir o ambiente completo
docker compose up

# Serviços definidos :
# - db: PostgreSQL
# - app: Django
```
