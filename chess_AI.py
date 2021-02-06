import random

piece_values = {"p": 1, "N": 3.05, "B": 3.33, "R": 5.63, "Q": 9.5, 'K': 0}
CHECKMATE = 1000
STALEMATE = 0

"""Piece values are determined as zero-sum game: white wants to maximize points, so best outcome is + CHECKMATE
    Black wants to minimize points, best outcome is - CHECKMATE"""

def find_random_moves(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]


def find_most_material_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1 # makes piece values negative for black so black can maximize negative outcome
    opponent_min_max_score = CHECKMATE 
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        if gs.stale_mate:
            opponents_max_score = STALEMATE
        elif gs.check_mate:
            opponents_max_score = -CHECKMATE
        else:
            opponents_max_score = -CHECKMATE
            for opponents_move in opponents_moves:
                gs.make_move(opponents_move)
                gs.get_valid_moves()
                if gs.check_mate:
                    score = CHECKMATE
                elif gs.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(gs.board)
                if score > opponents_max_score:
                    opponents_max_score = score
                gs.undo_move()

        if opponents_max_score < opponent_min_max_score:
            opponent_min_max_score = opponents_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move

def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_values[square[1]]
            elif square[0] == 'b':
                score -= piece_values[square[1]]
    return score