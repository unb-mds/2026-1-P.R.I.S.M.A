# Stack Back-end – P.R.I.S.M.A

##  Definição Oficial

| Item | Tecnologia | Status |
|------|------------|--------|
| **Linguagem** | Python 3.11+ |  definido |
| **Framework** | Django |  definido (issue #3) |
| **Banco de Dados** | PostgreSQL 15 |  definido (issue #6) |
| **ORM** | Django ORM |  definido |
| **Containerização** | Docker + Docker Compose |  definido (issue #32) |

| **Testes** | pytest-django |  definido |

---

## Justificativa das Escolhas

### Django

-  Framework full stack, já vem com autenticação, admin, ORM
-  Segurança contra ataques comuns (SQL injection, XSS, CSRF)
-  Gerenciamento de migrações integrado
-  Comunidade grande e madura
-  A equipe já estudou (issue #3)

### PostgreSQL

-  Banco relacional robusto e confiável
-  Suporte a dados abertos (modelagem legislativa)
-  Performance comprovada
-  A equipe já estudou (issue #6)

### Docker

-  Garante consistência entre ambientes
-  Facilita onboarding de novos desenvolvedores
-  Documentação de setup já existe (issue #32)
-  A equipe já estudou (issue #32)

---


---

## Dependências Principais

| Pacote | Uso |
|--------|-----|
| `django` | Framework web |
| `psycopg2-binary` | Driver PostgreSQL |
| `pytest-django` | Testes |

---

## Segurança

| Prática | Implementação |
|---------|---------------|
| **Autorização** | Permissões baseadas em grupos |
| **Senhas** | Hashing com PBKDF2 (padrão Django) |
| **CSRF** | Proteção ativa por padrão |
| **SQL Injection** | ORM previne |

---

**Referências:**
- [Issue #3 - Inicialização Django](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/3)
- [Issue #4 - Sistema de Usuários](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/4)
- [Issue #6 - Estrutura de Dados](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/6)
- [Issue #32 - Configuração de Ambiente](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/32)