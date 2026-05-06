# Estudo sobre APIs

### O que são APIs?

Application Programming Interface, ou Interface de Programação de Aplicações. 

São um conjunto de regras e protocolos que permite que dois softwares "conversem" entre si, trocando dados e funcionalidades com segurança.

Atua como como uma ponte ou intermediário, permitindo que um sistema solicite informações ou serviços de outro sistema.

### Como funciona?

Analogicamente, a API seria um garçom: Ele permite que os clientes façam pedidos, leva-os até a cozinha de forma que os cozinheiros entendam e traz a resposta (o prato) de volta aos clientes. 
A cozinha seria o servidor/banco de dados que é onde ocorre o processamento dos dados solicitados no pedido.

> É uma forma de comunicação que permite trafegar informações entre diferentes sistemas.

### Representação Prática de uma Requisição (Request)

Na prática, a comunicação entre o cliente e a API ocorre através do protocolo **HTTP**. Abaixo, vemos um exemplo de como o "pedido" (Request) é feito para saber a temperatura de uma cidade e como a "resposta" (Response) retorna com os dados solicitados e um código de status (200), indicando que tudo deu certo:

```json
GET /temperatura/sao-paulo

Response: 200 { "temperatura": "26 C" }
```