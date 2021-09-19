from src.piece import Piece

class Rook(Piece):
    def __init__(self, code):
        super().__init__(code)
    def can_move(self, board, piece_idx, dest_idx):
        ''' FIXME: determine whether or not piece_idx can move onto dest_idx
            We need to ensure:
                1) piece_idx and dest_idx correspond to indices in the board array
                2) the move is in the particular piece's moveset
                3) the space is either empty or contains an opponent's piece
        '''
        return True