import tkinter as tk
from tkinter import messagebox
import threading
import pickle

TAMANHO_TABULEIRO = 16
TAMANHO_CASA = 30
CORES_JOGADORES = {'A': 'black', 'B': 'white'}

def criar_tabuleiro():
    tabuleiro = [[None for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
    # Jogador A (canto superior esquerdo)
    for i in range(4):
        for j in range(4 - i):
            tabuleiro[i][j] = 'A'
    # Jogador B (canto inferior direito)
    for i in range(4):
        for j in range(4 - i):
            tabuleiro[TAMANHO_TABULEIRO-1-i][TAMANHO_TABULEIRO-1-j] = 'B'
    return tabuleiro

class HalmaGame(tk.Frame):
    def __init__(self, master, enviar_jogada_callback):
        super().__init__(master)
        self.tabuleiro = criar_tabuleiro()
        self.enviar_jogada_callback = enviar_jogada_callback
        self.canvas = tk.Canvas(self, width=TAMANHO_TABULEIRO*TAMANHO_CASA, height=TAMANHO_TABULEIRO*TAMANHO_CASA)
        self.canvas.pack()
        self.selecionado = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.desenhar_tabuleiro()

    def desenhar_tabuleiro(self):
        self.canvas.delete("all")
        for i in range(TAMANHO_TABULEIRO):
            for j in range(TAMANHO_TABULEIRO):
                x0 = j * TAMANHO_CASA
                y0 = i * TAMANHO_CASA
                x1 = x0 + TAMANHO_CASA
                y1 = y0 + TAMANHO_CASA
                cor_casa = "yellow" if self.selecionado == (i, j) else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor_casa, outline="gray")
                peca = self.tabuleiro[i][j]
                if peca:
                    cor = CORES_JOGADORES.get(peca, "black")
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=cor)

    def on_click(self, event):
        linha = event.y // TAMANHO_CASA
        coluna = event.x // TAMANHO_CASA
        if linha < 0 or linha >= TAMANHO_TABULEIRO or coluna < 0 or coluna >= TAMANHO_TABULEIRO:
            return
        if self.selecionado:
            origem = self.selecionado
            destino = (linha, coluna)
            if self.movimento_valido(origem, destino):
                self.mover_peca(origem, destino)
                self.enviar_jogada_callback(origem, destino)
            self.selecionado = None
            self.desenhar_tabuleiro()
        elif self.tabuleiro[linha][coluna]:
            self.selecionado = (linha, coluna)
            self.desenhar_tabuleiro()

    def movimento_valido(self, origem, destino):
        oi, oj = origem
        di, dj = destino
        if self.tabuleiro[di][dj] is not None:
            return False
        # Movimento simples (adjacente)
        if abs(oi-di) <= 1 and abs(oj-dj) <= 1 and (oi != di or oj != dj):
            return True
        # Pulo sobre peça (horizontal, vertical ou diagonal)
        if abs(oi-di) == 2 and abs(oj-dj) == 2:
            mi, mj = (oi+di)//2, (oj+dj)//2
            return self.tabuleiro[mi][mj] is not None
        if abs(oi-di) == 2 and oj == dj:
            mi = (oi+di)//2
            return self.tabuleiro[mi][oj] is not None
        if abs(oj-dj) == 2 and oi == di:
            mj = (oj+dj)//2
            return self.tabuleiro[oi][mj] is not None
        return False

    def mover_peca(self, origem, destino):
        oi, oj = origem
        di, dj = destino
        self.tabuleiro[di][dj] = self.tabuleiro[oi][oj]
        self.tabuleiro[oi][oj] = None

