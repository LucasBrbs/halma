# Interface do servico RMI para o jogo Halma
# Define os metodos que podem ser chamados remotamente

import rpyc
import threading
from rpyc.utils.server import ThreadedServer

class HalmaGameService(rpyc.Service):
    # Classe que implementa o servico RMI para comunicacao entre jogadores
    
    # Variaveis de classe para compartilhar entre todas as instancias
    jogadores_conectados = {}  # dict mapping player_id -> conexao
    jogadas_pendentes = {}     # jogadas aguardando processamento
    mensagens_chat = {}        # mensagens de chat por jogador
    jogador_desistiu = {}      # controle de desistencia
    proximo_id = 1             # contador para IDs unicos
    conexao_para_id = {}       # mapeamento reverso conexao -> id
    lock = threading.Lock()    # sincronizacao de threads
    
    def __init__(self):
        self.conexao_atual = None
    
    def on_connect(self, conn):
        # Chamado quando um cliente se conecta
        print(f"[Servidor RMI] Cliente conectado: {conn}")
        self.conexao_atual = conn
        # Nao registra automaticamente - aguarda chamada explicita
    
    def on_disconnect(self, conn):
        # Chamado quando um cliente se desconecta
        print(f"[Servidor RMI] Cliente desconectado: {conn}")
        with HalmaGameService.lock:
            if conn in HalmaGameService.conexao_para_id:
                player_id = HalmaGameService.conexao_para_id[conn]
                del HalmaGameService.conexao_para_id[conn]
                del HalmaGameService.jogadores_conectados[player_id]
    
    def exposed_registrar_jogador(self):
        # Registra um novo jogador e retorna seu ID e status de host
        conn = self.conexao_atual
        with HalmaGameService.lock:
            # Verifica se ja esta registrado
            if conn in HalmaGameService.conexao_para_id:
                player_id = HalmaGameService.conexao_para_id[conn]
                is_host = (player_id == 1)
                print(f"[Servidor RMI] Jogador {player_id} ja registrado")
                return player_id, is_host
            
            # Encontra um ID disponivel (1 ou 2)
            player_id = 1 if 1 not in HalmaGameService.jogadores_conectados else 2
            is_host = (player_id == 1)
            
            # Registra o jogador nas estruturas de dados
            HalmaGameService.jogadores_conectados[player_id] = conn
            HalmaGameService.conexao_para_id[conn] = player_id
            HalmaGameService.jogadas_pendentes[player_id] = []
            HalmaGameService.mensagens_chat[player_id] = []
            HalmaGameService.jogador_desistiu[player_id] = False
            
            print(f"[Servidor RMI] Jogador {player_id} registrado como {'host' if is_host else 'cliente'}")
            return player_id, is_host
    
    def exposed_enviar_jogada(self, player_id, origem, destino):
        # Recebe uma jogada de um cliente e a envia para o oponente
        print(f"[Servidor RMI] Jogada recebida do jogador {player_id}: {origem} -> {destino}")
        
        with HalmaGameService.lock:
            # Identifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.jogadas_pendentes:
                HalmaGameService.jogadas_pendentes[oponente_id] = []
            # Adiciona a jogada na lista do oponente
            HalmaGameService.jogadas_pendentes[oponente_id].append((origem, destino))
            return True
    
    def exposed_obter_jogada(self, player_id):
        # Retorna jogadas pendentes para o cliente que chama
        with HalmaGameService.lock:
            if player_id in HalmaGameService.jogadas_pendentes and HalmaGameService.jogadas_pendentes[player_id]:
                return HalmaGameService.jogadas_pendentes[player_id].pop(0)
        return None
    
    def exposed_enviar_mensagem_chat(self, player_id, mensagem):
        # Envia mensagem de chat para o oponente
        print(f"[Servidor RMI] Chat do jogador {player_id}: {mensagem}")
        
        with HalmaGameService.lock:
            # Identifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.mensagens_chat:
                HalmaGameService.mensagens_chat[oponente_id] = []
            # Adiciona a mensagem na lista do oponente
            HalmaGameService.mensagens_chat[oponente_id].append(f"Jogador {player_id}: {mensagem}")
            return True
    
    def exposed_obter_mensagem_chat(self, player_id):
        # Retorna mensagens de chat pendentes para o cliente que chama
        with HalmaGameService.lock:
            if player_id in HalmaGameService.mensagens_chat and HalmaGameService.mensagens_chat[player_id]:
                return HalmaGameService.mensagens_chat[player_id].pop(0)
        return None
    
    def exposed_desistir_jogo(self, player_id):
        # Marca que o jogador desistiu e notifica o oponente
        print(f"[Servidor RMI] Jogador {player_id} desistiu do jogo")
        
        with HalmaGameService.lock:
            HalmaGameService.jogador_desistiu[player_id] = True
            # Notifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.jogador_desistiu:
                HalmaGameService.jogador_desistiu[oponente_id] = False
            return True
    
    def exposed_verificar_desistencia(self, player_id):
        # Verifica se o oponente desistiu
        with HalmaGameService.lock:
            oponente_id = 2 if player_id == 1 else 1
            desistiu = HalmaGameService.jogador_desistiu.get(oponente_id, False)
            if desistiu:
                print(f"[Servidor RMI] Informando jogador {player_id} que oponente desistiu")
            return desistiu
