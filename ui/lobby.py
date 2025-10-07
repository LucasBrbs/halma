import tkinter as tk
from ui.game import HalmaGame

def iniciar_lobby():
    root = tk.Tk()
    root.title("Halma - Lobby e Chat")

    # Frame principal
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.LEFT)

    # Chat
    chat_frame = tk.Frame(main_frame)
    chat_frame.pack(side=tk.TOP)
    chat_log = tk.Text(chat_frame, height=15, width=40, state=tk.DISABLED)
    chat_log.pack(side=tk.TOP)
    chat_entry = tk.Entry(chat_frame, width=30)
    chat_entry.pack(side=tk.LEFT)
    send_button = tk.Button(chat_frame, text="Enviar")
    send_button.pack(side=tk.LEFT)

    # Função para adicionar mensagem ao chat
    def adicionar_mensagem_chat(msg):
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, msg + "\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.see(tk.END)

    # Função para enviar mensagem de chat (adapte para enviar pela rede)
    def enviar_mensagem_chat():
        msg = chat_entry.get()
        if msg:
            adicionar_mensagem_chat("Você: " + msg)
            # TODO: Enviar mensagem para o servidor/oponente
            # Exemplo: network_client.enviar_mensagem_chat(msg)
            chat_entry.delete(0, tk.END)
    send_button.config(command=enviar_mensagem_chat)
    chat_entry.bind("<Return>", lambda event: enviar_mensagem_chat())

    # Função para enviar jogada pela rede (adapte para enviar pela rede)
    def enviar_jogada(origem, destino):
        adicionar_mensagem_chat(f"Jogada enviada: {origem} -> {destino}")
        # TODO: Enviar jogada para o servidor/oponente
        # Exemplo: network_client.enviar_jogada(origem, destino)

    # Frame do jogo Halma
    game_frame = tk.Frame(root)
    game_frame.pack(side=tk.RIGHT)
    halma = HalmaGame(game_frame, enviar_jogada)
    halma.pack()

    # Função para receber jogada remota (chame quando receber do servidor)
    def receber_jogada_remota(origem, destino):
        halma.aplicar_jogada_remota(origem, destino)
        adicionar_mensagem_chat(f"Jogada recebida: {origem} -> {destino}")

    # Função para receber mensagem de chat remota
    def receber_mensagem_chat_remota(msg):
        adicionar_mensagem_chat("Oponente: " + msg)

    # TODO: Integre as funções acima ao seu sistema de rede:
    # network_client.on_jogada_recebida = receber_jogada_remota
    # network_client.on_chat_recebido = receber_mensagem_chat_remota

    root.mainloop()