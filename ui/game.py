class NetworkedHalmaGame(HalmaGame):
    def __init__(self, master, conexao, is_host):
        super().__init__(master, self.enviar_jogada_rede)
        self.conexao = conexao
        self.is_host = is_host
        self.jogador = 'A' if is_host else 'B'
        self.eh_minha_vez = is_host  # Host (A / Azul) sempre começa
        self.atualizar_titulo_turno()
        threading.Thread(target=self.ouvir_rede, daemon=True).start()

    def atualizar_titulo_turno(self):
        if self.eh_minha_vez:
            nome = 'Azul' if self.jogador == 'A' else 'Vermelho'
            self.master.master.title(f"Halma - Seu turno ({nome})")
        else:
            nome = 'Azul' if self.jogador == 'B' else 'Vermelho'
            self.master.master.title(f"Halma - Turno do oponente ({nome})")

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

                # 🔹 Depois de jogar, sempre passa a vez
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
        dados = pickle.dumps((origem, destino))
        tamanho = len(dados).to_bytes(4, "big")  # prefixo com tamanho
        self.conexao.sendall(tamanho + dados)

    def ouvir_rede(self):
        while True:
            try:
                # Lê o tamanho da mensagem
                cabecalho = self.conexao.recv(4)
                if not cabecalho:
                    break
                tamanho = int.from_bytes(cabecalho, "big")

                # Lê os dados completos
                dados = b""
                while len(dados) < tamanho:
                    pacote = self.conexao.recv(tamanho - len(dados))
                    if not pacote:
                        break
                    dados += pacote

                origem, destino = pickle.loads(dados)
                self.aplicar_jogada_remota(origem, destino)

                # 🔹 Após jogada do oponente, minha vez
                self.eh_minha_vez = True
                self.atualizar_titulo_turno()
                self.verificar_vitoria_derrota()
            except Exception as e:
                print(f"[ERRO na thread de rede]: {e}")
                break

    def aplicar_jogada_remota(self, origem, destino):
        self.mover_peca(origem, destino)
        self.desenhar_tabuleiro()
        # ❌ Não mexe em turno aqui

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
            self.master.master.destroy()  # 🔹 Fecha janela
        elif todas_na_base('A' if self.jogador == 'B' else 'B'):
            messagebox.showinfo("Derrota", "O oponente venceu!")
            self.master.master.destroy()  # 🔹 Fecha janela
