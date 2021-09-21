from src.piece import Piece

class Knight(Piece):
    def __init__(self, code):
        super().__init__(code)

    def get_proximity(self, piece_file, piece_rank):
        ''' Return the valid move indices for the knight '''
        return [
            (piece_rank - 2, piece_file - 1), (piece_rank - 1, piece_file - 2),
            (piece_rank - 2, piece_file + 1), (piece_rank - 1, piece_file + 2),
            (piece_rank + 2, piece_file - 1), (piece_rank + 1, piece_file - 2),
            (piece_rank + 2, piece_file + 1), (piece_rank + 1, piece_file + 2),
        ]

    def move(self, board, piece_file, piece_rank, dest_file, dest_rank):
        ''' Move the knight onto the destination tile '''
        # swap pieces
        board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
        # capture piece
        board.data[piece_rank][piece_file] = Piece(0)

    def can_move(self, game, piece_file, piece_rank, dest_file, dest_rank):
        ''' Return True if the piece can move onto the specified space '''
        if not game.board.in_bounds((dest_rank, dest_file)): return False
        move_list = self.valid_moves(game.board, piece_file, piece_rank)
        if (dest_rank, dest_file) in move_list:
            if self.is_opponent(game.board.data[dest_rank][dest_file]) or not game.board.data[dest_rank][dest_file].code:
                return True
        return False