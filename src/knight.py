from src.piece import Piece

class Knight(Piece):
    def __init__(self, code, position):
        super().__init__(code, position)
        self.value = 3

    def get_proximity(self, game):
        ''' Return the valid move indices for the knight '''
        rank, file_ = self.rank, self.file_
        return list(filter(game.board.in_bounds, [
            (rank - 2, file_ - 1), (rank - 1, file_ - 2),
            (rank - 2, file_ + 1), (rank - 1, file_ + 2),
            (rank + 2, file_ - 1), (rank + 1, file_ - 2),
            (rank + 2, file_ + 1), (rank + 1, file_ + 2),
        ]))

    def move(self, board, dest_rank, dest_file):
        ''' Move the knight onto the destination tile '''
        rank, file_ = self.rank, self.file_
        # swap pieces
        board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
        # capture piece
        if board.data[rank][file_].code:
            board.data[rank][file_] = Piece(0, (rank * 8) + file_)
        # update coordinates
        self.rank = dest_rank
        self.file_ = dest_file

    def can_move(self, game, dest_rank, dest_file):
        ''' Return True if the piece can move onto the specified space '''
        if not game.board.in_bounds((dest_rank, dest_file)): return False
        move_list = self.valid_moves(game)
        if (dest_rank, dest_file) in move_list:
            if self.is_opponent(game.board.data[dest_rank][dest_file]) or not game.board.data[dest_rank][dest_file].code:
                return True
        return False