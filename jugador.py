from helper import send, recv


class Jugador:
    def __init__(self, conn, addr, nombre_jugador, simbolo):
        self.conn = conn
        self.addr = addr
        self.nombre_jugador = nombre_jugador
        self.simbolo = simbolo