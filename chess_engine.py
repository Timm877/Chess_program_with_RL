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
    
    def make_move(self, move):
        self.board[move.start_row, move.start_col] = "  "
        self.board[move.end_row, move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row, move.start_col] = move.piece_moved
            self.board[move.end_row, move.end_col] = move.piece_captured 
            self.white_to_move = not self.white_to_move

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
        return moves

    def get_rook_moves(self, r, c, moves):      
        i = r + 1
        other_piece = True
        if i <= 7:
            for i in range(i, 8):
                if other_piece:
                    if self.board[i, c] == "  ": 
                        moves.append(Move((r, c), (i, c), self.board))              
                    elif self.board[i, c][0] != self.board[r, c][0]: #if color of met piece is not equal to your piece
                        moves.append(Move((r, c), (i, c), self.board))
                        other_piece = False           
                    elif self.board[i, c][0] == self.board[r, c][0]: 
                        other_piece = False

        i = r - 1
        other_piece = True
        if i >= 0:
            for i in range(i, -1, -1):
                if other_piece:
                    if self.board[i, c] == "  ":
                        moves.append(Move((r, c), (i, c), self.board))                            
                    elif self.board[i, c][0] != self.board[r, c][0]: 
                        moves.append(Move((r, c), (i, c), self.board))  
                        other_piece = False 
                    elif self.board[i, c][0] == self.board[r, c][0]:
                        other_piece = False          

        i = c + 1
        other_piece = True
        if i <= 7:
            for i in range(i, 8):
                if other_piece:
                    if self.board[r, i] == "  ": 
                        moves.append(Move((r,c), (r, i), self.board))             
                    elif self.board[r, i][0] != self.board[r, c][0]: 
                        moves.append(Move((r, c), (r, i), self.board))
                        other_piece = False
                    elif self.board[r, i][0] == self.board[r, c][0]:
                        other_piece = False

        i = c - 1
        other_piece = True
        if i >= 0:
            for i in range(i, -1, -1):
                if other_piece:
                    if self.board[r, i] == "  ":
                        moves.append(Move((r,c), (r, i), self.board))                
                    elif self.board[r, i][0] != self.board[r, c][0]: 
                        moves.append(Move((r, c), (r, i), self.board))   
                        other_piece = False 
                    elif self.board[r, i][0] == self.board[r, c][0]: 
                        other_piece = False

        return moves        
        
    def get_knight_moves(self, r, c, moves):
        if (r + 2 <= 7) and (c + 1 <= 7):
            if self.board[r + 2, c + 1][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r+2, c+1), self.board)) 
        if (r + 2 <= 7) and (c - 1 >= 0):
            if self.board[r + 2, c - 1][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r+2, c-1), self.board))
        if (r - 2 >= 0) and (c + 1 <= 7):
            if self.board[r - 2, c + 1][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r-2, c+1), self.board))  
        if (r - 2 >= 0) and (c - 1 >= 0):
            if self.board[r - 2, c - 1][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r-2, c-1), self.board)) 
        if (r + 1 <= 7) and (c + 2 <= 7):
            if self.board[r + 1, c + 2][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r + 1, c+2), self.board)) 
        if (r + 1 <= 7) and (c - 2 >= 0):
            if self.board[r + 1, c - 2][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r+1, c-2), self.board))
        if (r - 1 >= 0) and (c + 2 <= 7):
            if self.board[r - 1, c + 2][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r-1, c+2), self.board))  
        if (r - 1 >= 0) and (c - 2 >= 0):
            if self.board[r - 1, c - 2][0] != self.board[r, c][0]:
                moves.append(Move((r, c), (r-1, c-2), self.board)) 
        return moves
            
    def get_bishop_moves(self, r, c, moves):
        pass
    def get_queen_moves(self, r, c, moves):
        pass
    def get_king_moves(self, r, c, moves):
        pass


    """check if move is valid (if a pawn moves, the king may be checkmate (if black moves, check moves for white)"""
    def get_valid_moves(self):
        return self.get_possible_moves() #no checks for now


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
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col


    """override the equals method"""
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
            
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
