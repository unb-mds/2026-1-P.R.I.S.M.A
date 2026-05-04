# Estudo sobre Backend

## O que e backend?
Backend é a parte do sistema que o usuário não vê. Enquanto o frontend fica mostrando botão, tela, animação, o backend tá lá atrás fazendo o trabalho pesado.

Ele roda num servidor. Quem cuida de processar dados, aplicar regras, garantir segurança e conversar com banco de dados é ele.

## O que o backend faz?
De forma simples, o backend serve pra:

- Receber o que o frontend manda
- Aplicar as regras que o sistema precisa seguir
- Validar os dados 
- Mexer no banco de dados, seja pra ler ou salvar
- Devolver uma resposta pro frontend

**Um exemplo:** quando você tenta logar num site, o frontend envia teu e-mail e senha. O backend vai lá, vê se o usuário existe, confere a senha e decide se libera ou não. 

## Como frontend e backend conversam entre si?
Eles trocam ideia usando HTTP. É tipo assim: o frontend faz um pedido, o backend responde.

O pedido (requisição) geralmente vem com:

- Método (GET pra buscar, POST pra criar, PUT pra atualizar, DELETE pra remover)
- URL 
- Headers (informações extras, tipo token de autenticação)
- Body (os dados em si, normalmente JSON)

Ai o backend responde com:

- Um código de status (200 deu bom, 404 não achou, 500 o servidor explodiu)
- Os dados que foram pedidos

## O que é uma API?
API é basicamente a ponte. É como o frontend sabe como pedir as coisas pro backend.

Da pra pensar num cardápio. A API mostra o que tem disponível, como pedir e o que vai voltar.

Hoje em dia o padrão mais usado é o REST. Nele você tem URLs que representam recursos, tipo /usuarios ou /pedidos.

## Organização do backend
Olha, se você não organizar o código, vira uma zona. 

Por isso costuma separar em camadas:

- **Controller**: recebe a requisição, faz uma validação básica, chama o service
- **Service**: aqui mora a lógica, as regras de negócio, as decisões importantes
- **Repository**: só fala com o banco de dados, não decide nada

Isso facilita a vida na hora de dar manutenção.

## Banco de dados
O backend precisa guardar informações em algum lugar. Pra isso serve o banco de dados.

Tem dois tipos principais:

- Relacional: PostgreSQL, MySQL, SQLite
- Não relacional: MongoDB

A escolha depende do que você tá fazendo.

## Segurança
Uma boa parte da segurança do sistema é responsabilidade do backend.

Algumas coisas importantes:

- **Autenticação**: saber quem é o usuário
- **Autorização**: saber o que ele pode ou não fazer
- **Validação**: nunca confiar nos dados que vêm do frontend
- **Senhas**: nunca salvar em texto puro, sempre usar hash

## Testes
Testar backend é pra evitar que o sistema quebre depois.

Os tipos mais comuns:

- Testes unitários: testam uma função ou método sozinho
- Testes de integração: testam como as partes conversam entre si
- Testes de API: testam os endpoints direto

Em Python, o pessoal costuma usar o famoso pytest.

## Como tudo funciona junto?
Quando o usuário faz alguma coisa, o caminho é mais ou menos esse:

- Frontend manda a requisição
- Backend recebe no controller
- Controller chama o service
- Service processa a lógica
- Service chama o repository
- Repository acessa o banco
- A resposta volta pelo mesmo caminho
- Frontend mostra o resultado na tela

Backend é invisível, mas sem ele nada funciona. Ele processa, guarda, protege e devolve os dados.