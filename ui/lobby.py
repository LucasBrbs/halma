import tkinter as tk
from network.server import iniciar_servidor
from network.client import ClienteRMI
from network.config import PORTA_PADRAO
from ui.game import NetworkedHalmaGame
import threading
import time

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
    porta_entry.insert(0, str(PORTA_PADRAO))
    tk.Label(conn_frame, text="IP:").pack(side=tk.LEFT)
    ip_entry = tk.Entry(conn_frame, width=12)
    ip_entry.pack(side=tk.LEFT)
    ip_entry.insert(0, "127.0.0.1")

    def iniciar_jogo(cliente_rmi):
        game_root = tk.Tk()
        game_root.title("Halma - Jogo e Chat")

        # Frame do jogo
        game_frame = tk.Frame(game_root)
        game_frame.pack(side=tk.LEFT)
        game = NetworkedHalmaGame(game_frame, cliente_rmi)
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
                adicionar_mensagem_chat("Voce: " + msg)
                # Usa RMI para enviar mensagem de chat
                cliente_rmi.enviar_mensagem_chat(msg)
                chat_entry.delete(0, tk.END)
        send_button.config(command=enviar_mensagem_chat)
        chat_entry.bind("<Return>", lambda event: enviar_mensagem_chat())

        # Passa funcao para adicionar mensagem de chat para o game
        game.adicionar_mensagem_chat = adicionar_mensagem_chat

        game_root.mainloop()

    def hospedar():
        porta = int(porta_entry.get())
        escolha_jogador = tk.Toplevel()
        escolha_jogador.title("Escolha quem comeca")
        var = tk.StringVar(value="A")
        tk.Label(escolha_jogador, text="Quem comeca?").pack()
        tk.Radiobutton(escolha_jogador, text="Servidor (Preto)", variable=var, value="A").pack()
        tk.Radiobutton(escolha_jogador, text="Cliente (Branco)", variable=var, value="B").pack()
        def iniciar_servidor_com_escolha():
            escolha_jogador.destroy()
            # Inicia o servidor RMI
            servidor_rmi = iniciar_servidor(porta)
            if servidor_rmi:
                root.destroy()
                print(f"[Servidor RMI] Aguardando conexoes na porta {porta}...")
                # Aguarda ate dois jogadores conectarem
                cliente_rmi = aguardar_dois_jogadores(porta, var.get())
                if cliente_rmi:
                    iniciar_jogo(cliente_rmi)
        tk.Button(escolha_jogador, text="Iniciar", command=iniciar_servidor_com_escolha).pack()
    
    def aguardar_dois_jogadores(porta, escolha_inicial):
        # Funcao auxiliar para aguardar conexao de dois jogadores
        # Simula ser um cliente conectado ao proprio servidor
        cliente_rmi = ClienteRMI()
        tentativas = 0
        max_tentativas = 60  # 30 segundos tentando
        
        while tentativas < max_tentativas:
            conexao = cliente_rmi.conectar_servidor("127.0.0.1", porta)
            if conexao:
                # Se a escolha inicial era servidor (A), o host eh True
                # Caso contrario, inverte a logica
                if escolha_inicial == "A":
                    cliente_rmi.is_host = True
                else:
                    cliente_rmi.is_host = False
                return cliente_rmi
            time.sleep(0.5)
            tentativas += 1
        
        print("[Erro] Tempo limite para aguardar conexoes")
        return None

    def entrar():
        ip = ip_entry.get()
        porta = int(porta_entry.get())
        cliente_rmi = ClienteRMI()
        try:
            conexao = cliente_rmi.conectar_servidor(ip, porta)
            if conexao:
                print(f"[Cliente RMI] Conectado com sucesso a {ip}:{porta}")
                root.destroy()
                iniciar_jogo(cliente_rmi)
            else:
                print(f"[Cliente RMI] Falha ao conectar a {ip}:{porta}")
        except Exception as e:
            print(f"[Cliente RMI] Erro ao conectar: {e}")

    tk.Button(conn_frame, text="Hospedar", command=hospedar).pack(side=tk.LEFT, padx=5)
    tk.Button(conn_frame, text="Entrar", command=entrar).pack(side=tk.LEFT, padx=5)

    root.mainloop()