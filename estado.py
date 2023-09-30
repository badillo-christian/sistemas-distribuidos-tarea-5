from helper import send, Estado

class EstadoJuego:
    def __init__(self, n):
        self.enEjecucion = True
        self.turn = 0
        self.tamanio_tablero = n
        self.tablero = [[' ' for x in range(self.tamanio_tablero)] for y in range(self.tamanio_tablero)]
        self.row = [0 for x in range(self.tamanio_tablero)]
        self.col = [0 for x in range(self.tamanio_tablero)]
        self.diag = [0, 0]
        self.contador_simbolos = 0
        self.ganador = None
        self.perdedor = None
        self.empate = False

    def cambia_turno(self):
        self.turn = not self.turn

    def movimiento(self, jugador, x, y):
        if 0 <= x < self.tamanio_tablero and 0 <= y < self.tamanio_tablero and self.tablero[x][y] == ' ':
            self.tablero[x][y] = jugador.simbolo
            self.contador_simbolos += 1
            self.row[x] += 1 if jugador.simbolo == 'X' else -1
            self.col[y] += 1 if jugador.simbolo == 'X' else -1
            if x == y:
                self.diag[0] += 1 if jugador.simbolo == 'X' else -1
            if self.tamanio_tablero - x - 1 == y:
                self.diag[1] += 1 if jugador.simbolo == 'X' else -1
            if (abs(self.row[x]) == self.tamanio_tablero or abs(self.col[y]) == self.tamanio_tablero
                    or abs(self.diag[0]) == self.tamanio_tablero or abs(self.diag[1]) == self.tamanio_tablero):
                return Estado.VICTORIA
            if self.contador_simbolos == pow(self.tamanio_tablero, 2):
                return Estado.EMPATE
            self.cambia_turno()
            return 1
        return 0