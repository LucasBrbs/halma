# 🎮 Seega Multiplayer com Sockets (Python + Tkinter)

Projeto individual da disciplina de **Programação Paralela e Distribuída (IFCE, 2025.1)** com o objetivo de implementar o jogo de tabuleiro **Seega**, utilizando **sockets TCP em Python** para comunicação em rede e **Tkinter** para a interface gráfica.

---

## 📌 Sumário

- [📷 Visão Geral](#-visão-geral)
- [🚀 Execução](#-execução)
- [🧠 Regras do Jogo Seega](#-regras-do-jogo-seega)
- [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📡 Comunicação em Rede](#-comunicação-em-rede)
- [🗂 Estrutura de Pastas](#-estrutura-de-pastas)
- [⚙️ Funcionalidades Implementadas](#️-funcionalidades-implementadas)
- [📌 Observações Técnicas](#-observações-técnicas)
- [📚 Curiosidades e Justificativas](#-curiosidades-e-justificativas)

---

## 📷 Visão Geral

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Seega_board.svg" width="200" align="right" />

**Seega** é um antigo jogo de origem africana baseado em estratégia, bloqueio e captura. Dois jogadores disputam em um tabuleiro 5x5 tentando eliminar ou imobilizar as peças adversárias.

Este projeto implementa:

- Jogo **em tempo real**, multiplayer peer-to-peer (host + cliente)
- Interface gráfica amigável com **área de jogo**, **chat** e **logs**
- **Controle de turnos**, fases e regras completas
- Comunicação 100% via **sockets TCP**

---

## 🚀 Execução

### Pré-requisitos

- Python 3.10 ou superior
- Compatível com Windows, Linux ou macOS

### Rodando o jogo

```bash
# Clone ou extraia os arquivos
cd seega

# Execute o arquivo principal
python main.py
```

### Como jogar

1. **Jogador 1 (host)**: Clique em **Hospedar** e informe a porta (ex: 5000).
2. **Jogador 2 (convidado)**: Clique em **Entrar**, insira o IP do host e a mesma porta.
3. Após conexão, a interface do jogo será carregada para ambos.
4. A partida segue as regras do Seega (ver abaixo).

---

## 🧠 Regras do Jogo Seega

1. **Fase de Colocação**:
   - Cada jogador coloca 12 peças alternadamente.
   - A **casa central (2,2)** é bloqueada durante esta fase.

2. **Fase de Movimentação**:
   - Os jogadores movem uma peça por vez para uma casa **vazia e adjacente (ortogonal)**.
   - Se uma peça inimiga ficar **entre duas suas**, ela é **capturada**.

3. **Condições de Vitória**:
   - Um jogador **vence** quando o oponente:
     - Não tem mais peças, ou
     - Desiste.

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
  - Comandos de jogo (movimentações, capturas, desistência)
- As mensagens são **serializadas em JSON**, garantindo portabilidade e clareza.

---

## 🗂 Estrutura de Pastas

```
seega/
├── main.py               # Ponto de entrada
├── ui/
│   ├── lobby.py          # Tela inicial (Hospedar/Entrar)
│   └── game_ui.py        # Interface principal do jogo
└── network/
    ├── server.py         # Inicializa o servidor TCP
    └── client.py         # Conecta a um servidor existente
```

---

## ⚙️ Funcionalidades Implementadas

✅ Hospedar ou entrar em partidas  
✅ Interface gráfica com **tabuleiro 5x5**, chat e logs  
✅ Controle de turno e **troca automática**  
✅ Fase de colocação com **bloqueio da casa central**  
✅ Fase de movimentação com **validação ortogonal**  
✅ Regras de **captura ortogonal**  
✅ Indicação de **vitória ou derrota**  
✅ Botão de **desistência**  
✅ Logs da partida e mensagens em tempo real

---

## 📌 Observações Técnicas

- A interface foi feita com foco em **simplicidade e clareza**, sem uso de bibliotecas externas.
- A escuta de dados da conexão ocorre em **thread separada**, evitando travamento da interface.
- Todos os comandos de jogo (ex: movimentar, capturar) são enviados como **eventos JSON**.
- A interface é adaptável para futuras funcionalidades, como placar, cronômetro ou bot.

---

## 📚 Curiosidades e Justificativas

- O **Seega** foi escolhido por sua simplicidade e **potencial estratégico**, o que permite testar comunicação P2P com uma mecânica envolvente.
- A interface com Tkinter é leve, nativa e funcional mesmo sem bibliotecas externas.
- A arquitetura do projeto permite futuras melhorias como:
  - Suporte a IA / bot
  - Replay de jogadas
  - Persistência de partidas com SQLite
- O projeto foi desenvolvido de forma **progressiva**, com testes manuais a cada etapa.

---

## 👤 Autor

Desenvolvido por **Anthony Davi**  
Aluno do curso de **Engenharia de Computação - IFCE**  
Disciplina: Programação Paralela e Distribuída (2025.1)  
Professor: *Cidcley T. de Souza*  
Contato: [anthony.davi.sousa08@aluno.ifce.edu.br]

---

