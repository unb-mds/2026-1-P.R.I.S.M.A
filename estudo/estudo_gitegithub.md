# Estudo sobre Git

Git é um software de controle de versão. GitHub é um serviço onde você hospeda repositórios Git na nuvem. 

## Repositório

Repositório é a pasta onde seu projeto mora. Mas não é uma pasta qualquer. O Git fica de olho em tudo que acontece dentro dela.

Repositório pode ser local (no seu computador) ou remoto.

## Branch

Branch é uma ramificação. Pensa numa árvore. O tronco principal é a main (ou master). As branches são galhos que saem dele.

Você cria uma branch quando quer testar alguma coisa sem estragar o que já tá funcionando. Depois que testou e viu que deu certo, você junta de volta no tronco.

Cada branch tem sua própria história de commits. Uma não bagunça a outra.

## Commit

Commit é uma versão do seu código naquele momento. O Git guarda. Se mais tarde você fizer besteira, volta pra foto anterior.

Um commit tem três coisas: um código identificador (hash), uma mensagem (que você escreve), e as mudanças que foram feitas.

## Clone

Clone é fazer uma cópia de um repositório que tá no GitHub (ou outro lugar) pro seu computador. Você baixa tudo: código, histórico de commits, branches, tudo.

Se o repositório for público, qualquer um pode clonar. Se for privado, só quem tem acesso.

## Fork

Fork é tipo um clone, mas no GitHub. Você aperta um botão e o GitHub cria uma cópia do repositório na sua conta.

A diferença: clone é na sua máquina, fork é no servidor. Fork serve muito pra contribuir com projeto dos outros. Você faz o fork, mexe no seu, e depois pede pro dono original puxar suas alterações.

## Pull request (ou merge request)

Pull request é um pedido. Você fez alterações numa branch, mandou pro repositório remoto, e agora quer que alguém aprove e junte com a branch principal.

É muito comum em trabalho em equipe e em projetos open source. Alguém olha seu código, comenta se precisa mudar alguma coisa, e depois aprova.

No GitLab chamam de merge request. No GitHub chamam de pull request. É a mesma coisa.

## Tag

Tag é uma etiqueta. Você marca um commit específico com um nome. Geralmente usam tags pra marcar versões: `v1.0`, `v2.0.1`, etc.

Diferente da branch, a tag não muda. Ela aponta pra um commit e fica lá pra sempre.

## Comandos básicos

`git init`  
Começa um projeto novo com Git. Você roda dentro da pasta do projeto e pronto, agora o Git tá olhando tudo ali.

`git add <arquivo>` ou `git add .`  
Adiciona os arquivos que você quer preparar pro commit. O ponto adiciona tudo que foi alterado.

`git commit -m "mensagem aqui"`  
Guarda os arquivos que você adicionou no histórico. A mensagem tem que fazer sentido, senão ninguém entende nada depois.

`git log`  
Mostra o histórico de commits. Quem fez, quando fez, a mensagem, o código do commit.

`git status`  
Mostra o estado atual. O que foi modificado, o que tá pronto pra commit, o que ainda não foi adicionado.

`git diff`  
Mostra linha por linha o que mudou nos arquivos. Útil pra lembrar o que você fez antes de dar commit.

## Trabalhando com branches

`git branch`  
Mostra em qual branch você está. Também lista todas as branches do projeto.

`git checkout <nome-da-branch>`  
Troca de branch. Você sai de uma e vai pra outra.

`git checkout -b <nome-da-nova-branch>`  
Cria uma nova branch a partir da branch atual e já troca pra ela. É o atalho mais usado.

`git merge <branch>`  
Pega o que tem na branch que você passou e junta com a branch atual. É assim que você traz o trabalho dos outros pro seu lado.

## Repositórios remotos

`git remote add <nome> <url>`  
Conecta seu repositório local com um repositório remoto. O nome mais comum é `origin`. Exemplo:  
`git remote add origin https://github.com/usuario/repo.git`

`git push <nome> <branch>`  
Manda seus commits locais pro repositório remoto. Exemplo: `git push origin main`

`git pull <nome> <branch>`  
Pega as alterações do repositório remoto e já junta com seu código local.

`git fetch`  
Sincroniza seu histórico local com o que tem no remoto. Ele baixa as novidades mas não junta com seu código. Você pode olhar antes de resolver o que fazer.

## Sobre `origin`

`origin` é só um nome padrão. Você poderia chamar de `meu-servidor` ou `remoto`, mas todo mundo usa `origin` por convenção. Quando você clona um repositório, o Git já configura o `origin` automaticamente.

## main vs master

Antigamente a branch padrão se chamava `master`. Por questões de inclusão, o GitHub e outras plataformas mudaram o padrão pra `main`.

Mas tem empresa que ainda usa `master` porque o projeto é antigo ou porque ninguém quis mudar. Na prática, é a mesma coisa. Você tem que olhar qual é o nome usado no repositório que você tá mexendo.

## .gitignore

`.gitignore` é um arquivo especial. Nele você lista pastas e arquivos que o Git deve ignorar completamente. Coisas como:

- pastas `node_modules`
- logs
- arquivos temporários do sistema

Você cria o arquivo `.gitignore` na raiz do projeto, coloca o que não quer versionar, e o Git finge que essas coisas não existem.

## Merge

Merge é o ato de juntar duas branches. Pode acontecer de duas pessoas alterarem a mesma linha do mesmo arquivo. Aí dá conflito. Você precisa resolver manualmente, escolhendo qual versão fica ou fazendo um meio termo.

Depois de resolver, você dá commit do merge. 

## Fork

Fork é uma cópia de um repositório que vai pra sua conta do GitHub. Você faz fork quando quer mexer num projeto que não é seu sem pedir permissão antes.

Depois de mexer no fork, você pode mandar um **pull request** pedindo pro dono original puxar suas alterações.

É muito comum em projetos open source. Você não tem permissão pra mexer direto, então faz um fork, altera, e pede pra entrar.

## Fluxo comum no dia a dia

1. `git pull origin main` (ou master) pra pegar o que tem de novo
2. `git checkout -b minha-feature` cria branch nova
3. Trabalha, faz commits
4. `git push origin minha-feature` manda pro repositório remoto
5. Abre um pull request no GitHub
6. Depois que aprovam, faz merge
7. Volta pra main, dá pull de novo, e continua

Git não é difícil, mas tem uns conceitos que confundem no começo. Branch, merge, remote, origin... Depois que você entende o fluxo, faz sentido. A dica é: usa `git status` toda hora. Ele te mostra onde você está.

## Referencias

Curso de Git e Github [Completo] Victor Lima - via Youtube
Aprenda Git e Github do Zero - guia completo Fernanda Kipper - via Youtube
https://learn.microsoft.com/pt-br/training/github/ Microsoft LEARN PARA GITHUB


