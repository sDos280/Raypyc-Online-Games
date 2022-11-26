import pickle
import socket

import network
import player


def who_wins(_board):
    checks = [
        [[0, 0], [0, 1], [0, 2]],  # first row
        [[1, 0], [1, 1], [1, 2]],  # second row
        [[2, 0], [2, 1], [2, 2]],  # third row
        [[0, 0], [1, 0], [2, 0]],  # first column
        [[0, 1], [1, 1], [2, 1]],  # second column
        [[0, 2], [1, 2], [2, 2]],  # third column
        [[2, 0], [1, 1], [0, 2]],  # diagonal left-right down-up
        [[0, 0], [1, 1], [2, 2]]  # diagonal left-right up-down
    ]
    value = 0
    for check in checks:
        value = 0
        for i in range(3):
            value += _board[check[i][0]][check[i][1]]
        if abs(value) == 3:  # if value equal to -3 or 3
            return value
    return value


server_ip = "10.0.0.22"
port_number = 5555
buffer_size = 1024

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((server_ip, port_number))

print("UDP server up and listening")
print(f"Server is bind at {server_ip}:{port_number}")
players: dict[player.Player] = dict()
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
turn_x = True

while True:
    if len(players) == 0:
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        turn_x = True

    data_bytes, address = server_sock.recvfrom(buffer_size)
    data = pickle.loads(data_bytes)
    data_network_type = data[0]
    data_content = data[1]
    match data_network_type:
        case network.NetworkTypes.CONNECTION:
            print(f"Client Connected, IP Address: {address[0]}, {address[1]}")
        case network.NetworkTypes.DISCONNECT:
            print(f"Client Disconnected, IP Address: {address[0]}, {address[1]}")
            del players[data_content]
        case network.NetworkTypes.SET_PLAYER:
            players[data_content.my_hash] = data_content
        case network.NetworkTypes.GET_PLAYERS:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.PLAYERS, players]), address)
        case network.NetworkTypes.SET_CELL:
            if turn_x == data_content[2]:
                if board[int(data_content[0])][int(data_content[1])] == 0:
                    if data_content[2]:  # x turn
                        board[int(data_content[0])][int(data_content[1])] = -1
                    else:  # o turn
                        board[int(data_content[0])][int(data_content[1])] = 1
                turn_x = not turn_x
        case network.NetworkTypes.GET_TURN:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.TURN_X, turn_x]), address)
        case network.NetworkTypes.GET_PLAYER_TURN:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.TURN_X, len(players) % 2 == 0]), address)
        case network.NetworkTypes.GET_BOARD:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.BOARD, board]), address)
        case network.NetworkTypes.WHO_IS_WINNING:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.HOW_WIN, who_wins(board)]), address)
        case network.NetworkTypes.RESET_GAME:
            board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
            turn_x = True
