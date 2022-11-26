import pickle
import socket
import player
import network

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
            board[data_content[0]][data_content[1]] = data_content[2]
        case network.NetworkTypes.GET_TURN:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.TURN_X, turn_x]), address)
        case network.NetworkTypes.GET_PLAYER_TURN:
            server_sock.sendto(pickle.dumps([network.NetworkTypes.TURN_X, len(players) % 2 == 0]), address)

