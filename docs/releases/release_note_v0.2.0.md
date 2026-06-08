# Release Notes – P.R.I.S.M.A (Release 2)

## **Versão:** v0.2.0

## Resumo da Release

- **Código e infraestrutura ** – ambiente Docker, gerenciador UV, linters, pré-commit, testes iniciais e organização do código.
- **Práticas ágeis ** – 8 sprints documentadas, GitHub Projects (kanban), commits atômicos e rastreáveis.
- **Documentação e Gitpage ** – README completo, arquitetura documentada, guias de contribuição e release notes.

---

## Código e Infraestrutura

### Ambiente Docker (produção e desenvolvimento)

- `compose.yml` e `dockerfile` prontos para subir toda a aplicação com um comando.
- Variáveis de ambiente gerenciadas via `.env_docker.exemplo` e `.env_local.exemplo`.
- README com instruções claras para rodar com Docker (recomendado) ou localmente.

### Gerenciador de pacotes UV

- Migração do `pip` para `uv` instalação mais rápida e reproduzível.
- Arquivos `pyproject.toml` e `uv.lock` versionados.
- Comandos `uv sync` e `uv run` padronizados.

### Qualidade e padronização de código

- **Linters e formatadores** configurados:
  - Python: Black (formatação), Flake8 (linting), isort (ordenação de imports)
  - JS/CSS/HTML: Prettier
- **Pre-commit** integrado ao Git: todos os hooks rodam automaticamente antes de cada commit.
- Arquivos de configuração: `.flake8`, `.pre-commit-config.yaml`, `pyproject.toml`.

### Organização do código Django

- Aplicações modulares: `config` (configurações) e `home` (lógica principal).
- Separação clara entre views, models, templates e arquivos estáticos.
- Código já formatado e refatorado segundo as regras dos linters.

---

## Práticas Ágeis

### Sprints documentadas

- **8 sprints completas** (sprint-0 até sprint-7) registradas na pasta `docs/Sprints/`.
- Cada sprint contém planning, review, retrospectiva e entregas realizadas.
- Modelo de sprint padronizado (`template-sprint.md`) para facilitar a documentação futura.

### Gestão de tarefas (GitHub Projects)

- Quadro kanban com colunas: `Todo` → `In Progress` → `Review`→ `Done`.
- Issues e PRs vinculados às tarefas, garantindo rastreabilidade.
- Atribuição de responsáveis e uso de labels (ex: `frontend`, `backend`, `documentation`).

### Rastreabilidade e commits atômicos

- Commits descritivos, atômicos e referenciando issues/PRs.
- Padrões de commit e branch documentados em `documentacao-padroes-commits-branches.md`.
- Uso consistente de Pull Requests para revisão de código.

---

## Documentação e Gitpage

### README e documentação do usuário

- README principal com foco em **Docker (recomendado)** e também em execução local com `uv`.
- Explicação clara de pré-requisitos, variáveis de ambiente, migrações e comandos úteis.
- Guias de instalação e configuração para novos desenvolvedores.

### Documentação de arquitetura (Gitpage)

- Pasta `docs/Arquitetura/` com:
  - `documento-c4.md` – diagramas C4 (contexto, contêineres, componentes).
  - `definir-arquitetura.md` – escolha do padrão MTV do Django.
  - `arquitetura-interna.md` – estrutura de pastas, fluxo de dados, camadas.
  - `tecnologias_projeto.md` – descrição detalhada de cada tecnologia.
- Conteúdo publicado via GitHub Pages

### Documentação comunitária

- `CODE_OF_CONDUCT.md` – código de conduta para colaboradores.
- `CONTRIBUTING.md` – guia de contribuição (como abrir issues, enviar PRs, padrões de commit).
- Templates de issue e PR (em `docs/templates_issue/`).

### Release Notes

- Release anterior (`v0.1.0`) documentada em `docs/releases/release_note_v0.1.0.md`.
- Esta release (`v.2.0`) segue o mesmo padrão, registrando o progresso do projeto.

---
