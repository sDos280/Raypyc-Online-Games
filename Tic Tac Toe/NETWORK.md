# Network

the network class will be the connector object (that receive/send data) for the client 

* sock - the socket object that we create 
* server - the server ip that we want to connect to (example: `"10.0.0.22"`)
* port - the port number that the sever is bind to (example: `5555`)

# NetworkTypes

the NetworkType class is an enum of all the Action/Data that the Network transform/get

| Type Name       | summery                                                                                               |
|:----------------|:------------------------------------------------------------------------------------------------------|
| CONNECT         | just send some data that said like "a connection from (MyIp)" [^note1]                                |
| DISCONNECT      | send the hash of the this player so the server can disconnect/unload this player from the server data |
| SET_PLAYER      | send data of a Player (a Player class) to be set in the server                                        |
| GET_PLAYERS     | get data of the players (a dict keys: player_hash, values: Player )                                   |
| PLAYERS         | a dict keys:player_hash, values:Player                                                                |
| SET_CELL        | send the data of the cell that the client what to change (row: int, column: int, number: int)         |
| GET_TURN        | get the turn of the game. if True it is X turn if False it is O turn                                  |  
| GET_PLAYER_TURN | get the player turn so the client will know if he o ot x                                              |
| TURN_X          | data of a turn. if True it is X turn if False it is O turn                                            |

[^note1]: we need to send this message so the server will know that this ip is connected to the game.


# Functions
* `connect(None) -> None` connect to the server (send "hello world" as data to the server)
* `recv(bytes_length: int) -> bytes:` receive data from the socket
* `sendto_server(data: bytes) -> None` send the provided data to the server

# sources that helped
https://pythontic.com/modules/socket/udp-client-server-example