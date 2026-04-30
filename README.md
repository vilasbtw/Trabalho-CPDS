# Trabalho-CPDS

## Integrantes
- Kaique Vilas Boa
- Evelyn Theodoro
- Kauany das Gracas


## Distributed Message Bus com Relógio de Lamport
Este projeto consiste em um sistema de troca de mensagens via linha de comando (CMD) que aplica conceitos fundamentais de Sistemas Distribuídos. O sistema utiliza um barramento centralizado (Message Bus) para gerenciar a comunicação entre múltiplos clientes, garantindo a ordenação causal de eventos através de relógios lógicos e mantendo logs de auditoria.

## Funcionalidades
Comunicação Unicast: Envio de mensagens diretas e privadas entre usuários registrados.

Relógio Lógico de Lamport: Implementação de sincronização de tempo para garantir a ordem correta das mensagens em um ambiente distribuído.

Criptografia Base64: Camada de codificação (simulando cifragem) para garantir que o texto original não trafegue de forma legível na rede.

Auditoria de Logs: Registro automático no servidor de todas as transações, incluindo o carimbo de tempo (timestamp) de envio e recebimento (ACK).

Multithreading: Suporte para múltiplos clientes conectados simultaneamente ao servidor.

## Estrutura do Projeto
message_buffer.py: O servidor central que coordena o tráfego de mensagens, gerencia os usuários conectados e gera os logs de auditoria.

comunicador.py: Interface do usuário (Cliente) para registro, envio e recebimento de mensagens.

utils/relogio_logico.py: Componente responsável pela lógica de incremento e sincronização do tempo lógico.

crypto/criptografia.py: Módulo que realiza a codificação e decodificação das mensagens em Base64.

## Como Executar
Como você já clonou o projeto, siga estes passos nos terminais do seu computador:

1. Iniciar o Servidor (Barramento)
O servidor deve ser o primeiro a ser iniciado. Ele ficará aguardando conexões na porta 5000.

Bash
python message_buffer.py

2. Iniciar os Clientes
Abra novos terminais para cada usuário que deseja criar (ex: um para "Alice" e outro para "Bob") e execute:

Bash
python comunicador.py

3. Utilização no Terminal
Digite seu Nome quando solicitado (use apenas letras e números).

Escolha a opção 1 para "Enviar Mensagem".

Informe o nome do Destinatário (ex: Bob).

Digite sua mensagem (limite de 100 caracteres) e pressione Enter.

O sistema exibirá a confirmação e o destinatário verá a mensagem com o tempo lógico sincronizado.

## Conceitos Aplicados
Relógio Lógico (Sincronização)
Para resolver o problema da falta de um relógio global em sistemas distribuídos, implementamos o Relógio de Lamport. Sempre que uma mensagem é recebida, o cliente executa:

Tempo_Local = max(Tempo_Local, Tempo_Recebido) + 1

Auditoria e Transparência
O servidor mantém um ficheiro em server/auditoria_log.txt que regista:

O carimbo de tempo do envio.

Identificação do remetente e destinatário.

O carimbo de tempo da receção (ACK).

O conteúdo cifrado da mensagem.
