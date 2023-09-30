from helper import *
from estado import EstadoJuego


class JuegoGato:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.state = EstadoJuego(N)
        send(self.player1.conn, Estado.JUGADOR_CONECTADO)
        send(self.player2.conn, Estado.JUGADOR_CONECTADO)
        while self.state.enEjecucion:
            self.espera_movimiento()

    def espera_movimiento(self):
        if self.state.turn == 0:
            send(self.player1.conn, Estado.TU_TURNO)
            send(self.player2.conn, Estado.NOT_TU_TURNO)
            msg = recv(self.player1.conn)
            msg = [int(x) for x in msg.split(',')]
            ret = self.state.movimiento(self.player1, msg[0], msg[1])
            if ret != 0:  
                send(self.player1.conn, (msg[0], msg[1], self.player1.simbolo))
                send(self.player2.conn, (msg[0], msg[1], self.player1.simbolo))
            if ret == Estado.VICTORIA:  
                self.state.ganador = self.player1
                self.state.perdedor = self.player2
                self.victoria()
            if ret == Estado.EMPATE:
                self.state.empate = True
                self.empate()
        else:
            send(self.player2.conn, Estado.TU_TURNO)
            send(self.player1.conn, Estado.NOT_TU_TURNO)
            msg = recv(self.player2.conn)
            msg = [int(x) for x in msg.split(',')]
            ret = self.state.movimiento(self.player2, msg[0], msg[1])
            if ret != 0:
                send(self.player1.conn, (msg[0], msg[1], self.player2.simbolo))
                send(self.player2.conn, (msg[0], msg[1], self.player2.simbolo))
            if ret == Estado.VICTORIA:
                self.state.ganador = self.player2
                self.state.perdedor = self.player1
                self.victoria()
            if ret == Estado.EMPATE:
                self.state.empate = True
                self.empate()

    def victoria(self):
        send(self.state.ganador.conn, Estado.VICTORIA)
        send(self.state.perdedor.conn, Estado.DERROTA)
        self.detener()

    def empate(self):
        send(self.player1.conn, Estado.EMPATE)
        send(self.player2.conn, Estado.EMPATE)
        self.detener()

    def detener(self):
        self.state.enEjecucion = False
        self.player1.conn.close()
        self.player2.conn.close()
