import socket
import sys
from helper import *
import rpyc

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)

conn = rpyc.connect(IP, 12345)

def main():
    nombre_jugador = sys.argv[1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(ADDR)
    tablero = [[' ' for x in range(N)] for y in range(N)]

    def print_tablero():
        print(f'''               Y/X   0   1   2

                 0   {tablero[0][0]} | {tablero[0][1]} | {tablero[0][2]}
                    ---|---|---
                 1   {tablero[1][0]} | {tablero[1][1]} | {tablero[1][2]}
                    ---|---|---
                 2   {tablero[2][0]} | {tablero[2][1]} | {tablero[2][2]}''')

    send(server, nombre_jugador)
    print(f"[CONEXION] Cliente se ha conectedo al server: {IP}:{PORT}")
    print("[ESPERANDO] Esperando por un jugador...")
    msg = recv(server)
    if msg == Estado.JUGADOR_CONECTADO:
        print(f"[SERVER] Jugador Conectado")
        print_tablero()
    while True:
        msg = recv(server)
        if msg == Estado.DESCONECTADO:
            server.close()
            break
        elif msg == Estado.TU_TURNO:
            print("Tu Turno (Y,X)...")
            send(server, input("> "))
        elif msg == Estado.NOT_TU_TURNO:
            print("Turno del oponente...")
        elif msg == Estado.VICTORIA:
            print_tablero()
            print("Ganaste... :)")
            conn.root.actualiza_marcador_server(nombre_jugador)
            server.close()
            break
        elif msg == Estado.DERROTA:
            print_tablero()
            print("Perdiste... :(")
            server.close()
            break
        elif msg == Estado.EMPATE:
            print_tablero()
            print("Juego empatado... :|")
            server.close()
            break
        else:
            tablero[msg[0]][msg[1]] = msg[2]
            print_tablero()

if __name__ == "__main__":
    main()