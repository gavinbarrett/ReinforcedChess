from src.piece import Piece

class Rook(Piece):
	def __init__(self, code, promoted=False):
		super().__init__(code)
		self.value = 5
		self.has_moved = False
		self.promoted = promoted

	def get_proximity(self, game, piece_rank, piece_file):
		return [
			list(filter(game.board.in_bounds, [(piece_rank, piece_file - 1), (piece_rank, piece_file - 2), (piece_rank, piece_file - 3), (piece_rank, piece_file - 4), (piece_rank, piece_file - 5), (piece_rank, piece_file - 6), (piece_rank, piece_file - 7)])),
			list(filter(game.board.in_bounds, [(piece_rank, piece_file + 1), (piece_rank, piece_file + 2), (piece_rank, piece_file + 3), (piece_rank, piece_file + 4), (piece_rank, piece_file + 5), (piece_rank, piece_file + 6), (piece_rank, piece_file + 7)])),
			list(filter(game.board.in_bounds, [(piece_rank - 1, piece_file), (piece_rank - 2, piece_file), (piece_rank - 3, piece_file), (piece_rank - 4, piece_file), (piece_rank - 5, piece_file), (piece_rank - 6, piece_file), (piece_rank - 7, piece_file)])),
			list(filter(game.board.in_bounds, [(piece_rank + 1, piece_file), (piece_rank + 2, piece_file), (piece_rank + 3, piece_file), (piece_rank + 4, piece_file), (piece_rank + 5, piece_file), (piece_rank + 6, piece_file), (piece_rank + 7, piece_file)])),
		]
	
	def valid_moves(self, game, piece_rank, piece_file):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		move_set = self.get_proximity(game, piece_rank, piece_file)
		moves = []
		for move in move_set:
			moves.extend(self.check_path(game.board, move))
		return moves

	def move(self, board, piece_rank, piece_file, dest_rank, dest_file):
		# swap pieces
		board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
		# capture piece
		if board.data[piece_rank][piece_file].code:
			board.data[piece_rank][piece_file] = Piece(0)
		self.has_moved = True

	def can_move(self, game, piece_rank, piece_file, dest_rank, dest_file):
		if not game.board.in_bounds((dest_rank, dest_file)): return False
		# return all valid moves
		move_list = self.valid_moves(game, piece_rank, piece_file)
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