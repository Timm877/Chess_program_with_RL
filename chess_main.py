''' Main driver: for displaying current game state and handling user input.'''
## FINISHED VIDEO 1
import pygame as p
import os
import numpy as np
import chess_engine


p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    for filename in os.listdir('images'):
        IMAGES[str(filename[:-4])] = p.transform.scale(p.image.load("images/" + str(filename)), (SQ_SIZE, SQ_SIZE))


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False #flag variable for whe a mode is made
    load_images()
    running = True
    sq_selected = () #last click of user
    player_clicks = [] # keep track of player clicks (2 tuples)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x,y so col, row
                col  = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col): #twice on same square (UNDO)
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col) #better notation
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2: #two mouse clicks
                    move = chess_engine.Move(player_clicks[0],player_clicks[1], gs.board)
                    if move in valid_moves:
                        print(move.get_chess_notation())
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()
                        player_clicks = []
                    if move not in valid_moves:
                        move_made = False
                        sq_selected = ()
                        player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  #undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
                    
        if move_made:
            valid_moves = gs.get_valid_moves() #move is made, generate new set of valid moves
            move_made = False

        draw_GameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_GameState(screen, gs):
    draw_board(screen) # draw squares
    draw_pieces(screen, gs.board) # draw pieces on top


def draw_board(screen):
    colors = [p.Color((235, 235, 208)), p.Color((119, 148, 85))]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) % 2)]
            p.draw.rect(screen, color, p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            

def draw_pieces(screen, gs):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = gs[i,j]
            if piece != "  ":
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()

