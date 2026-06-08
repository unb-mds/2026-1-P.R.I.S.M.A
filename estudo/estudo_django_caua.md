# Estudo sobre Django

## O que é Django?

Django é um framework web feito em Python. Framework é um conjunto de ferramentas que já vem bem completo.

Ele é full stack, ou seja, cuida tanto da parte do servidor (backend) quanto da parte de organização do banco de dados e até ajuda com os templates (frontend).

Django é conhecido por ser eficiente, seguro e escalável. Dá pra começar com um site pequeno e se um dia ele crescer pra milhões de usuários, o Django aguenta.

Um exemplo famoso: o Instagram usa Django.Com bilhões de pessoas usam todo dia. Então dá pra confiar.

O Django é basicamente um conjunto de ferramentas em Python que facilita a vida de quem desenvolve web. Você escreve menos código, ganha tempo, e ainda faz as coisas do jeito certo.

## O padrão MVT

Django usa o padrão Model-View-Template.

### Model (modelo)

O Model é a parte que cuida do banco de dados. Você escreve uma classe em Python, e o Django transforma aquilo em tabela no banco. Sem escrever SQL na mão.

Por exemplo, se você quer guardar usuários com nome e email, você faz uma classe Usuario com os campos nome e email. O Django cria a tabela sozinho, faz as colunas, e ainda te dá um monte de funções pra buscar, salvar, deletar.

O Model gerencia a estrutura das tabelas. Ele é o responsável por falar com o banco de dados sem você precisar se preocupar com os detalhes de baixo nível.

### View (visão)

A View é onde mora a lógica. É ela que recebe a requisição que vem do usuário, faz as coisas acontecerem, e devolve uma resposta.

Se o usuário pedir a lista de produtos, a view vai no banco (usando o Model), busca os produtos, processa o que precisar, e manda pro template.

A View controla as regras. Quem decide o que pode ou não pode ser feito é ela. Quem decide o que mostrar em cada situação também.

### Template

Template é o frontend. É o HTML com uns lugares especiais onde você joga os dados que vieram da view.

O template não tem lógica complicada. Ele só recebe os dados e mostra na tela do jeito que o designer definiu. Você pode colocar variáveis, uns loops básicos (tipo mostrar todos os itens de uma lista), e uns ifs simples.

O layout visual fica no template. É lá que você coloca CSS, JavaScript, imagens.

### O fluxo completo MVT

Quando alguem acessa uma pagina:

1. A requisição chega no Django
2. Uma view é chamada (você define qual URL chama qual view)
3. A view conversa com o model pra buscar ou salvar dados
4. A view processa a logica necessaria
5. A view passa os dados pro template
6. O template gera o HTML
7. O Django devolve esse HTML pro navegador

Model cuida do banco, View cuida da lógica, Template cuida da aparência.

## Vantagens do Django

O Django já vem com um monte de coisa pronta.

### Segurança contra ataques

Django já bloqueia vários tipos de ataque comuns. Coisa de segurança web que a galera sofre pra implementar, o Django já faz automático.

### Gerenciamento de migrações de banco de dados

Quando você muda seu model (adiciona um campo novo, por exemplo), o Django descobre o que mudou e cria um arquivo de migração. Você roda um comando e ele altera o banco sem perder dados.

### Interface de administração (admin)

O Django cria automaticamente um painel de administração pra você. É uma página pronta, bonitinha, onde você pode criar, editar e deletar os dados do seu sistema.

Isso é muito útil pra testar, pra gerenciar conteúdo, ou pra entregar rápido um sistema interno. Muita empresa usa o admin do Django como ferramenta de gestão.

Django é um framework muito bom, ele já vem com muitas funcionalidades.

Django é Python.

## Fonte de estudo

hashtagtreinamento
Autor do artigo
Heitor Catunda
Video no youtube visto: https://youtu.be/1SgIkOczqFY?si=sGNc5d3jY-y5issn
