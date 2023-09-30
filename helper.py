from pickle import dumps, loads
import enum
import select

ENCODING = 'utf-8'
TAMANIO_CABECERA = 10
SIMBOLO = ('X', 'O')
N = 3

class Estado(enum.Enum):
    JUGADOR_CONECTADO = 0
    DESCONECTADO = 1
    TU_TURNO = 2
    NOT_TU_TURNO = 3
    VICTORIA = 4
    DERROTA = 5
    EMPATE = 6

def send(socket, msg):
    msg = dumps(msg)
    msg = bytes(f'{len(msg):<{TAMANIO_CABECERA}}', ENCODING) + msg
    socket.sendall(msg)

def recv(socket):
    full_msg = b''
    new_msg = True
    while True:
        msg = socket.recv(4096)
        if new_msg:
            msglen = int(msg[:TAMANIO_CABECERA])
            new_msg = False
        full_msg += msg
        if len(full_msg) - TAMANIO_CABECERA >= msglen:
            d = loads(full_msg[TAMANIO_CABECERA:])
            break
    return d
