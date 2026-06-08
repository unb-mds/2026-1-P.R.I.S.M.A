# O que são Requisitos de Software

Requisitos de software definem o que um sistema precisa fazer e como ele deve se comportar. Eles servem como um "norte" para o projeto, guiando a equipe de desenvolvimento.

## Principais categorias

**Requisitos funcionais**: descrevem as funcionalidades do sistema. Por exemplo: "O sistema deve gerar um PDF com o relatório semanal." Geralmente são visíveis para o usuário.

**Requisitos não funcionais**: tratam das qualidades e restrições do sistema, como desempenho, segurança ou disponibilidade. Exemplo: "O sistema precisa funcionar 24 horas por dia." O usuário não percebe esses requisitos diretamente, mas eles são essenciais para o bom funcionamento.

## Elicitação de requisitos

Elicitação é o processo de descobrir e entender o que o sistema precisa fazer, conversando com clientes, usuários e outros envolvidos. Antes de programar, é preciso saber: o que o usuário quer? Que problemas ele precisa resolver? Como ele trabalha atualmente?

Técnicas comuns incluem entrevistas, questionários, observação, workshops e prototipação. Pular essa etapa pode levar a um sistema que ninguém pediu, funcionalidades esquecidas ou desperdício de tempo e dinheiro.

## Análise de requisitos

Depois de coletar os requisitos, é hora de organizá-los. Nem tudo o que é pedido pode ser feito. Nessa etapa, identificamos conflitos, priorizamos o que é mais importante e avaliamos a viabilidade técnica. O objetivo é deixar os requisitos mais claros e prontos para o desenvolvimento.

## Especificação

Aqui os requisitos são registrados por escrito. A forma de documentar varia conforme o projeto:

- **Documentos formais**: descrições detalhadas e técnicas, com linguagem mais rígida. Úteis em projetos grandes ou críticos. Exemplo: "O sistema deve permitir login com e-mail e senha, validando os dados no banco."

- **User stories/historia de usuarios**: frases curtas sob a perspectiva do usuário, comuns em métodos ágeis como Scrum. Estrutura típica: "Como [tipo de usuário], quero [ação], para [objetivo]." Exemplo: "Como usuário, quero gerar um relatório em PDF para acompanhar minhas atividades semanais."

- **Casos de uso**: descrevem passo a passo a interação entre usuário e sistema, incluindo fluxos normais e exceções. Exemplo: "Usuário acessa o sistema, insere login e senha, sistema valida os dados e direciona para a página inicial."

## Validação

Nesse momento, o cliente ou usuário confirma se os requisitos registrados estão corretos. A pergunta principal é: "É isso mesmo que você quer?" Se houver erro, ainda dá tempo de corrigir antes do desenvolvimento.

## Priorização de requisitos

Como quase sempre há mais trabalho do que tempo disponível, é preciso decidir o que fazer primeiro. Uma técnica bem prática é o **MoSCoW**:

- **Must (indispensável)**: sem esses requisitos, o sistema não funciona direito.
- **Should (relevante)**: trazem muito valor, mas podem ser adiados se necessário.
- **Could (opcional)**: são melhorias ou extras, ficam para depois.
- **Won't (fora do escopo atual)**: itens que ficam para versões futuras, evitando que o projeto cresça sem controle.

## Documentação e rastreabilidade

Documentar requisitos significa deixá-los claros, completos, consistentes e objetivos. Já a rastreabilidade permite acompanhar cada requisito ao longo do projeto: saber de onde veio, onde foi implementado e o que depende dele.
