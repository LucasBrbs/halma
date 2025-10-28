# Responsavel por hospedar o servidor RMI e aceitar conexoes de clientes
import rpyc
from rpyc.utils.server import ThreadedServer
from network.rmi_service import HalmaGameService
from network.config import PORTA_PADRAO
import threading

# Variavel global para controlar o servidor RMI
servidor_rmi = None

def iniciar_servidor(porta=PORTA_PADRAO):
    # Inicia o servidor RMI na porta especificada
    global servidor_rmi
    try:
        print(f"[Servidor RMI] Iniciando servidor na porta {porta}...")
        # Cria o servidor threadead para suportar multiplos clientes
        servidor_rmi = ThreadedServer(HalmaGameService, port=porta)
        print(f"[Servidor RMI] Servidor iniciado com sucesso na porta {porta}")
        print(f"[Servidor RMI] Aguardando conexoes de clientes...")
        # Inicia o servidor em thread separada para nao bloquear a interface
        thread_servidor = threading.Thread(target=servidor_rmi.start, daemon=True)
        thread_servidor.start()
        return servidor_rmi
    except Exception as e:
        print(f"[Servidor RMI] Erro ao iniciar servidor: {e}")
        return None

def parar_servidor():
    # Para o servidor RMI se estiver rodando
    global servidor_rmi
    if servidor_rmi:
        print("[Servidor RMI] Parando servidor...")
        servidor_rmi.close()
        servidor_rmi = None
        print("[Servidor RMI] Servidor parado")
