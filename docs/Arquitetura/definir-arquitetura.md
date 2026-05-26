# Definição da Arquitetura — P.R.I.S.M.A

## Arquitetura Escolhida: **MVC (Model-View-Controller) / MTV do Django**

O P.R.I.S.M.A utiliza a arquitetura **MTV (Model-Template-View)** nativa do Django, que é uma variação do padrão MVC (Model-View-Controller).

## Por que esta escolha?

| Motivo | Explicação |
|--------|------------|
| **Nativa do Django** | O framework já organiza o código desta forma, sem necessidade de camadas extras |
| **Separação de responsabilidades** | Model (dados), View (lógica) e Template (interface) ficam isolados |
| **Facilidade de manutenção** | Cada componente tem seu lugar definido |
| **Escalabilidade** | Permite crescimento organizado do código |
| **Curva de aprendizado** | A equipe já estudou Django (issue #3) |

## Estrutura Adotada
┌─────────────────────────────────────────────────────┐
│ Template (HTML) │
│ Interface com o usuário │
└───────────────────────┬─────────────────────────────┘
↓ (requisição HTTP)
┌─────────────────────────────────────────────────────┐
│ View (views.py) │
│ Lógica de negócio + controle │
└───────────────────────┬─────────────────────────────┘
↓ (consulta)
┌─────────────────────────────────────────────────────┐
│ Model (models.py) │
│ Acesso ao banco de dados │
└───────────────────────┬─────────────────────────────┘
↓
┌─────────────────────────────────────────────────────┐
│ PostgreSQL │
│ Banco de Dados │
└─────────────────────────────────────────────────────┘

## Comparação com outras arquiteturas

| Arquitetura | Vantagens | Desvantagens | Por que não foi escolhida |
|-------------|-----------|--------------|--------------------------|
| **MVC/MTV** | Nativa do Django, simples | Pode ficar confusa em projetos muito grandes |  **ESCOLHIDA** |
| **Camadas** | Organizada, fácil manutenção | Exige mais código boilerplate | Desnecessária para o escopo atual |
| **Modular** | Ótima para equipes grandes | Exige padronização rígida | Projeto ainda não tem essa escala |
| **Clean Architecture** | Muito escalável | Complexa para projetos pequenos/médios | Overengineering para o P.R.I.S.M.A |

## Decisão Final

O P.R.I.S.M.A adotará a arquitetura **MTV do Django**, aproveitando as vantagens nativas do framework e garantindo:

-  Código organizado por padrão
-  Separação clara entre dados, lógica e interface
-  Facilidade para novos desenvolvedores se integrarem
-  Consistência com a documentação oficial do Django

---

**Referências:**
- [Estudo sobre Django - issue #3](https://github.com/unb-mds/2026-1-P.R.I.S.M.A/issues/3)
- [Django MTV Architecture - Documentação Oficial](https://docs.djangoproject.com/en/5.0/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view)