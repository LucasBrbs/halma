# Responsável por exibir a tela de lobby (entrada do jogo)
import tkinter as tk
from network.server import iniciar_servidor
from network.client import conectar_servidor

def iniciar_lobby():
    def hospedar():
        porta = entry_porta.get()
        if porta.isdigit():
            janela.destroy()
            iniciar_servidor(int(porta))
        else:
            print("Porta inválida")

    def entrar():
        ip = entry_ip.get()
        porta = entry_porta.get()
        if porta.isdigit():
            janela.destroy()
            conectar_servidor(ip, int(porta))
        else:
            print("IP ou Porta inválidos")

    janela = tk.Tk()
    janela.title("Seega - Lobby")
    janela.geometry("300x200")

    tk.Label(janela, text="Porta:").pack()
    entry_porta = tk.Entry(janela)
    entry_porta.pack()

    tk.Label(janela, text="IP (apenas para entrar):").pack()
    entry_ip = tk.Entry(janela)
    entry_ip.pack()

    tk.Button(janela, text="Hospedar", command=hospedar).pack(pady=10)
    tk.Button(janela, text="Entrar", command=entrar).pack()

    janela.mainloop()
