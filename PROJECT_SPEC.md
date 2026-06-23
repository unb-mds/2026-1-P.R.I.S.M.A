# PRISMA Insight - Especificação Técnica do Projeto

Este documento descreve as especificações completas para a reconstrução do **PRISMA Insight**, um dashboard de monitoramento de repositórios GitHub focado em análise de métricas de software e visibilidade de progresso para o time P.R.I.S.M.A.

## 1. Visão Geral
O PRISMA Insight é uma Single Page Application (SPA) reativa que se conecta à API do GitHub para extrair e visualizar dados críticos de desenvolvimento: commits, issues e diferenças de código (diffs).

## 2. Pilha Tecnológica (Tech Stack)
- **Frontend:** React 19 + TypeScript
- **Estilização:** Tailwind CSS (Arquitetura Dark-First)
- **Animações:** `motion` (motion/react)
- **Visualização de Dados:** Recharts (Gráficos de Área e Barra)
- **Ícones:** Lucide React
- **Processamento de Datas:** date-fns

## 3. Identidade Visual (Design System)
O projeto utiliza um tema "Cyber-Noir" / "High-Tech":
- **Base:** `#0f172a` (Slate 950)
- **Cards:** `#1e293b` (Slate 800) com bordas Slate 800.
- **Destaque Primário:** Cyan 500 (`#22d3ee`) - usado para interações, luzes e status ativos.
- **Tipografia:** 
  - Sans: Inter (ou similar)
  - Mono: Fontes mono-espaçadas para SHAs, timestamps e logs.
- **Efeitos:** Blur de fundo (backdrop-blur), Glow (sombras cyan pulsantes) e animações de entrada suaves (fade-in, scale-up).

## 4. Funcionalidades Principais

### 4.1. Autenticação e Sincronização
- Campo de input para Personal Access Token do GitHub.
- Armazenamento persistente no `localStorage` sob a chave `gh_token`.
- Botão "Sincronizar" com feedback visual de carregamento e animação de rotação (spin).

### 4.2. Dashboards de Métricas (Top Cards)
Quatro cards principais no topo com animações de hover e glows:
1. **Frequência de Commits:** Total de commits com um mini sparkline decorativo.
2. **Open Issues:** Contagem de issues com estado 'open'.
3. **Colaboradores:** Número de autores únicos baseados em email, com avatars sobrepostos.
4. **Build Status:** Status simulado de integridade do sistema (100% Healthy) com pulso animado.

### 4.3. Monitoramento Analítico (Gráficos)
- **StatsCharts:** Gráfico de área composto mostrando a progressão temporal de Commits e Issues. 
- Eixo X agregando dados por intervalos de tempo significativos.

### 4.4. Mapa de Calor (Activity Heatmap)
- Visualização estilo GitHub de 90 dias de atividade.
- Soma ponderada de Commits + Issues abertas/fechadas.
- Cores em escala de Cyan (Escuro para claro conforme densidade).

### 4.5. Estatísticas de Colaboradores (Ranking)
- Grid de cards de usuários com lógica de mapeamento `email -> login`.
- Reconhecimento do "Top Contributor" com ícone de troféu (`Award`).
- Métricas individuais: Contagem de commits, issues e último comentário/mensagem de commit.

### 4.6. Timeline Semanal
- Navegação entre semanas (Left/Right).
- Sumário de atividade semanal.
- Log de atividades da semana selecionada com distinção visual entre commits e issues.

### 4.7. Git Log & Seleção de Diff
- Tabela interativa de commits.
- Permite selecionar EXATAMENTE dois commits (Base e Head) clicando nas linhas.
- Suporte para limpar seleção.

### 4.8. Seção de Diferenças (Diff Explorer)
- Só aparece quando dois commits estão selecionados.
- Exibe estatísticas de Adições (+) e Remoções (-).
- Lista de arquivos alterados com syntax highlighting básico para patches de diff (Verde para adições, Rosa para remoções).

## 5. Estrutura de Arquivos Recomendada
```
/src
  /components
    ActivityHeatmap.tsx     # Grid de 90 dias
    Charts.tsx              # Recharts implementation
    CollaboratorStats.tsx   # Ranking e Avatars
    CommitLog.tsx           # Tabela de commits
    DiffSection.tsx         # Visualizador de Diff/Patch
    WeeklyTimeline.tsx      # Navegação temporal
  App.tsx                   # Layout principal e orquestração de dados
  index.css                 # Configurações do Tailwind @theme
```

## 6. Lógica de Dados (API GitHub)
O app deve consumir os seguintes endpoints:
1. `GET /repos/{owner}/{repo}/commits`
2. `GET /repos/{owner}/{repo}/issues?state=all`
3. `GET /repos/{owner}/{repo}/compare/{base}...{head}` (para a Seção de Diff)

## 7. Melhores Práticas Implementadas
- **Lazy Loading:** O dashboard carrega os dados sob demanda ou na inicialização se o token existir.
- **Tratamento de Erros:** Banner de erro persistente e estilizado se a API falhar (ex: Token inválido).
- **Acessibilidade:** Targets de clique claros e feedback tátil visual em todos os botões.
- **Responsividade:** Layout em Grid que se adapta de 1 a 4 colunas dependendo do viewport.