class NetworkedHalmaGame(HalmaGame):
    def __init__(self, master, conexao, is_host):
        print("[DEBUG] Entrou no construtor NetworkedHalmaGame")
        print(f"[DEBUG] conexao = {conexao}")
        print(f"[DEBUG] is_host = {is_host}")
        super().__init__(master, self.enviar_jogada_rede)
        self.desistido = False
        self.conexao = conexao
        self.is_host = is_host
        self.jogador = 'A' if is_host else 'B'
        self.eh_minha_vez = is_host
        self.atualizar_titulo_turno()
        print("[DEBUG] Antes de iniciar thread ouvir_rede")
        threading.Thread(target=self.ouvir_rede, daemon=True).start()
        print("[DEBUG] Depois de iniciar thread ouvir_rede")
        # Botão de desistência
        btn_desistir = tk.Button(self.master, text="Desistir", command=self.desistir)
        btn_desistir.pack(side=tk.BOTTOM, pady=10)

    def atualizar_titulo_turno(self):
        if self.eh_minha_vez:
            self.master.master.title(f"Halma - Seu turno ({'Azul' if self.jogador == 'A' else 'Vermelho'})")
        else:
            self.master.master.title("Halma - Turno do oponente")


    def on_click(self, event):
        if not self.eh_minha_vez:
            messagebox.showinfo("Turno", "Aguarde o turno do oponente!")
            return
        linha = event.y // TAMANHO_CASA
        coluna = event.x // TAMANHO_CASA
        if linha < 0 or linha >= TAMANHO_TABULEIRO or coluna < 0 or coluna >= TAMANHO_TABULEIRO:
            return
        if self.selecionado:
            origem = self.selecionado
            destino = (linha, coluna)
            if self.tabuleiro[origem[0]][origem[1]] != self.jogador:
                self.selecionado = None
                self.desenhar_tabuleiro()
                messagebox.showinfo("Movimento inválido", "Selecione uma peça da sua cor!")
                return
            if self.movimento_valido(origem, destino):
                self.mover_peca(origem, destino)
                self.enviar_jogada_rede(origem, destino)
                # Depois de jogar, sempre passa a vez
                self.eh_minha_vez = False
                self.atualizar_titulo_turno()
                self.verificar_vitoria_derrota()
            else:
                messagebox.showinfo("Movimento inválido", "Movimento não permitido!")
            self.selecionado = None
            self.desenhar_tabuleiro()
        elif self.tabuleiro[linha][coluna] == self.jogador:
            self.selecionado = (linha, coluna)
            self.desenhar_tabuleiro()
        elif self.tabuleiro[linha][coluna]:
            messagebox.showinfo("Movimento inválido", "Selecione apenas suas peças!")

    def enviar_jogada_rede(self, origem, destino):
        print(f"[DEBUG] Enviando jogada: origem={origem}, destino={destino}, jogador local={self.jogador}")
        try:
            dados = pickle.dumps((origem, destino))
            tamanho = len(dados).to_bytes(4, "big")  # prefixo com tamanho
            self.conexao.sendall(tamanho + dados)
            print("[DEBUG] Jogada enviada com sucesso!")
        except Exception as e:
            print(f"[ERRO ao enviar jogada]: {e}")

    def desistir(self):
        if not self.desistido:
            self.desistido = True
            dados = pickle.dumps({"desistir": True})
            tamanho = len(dados).to_bytes(4, "big")
            self.conexao.sendall(tamanho + dados)
            messagebox.showinfo("Desistência", "Você desistiu do jogo.")
            self.master.master.destroy()

    def ouvir_rede(self):
        print("[DEBUG] Thread de rede iniciada")
        while True:
            try:
                cabecalho = self.conexao.recv(4)
                if not cabecalho:
                    print("[DEBUG] Conexão fechada pelo oponente.")
                    break
                tamanho = int.from_bytes(cabecalho, "big")
                dados = b""
                while len(dados) < tamanho:
                    pacote = self.conexao.recv(tamanho - len(dados))
                    if not pacote:
                        print("[DEBUG] Conexão interrompida no meio da mensagem.")
                        break
                    dados += pacote
                if len(dados) < tamanho:
                    print("[DEBUG] Mensagem incompleta recebida, abortando jogada.")
                    continue
                recebido = pickle.loads(dados)
                if isinstance(recebido, dict) and "chat" in recebido:
                    if hasattr(self, "adicionar_mensagem_chat"):
                        self.adicionar_mensagem_chat("Oponente: " + recebido["chat"])
                elif isinstance(recebido, dict) and "desistir" in recebido:
                    messagebox.showinfo("Desistência", "O oponente desistiu do jogo.")
                    self.master.master.destroy()
                    break
                elif isinstance(recebido, tuple):
                    origem, destino = recebido
                    self.aplicar_jogada_remota(origem, destino)
                    self.eh_minha_vez = True
                    self.atualizar_titulo_turno()
                    self.verificar_vitoria_derrota()
            except Exception as e:
                import traceback
                print(f"[ERRO na thread de rede]: {e}")
                traceback.print_exc()
                break

    def aplicar_jogada_remota(self, origem, destino):
        self.mover_peca(origem, destino)
        self.desenhar_tabuleiro()
        # Não mexe em turno aqui

    def verificar_vitoria_derrota(self):
        # Verifica se todas as peças do jogador estão na base adversária
        def todas_na_base(jogador):
            if jogador == 'A':
                for i in range(4):
                    for j in range(4 - i):
                        if self.tabuleiro[TAMANHO_TABULEIRO-1-i][TAMANHO_TABULEIRO-1-j] != 'A':
                            return False
                return True
            else:
                for i in range(4):
                    for j in range(4 - i):
                        if self.tabuleiro[i][j] != 'B':
                            return False
                return True
        if todas_na_base(self.jogador):
            messagebox.showinfo("Vitória!", "Parabéns, você venceu!")
            self.master.master.destroy()  # Fecha janela
        elif todas_na_base('A' if self.jogador == 'B' else 'B'):
            messagebox.showinfo("Derrota", "O oponente venceu!")
            self.master.master.destroy()  # Fecha janela
