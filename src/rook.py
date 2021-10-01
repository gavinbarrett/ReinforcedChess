from src.piece import Piece

class Rook(Piece):
	def __init__(self, code, position, promoted=False):
		super().__init__(code, position)
		self.value = 5
		self.has_moved = False
		self.promoted = promoted

	def get_proximity(self, game):
		rank, file_ = self.rank, self.file_
		return [
			list(filter(game.board.in_bounds, [(rank, file_ - 1), (rank, file_ - 2), (rank, file_ - 3), (rank, file_ - 4), (rank, file_ - 5), (rank, file_ - 6), (rank, file_ - 7)])),
			list(filter(game.board.in_bounds, [(rank, file_ + 1), (rank, file_ + 2), (rank, file_ + 3), (rank, file_ + 4), (rank, file_ + 5), (rank, file_ + 6), (rank, file_ + 7)])),
			list(filter(game.board.in_bounds, [(rank - 1, file_), (rank - 2, file_), (rank - 3, file_), (rank - 4, file_), (rank - 5, file_), (rank - 6, file_), (rank - 7, file_)])),
			list(filter(game.board.in_bounds, [(rank + 1, file_), (rank + 2, file_), (rank + 3, file_), (rank + 4, file_), (rank + 5, file_), (rank + 6, file_), (rank + 7, file_)])),
		]
	
	def valid_moves(self, game):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		move_set = self.get_proximity(game)
		moves = []
		for move in move_set:
			moves.extend(self.check_path(game.board, move))
		return moves

	def move(self, board, dest_rank, dest_file):
		rank, file_ = self.rank, self.file_
		# swap pieces
		board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
		# capture piece
		if board.data[rank][file_].code:
			board.data[rank][file_] = Piece(0, (rank * 8) + file_)
		# update piece coordinates
		self.rank = dest_rank
		self.file_ = dest_file
		# set piece as having moved
		self.has_moved = True

	def can_move(self, game, dest_rank, dest_file):
		if not game.board.in_bounds((dest_rank, dest_file)): return False
		# return all valid moves
		move_list = self.valid_moves(game)
		# check if the piece can move to the destination
		return (dest_rank, dest_file) in move_list
	
	def check_path(self, board, move_list):
		moves = []
		for move in list(filter(board.in_bounds, move_list)):
			other_piece = board.data[move[0]][move[1]]
			if not other_piece.code:
				moves.append(move)
			elif other_piece.code and self.is_opponent(other_piece):
				moves.append(move)
				return moves
			else:
				return moves
		return moves