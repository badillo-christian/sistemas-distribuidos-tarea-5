import socket
import threading
from collections import deque
from helper import recv, SIMBOLO
from jugador import Jugador
from juego_gato import JuegoGato
import rpyc
from rpyc.utils.server import ThreadedServer
from threading import Thread

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
PORT_RPC = 12345
ADDR = (IP, PORT)

mutex = threading.Lock()
marcador_juegos = {}

class Marcador(rpyc.Service):
    def exposed_actualiza_marcador_server(self, nombre_jugador):
        print('Metodo invokado via RPC para actualizar la variable del server marcador_juegos')
        print('dicha variable: marcador_juegos, indica el numero de victorias por jugador')
        mutex.acquire()
        try:
            if nombre_jugador not in marcador_juegos:
                marcador_juegos[nombre_jugador] = 0
            marcador_juegos[nombre_jugador] += 1
            print(marcador_juegos)
        finally:
            mutex.release()

def GameHandler(conn1, addr1, conn2, addr2):
    nombre_jugador_1 = recv(conn1)
    nombre_jugador_2 = recv(conn2)
    player1 = Jugador(conn1, addr1, nombre_jugador_1, SIMBOLO[0])
    player2 = Jugador(conn2, addr2, nombre_jugador_2, SIMBOLO[1])
    print(f"[JUEGO INICIADO] {nombre_jugador_1} vs {nombre_jugador_2}")
    game = JuegoGato(player1, player2)
    del game
    print(f"[JUEGO FINALIZADO] {nombre_jugador_1} vs {nombre_jugador_2}")

def main():
    print("[INICIALIZADO RPC] Server RPC inicializado...")
    serverRPC = ThreadedServer(Marcador, port = PORT_RPC)
    threadRPC = Thread(target = serverRPC.start)
    threadRPC.daemon = True
    threadRPC.start()
    print(f"[ESCUCHANDO RPC] Server RPC escuchando en: {IP}:{PORT_RPC}")
    print("[INICIALIZADO] Server inicializado...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print(f"[ESCUCHANDO] Server escuchando en: {IP}:{PORT}")
    queue = deque()
    while True:
        conn, addr = server.accept()
        print(f"[NUEVA CONEXION] {addr} conectado")
        queue.append((conn, addr))
        while len(queue) >= 2:
            (conn1, addr1) = queue.popleft()
            (conn2, addr2) = queue.popleft()
            thread = threading.Thread(target=GameHandler, args=(conn1, addr1, conn2, addr2))
            thread.start()

if __name__ == "__main__":
    main()