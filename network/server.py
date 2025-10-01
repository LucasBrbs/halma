# Responsável por hospedar o servidor e aceitar conexão de um cliente
import socket
from ui.game import GameUI

def iniciar_servidor(porta):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', porta))
    servidor.listen(1)
    print(f"[Servidor] Aguardando conexão na porta {porta}...")

    conexao, endereco = servidor.accept()
    print(f"[Servidor] Conectado com {endereco}")
    GameUI(conexao, is_host=True)
