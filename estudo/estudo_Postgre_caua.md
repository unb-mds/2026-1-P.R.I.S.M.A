# Estudo sobre PostgreSQL

## O que é PostgreSQL?

PostgreSQL é um banco de dados objeto-relacional. Isso significa que ele é relacional (tabelas, linhas, colunas, chaves) mas também tem alguns conceitos de orientação a objetos, tipo herança.

Ele segue o modelo cliente-servidor. Tem um servidor do banco rodando em alguma máquina, e vários clientes (sua aplicação, o terminal, uma ferramenta gráfica) se conectam a ele. O servidor recebe as consultas, processa, e devolve os resultados.

O PostgreSQL é famoso por ser confiável, ter boa performance e seguir os padrões SQL direitinho. Muita empresa usa em produção, desde projeto pequeno até sistema gigante.

## Como o PostgreSQL armazena os dados

O PostgreSQL guarda os dados usando um sistema chamado "heap". Os registros vão sendo colocados onde tem espaço, sem ordem específica.

Ele divide tudo em paginas fixas de 8 KB. Cada pagina é um bloco de dados. Quando você insere uma linha, ela vai pra alguma pagina disponível. Se não couber numa pagina, entra outra estrategia.

Páginas de 8 KB é o padrão. Dá pra mudar na hora de compilar, mas ninguém mexe nisso.

## TOAST (armazenamento de dados grandes)

TOAST significa The Oversized-Attribute Storage Technique. É a técnica que o PostgreSQL usa pra lidar com dados muito grandes, tipo um texto gigante, um arquivo, ou um JSON enorme.

Quando um campo passa do tamanho de uma página (8 KB), ele não cabe. O TOAST entra em ação automaticamente. Nem precisa configurar nada.

O que acontece: o PostgreSQL tenta comprimir o dado. Ele usa algoritmos como PGLZ (padrão antigo) ou LZ4 (mais rápido). Se mesmo comprimido ainda tá grande, ele joga esse dado pra fora da linha principal, guarda numa tabela separada, e deixa na tabela original só um ponteiro.

Isso mantém as paginas principais com tamanho variavel. Você não percebe. O TOAST é transparente.

## MVCC (controle de concorrencia) IMPORTANTISSIMO

MVCC significa Multi-Version Concurrency Control. É um dos conceitos mais importantes do PostgreSQL.

O problema que ele resolve: várias pessoas usando o banco ao mesmo tempo. Um usuário está atualizando um registro enquanto outro está lendo. Como fazer sem travar o sistema?

A solução do MVCC é manter várias versões da mesma linha.

Exemplo: você tem uma linha com o valor "João". Alguém atualiza pra "José". O PostgreSQL não apaga o "João". Ele marca ele como obsoleto e cria uma nova versão com "José". Quem está lendo enquanto a atualização acontece ainda vê a versão antiga. Quem começa a ler depois vê a nova.

Isso permite que todo mundo leia sem esperar e escreva sem travar o banco inteiro. Mas gera um problema: dados obsoletos acumulam.

É aí que entra o autovacuum. O autovacuum é um processo automático que roda de tempos em tempos, procurando essas versões antigas que ninguém mais usa, e limpa. Se o autovacuum não rodar, o banco cresce sem parar e a performance é destruida.

## WAL (Write-Ahead Logging)

WAL significa Write-Ahead Logging. É um mecanismo que garante durabilidade e integridade dos dados.

A ideia é simples: antes de qualquer alteração ser escrita nos arquivos principais do banco, ela é anotada primeiro num log separado chamado WAL. Esse log fica no disco.

Pensa assim: você vai atualizar um registro. O PostgreSQL primeiro escreve no WAL: "vou mudar a linha X de valor A pra valor B". Depois de escrever no WAL, aí sim ele faz a alteração na página de dados.

Por que isso é bom? Porque se o sistema cair no meio da operação, quando ele voltar, o banco olha o WAL. Ele vê o que estava sendo feito, e consegue recuperar ou desfazer a operação incompleta. Não perde dado.

O WAL também ajuda na replicação. Quando você tem um banco principal e uma cópia, a cópia pode ficar lendo o WAL e aplicando as mesmas alterações. É assim que replicas funcionam.

## Checkpoints

Checkpoint é o processo que sincroniza o que está na memoria (os buffers sujos) com o disco.

Explicação: o PostgreSQL mantém uma area em memoria chamada shared buffers. As páginas de dados ficam ali pra acesso rápido. Quando você altera uma pagina, ela vira "dirty buffer" (buffer sujo). A alteração está na memória, mas ainda não foi escrita no disco.

De tempos em tempos, o PostgreSQL faz um checkpoint. Ele pega todos os dirty buffers e força a escrita no disco. Isso mantém a consistência.

Checkpoint também limita o trabalho de recuperação. Se o banco cair, a recuperação precisa ler o WAL a partir do último checkpoint. Quanto mais frequente o checkpoint, mais rápido a recuperação.

## Como tudo se junta

Quando você faz uma alteração no PostgreSQL:

1. O MVCC cria uma nova versão da linha, sem apagar a antiga
2. A alteração é anotada no WAL
3. A página na memória (shared buffer) é atualizada e marcada como suja
4. O WAL é garantido no disco (se tiver commit, já tá seguro)
5. A página suja vai ficar na memória até o próximo checkpoint
6. O checkpoint escreve no disco
7. O autovacuum depois vai limpar as versões antigas

PostgreSQL é um banco robusto. E tem mecanismos sofisticados que funcionam sozinhos na maior parte do tempo.

O MVCC permite concorrencia sem dor de cabeça. O WAL garante que seu dado não some. O TOAST guarda coisas grandes sem você se preocupar. O autovacuum limpa a bagunça que o MVCC deixa pra trás.

Você não precisa entender tudo isso pra usar PostgreSQL no dia a dia. Mas quando alguma coisa der errado (performance caindo, ele crescendo demais, recuperação lenta), saber como funciona ajuda muito.

Referencias de estudo:
https://youtu.be/KKxwFVk8bsg?si=HIYpKjainJFiXotY (IlustraDev)
https://youtu.be/P8rrhZTPEAQ?si=OpyL5Py7U5bTC853 (The Coding Gopher)
https://www.driven.com.br/blog/postgre-sql/
