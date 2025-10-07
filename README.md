# 🎮 Halma Multiplayer com Sockets (Python + Tkinter)

Projeto individual da disciplina de **Programação Paralela e Distribuída (IFCE, 2025.1)** com o objetivo de implementar o jogo de tabuleiro **Halma**, utilizando **sockets TCP em Python** para comunicação em rede e **Tkinter** para a interface gráfica.

---

## 📌 Sumário

- [📷 Visão Geral](#-visão-geral)
- [🚀 Execução](#-execução)
- [🧠 Regras do Jogo Halma](#-regras-do-jogo-halma)
- [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📡 Comunicação em Rede](#-comunicação-em-rede)
- [🗂 Estrutura de Pastas](#-estrutura-de-pastas)
- [⚙️ Funcionalidades Implementadas](#️-funcionalidades-implementadas)
- [📌 Observações Técnicas](#-observações-técnicas)
- [📚 Curiosidades e Justificativas](#-curiosidades-e-justificativas)

---

## 📷 Visão Geral

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/Halma_Board.svg" width="200" align="right" />

**Halma** é um clássico jogo de tabuleiro de estratégia para dois jogadores. O objetivo é mover todas as suas peças do canto inicial para o canto oposto do tabuleiro, utilizando movimentos simples ou pulando sobre outras peças (sem capturá-las).

Este projeto implementa:

- Jogo **em tempo real**, multiplayer peer-to-peer (host + cliente)
- Interface gráfica amigável com **área de jogo**, **chat** e **logs**
- **Controle de turnos** e regras básicas do Halma
- Comunicação 100% via **sockets TCP**

---

## 🚀 Execução

### Pré-requisitos

- Python 3.10 ou superior
- Compatível com Windows, Linux ou macOS

### Rodando o jogo

```bash
# Clone ou extraia os arquivos
cd halma

# Execute o arquivo principal
python3 main.py
```

### Como jogar

1. **Jogador 1 (host)**: Inicie o servidor e informe a porta (ex: 5000).
2. **Jogador 2 (convidado)**: Conecte usando o IP do host e a mesma porta.
3. Após conexão, a interface do jogo será carregada para ambos.
4. A partida segue as regras do Halma (ver abaixo).

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

- 🐍 **Python 3.12**
- 🎨 **Tkinter** (interface gráfica nativa do Python)
- 🌐 **Socket TCP/IP** (`socket`)
- 🔄 **Threading** (`threading`) para escuta paralela
- 🧠 **JSON** para serialização de mensagens entre jogadores

---

## 📡 Comunicação em Rede

A arquitetura segue o padrão **cliente-servidor**, usando sockets TCP:

- O **host** (servidor) escuta uma porta e aguarda a conexão.
- O **convidado** (cliente) se conecta usando IP + porta.
- A comunicação é **bidirecional**:
  - Mensagens de texto (chat)
  - Comandos de jogo (movimentações)
- As mensagens são **serializadas em JSON**, garantindo portabilidade e clareza.

---

## 🗂 Estrutura de Pastas

```
halma/
├── main.py               # Ponto de entrada
├── ui/
│   ├── lobby.py          # Tela inicial (Lobby, Chat)
│   └── game.py           # Interface principal do jogo Halma
└── network/
    ├── server.py         # Inicializa o servidor TCP
    └── client.py         # Conecta a um servidor existente
```

---

## ⚙️ Funcionalidades Implementadas

✅ Hospedar ou entrar em partidas  
✅ Interface gráfica com **tabuleiro 16x16**, chat e logs  
✅ Controle de turno  
✅ Movimentação e pulos válidos das peças  
✅ Indicação de vitória  
✅ Logs da partida e mensagens em tempo real

---

## 📌 Observações Técnicas

- A interface foi feita com foco em **simplicidade e clareza**, sem uso de bibliotecas externas.
- A escuta de dados da conexão ocorre em **thread separada**, evitando travamento da interface.
- Todos os comandos de jogo (ex: movimentar) são enviados como **eventos JSON**.
- A interface é adaptável para futuras funcionalidades, como placar, cronômetro ou bot.

---

## 📚 Curiosidades e Justificativas

- O **Halma** foi escolhido por ser um jogo clássico de estratégia, permitindo testar comunicação P2P com uma mecânica envolvente.
- A interface com Tkinter é leve, nativa e funcional mesmo sem bibliotecas externas.
- A arquitetura do projeto permite futuras melhorias como:
  - Suporte a IA / bot
  - Replay de jogadas
  - Persistência de partidas com SQLite
- O projeto foi desenvolvido de forma **progressiva**, com testes manuais a cada etapa.

---

## 👤 Autor

Desenvolvido por **Lucas Barbosa de Oliveira**  
Aluno do curso de **Engenharia de Computação - IFCE**  
Disciplina: Programação Paralela e Distribuída (2025.2)  
Professor: *Cidcley T. de Souza*  
Contato: [lucasbarbosa2807@gmail.com]

---