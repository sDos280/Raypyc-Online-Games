import ctypes
import pickle
import random

import raypyc

import network
import player


def main():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    TILE_WIDTH = 100
    TILE_HEIGHT = 100
    BOARD_START_DRAW_X = int(SCREEN_WIDTH / 2 - TILE_WIDTH * 1.5)
    BOARD_START_DRAW_Y = int(SCREEN_HEIGHT / 2 - TILE_HEIGHT * 1.5)

    raypyc.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Tic Tac Toe")

    net = network.Network()
    net.sendto_server(pickle.dumps([network.NetworkTypes.GET_PLAYER_TURN, ""]))
    this_start_player_turn = pickle.loads(net.recv(1024))[1]  # receive this player turn

    this_player = player.Player(this_start_player_turn)
    net.sendto_server(pickle.dumps([network.NetworkTypes.SET_PLAYER, this_player]))  # send this player data to the server

    raypyc.set_target_fps(60)

    while not raypyc.window_should_close():
        mouse_position = raypyc.get_mouse_position()
        over_cell = [-1, -1]  # row column
        if BOARD_START_DRAW_X < mouse_position.x <= BOARD_START_DRAW_X + TILE_WIDTH * 3 and \
                BOARD_START_DRAW_Y < mouse_position.y <= BOARD_START_DRAW_Y + TILE_HEIGHT * 3:
            over_cell[0] = (mouse_position.y - BOARD_START_DRAW_Y) // TILE_HEIGHT
            over_cell[1] = (mouse_position.x - BOARD_START_DRAW_X) // TILE_WIDTH
            if raypyc.is_mouse_button_pressed(0):
                net.sendto_server(pickle.dumps([network.NetworkTypes.SET_CELL, [over_cell[0], over_cell[1], this_player.is_x]]))  # send this player data to the server
        else:
            over_cell = [-1, -1]

        net.sendto_server(pickle.dumps([network.NetworkTypes.GET_BOARD, ""]))
        current_board = pickle.loads(net.recv(1024))[1]  # receive current board

        net.sendto_server(pickle.dumps([network.NetworkTypes.WHO_IS_WINNING, ""]))
        current_winner = pickle.loads(net.recv(1024))[1]  # receive current winner

        raypyc.begin_drawing()

        raypyc.clear_background(raypyc.RAYWHITE)

        # draw board line
        for i in range(1, 3):
            raypyc.draw_line_ex(raypyc.Vector2(BOARD_START_DRAW_X + TILE_WIDTH * i, BOARD_START_DRAW_Y),
                                raypyc.Vector2(BOARD_START_DRAW_X + TILE_WIDTH * i, BOARD_START_DRAW_Y + 3 * TILE_HEIGHT),
                                5, raypyc.BLACK)  # vertical lines
            raypyc.draw_line_ex(raypyc.Vector2(BOARD_START_DRAW_X, BOARD_START_DRAW_Y + TILE_HEIGHT * i),
                                raypyc.Vector2(BOARD_START_DRAW_X + 3 * TILE_WIDTH, BOARD_START_DRAW_Y + TILE_HEIGHT * i),
                                5, raypyc.BLACK)  # horizontal lines

        for i in range(3):
            for j in range(3):
                if current_board[i][j] == -1:
                    raypyc.draw_rectangle(BOARD_START_DRAW_X + TILE_WIDTH * j, BOARD_START_DRAW_Y + TILE_HEIGHT * i, TILE_WIDTH, TILE_HEIGHT, raypyc.GREEN)
                elif current_board[i][j] == 1:
                    raypyc.draw_rectangle(BOARD_START_DRAW_X + TILE_WIDTH * j, BOARD_START_DRAW_Y + TILE_HEIGHT * i, TILE_WIDTH, TILE_HEIGHT, raypyc.RED)

        if current_winner == -3:
            raypyc.clear_background(raypyc.RAYWHITE)
            raypyc.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, raypyc.GREEN)
        elif current_winner == 3:
            raypyc.clear_background(raypyc.RAYWHITE)
            raypyc.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, raypyc.RED)

        raypyc.end_drawing()

    net.sendto_server(pickle.dumps([network.NetworkTypes.DISCONNECT, this_player.my_hash]))
    raypyc.close_window()


if __name__ == '__main__':
    main()
