import tkinter as tk
from network.server import iniciar_servidor
from network.client import conectar_servidor
from ui.game import NetworkedHalmaGame
import socket
import threading
import pickle

def iniciar_lobby():
    root = tk.Tk()
    root.title("Halma - Lobby e Chat")

    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.LEFT)

    conn_frame = tk.Frame(main_frame)
    conn_frame.pack(side=tk.TOP, pady=10)
    tk.Label(conn_frame, text="Porta:").pack(side=tk.LEFT)
    porta_entry = tk.Entry(conn_frame, width=6)
    porta_entry.pack(side=tk.LEFT)
    porta_entry.insert(0, "12345")
    tk.Label(conn_frame, text="IP:").pack(side=tk.LEFT)
    ip_entry = tk.Entry(conn_frame, width=12)
    ip_entry.pack(side=tk.LEFT)
    ip_entry.insert(0, "127.0.0.1")

    def iniciar_jogo(conexao, is_host):
        game_root = tk.Tk()
        game_root.title("Halma - Jogo e Chat")

        # Frame do jogo
        game_frame = tk.Frame(game_root)
        game_frame.pack(side=tk.LEFT)
        game = NetworkedHalmaGame(game_frame, conexao, is_host)
        game.pack()

        # Frame do chat
        chat_frame = tk.Frame(game_root)
        chat_frame.pack(side=tk.RIGHT, padx=10)
        chat_log = tk.Text(chat_frame, height=20, width=40, state=tk.DISABLED)
        chat_log.pack(side=tk.TOP)
        chat_entry = tk.Entry(chat_frame, width=30)
        chat_entry.pack(side=tk.LEFT)
        send_button = tk.Button(chat_frame, text="Enviar")
        send_button.pack(side=tk.LEFT)

        def adicionar_mensagem_chat(msg):
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, msg + "\n")
            chat_log.config(state=tk.DISABLED)
            chat_log.see(tk.END)

        def enviar_mensagem_chat():
            msg = chat_entry.get()
            if msg:
                adicionar_mensagem_chat("Você: " + msg)
                dados = pickle.dumps({"chat": msg})
                tamanho = len(dados).to_bytes(4, "big")
                conexao.sendall(tamanho + dados)
                chat_entry.delete(0, tk.END)
        send_button.config(command=enviar_mensagem_chat)
        chat_entry.bind("<Return>", lambda event: enviar_mensagem_chat())

        # Remover a thread ouvir_chat, pois o game vai ler tudo
        # threading.Thread(target=ouvir_chat, daemon=True).start()

        # Passar função para adicionar mensagem de chat para o game
        game.adicionar_mensagem_chat = adicionar_mensagem_chat

        game_root.mainloop()

    def hospedar():
        porta = int(porta_entry.get())
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(('', porta))
        servidor.listen(1)
        root.destroy()
        print(f"[Servidor] Aguardando conexão na porta {porta}...")
        conexao, endereco = servidor.accept()
        print(f"[Servidor] Conectado com {endereco}")
        iniciar_jogo(conexao, True)

    def entrar():
        ip = ip_entry.get()
        porta = int(porta_entry.get())
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cliente.connect((ip, porta))
            print(f"[Cliente] Conectado com sucesso a {ip}:{porta}")
            root.destroy()
            iniciar_jogo(cliente, False)
        except Exception as e:
            print(f"[Cliente] Erro ao conectar: {e}")

    tk.Button(conn_frame, text="Hospedar", command=hospedar).pack(side=tk.LEFT, padx=5)
    tk.Button(conn_frame, text="Entrar", command=entrar).pack(side=tk.LEFT, padx=5)

    root.mainloop()