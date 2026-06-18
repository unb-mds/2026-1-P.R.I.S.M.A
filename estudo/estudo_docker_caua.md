# Estudo sobre Docker

## O que é Docker?

Docker é uma tecnologia de containers. Container é tipo uma caixinha onde você coloca seu aplicativo e tudo que ele precisa pra rodar.

A ideia é simples: você empacota seu código junto com as dependências, bibliotecas, configurações. Esse pacote roda em qualquer lugar que tenha Docker instalado. Não importa se é na sua maquina, no servidor da empresa, ou na nuvem. Funciona igual.

# O que é uma Máquina Virtual?

## O problema que a maquina virtual resolve

Imagina que você tem um computador só. Um PC normal, com Windows instalado. Mas você precisa rodar um programa que só funciona no Linux. O que faz?

Opção 1: formatar o PC e instalar Linux. Mas dai perde o Windows.

Opção 2: comprar outro computador. Caro.

Opção 3: usar maquina virtual.

## O que é uma maquina virtual?

Máquina virtual é você fingir que tem um computador dentro do seu computador.

Pensa assim: seu computador de verdade (chama "maquina hospedeira") vai rodar um programa especial. Esse programa cria uma "maquina de mentira" dentro dela. Dentro dessa maquina de mentira, você instala outro sistema operacional.

Pra quem tá dentro da maquina virtual, parece que é um computador de verdade. Tem placa mãe, processador, memória, disco rígido. Mas é tudo inventado. É software imitando hardware.

## O que é hipervisor?

Hipervisor é o programa que cria e gerencia as máquinas virtuais.

Ele é o responsável por enganar o sistema operacional convidado. O sistema convidado acha que está no controle do hardware, mas na verdade o hipervisor que tá controlando tudo.

VM : Virtual Machine (maquina virtual)

Tipos de hipervisor:

**Hipervisor tipo 2**: roda como um programa normal dentro do seu sistema operacional. Exemplos: VirtualBox, VMware Workstation. Você abre o programa, clica em "criar máquina virtual", e pronto.

**Hipervisor tipo 1**: roda direto no hardware, sem sistema operacional embaixo. É mais profissional, usado em servidores. Exemplos: VMware ESXi, Microsoft Hyper-V.

Pra quem tá começando, só importa saber o VirtualBox e o VMware Workstation.

## Exemplo prático

Vamos montar uma:

1. Seu computador (Windows 11, 16 GB de RAM, 500 GB de disco)
2. Você instala o VirtualBox (hipervisor)
3. Dentro do VirtualBox, você cria uma máquina virtual. Define: 2 GB de RAM, 50 GB de disco, 2 processadores.
4. Você coloca o ISO do Ubuntu e instala Linux dentro dessa VM.
5. Pronto. Agora você tem Windows rodando seu computador, e dentro dele um Linux rodando.

As duas coisas funcionam ao mesmo tempo. Você pode alternar entre as duas janelas.

## Como a VM enxerga o hardware?

O hipervisor faz "tradução". Quando o sistema dentro da VM tenta acessar o disco, o hipervisor pega esse pedido e repassa pro disco de verdade. Só que controlando o que pode ou não pode.

O sistema convidado acha que está falando com um disco de verdade. Mas é o hipervisor no meio.

## Quanto custa em recurso?

Máquina virtual é pesada. Cada VM cria um sistema operacional completo, do zero. Isso significa:

- Cada VM precisa de RAM separada (tipo 2, 4, 8 GB por VM)
- Cada VM precisa de espaço em disco (instalar o SO + programas)
- Cada VM começa com boot do zero (leva de 30 segundos a alguns minutos)
- Cada VM tem processos próprios, serviços próprios, tudo repetido

Se você tem 16 GB de RAM e roda duas VMs com 4 GB cada, já perdeu 8 GB. Só sobrou 8 GB pra sua máquina principal.

## Pra que servem as VMs hoje?

- Testar outros sistemas operacionais sem formatar
- Criar ambientes isolados pra testar software duvidoso
- Em empresas, rodar vários servidores numa mesma máquina física
- Ter versões antigas do Windows pra testar compatibilidade

## E o Docker?

Docker é diferente. Ele não cria um sistema operacional inteiro. Ele compartilha o kernel do seu computador.

Por isso é mais leve. Não precisa de 2 GB de RAM. Não precisa de 30 segundos pra iniciar. Não precisa instalar um SO(Sistema Operacional) do zero.

Mas também não roda qualquer sistema. Se você tem Linux hospedeiro, só roda Linux nos containers. Não dá pra rodar Windows dentro de container Linux.

Máquina virtual é você criar um computador falso dentro do real. Hipervisor é o programa que faz essa mágica. VM é pesada e lenta, mas roda qualquer sistema operacional.

Docker é mais leve e rápido, mas tem algumas limitações.

Os dois têm seu uso. Pra testar outro SO, vai de VM. Pra rodar aplicação em produção, vai de Docker.

## Imagem e Container

**Imagem**: é um pacote estático. Um arquivo. Ela contém tudo que um aplicativo precisa pra rodar: código, bibliotecas, configurações, variáveis de ambiente. A imagem não roda. Ela só existe, guardada no seu disco.

**Container**: é a imagem em execução. Você pega a imagem e "roda" ela. Aí vira um container. O container tem processo rodando, consome memória, usa CPU. Ele está vivo.

Com poucos comandos você baixa uma imagem, sobe um container, e tá com um banco PostgreSQL rodando em segundos. Sem instalar nada na maquina além de Docker.

Imagens vêm de um repositório de imagens. O mais famoso é o Docker Hub.

## Docker vs Maquina Virtual

Muita gente confunde container com maquina virtual. Não é a mesma coisa.

**Maquina virtual**: você tem um hipervisor rodando por baixo. Ele cria VMs completas, cada uma com seu próprio sistema operacional. Cada VM leva uns 5, 10, 20 GB. Levam minutos pra iniciar. Consome bastante RAM e CPU.

**Docker**: você tem um único sistema operacional hospedeiro. O Docker compartilha o kernel dele com todos os containers. Cada container é só o aplicativo e suas dependências. Tem tipo 50 MB, 200 MB. Inicia em segundos. Gasta muito menos recurso.

Resumo: VM virtualiza hardware. Container virtualiza o sistema operacional.

## Vantagens dos containers

**Escalabilidade**: precisa rodar mais copias do seu app? É facil. Sobe mais containers. Dá pra ter dezenas rodando junto.

**Isolamento**: cada container é separado. Se um cair, os outros continuam. Se um tiver vazamento de memória, não afeta o vizinho.

**Facilidade de backup**: como tudo que importa tá dentro do container ou em volumes separados, fica facil de versionar, copiar, restaurar.

**Reprodutibilidade**: roda na sua maquina, roda no servidor, roda na maquina do colega. Sem o famoso "mas na minha máquina funciona".
