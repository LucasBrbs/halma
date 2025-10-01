# Responsável por conectar a um servidor existente
import socket
from ui.game import GameUI

def conectar_servidor(ip, porta):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ip, porta))
        print(f"[Cliente] Conectado com sucesso a {ip}:{porta}")
        GameUI(cliente, is_host=False)
    except Exception as e:
        print(f"[Cliente] Erro ao conectar: {e}")
