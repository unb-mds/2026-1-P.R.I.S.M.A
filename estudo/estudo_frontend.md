# Estudo sobre Frontend

## O que é frontend?

Frontend é a parte que o usuário vê e interage. Tudo aquilo que aparece na tela: botão, formulário, menu, animação, cores, texto. Se o usuário consegue clicar, ler ou digitar, é frontend.

O frontend é a cara do sistema. É ele que mostra os dados que vieram do backend e manda de volta o que o usuário fez.

## O que o frontend faz?

As funções do frontend são:

- Mostrar informações na tela
- Receber o que o usuário digita ou clica
- Enviar requisições pro backend
- Atualizar a interface
- Dar feedback visual pro usuário

Um exemplo: quando você abre um e-mail, o frontend pede pro backend a lista de mensagens, recebe os dados e monta aquela lista bonitinha na tela. Se você clica em responder, é o frontend que abre o campo de texto e depois envia sua resposta de volta.

## Linguagens que o frontend usa

No frontend web, as linguagens são essas três:

- HTML é a estrutura. Define o que é um botão, um título, um parágrafo.
- CSS é o estilo. Cor, tamanho, posição, sombra, animação.
- JavaScript é o comportamento. Faz as coisas acontecerem quando o usuário interage.

Se o projeto for rodar num navegador, é HTML, CSS e JavaScript

## Como o frontend conversa com o backend?

Por exemplo, quando a página carrega, o frontend pode fazer uma requisição GET pra buscar a lista de usuários. Quando o usuário clica em "salvar", o frontend manda um POST com os dados do formulário.

Depois que o backend responde, o frontend decide o que fazer com a resposta. Se deu certo, mostra uma mensagem de sucesso. Se deu erro, mostra um alerta.

## Frameworks e bibliotecas

JavaScript puro funciona, mas pra projetos maiores a galera costuma usar frameworks ou bibliotecas. Elas ajudam a organizar o código .

## CSS também tem frameworks

Escrever CSS do zero pode dar trabalho. Por isso existem bibliotecas que já entregam componentes prontos e estilos pré-definidos.

Opções bem conhecidas:

- Tailwind (você usa classes direto no HTML)
- Bootstrap (um dos mais antigos, bem completo)

## Responsividade

Hoje em dia ninguém acessa site só pelo computador. Tem celular, tablet, monitor gigante. O frontend precisa se adaptar a todos esses tamanhos de tela.

Responsividade é isso: o layout se reorganiza conforme o espaço disponível.

## Estado da aplicação

Uma coisa importante no frontend é gerenciar o estado. Estado é basicamente a informação que o frontend guarda enquanto o usuário usa o sistema.

Por exemplo: saber se o usuário está logado ou não, o que ele digitou num formulário, se uma lista já foi carregada.

Em projetos pequenos, você guarda isso em variáveis JavaScript.

## O que é SPA?

SPA significa Single Page Application. Um tipo de frontend que carrega uma única página HTML e vai trocando o conteúdo conforme o usuário navega, sem recarregar a pagina inteira.

A sensação é de que o site é mais rápido, porque só atualiza o que precisa. Exemplos: Gmail, Google Drive, Spotify.

## Performance no frontend

O frontend precisa ser rápido, principalmente em celular ou internet ruim.

Aqui algumas práticas comuns:

- Otimizar imagens (não mandar uma foto com 10MB)
- Minificar (remoção de dados redundantes) codigo.
- Evitar renderizações desnecessárias

## Testes no frontend

Testar frontend é diferente de testar backend. Não testa só lógica, se testa também se o botão aparece, se o clique funciona, se a tela se comporta direito.

## Como tudo funciona junto?

Quando o usuário entra no sistema:

- O frontend carrega o HTML, CSS e JavaScript
- O JavaScript manda uma requisição pro backend
- O backend responde com dados
- O frontend monta a tela com esses dados
- O usuario clica em algo
- O frontend manda outra requisição
- O ciclo se repete
