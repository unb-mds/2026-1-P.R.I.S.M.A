# Estudo sobre Postman

## O que é Postman?

Postman é uma ferramenta pra testar APIs. Pensa num carteiro: você manda a requisição, ele entrega no servidor, e traz a resposta de volta. Por isso chama de carteiro.

Com ele você consegue mandar requisições HTTP sem precisar escrever código nenhum. É uma interface gráfica onde você monta a requisição, aperta um botão, e vê o que o servidor responde.

Antes do Postman, o pessoal usava o terminal com curl, ou escrevia script de teste. Era chato. O Postman deixou mais fácil.

## Por que usar Postman?

Primeiro a interface é intuitiva. Você não precisa decorar comando. Tudo é botão, campo, menu. Qualquer programador consegue usar.

Segundo porque tem uma comunidade enorme. Se você tiver dúvida, alguém já respondeu no Google.

Terceiro porque ajuda na documentação. O Postman tem um recurso de documentação integrado que gera uma página bonitinha automática a partir dos seus testes.

Documentação boa aumenta ajuda a entender o código e melhora a estabilidade das aplicações porque você testa antes de integrar.

## Configuração inicial

Primeiro você precisa criar uma conta. Dá pra usar com login do Google ou email normal.

Depois você baixa a versão desktop (mais comum) ou usa direto no navegador pela versão cloud.

O Postman organiza tudo em workspaces. Workspace é tipo uma pasta separada. Você pode ter um workspace pra projeto pessoal, outro pro trabalho, outro pra testes. Cada workspace tem suas próprias coleções, variáveis e históricos.

Se você trabalha em equipe, dá pra compartilhar workspace com os outros. Todo mundo vê as mesmas requisições e documentação.

## Criando coleções e requisições

Coleção é um grupo de requisições. Você agrupa tudo que é relacionado. Por exemplo, uma coleção "API de Usuários" pode ter requisição de criar usuário, buscar usuário, atualizar, deletar.

Dentro da coleção você pode criar pastas pra organizar melhor. Por exemplo, dentro da coleção de usuários você cria uma pasta "autenticação" e outra "perfil".

Pra criar uma requisição, você precisa de algumas coisas:

**Método HTTP**: é o verbo. GET (buscar), POST (criar), PUT (atualizar tudo), PATCH (atualizar só uma parte), DELETE (remover).

**Endpoint**: é a URL. `https://api.exemplo.com/usuarios/1` por exemplo.

**Headers**: cabeçalhos. Coisa tipo autenticação, formato do conteúdo, etc.

**Body**: o corpo da requisição. Onde você coloca os dados que vai enviar. O formato mais comum hoje é JSON.

Exemplo de body em JSON:

```json
{
  "nome": "João",
  "email": "joao@email.com"
}

## Na prática

Você pega uma API real. Pode ser uma API pública de teste.

Manda a requisição, aperta Send, e o Postman mostra a resposta.

A resposta vem com:

Status code: código HTTP. 200 sucesso, 201 criado, 400 erro na requisição, 401 não autorizado, 403 sem permissão, 404 não encontrado, 500 erro no servidor.

Body: os dados que o servidor devolveu.

Time: quanto tempo demorou.

Se a API precisa de autenticação, você configura um header chamado Authorization com o token. Por exemplo: Bearer token123456.

O Postman guarda histórico de todas as requisições que você mandou. Dá pra repetir, editar, salvar como exemplo.
```
