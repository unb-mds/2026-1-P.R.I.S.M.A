# Tecnologias do Projeto — P.R.I.S.M.A

Este documento descreve as ferramentas e tecnologias que compõem o ecossistema do P.R.I.S.M.A.

---

## 1. Django

### O que é

Django é um framework web full stack escrito em Python. Ele fornece autenticação, ORM, admin, templates e roteamento de URLs prontos para uso.

### Como funciona no P.R.I.S.M.A

- Gerencia as rotas (urls.py → views.py → models.py)
- ORM para acesso ao PostgreSQL
- Interface administrativa automática
- Sistema de autenticação (issue #4)

### Papel no sistema

É o **coração do backend**. Toda requisição passa por ele.

---

## 2. PostgreSQL

### O que é

Banco de dados relacional robusto, conhecido por confiabilidade e conformidade com padrões SQL.

### Como funciona no P.R.I.S.M.A

- Armazena todos os dados do sistema
- Usado via Django ORM
- Containerizado com Docker

### Papel no sistema

**Persistência de dados**: processos, usuários, alertas, configurações.

---

## 3. Docker

### O que é

Tecnologia de containers que empacota aplicações com suas dependências.

### Como funciona no P.R.I.S.M.A

- Define `docker-compose.yml` com serviços: backend, banco, frontend
- Garante que todos rodem o mesmo ambiente
- Facilita deploy em produção

### Papel no sistema

**Infraestrutura como código**: qualquer desenvolvedor sobe o projeto com `docker-compose up`.

---

## 4. Git + GitHub

### O que é

Git é controle de versão. GitHub é hospedagem de repositórios Git na nuvem.

### Como funciona no P.R.I.S.M.A

- Todo código versionado
- Issues para gerenciamento de tarefas
- Pull requests para revisão de código
- GitHub Pages para documentação (issue #26)

### Papel no sistema

**Organização e colaboração**: centraliza código, documentação e gestão do projeto.

---

## 5. Figma

### O que é

Ferramenta de design de interfaces baseada em nuvem.

### Como funciona no P.R.I.S.M.A

- Protótipos de baixa e alta fidelidade (issue #29)
- Colaboração em tempo real entre a parte de desing e devs
- Dev Mode para desenvolvedores extraírem especificações

### Papel no sistema

**Design e prototipagem**: validação visual antes da codificação.

---

## 6. MkDocs + GitHub Pages

### O que é

MkDocs é um gerador de sites estáticos para documentação. GitHub Pages hospeda o site gerado.

### Como funciona no P.R.I.S.M.A

- Documentação escrita em Markdown
- MkDocs gera HTML
- GitHub Pages publica (issue #26)

### Papel no sistema

**Documentação acessível**: centraliza informações do projeto para a equipe.

---

## 7. Django Filter (django-filter)

### O que é

Biblioteca para criação declarativa de filtros de consulta no Django.

### Por que será usado

- Simplifica a criação de buscas e filtros
- Reduz código boilerplate
- Previne SQL injection (usa ORM)
- Integração nativa com Django REST Framework

### Papel no sistema

**Busca e filtragem de dados**: processos legislativos, proposições, alertas.

---

## 8. Integrações Externas (em desenvolvimento)

| API | Uso | Status |
|-----|-----|--------|
| Dados Abertos Câmara | Proposições, tramitações, parlamentares | issue #7 |
| Dados Abertos Senado | Projetos de lei, votações | issue #7 |

---

**Referências:**
- [Estudo sobre Django](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/3)
- [Estudo sobre Docker](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/32)
- [Estudo sobre PostgreSQL](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/6)
- [Estudo sobre Figma](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/29)
- [Estudo sobre Git/GitHub](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/26)
- [Estudo sobre Django Filter](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/30)