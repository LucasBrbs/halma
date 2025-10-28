# Esse arquivo conecta o jogador ao servidor usando RMI
import rpyc
from network.config import PORTA_PADRAO, TIMEOUT_REDE

class ClienteRMI:
    # Classe para gerenciar conexao RMI com o servidor
    
    def __init__(self):
        self.conexao = None
        self.player_id = None
        self.is_host = False
    
    def conectar_servidor(self, ip, porta=PORTA_PADRAO):
        # Conecta ao servidor RMI
        # ip: endereco do servidor (ex: '127.0.0.1')  
        # porta: numero da porta (ex: 18861)
        try:
            print(f"[Cliente RMI] Tentando conectar a {ip}:{porta}...")
            # Estabelece conexao RMI com timeout
            self.conexao = rpyc.connect(ip, porta, config={
                'sync_request_timeout': TIMEOUT_REDE
            })
            print(f"[Cliente RMI] Conectado com sucesso a {ip}:{porta}")
            
            # Registra o jogador no servidor e obtem informacoes
            self.player_id, self.is_host = self.conexao.root.registrar_jogador()
            print(f"[Cliente RMI] Registrado como jogador {self.player_id}, host: {self.is_host}")
            
            return self.conexao
        except Exception as e:
            # Se der erro, mostra a mensagem
            print(f"[Cliente RMI] Erro ao conectar: {e}")
            return None
    
    def desconectar(self):
        # Fecha a conexao RMI
        if self.conexao:
            try:
                self.conexao.close()
                print("[Cliente RMI] Desconectado do servidor")
            except Exception as e:
                print(f"[Cliente RMI] Erro ao desconectar: {e}")
            finally:
                self.conexao = None
    
    def enviar_jogada(self, origem, destino):
        # Envia uma jogada para o servidor
        if not self.conexao:
            print("[Cliente RMI] Erro: Nao conectado ao servidor")
            return False
        try:
            resultado = self.conexao.root.enviar_jogada(self.player_id, origem, destino)
            print(f"[Cliente RMI] Jogada enviada: {origem} -> {destino}")
            return resultado
        except Exception as e:
            print(f"[Cliente RMI] Erro ao enviar jogada: {e}")
            return False
    
    def obter_jogada(self):
        # Obtem a proxima jogada do oponente
        if not self.conexao:
            return None
        try:
            jogada = self.conexao.root.obter_jogada(self.player_id)
            if jogada:
                print(f"[Cliente RMI] Jogada recebida: {jogada}")
            return jogada
        except Exception as e:
            print(f"[Cliente RMI] Erro ao obter jogada: {e}")
            return None
    
    def enviar_mensagem_chat(self, mensagem):
        # Envia mensagem de chat para o oponente
        if not self.conexao:
            return False
        try:
            resultado = self.conexao.root.enviar_mensagem_chat(self.player_id, mensagem)
            print(f"[Cliente RMI] Mensagem de chat enviada: {mensagem}")
            return resultado
        except Exception as e:
            print(f"[Cliente RMI] Erro ao enviar mensagem: {e}")
            return False
    
    def obter_mensagem_chat(self):
        # Obtem a proxima mensagem de chat
        if not self.conexao:
            return None
        try:
            mensagem = self.conexao.root.obter_mensagem_chat(self.player_id)
            if mensagem:
                print(f"[Cliente RMI] Mensagem de chat recebida: {mensagem}")
            return mensagem
        except Exception as e:
            print(f"[Cliente RMI] Erro ao obter mensagem: {e}")
            return None
    
    def desistir_jogo(self):
        # Informa ao servidor que o jogador desistiu
        if not self.conexao:
            return False
        try:
            resultado = self.conexao.root.desistir_jogo(self.player_id)
            print("[Cliente RMI] Desistencia enviada ao servidor")
            return resultado
        except Exception as e:
            print(f"[Cliente RMI] Erro ao desistir: {e}")
            return False
    
    def verificar_desistencia(self):
        # Verifica se o oponente desistiu
        if not self.conexao:
            return False
        try:
            desistiu = self.conexao.root.verificar_desistencia(self.player_id)
            if desistiu:
                print("[Cliente RMI] Oponente desistiu do jogo")
            return desistiu
        except Exception as e:
            print(f"[Cliente RMI] Erro ao verificar desistencia: {e}")
            return False

# Funcao de compatibilidade com o codigo antigo
def conectar_servidor(ip, porta=PORTA_PADRAO):
    # Cria um cliente RMI e conecta ao servidor
    cliente = ClienteRMI()
    conexao = cliente.conectar_servidor(ip, porta)
    if conexao:
        return cliente
    return None
