''' Storing all information of current state. Determines legal moves.'''
import numpy as np
class GameState():
    def __init__(self):
        self.board = np.array([
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N' : self.get_knight_moves, 
                                'B': self.get_bishop_moves, 'Q' : self.get_queen_moves, 'K' : self.get_king_moves}
        self.white_to_move = True
        self.move_log = []

        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False

   
    def make_move(self, move):
        self.board[move.start_row, move.start_col] = "  "
        self.board[move.end_row, move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        if move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row, move.end_col] = move.piece_moved[0] + 'Q'
        
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row, move.start_col] = move.piece_moved
            self.board[move.end_row, move.end_col] = move.piece_captured 
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            if move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

        self.check_mate = False
        self.stale_mate = False

    """check if move is possible (a pawn could move 1 step or 2 steps forward)."""
    def get_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c]
                if (turn[0] == 'w' and self.white_to_move) or (turn[0] == 'b' and not self.white_to_move):
                    piece = turn[1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):

        if self.white_to_move: #white plays from bottom to top, from 7 to 0            
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1,c - 1][0] == "b":  #strike enmy piece 
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1,c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r - 1 >= 0:
                if self.board[r - 1, c] == "  ":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2, c] == "  ":
                        moves.append(Move((r, c), (r - 2, c), self.board))

        if not self.white_to_move: #black plays           
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1,c - 1][0] == "w":  #strike enmy piece 
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r + 1,c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if r + 1 <= 7:
                if self.board[r + 1, c] == "  ": 
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2, c] == "  ":
                        moves.append(Move((r, c), (r + 2, c), self.board))                   

    def get_rook_moves(self, r, c, moves):      
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row, end_col]
                    if end_piece == "  ": 
                        moves.append(Move((r, c), (end_row, end_col), self.board))              
                    elif end_piece[0] == enemy: #if color of met piece is not equal to your piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break          
                    else: 
                        break 
                else:
                    break 
        
    def get_knight_moves(self, r, c, moves):

        knight_directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))    
        ally = "w" if self.white_to_move else "b"
        for d in knight_directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row, end_col]
                if end_piece[0] != ally:
                    moves.append(Move((r,c), (end_row, end_col), self.board))
            
    def get_bishop_moves(self, r, c, moves):

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row, end_col]
                    if end_piece == "  ":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else: 
                        break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        king_moves = ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row, end_col]
                if end_piece[0] != ally:
                    moves.append(Move((r,c), (end_row, end_col), self.board))

    """check if move is valid (if a pawn moves, the king may be checkmate (if black moves, check moves for white)"""
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                
                return True

        return False

    def get_valid_moves(self):
        moves = self.get_possible_moves()
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
            
        return moves

class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                     "e": 4, "f": 5, "g": 6, "h": 7}     
    cols_to_files = {v: k for k, v in files_to_cols.items()}  

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row, self.start_col] #cannot be empty
        self.piece_captured = board[self.end_row, self.end_col] #could be empty

        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col


    """override the equals method"""
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
            
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
