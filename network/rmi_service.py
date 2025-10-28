# Interface do servico RMI para o jogo Halma
# Define os metodos que podem ser chamados remotamente

import rpyc
import threading
from rpyc.utils.server import ThreadedServer

class HalmaGameService(rpyc.Service):
    # Classe que implementa o servico RMI para comunicacao entre jogadores
    
    # Variaveis de classe para compartilhar entre todas as instancias
    jogadores_conectados = []  # lista de conexoes ativas
    jogadas_pendentes = {}     # jogadas aguardando processamento
    mensagens_chat = {}        # mensagens de chat por jogador
    jogador_desistiu = {}      # controle de desistencia
    lock = threading.Lock()    # sincronizacao de threads
    
    def on_connect(self, conn):
        # Chamado quando um cliente se conecta
        print(f"[Servidor RMI] Cliente conectado: {conn}")
        with HalmaGameService.lock:
            HalmaGameService.jogadores_conectados.append(conn)
            player_id = len(HalmaGameService.jogadores_conectados)
            HalmaGameService.jogadas_pendentes[player_id] = []
            HalmaGameService.mensagens_chat[player_id] = []
            HalmaGameService.jogador_desistiu[player_id] = False
            # Armazena informacoes na conexao
            setattr(conn, 'player_id', player_id)
            setattr(conn, 'is_host', (player_id == 1))
        print(f"[Servidor RMI] Jogador {player_id} configurado como {'host' if player_id == 1 else 'cliente'}")
    
    def on_disconnect(self, conn):
        # Chamado quando um cliente se desconecta
        print(f"[Servidor RMI] Cliente desconectado: {conn}")
        with HalmaGameService.lock:
            if conn in HalmaGameService.jogadores_conectados:
                HalmaGameService.jogadores_conectados.remove(conn)
    
    def exposed_registrar_jogador(self):
        # Registra um novo jogador e retorna seu ID e status de host
        # Procura a conexao atual na lista de conectados
        conn_atual = None
        with HalmaGameService.lock:
            # A ultima conexao adicionada eh a atual
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
        
        if conn_atual:
            player_id = getattr(conn_atual, 'player_id', 0)
            is_host = getattr(conn_atual, 'is_host', False)
            print(f"[Servidor RMI] Jogador {player_id} registrado")
            return player_id, is_host
        
        return 0, False
    
    def exposed_enviar_jogada(self, origem, destino):
        # Recebe uma jogada de um cliente e a envia para o oponente
        # Identifica o jogador pela ultima conexao (simplificado)
        player_id = 1  # sera atualizado abaixo
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                # Usa a ultima conexao como referencia (pode melhorar depois)
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
        
        print(f"[Servidor RMI] Jogada recebida do jogador {player_id}: {origem} -> {destino}")
        
        with HalmaGameService.lock:
            # Identifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.jogadas_pendentes:
                HalmaGameService.jogadas_pendentes[oponente_id] = []
            # Adiciona a jogada na lista do oponente
            HalmaGameService.jogadas_pendentes[oponente_id].append((origem, destino))
        
        return True
    
    def exposed_obter_jogada(self):
        # Retorna a proxima jogada pendente para este jogador
        # Identifica o jogador pela ultima conexao (simplificado)
        player_id = 1
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
            
            if player_id in HalmaGameService.jogadas_pendentes and HalmaGameService.jogadas_pendentes[player_id]:
                jogada = HalmaGameService.jogadas_pendentes[player_id].pop(0)
                print(f"[Servidor RMI] Enviando jogada para jogador {player_id}: {jogada}")
                return jogada
            return None
    
    def exposed_enviar_mensagem_chat(self, mensagem):
        # Envia mensagem de chat para o oponente
        player_id = 1
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
        
        print(f"[Servidor RMI] Mensagem de chat do jogador {player_id}: {mensagem}")
        
        with HalmaGameService.lock:
            # Identifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.mensagens_chat:
                HalmaGameService.mensagens_chat[oponente_id] = []
            # Adiciona mensagem na lista do oponente
            HalmaGameService.mensagens_chat[oponente_id].append(mensagem)
        
        return True
    
    def exposed_obter_mensagem_chat(self):
        # Retorna a proxima mensagem de chat pendente
        player_id = 1
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
            
            if player_id in HalmaGameService.mensagens_chat and HalmaGameService.mensagens_chat[player_id]:
                mensagem = HalmaGameService.mensagens_chat[player_id].pop(0)
                print(f"[Servidor RMI] Enviando mensagem de chat para jogador {player_id}")
                return mensagem
            return None
    
    def exposed_desistir_jogo(self):
        # Marca que o jogador desistiu e notifica o oponente
        player_id = 1
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
        
        print(f"[Servidor RMI] Jogador {player_id} desistiu do jogo")
        
        with HalmaGameService.lock:
            HalmaGameService.jogador_desistiu[player_id] = True
            # Notifica o oponente
            oponente_id = 2 if player_id == 1 else 1
            if oponente_id not in HalmaGameService.jogador_desistiu:
                HalmaGameService.jogador_desistiu[oponente_id] = False
        
        return True
    
    def exposed_verificar_desistencia(self):
        # Verifica se o oponente desistiu
        player_id = 1
        
        with HalmaGameService.lock:
            if HalmaGameService.jogadores_conectados:
                conn_atual = HalmaGameService.jogadores_conectados[-1]
                player_id = getattr(conn_atual, 'player_id', 1)
            
            oponente_id = 2 if player_id == 1 else 1
            desistiu = HalmaGameService.jogador_desistiu.get(oponente_id, False)
            if desistiu:
                print(f"[Servidor RMI] Informando jogador {player_id} que oponente desistiu")
            return desistiu
