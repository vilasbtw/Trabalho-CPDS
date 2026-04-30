# Trabalho-CPDS - Sistema de Mensageria Distribuído

**Disciplina:** Computação Paralela e Sistemas Distribuídos  
**Integrantes:** Kaique Vilas Boa · Evelyn Theodoro · Kauany das Graças

---

## Sobre o projeto

Este projeto implementa um Message Bus distribuído via linha de comando. A arquitetura é cliente-servidor sobre TCP/IP: um servidor central roteia mensagens entre múltiplos clientes conectados simultaneamente, garantindo a ordenação dos eventos por meio do Relógio Lógico e mantendo uma trilha de auditoria em arquivo físico.

---

## Funcionalidades

| Recurso | Descrição |
|---|---|
| **Unicast** | Envio de mensagem direta e privada para um usuário específico |
| **Broadcast** | Envio de mensagem global para todos os clientes conectados |
| **Multicast** | Envio de mensagem para todos os membros de um canal nomeado |
| **Canais** | Criação, entrada e saída de canais nomeados pelo cliente |
| **Relógio Lógico** | Cada mensagem carrega um carimbo lógico de tempo (`tp`); ao receber, o cliente executa `max(local, recebido) + 1` |
| **ACK com timestamp** | O consumidor confirma o recebimento com seu próprio carimbo lógico (`tc`) |
| **Auditoria em log** | O servidor grava produtor, consumidor, `tp`, `tc` e conteúdo cifrado em `server/auditoria_log.txt` |
| **Criptografia Base64** | O conteúdo das mensagens é codificado antes de trafegar na rede |
| **Exclusão mútua** | `threading.Lock` protege todas as estruturas compartilhadas do servidor |
| **Nomeação de clientes** | Cada cliente se registra com um nome único (letras e números) |

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/vilasbtw/Trabalho-CPDS.git
cd Trabalho-CPDS
```

### 2. Iniciar o servidor

O servidor deve ser iniciado primeiro. Ele ficará escutando conexões na porta `5000`.

```bash
python server/message_buffer.py
```

### 3. Iniciar os clientes

Abra um terminal separado para cada usuário que deseja simular e execute:

```bash
python -m client.comunicador
```

---

## Como usar

Após iniciar o cliente, informe um nome de usuário único. O menu principal será exibido:

```
=== SISTEMA DE MENSAGENS ===
1. Enviar Mensagem (Unicast)
2. Enviar para Todos (Broadcast)
3. Gerenciar Canais
4. Enviar para Canal (Multicast)
0. Sair
```

### Unicast
Escolha `1`, informe o nome do destinatário e a mensagem (limite de 100 caracteres).

### Broadcast
Escolha `2` e informe a mensagem. Todos os clientes conectados receberão.

### Gerenciar canais
Escolha `3` para acessar o submenu de canais:
- **Criar canal** - cria um novo canal e já adiciona você como membro
- **Entrar em canal** - inscreve você em um canal existente
- **Sair de canal** - remove você de um canal
- **Listar canais** - exibe todos os canais e seus membros

### Multicast
Escolha `4`, informe o nome do canal e a mensagem. Todos os membros do canal receberão.

---

## Auditoria

Após a troca de mensagens, verifique o arquivo gerado em `server/auditoria_log.txt`. Cada linha registra uma entrega confirmada no formato:

```
[T:<tp>] <produtor> -> <consumidor> [T:<tc>] | Conteúdo: <mensagem_cifrada>
```

- `tp` — carimbo lógico de **envio** (produtor)
- `tc` — carimbo lógico de **recebimento** (consumidor, via ACK)