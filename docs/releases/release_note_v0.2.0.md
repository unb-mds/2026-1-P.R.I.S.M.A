# Release Notes - P.R.I.S.M.A

**Versao:** v0.2.0
**Data:** 26/06/2026

---

## Resumo da Release

- **Codigo e infraestrutura (60%)** – Backend, integracoes com APIs, modelos de dados, autenticacao, alertas, SLA, dashboard, favoritos, perfil de usuario, linters e pre-commit.
- **Praticas ageis (30%)** – 8 sprints documentadas, GitHub Projects (kanban), commits atomicos e rastreabilidade de issues e PRs.
- **Documentacao (10%)** – README atualizado com Docker/uv e documentacao de arquitetura.

---

## O que foi feito na Release 2

### Codigo e Infraestrutura (60%)

#### Backend e Integracoes

- **Sincronizacao com APIs da Camara e do Senado:** Integracao com API de Dados Abertos da Camara e com a nova API do Senado para atualizar dados de propostas e tramitacoes. Extrai detalhes de tramitacoes e gera notificacoes automaticas para novas movimentacoes.
  - **Link:** [#7 - Consumo de Dados Abertos (Camara e Senado)](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/7)

- **Modelos e dados de processo:** Implementacao de modelos centrais: ProcessoLegislativo, Movimentacao, TermoMonitorado, Notificacao e UserProfile. Relacoes entre usuarios, processos e alertas permitem monitoramento e acompanhamento personalizado.
  - **Link:** [#6 - Estrutura Base do Processo Legislativo e Termos](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/6)

- **Sistema de usuarios e autenticacao:** Configuracao do sistema de usuarios e login, com perfis e preferencias armazenados em UserProfile.
  - **Link:** [#4 - Configuracao de Sistema de Usuarios e Login](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/4)

- **Inicializacao do projeto Django:** Configuracao inicial do Django, incluindo estrutura de pastas, settings base e integracao com banco de dados.
  - **Link:** [#3 - Inicializacao do Projeto Django](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/3)

- **Alertas e notificacoes:** Implementacao do motor de alertas com notificacoes de estagnacao e atualizacao de processos.
  - **Link:** [#17 - Motor de Alertas (Favoritos e Dormentes)](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/17)

- **Tracking de tempo e SLA:** Monitoramento de tempo de fila e SLA para processos legislativos.
  - **Link:** [#16 - Tracking de Tempo de Fila e SLA](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/16)

- **Indicadores de tempo medio:** Calculo e consolidacao de indicadores de tempo medio de tramitacao e eficiencia.
  - **Link:** [#18 - Indicadores de Tempo Medio e Consolidacao](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/18)

- **Timeline e historico de tramitacao:** Estrutura do historico de tramitacao com timeline e registro de eventos.
  - **Link:** [#14 - Timeline e Historico de Tramitacao](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/14)

#### Frontend e Interface (inclui atualizacao da Gitpage)

- **Dashboard operacional de processos:** Implementacao do painel principal com indicadores de processos em andamento, processos estagnados e tempo medio de tramitacao. Calcula tempo medio de tramitacao a partir da data da primeira movimentacao e mostra contadores de processos em andamento e estagnados.
  - **Link:** [#62 - Adaptar dashboard para exibicao de velocidade e duracao de tramite](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/62)

- **Landing page e visao do produto:** Atualizacao da landing page com nova identidade visual, fluxo de dados e apresentacao do problema/solucao. A Gitpage foi atualizada para refletir a nova interface e experiencia do usuario.
  - **Link:** [Gitpage do Projeto](https://unb-mds.github.io/2026-1-P.R.I.S.M.A/)

- **Lista de processos com busca e filtros:** Criacao da pagina de processos com paginacao, filtros por ano, numero, tipo de proposicao, status e pesquisa livre em ementa ou ID. O sistema sincroniza sob demanda os processos exibidos na pagina atual.
  - **Link:** [#64 - Focar listagem e timeline de proposicoes no controle de SLA](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/64)

- **Favoritos e gerenciamento personalizado:** Adicao de favoritos/acompanhar proposicoes, com visualizacao de favoritos e filtros por status: todas, estagnadas, em tramitacao normal e urgencia. KPI de favoritos com totais, estagnadas, urgencia, tramitando e aprovadas.
  - **Link:** [#63 - Modificar filtros e metricas de favoritos para recortes temporais](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/63)

- **Alertas de processo e notificacoes:** Melhoria da gestao de alertas com notificacoes do tipo estagnacao e atualizacao. Pagina de alertas com lista para o usuario autenticado, contagem de urgencia e volume de estagnacao.
  - **Link:** [#61 - Reestruturar alertas para focar em prazos e estagnacao](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/61)

- **Perfil de usuario e preferencias:** Tela de usuario para ajustar preferencias de receber alertas de estagnacao, limite de dias e notificacoes de novas movimentacoes. Perfil armazenado em UserProfile.
  - **Link:** [#66 - Adicionar painel de configuracao para alertas de prazos e estagnacao](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/66)

#### Qualidade e Infraestrutura

- **Linters, formatadores e pre-commit:** Configuracao de ferramentas de qualidade de codigo (Black, Flake8, isort, Prettier) e integracao com pre-commit para garantir padronizacao e qualidade antes de cada commit.
  - **Link:** [#55 - Configurar linters, formaters e precommit](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/55)

---

### Praticas Ageis (30%)

- **Sprints documentadas:** 8 sprints completas (sprint-0 a sprint-7) com planning, review e retrospectiva registradas.
- **Gestao de tarefas:** Uso de quadro kanban (GitHub Projects) com colunas Todo -> In Progress -> Done, garantindo rastreabilidade de issues e PRs.
- **Commits atomicos:** Adocao de commits descritivos e atomicos, vinculados a issues e PRs.
- **Link:** [Documentacao das Sprints](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/tree/main/docs/Sprints)

---

### Documentacao (10%)

- **README:** Atualizado com instrucoes para rodar o projeto com Docker (recomendado) e localmente com uv.
- **Arquitetura:** Documentacao complementar com decisoes tecnicas e estrutura de pastas.
- **Link:** [README do Projeto](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/blob/main/README.md)

---

## Links uteis

- [Todas as issues do projeto](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues)
- [Gitpage do projeto](https://unb-mds.github.io/2026-1-P.R.I.S.M.A/)
- [README / Setup do projeto](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/blob/main/README.md)
- [Documentacao das Sprints](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/tree/main/docs/Sprints)

---
