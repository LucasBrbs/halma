# Esse arquivo conecta o jogador ao servidor
import socket

# Função para conectar ao servidor
# ip: endereço do servidor (ex: '127.0.0.1')
# porta: número da porta (ex: 12345)
def conectar_servidor(ip, porta):
    # Cria o socket do cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Tenta conectar ao servidor
        cliente.connect((ip, porta))
        print(f"[Cliente] Conectado com sucesso a {ip}:{porta}")
    except Exception as e:
        # Se der erro, mostra a mensagem
        print(f"[Cliente] Erro ao conectar: {e}")
