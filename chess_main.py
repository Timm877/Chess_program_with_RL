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
    game_over = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
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
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                print(move.get_chess_notation())
                                gs.make_move(valid_moves[i])
                                move_made = True
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  #undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
                    game_over = False
                if e.key == p.K_r: #reset whole board
                    gs = chess_engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False
                
        if move_made:
            valid_moves = gs.get_valid_moves() #move is made, generate new set of valid moves
            move_made = False

        draw_GameState(screen,gs, valid_moves, sq_selected)

        if gs.check_mate == True:
            #checkmate
            game_over = True
            if gs.white_to_move:
                draw_text(screen, 'Black wins by checkmate!')
            else:
                draw_text(screen, 'White wins by checkmate!')
        elif gs.stale_mate == True:
            #stalemate, remise
            game_over = True
            draw_text(screen, 'Remise by stalemate.')

        clock.tick(MAX_FPS)
        p.display.flip()

def highlight_moves(screen, gs, valid_moves, sq_selected):
    if sq_selected != (): #one mouse click, highlight moves
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(75)
        s.fill(p.Color('red'))
        screen.blit(s, (sq_selected[1] * SQ_SIZE, sq_selected[0] * SQ_SIZE))  
        s.fill(p.Color('yellow'))
        for i in range(len(valid_moves)):
            if (sq_selected[0] == valid_moves[i].start_row) and (sq_selected[1] == valid_moves[i].start_col):
                screen.blit(s, (valid_moves[i].end_col * SQ_SIZE, valid_moves[i].end_row * SQ_SIZE))      

def draw_GameState(screen, gs, valid_moves, sq_selected):
    draw_board(screen) # draw squares
    highlight_moves(screen, gs, valid_moves, sq_selected)
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

def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, p.Color('Black'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width() / 2,HEIGHT/2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('grey'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == '__main__':
    main()

