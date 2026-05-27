# Diagramas C4 — P.R.I.S.M.A

Este documento apresenta a arquitetura do sistema P.R.I.S.M.A utilizando o modelo **C4** (Contexto, Containers, Componentes e Codigo), com diagramas gerados em **Mermaid** para visualizacao direta no GitHub.

---

## Diagrama de Contexto

**Proposito:** Mostrar o sistema como um todo, seus usuarios e as interacoes com sistemas externos.

```mermaid
graph TB
    %% Entidades Externas
    User["<b>Usuario</b><br>Cidadao / Pesquisador"]
    Admin["<b>Administrador</b><br>Gestor do Sistema"]
    
    %% Sistema Principal
    System["<b>P.R.I.S.M.A</b><br>Sistema de Acompanhamento<br>Legislativo"]
    
    %% Sistemas Externos
    CamaraAPI["<b>API Camara</b><br>Dados Abertos<br>dadosabertos.camara.leg.br"]
    SenadoAPI["<b>API Senado</b><br>Dados Abertos<br>dadosabertos.senado.leg.br"]
    
    %% Conexões do Usuario
    User -->|"Consulta proposicoes<br>Configura alertas<br>Favorita processos"| System
    
    %% Conexões do Administrador
    Admin -->|"Gerencia dados<br>Configura sistema<br>Visualiza metricas"| System
    
    %% Conexões com Sistemas Externos
    System -->|"GET /proposicoes<br>GET /tramitacoes<br>GET /votacoes"| CamaraAPI
    System -->|"GET /projetos<br>GET /materias<br>GET /votacoes"| SenadoAPI
    
    %% Estilos
    classDef user fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef system fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef external fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    
    class User,Admin user
    class System system
    class CamaraAPI,SenadoAPI external
```

---

## Diagrama de Containers

**Proposito:** Mostrar as aplicacoes (containers) que compoem o sistema e como se comunicam.

```mermaid
graph TB
    %% Cliente
    subgraph Browser["<b>Navegador (Cliente)</b>"]
        Frontend["<b>Aplicacao Frontend</b><br>Django Templates<br>HTML / CSS / JavaScript<br>Porta: 8000"]
    end
    
    %% Servidor
    subgraph Server["<b>Servidor Docker</b>"]
        Backend["<b>Aplicacao Backend</b><br>Django + Python<br>Gunicorn / Uvicorn<br>Porta: 8000"]
        Database["<b>Banco de Dados</b><br>PostgreSQL 15<br>PostGIS (futuro)<br>Porta: 5432"]
    end
    
    %% Sistemas Externos
    subgraph External["<b>Sistemas Externos</b>"]
        CamaraAPI["<b>API Camara</b><br>REST / JSON<br>dadosabertos.camara.leg.br"]
        SenadoAPI["<b>API Senado</b><br>REST / JSON<br>dadosabertos.senado.leg.br"]
    end
    
    %% Conexões
    Frontend -->|"HTTP/REST<br>Requisicoes AJAX"| Backend
    Backend -->|"SQL/ORM<br>Consultas e Transacoes"| Database
    Backend -->|"HTTPS/JSON<br>Consumo de Dados"| CamaraAPI
    Backend -->|"HTTPS/JSON<br>Consumo de Dados"| SenadoAPI
    
    %% Estilos
    classDef frontend fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef backend fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef database fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef external fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    
    class Frontend frontend
    class Backend backend
    class Database database
    class CamaraAPI,SenadoAPI external
```

---

## Diagrama de Componentes (Backend)

**Proposito:** Mostrar os componentes internos do backend Django e suas relacoes.

