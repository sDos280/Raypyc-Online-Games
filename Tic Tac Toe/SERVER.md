# Server

the server will be the connector of all the clients

# server setup steps

1. we create the server socket and bind it to the ip and port that we will like

# server main loop

1. receive packages from the server socket
2. process the data received from the server socket

# process NetworkTypes 
if:
* CONNECTION - print the client address and the message form the client 
* DISCONNECT - print the disconnected client
* SET_PLAYER - set the player data by the given player data and hash

# server variables
* server_ip - the server ip
* port_number - the number of the port that hte server will bind to
* buffer_size - the size of the data buffer that comes from the socket
* server_sock - the server socket object
* players - dictionory of the player. (keys: hash of player, values: player)
* board - the tic-tac-toe board data 0-None -1-x 1-o
* turn_x - store the current turn if true it will be x turn otherwise it will be o turn