# 🎮 Halma Multiplayer com RMI/RPC (Python + Tkinter)

Projeto individual da disciplina de **Programação Paralela e Distribuída (IFCE, 2025.1)** com o objetivo de implementar o jogo de tabuleiro **Halma**, utilizando **RMI/RPC (RPyC) em Python** para comunicação em rede e **Tkinter** para a interface gráfica.

**🔄 Migrado de Sockets TCP para RMI/RPC** - Comunicação mais robusta e transparente.

---

## 📌 Sumário

- [📷 Visão Geral](#-visão-geral)
- [🚀 Execução](#-execução)
- [🧠 Regras do Jogo Halma](#-regras-do-jogo-halma)
- [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📡 Comunicação RMI/RPC](#-comunicação-rmirpc)
- [🏗️ Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [🗂 Estrutura de Pastas](#-estrutura-de-pastas)
- [⚙️ Funcionalidades Implementadas](#️-funcionalidades-implementadas)
- [🔄 Migração de Sockets para RMI](#-migração-de-sockets-para-rmi)
- [📌 Observações Técnicas](#-observações-técnicas)
- [� Autor](#-autor)

---

## 📷 Visão Geral

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/Halma_Board.svg" width="200" align="right" />

**Halma** é um clássico jogo de tabuleiro de estratégia para dois jogadores. O objetivo é mover todas as suas peças do canto inicial para o canto oposto do tabuleiro, utilizando movimentos simples ou pulando sobre outras peças (sem capturá-las).

Este projeto implementa:

- Jogo **em tempo real**, multiplayer cliente-servidor
- Interface gráfica amigável com **área de jogo**, **chat** e **logs**
- **Controle de turnos** e regras básicas do Halma
- Comunicação 100% via **RMI/RPC usando RPyC**

---

## 🚀 Execução

### Pré-requisitos

- Python 3.9 ou superior
- Biblioteca RPyC para RMI/RPC
- Compatível com Windows, Linux ou macOS

### Instalação

```bash
# Clone ou extraia os arquivos
cd halma

# Instale as dependências
pip install rpyc

# Execute o arquivo principal
python3 main.py
```

### Como jogar

1. **Hospedar partida**:
   - Clique em "Hospedar"
   - Escolha quem começa (Servidor ou Cliente)  
   - Porta padrão: 18861
   - Aguarde outro jogador conectar

2. **Entrar em partida**:
   - Digite o IP do servidor (ex: 127.0.0.1)
   - Porta: 18861 (padrão RMI)
   - Clique em "Entrar"

3. **Durante o jogo**:
   - Interface com tabuleiro, chat e controle de turnos
   - Clique nas peças para mover
   - Use o chat para conversar com o oponente

---

## 🧠 Regras do Jogo Halma

1. **Objetivo**:
   - Mover todas as suas peças do seu campo inicial para o campo oposto do tabuleiro.

2. **Movimentação**:
   - As peças podem se mover para casas adjacentes vazias (horizontal, vertical ou diagonal).
   - É permitido pular sobre peças (próprias ou do adversário) para casas vazias, em linha reta, podendo realizar múltiplos pulos em sequência.

3. **Condições de Vitória**:
   - Vence quem posicionar todas as suas peças no campo oposto primeiro.

---

## 🔧 Tecnologias Utilizadas

- 🐍 **Python 3.9+**
- 🎨 **Tkinter** (interface gráfica nativa do Python)
- 🌐 **RPyC** (biblioteca para RMI/RPC em Python)
- 🔄 **Threading** (`threading`) para escuta paralela
- 🧠 **Objetos Python** para comunicação direta entre processos

---

## 📡 Comunicação RMI/RPC

A arquitetura utiliza **RMI/RPC (Remote Method Invocation/Remote Procedure Call)** com RPyC:

### Vantagens sobre Sockets:
- **Transparência**: Chamar métodos remotos como se fossem locais
- **Simplicidade**: Sem protocolos manuais de comunicação
- **Robustez**: RPyC gerencia serialização, timeouts e reconexões automaticamente
- **Tipo-segurança**: Métodos com assinaturas bem definidas

### Métodos RMI Expostos:
- `registrar_jogador()` - Registra jogador e define se é host
- `enviar_jogada(origem, destino)` - Envia movimento para oponente  
- `obter_jogada()` - Recebe movimento do oponente
- `enviar_mensagem_chat(msg)` - Envia mensagem no chat
- `obter_mensagem_chat()` - Recebe mensagem do chat
- `desistir_jogo()` - Notifica desistência
- `verificar_desistencia()` - Verifica se oponente desistiu

### Configurações de Rede:
- **Porta padrão**: 18861 (padrão RPyC)
- **Timeout**: 30 segundos para operações RMI
- **Polling**: Cliente verifica novos dados a cada 100ms

## 🏗️ Arquitetura do Sistema

```
┌─────────────┐    RMI/RPC    ┌─────────────┐
│   Cliente   │ ◄──────────► │   Servidor  │
│     A       │   (RPyC)     │     RMI     │
│  (Host)     │              │ (HalmaGame  │
│            │              │  Service)   │
└─────────────┘              └─────────────┘
                                    ▲
                                    │ RMI/RPC
                                    ▼
                             ┌─────────────┐
                             │   Cliente   │
                             │     B       │
                             │ (Convidado) │
                             └─────────────┘
```

### Fluxo de Comunicação:
1. **Servidor RMI** inicia e aguarda conexões
2. **Cliente A** conecta e vira "host" (peças pretas)
3. **Cliente B** conecta e vira "convidado" (peças brancas) 
4. **Coordenação**: Servidor gerencia filas de jogadas e mensagens
5. **Polling**: Clientes fazem requisições periódicas para receber dados

---

## 🗂 Estrutura de Pastas

```
halma/
├── main.py               # Ponto de entrada
├── ui/
│   ├── lobby.py          # Tela inicial (Lobby, Chat)
│   └── game.py           # Interface principal do jogo Halma
└── network/
    ├── config.py         # Configurações de rede (porta, timeout)
    ├── rmi_service.py    # Serviço RMI que coordena o jogo
    ├── server.py         # Inicializa o servidor RMI
    └── client.py         # Cliente RMI para conectar ao servidor
```

---

## ⚙️ Funcionalidades Implementadas

✅ **Comunicação RMI/RPC** completa com RPyC  
✅ **Servidor RMI** multi-threaded coordenando jogadas  
✅ **Interface gráfica** com tabuleiro 16x16, chat e logs  
✅ **Controle de turnos** sincronizado entre jogadores  
✅ **Movimentação e pulos** válidos das peças Halma  
✅ **Chat em tempo real** entre jogadores  
✅ **Detecção de vitória/derrota** automática  
✅ **Sistema de desistência** com notificação  
✅ **Hospedagem e entrada** em partidas simplificada  

## � Migração de Sockets para RMI

### Antes (Sockets TCP):
```python
# Envio complexo com serialização manual
dados = pickle.dumps((origem, destino))
tamanho = len(dados).to_bytes(4, "big")
conexao.sendall(tamanho + dados)

# Recebimento com controle de protocolo
cabecalho = conexao.recv(4)
tamanho = int.from_bytes(cabecalho, "big")
dados = conexao.recv(tamanho)
recebido = pickle.loads(dados)
```

### Depois (RMI/RPC):
```python
# Chamada simples de método remoto
cliente_rmi.enviar_jogada(origem, destino)

# Recebimento transparente
jogada = cliente_rmi.obter_jogada()
```

### Benefícios da Migração:
- **90% menos código** de comunicação
- **Eliminação de bugs** de protocolo de rede
- **Maior robustez** com reconexão automática
- **Desenvolvimento mais rápido** e manutenível
- **Debugging facilitado** com logs automáticos

## 📌 Observações Técnicas

### Arquitetura RMI:
- **HalmaGameService**: Coordena todas as operações do jogo
- **ClienteRMI**: Encapsula chamadas remotas do cliente
- **ThreadedServer**: Suporte a múltiplos clientes simultâneos
- **Sincronização**: Locks para operações thread-safe

### Características Técnicas:
- **Porta padrão**: 18861 (substituiu 12345 dos sockets)
- **Timeout**: 30 segundos para operações RMI
- **Polling**: 100ms para atualizações em tempo real
- **Threading**: Escuta de rede em thread separada
- **Estado compartilhado**: Variáveis de classe para coordenação

### Melhorias Futuras Possíveis:
- Suporte a mais de 2 jogadores
- Persistência de partidas
- Sistema de ranking
- Replay de jogadas
- Bot com IA

---

## 👤 Autor

**Lucas Barbosa de Oliveira**  
📚 Engenharia de Computação - IFCE  
📖 Disciplina: Programação Paralela e Distribuída (2025.1)  
👨‍🏫 Professor: Cidcley T. de Souza  

---

**🎯 Projeto: Implementação completa do jogo Halma com comunicação RMI/RPC**  
**📅 Data: Outubro/2025**  
**🔧 Tecnologia: Python + RPyC + Tkinter**
Contato: [lucasbarbosa2807@gmail.com]

---