```mermaid
graph TB
    subgraph Django["<b>Django Application - Backend</b>"]
        
        subgraph Core["<b>Core / Config</b>"]
            Settings["settings.py<br>Configuracoes"]
            Urls["urls.py<br>Roteamento Principal"]
            WSGI["wsgi.py / asgi.py<br>Entrada do Servidor"]
        end
        
        subgraph Apps["<b>Django Apps</b>"]
            Home["Home App<br>Pagina Inicial"]
            Processos["Processos App<br>Issue #6"]
            Usuarios["Usuarios App<br>Issue #4"]
            Alertas["Alertas App<br>Issue #17"]
            Dashboard["Dashboard App<br>Issue #18"]
        end
        
        subgraph Layers["<b>Camadas Arquiteturais</b>"]
            Views["Views<br>Controllers<br>(logica de requisicao)"]
            Services["Services<br>Regras de Negocio<br>(Issue #30)"]
            Models["Models<br>Django ORM<br>(Estrutura de Dados)"]
            Repositories["Repositories<br>Acesso a Dados<br>(Issue #30)"]
        end
        
        subgraph Infrastructure["<b>Infraestrutura</b>"]
            Templates["Templates<br>HTML + DTL"]
            Static["Static Files<br>CSS / JS / Imagens"]
            Integrations["Integrations<br>APIs Externas<br>(Issue #7)"]
            Admin["Django Admin<br>Interface de Gestao"]
        end
    end
    
    %% Banco de Dados
    Database[("<b>PostgreSQL</b>")]
    
    %% APIs Externas
    CamaraAPI[("<b>API Camara</b>")]
    SenadoAPI[("<b>API Senado</b>")]
    
    %% Conexões Internas - Core
    Urls --> Views
    Settings --> Apps
    WSGI --> Settings
    
    %% Conexões Internas - Apps para Camadas
    Home -.-> Views
    Processos -.-> Views
    Usuarios -.-> Views
    Alertas -.-> Views
    Dashboard -.-> Views
    
    %% Fluxo entre Camadas
    Views --> Services
    Services --> Models
    Services --> Repositories
    Services --> Integrations
    
    %% Conexões com Templates e Static
    Views --> Templates
    Templates --> Static
    
    %% Acesso ao Banco
    Models --> Database
    Repositories --> Database
    
    %% Integracoes Externas
    Integrations --> CamaraAPI
    Integrations --> SenadoAPI
    
    %% Admin
    Admin --> Models
    
    %% Estilos
    classDef core fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef apps fill:#e0f2f1,stroke:#004d40,stroke-width:2px,color:#000
    classDef layers fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef infra fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#000
    classDef database fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef external fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    
    class Core,Settings,Urls,WSGI core
    class Apps,Home,Processos,Usuarios,Alertas,Dashboard apps
    class Layers,Views,Services,Models,Repositories layers
    class Infrastructure,Templates,Static,Integrations,Admin infra
    class Database database
    class CamaraAPI,SenadoAPI external
```

---

## Fluxo de Dados Completo

**Proposito:** Mostrar a sequencia de interacoes em uma requisicao tipica.

```mermaid
sequenceDiagram
    autonumber
    
    actor U as Usuario
    participant F as Frontend
    participant V as View
    participant S as Service
    participant M as Model
    participant DB as PostgreSQL
    participant I as Integration
    participant API as API Externa
    
    Note over U,API: Cenário: Usuario busca um processo legislativo
    
    U->>F: Acessa URL /processos/123/
    F->>V: GET /processos/123/
    
    Note over V: Valida parametros<br>Verifica permissoes
    
    V->>S: buscar_processo(id=123)
    S->>M: Processo.objects.get(id=123)
    M->>DB: SELECT * FROM processos WHERE id=123
    DB-->>M: Retorna dados (row)
    M-->>S: Retorna objeto Processo
    
    alt Dados Desatualizados (mais de 6 horas)
        S->>I: atualizar_dados_externos(id=123)
        I->>API: GET /proposicoes/123
        API-->>I: JSON com dados atualizados
        I-->>S: Dados transformados
        S->>M: update_or_create(...)
        M->>DB: INSERT/UPDATE processo
    end
    
    S-->>V: Retorna Processo (atualizado)
    
    V->>F: render(request, 'detalhe.html', context)
    F-->>U: Exibe pagina com dados do processo
    
    Note over U,API: Cenário alternativo: Processo nao existe
    
    V->>S: buscar_processo(id=99999)
    S->>M: Processo.objects.get(id=99999)
    M->>DB: SELECT * FROM processos WHERE id=99999
    DB-->>M: Retorna vazio
    M-->>S: DoesNotExist exception
    S-->>V: Processo nao encontrado
    V->>F: raise Http404()
    F-->>U: Exibe pagina 404
```

---

## Referencias

- [Modelo C4 - Documentacao Oficial](https://c4model.com/)
- [Mermaid.js - Documentacao](https://mermaid.js.org/)
- [Django Architecture - Documentacao Oficial](https://docs.djangoproject.com/)
- [Issue #31 - Documentacao de Arquitetura](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/31)

---
