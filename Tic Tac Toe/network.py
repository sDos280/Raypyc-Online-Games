import enum
import socket
import pickle

class NetworkTypes(enum.IntEnum):
    CONNECTION = enum.auto()
    DISCONNECT = enum.auto()
    SET_PLAYER = enum.auto()
    GET_PLAYERS = enum.auto()
    PLAYERS = enum.auto()
    SET_CELL = enum.auto()
    GET_TURN = enum.auto()
    GET_PLAYER_TURN = enum.auto()
    TURN_X = enum.auto()
    GET_BOARD = enum.auto()
    BOARD = enum.auto()
    WHO_IS_WINNING = enum.auto()
    HOW_WIN = enum.auto()
    RESET_GAME = enum.auto()


class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "10.0.0.22"
        self.port = 5555
        self.connect()

    def connect(self) -> None:
        self.sock.sendto(pickle.dumps([NetworkTypes.CONNECTION, "hello world"]), (self.server, self.port))

    def recv(self, bytes_length: int) -> bytes:
        return self.sock.recv(bytes_length)

    def sendto_server(self, data: bytes) -> None:
        self.sock.sendto(data, (self.server, self.port))
