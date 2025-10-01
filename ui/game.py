# Responsável por exibir a interface principal do jogo Seega
import tkinter as tk
import threading
import json

class GameUI:
    def __init__(self, conexao, is_host):
        self.conexao = conexao
        self.is_host = is_host
        self.janela = tk.Tk()
        self.janela.title("Seega")
        self.janela.geometry("900x600")

        # Estado do jogo
        self.turno = tk.StringVar()
        self.fase = tk.StringVar()
        self.tabuleiro = [["" for _ in range(5)] for _ in range(5)]
        self.minhas_pecas = 0
        self.pecas_colocadas_total = 0
        self.eh_minha_vez = is_host
        self.fase_atual = "colocacao"
        self.peca_selecionada = None

        # Mensagens e interface
        self._montar_layout()
        self.turno.set("Sua vez de jogar" if is_host else "Aguardando adversário")
        self.fase.set("Fase de Colocação")

        # Inicia thread para escutar o oponente
        threading.Thread(target=self.escutar_socket, daemon=True).start()
        self.janela.mainloop()

    def _montar_layout(self):
        frame_esquerda = tk.Frame(self.janela, width=600, height=600)
        frame_esquerda.pack(side="left", fill="both", expand=True)

        tk.Label(frame_esquerda, textvariable=self.turno).pack(pady=5)
        self.btn_desistir = tk.Button(frame_esquerda, text="Desistir", command=self.desistir)
        self.btn_desistir.pack()

        self.tabuleiro_frame = tk.Frame(frame_esquerda, bg="#ddd", width=500, height=500)
        self.tabuleiro_frame.pack(pady=10)
        self._criar_tabuleiro()

        tk.Label(frame_esquerda, textvariable=self.fase).pack(pady=5)

        # Chat e logs
        frame_direita = tk.Frame(self.janela, width=300, bg="#ccc")
        frame_direita.pack(side="right", fill="both")

        frame_chat = tk.Frame(frame_direita, height=350, bg="#ddd")
        frame_chat.pack(fill="x", padx=5, pady=5)
        tk.Label(frame_chat, text="Chat").pack()
        self.chat_text = tk.Text(frame_chat, height=15, state="disabled")
        self.chat_text.pack()

        self.chat_entry = tk.Entry(frame_chat)
        self.chat_entry.pack(fill="x", pady=5)
        self.chat_entry.bind("<Return>", self.enviar_mensagem)

        frame_logs = tk.Frame(frame_direita, bg="#bbb")
        frame_logs.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Label(frame_logs, text="Logs da Partida").pack()
        self.logs_text = tk.Text(frame_logs, height=10, state="disabled")
        self.logs_text.pack(fill="both", expand=True)

    def _criar_tabuleiro(self):
        self.botoes = []
        for linha in range(5):
            linha_botoes = []
            for coluna in range(5):
                btn = tk.Button(self.tabuleiro_frame, width=4, height=2, bg="white",
                                command=lambda l=linha, c=coluna: self.clique_celula(l, c))
                btn.grid(row=linha, column=coluna, padx=1, pady=1)
                if linha == 2 and coluna == 2:
                    btn.config(state="disabled", bg="black")  # Casa central bloqueada na colocação
                linha_botoes.append(btn)
            self.botoes.append(linha_botoes)

    def clique_celula(self, linha, coluna):
        if not self.eh_minha_vez:
            self.adicionar_log("Não é sua vez!")
            return

        if self.fase_atual == "colocacao":
            if self.tabuleiro[linha][coluna] != "":
                self.adicionar_log("Posição já ocupada.")
                return
            if linha == 2 and coluna == 2:
                self.adicionar_log("A casa central está bloqueada na fase de colocação.")
                return

            self.tabuleiro[linha][coluna] = "M"
            self.botoes[linha][coluna].config(bg="blue")
            self.minhas_pecas += 1
            self.pecas_colocadas_total += 1

            # Envia jogada ao oponente
            self.conexao.sendall(json.dumps({
                "tipo": "jogada",
                "conteudo": [linha, coluna]
            }).encode())

            if self.pecas_colocadas_total >= 24:
                self.fase.set("Fase de Movimentação")
                self.fase_atual = "movimentacao"
                self.adicionar_log("Fase de movimentação iniciada.")
                self.botoes[2][2].config(state="normal", bg="white")
            else:
                self.adicionar_log(f"Peça colocada em {chr(65 + linha)}{coluna + 1}")
                self.eh_minha_vez = False
                self.turno.set("Turno do oponente")

        elif self.fase_atual == "movimentacao":
            if self.peca_selecionada is None:
                if self.tabuleiro[linha][coluna] != "M":
                    self.adicionar_log("Selecione uma das suas peças.")
                    return
                self.peca_selecionada = (linha, coluna)
                self.botoes[linha][coluna].config(relief="sunken")
                self.adicionar_log(f"Peça selecionada em {chr(65 + linha)}{coluna + 1}")
            else:
                origem = self.peca_selecionada
                destino = (linha, coluna)
                if origem == destino:
                    self.botoes[linha][coluna].config(relief="raised")
                    self.peca_selecionada = None
                    return
                if self.tabuleiro[linha][coluna] != "":
                    self.adicionar_log("Destino já ocupado.")
                    return
                if not self.eh_movimento_valido(origem, destino):
                    self.adicionar_log("Movimento inválido.")
                    return

                # Aplica o movimento
                self.botoes[origem[0]][origem[1]].config(bg="white", relief="raised")
                self.tabuleiro[origem[0]][origem[1]] = ""
                self.tabuleiro[linha][coluna] = "M"
                self.botoes[linha][coluna].config(bg="blue")
                self.peca_selecionada = None

                self.adicionar_log(f"Você moveu de {chr(65 + origem[0])}{origem[1]+1} para {chr(65 + linha)}{coluna + 1}")
                self.conexao.sendall(json.dumps({
                    "tipo": "movimento",
                    "conteudo": {
                        "origem": origem,
                        "destino": destino
                    }
                }).encode())

                # Captura após o movimento
                capturadas = self.verificar_capturas(linha, coluna, "M", "O")
                for l, c in capturadas:
                    self.tabuleiro[l][c] = ""
                    self.botoes[l][c].config(bg="white")
                    self.adicionar_log(f"Você capturou peça em {chr(65 + l)}{c+1}")
                if capturadas:
                    self.conexao.sendall(json.dumps({
                        "tipo": "captura",
                        "conteudo": capturadas
                    }).encode())

                self.verificar_vitoria()
                self.eh_minha_vez = False
                self.turno.set("Turno do oponente")

    def eh_movimento_valido(self, origem, destino):
        l1, c1 = origem
        l2, c2 = destino
        return (l1 == l2 and abs(c1 - c2) == 1) or (c1 == c2 and abs(l1 - l2) == 1)

    def escutar_socket(self):
        while True:
            try:
                dados = self.conexao.recv(1024).decode()
                if not dados:
                    break
                mensagem = json.loads(dados)

                if mensagem["tipo"] == "chat":
                    self.adicionar_chat(f"Oponente: {mensagem['conteudo']}")

                elif mensagem["tipo"] == "jogada":
                    linha, coluna = mensagem["conteudo"]
                    self.tabuleiro[linha][coluna] = "O"
                    self.botoes[linha][coluna].config(bg="red")
                    self.pecas_colocadas_total += 1

                    if self.pecas_colocadas_total >= 24:
                        self.fase.set("Fase de Movimentação")
                        self.fase_atual = "movimentacao"
                        self.adicionar_log("Fase de movimentação iniciada.")
                        self.botoes[2][2].config(state="normal", bg="white")
                    else:
                        self.adicionar_log(f"Oponente colocou peça em {chr(65 + linha)}{coluna + 1}")
                        self.eh_minha_vez = True
                        self.turno.set("Sua vez de jogar")

                elif mensagem["tipo"] == "movimento":
                    origem = tuple(mensagem["conteudo"]["origem"])
                    destino = tuple(mensagem["conteudo"]["destino"])

                    self.tabuleiro[origem[0]][origem[1]] = ""
                    self.botoes[origem[0]][origem[1]].config(bg="white", relief="raised")

                    self.tabuleiro[destino[0]][destino[1]] = "O"
                    self.botoes[destino[0]][destino[1]].config(bg="red")

                    self.adicionar_log(f"Oponente moveu de {chr(65 + origem[0])}{origem[1]+1} para {chr(65 + destino[0])}{destino[1]+1}")
                    self.eh_minha_vez = True
                    self.turno.set("Sua vez de jogar")

                elif mensagem["tipo"] == "captura":
                    for l, c in mensagem["conteudo"]:
                        self.tabuleiro[l][c] = ""
                        self.botoes[l][c].config(bg="white")
                        self.adicionar_log(f"Sua peça foi capturada em {chr(65 + l)}{c+1}")
                    self.verificar_vitoria()

                elif mensagem["tipo"] == "vitoria":
                    self.adicionar_log("Oponente venceu. Você não tem mais peças.")
                    self.janela.after(2000, self.janela.quit)

                elif mensagem["tipo"] == "desistir":
                    self.adicionar_log("Oponente desistiu. Você venceu!")
                    self.janela.quit()

            except Exception as e:
                print(f"[ERRO] na escuta: {e}")
                break

    def verificar_capturas(self, linha, coluna, minha_cor, cor_oponente):
        capturas = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dl, dc in direcoes:
            l_meio, c_meio = linha + dl, coluna + dc
            l_fim, c_fim = linha + 2*dl, coluna + 2*dc
            if 0 <= l_meio < 5 and 0 <= c_meio < 5 and 0 <= l_fim < 5 and 0 <= c_fim < 5:
                if (self.tabuleiro[l_meio][c_meio] == cor_oponente and
                    self.tabuleiro[l_fim][c_fim] == minha_cor):
                    capturas.append((l_meio, c_meio))
        return capturas

    def verificar_vitoria(self):
        pecas_oponente = sum(row.count("O") for row in self.tabuleiro)
        pecas_minhas = sum(row.count("M") for row in self.tabuleiro)
        if pecas_oponente == 0:
            self.adicionar_log("Você venceu! O oponente não tem mais peças.")
            self.conexao.sendall(json.dumps({"tipo": "vitoria"}).encode())
            self.janela.after(2000, self.janela.quit)
        elif pecas_minhas == 0:
            self.adicionar_log("Você perdeu. Suas peças foram capturadas.")
            self.janela.after(2000, self.janela.quit)

    def enviar_mensagem(self, event):
        msg = self.chat_entry.get()
        if msg:
            self.adicionar_chat(f"Você: {msg}")
            try:
                self.conexao.sendall(json.dumps({"tipo": "chat", "conteudo": msg}).encode())
            except:
                self.adicionar_log("[ERRO] ao enviar mensagem.")
            self.chat_entry.delete(0, tk.END)

    def adicionar_log(self, texto):
        self.logs_text.config(state="normal")
        self.logs_text.insert(tk.END, texto + "\n")
        self.logs_text.config(state="disabled")

    def adicionar_chat(self, texto):
        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, texto + "\n")
        self.chat_text.config(state="disabled")

    def desistir(self):
        try:
            self.conexao.sendall(json.dumps({"tipo": "desistir"}).encode())
        except:
            pass
        self.adicionar_log("Você desistiu da partida.")
        self.janela.quit()
