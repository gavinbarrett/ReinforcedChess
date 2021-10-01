from src.piece import Piece

class Knight(Piece):
    def __init__(self, code):
        super().__init__(code)
        self.value = 3

    def get_proximity(self, game, piece_rank, piece_file):
        ''' Return the valid move indices for the knight '''
        return list(filter(game.board.in_bounds, [
            (piece_rank - 2, piece_file - 1), (piece_rank - 1, piece_file - 2),
            (piece_rank - 2, piece_file + 1), (piece_rank - 1, piece_file + 2),
            (piece_rank + 2, piece_file - 1), (piece_rank + 1, piece_file - 2),
            (piece_rank + 2, piece_file + 1), (piece_rank + 1, piece_file + 2),
        ]))

    def move(self, board, piece_rank, piece_file, dest_rank, dest_file):
        ''' Move the knight onto the destination tile '''
        # swap pieces
        board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
        # capture piece
        if board.data[piece_rank][piece_file].code:
            board.data[piece_rank][piece_file] = Piece(0)

    def can_move(self, game, piece_rank, piece_file, dest_rank, dest_file):
        ''' Return True if the piece can move onto the specified space '''
        if not game.board.in_bounds((dest_rank, dest_file)): return False
        move_list = self.valid_moves(game, piece_rank, piece_file)
        if (dest_rank, dest_file) in move_list:
            if self.is_opponent(game.board.data[dest_rank][dest_file]) or not game.board.data[dest_rank][dest_file].code:
                return True
        return False