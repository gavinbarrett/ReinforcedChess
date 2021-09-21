from src.piece import Piece

class Bishop(Piece):
	def __init__(self, code):
		super().__init__(code)

	def get_proximity(self, piece_file, piece_rank):
		return [
			[(piece_rank - 1, piece_file - 1), (piece_rank - 2, piece_file - 2), (piece_rank - 3, piece_file - 3), (piece_rank - 4, piece_file - 4), (piece_rank - 5, piece_file - 5), (piece_rank - 6, piece_file - 6), (piece_rank - 7, piece_file - 7)],
			[(piece_rank - 1, piece_file + 1), (piece_rank - 2, piece_file + 2), (piece_rank - 3, piece_file + 3), (piece_rank - 4, piece_file + 4), (piece_rank - 5, piece_file + 5), (piece_rank - 6, piece_file + 6), (piece_rank - 7, piece_file + 7)],
			[(piece_rank + 1, piece_file - 1), (piece_rank + 2, piece_file - 2), (piece_rank + 3, piece_file - 3), (piece_rank + 4, piece_file - 4), (piece_rank + 5, piece_file - 5), (piece_rank + 6, piece_file - 6), (piece_rank + 7, piece_file - 7)],
			[(piece_rank + 1, piece_file + 1), (piece_rank + 2, piece_file + 2), (piece_rank + 3, piece_file + 3), (piece_rank + 4, piece_file + 4), (piece_rank + 5, piece_file + 5), (piece_rank + 6, piece_file + 6), (piece_rank + 7, piece_file + 7)]
		]

	def valid_moves(self, board, piece_file, piece_rank):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		move_set = self.get_proximity(piece_file, piece_rank)
		moves = [list(filter(board.in_bounds, move_set[0]))]
		moves.append(list(filter(board.in_bounds, move_set[1])))
		moves.append(list(filter(board.in_bounds, move_set[2])))
		moves.append(list(filter(board.in_bounds, move_set[3])))
		return moves

	def move(self, board, piece_file, piece_rank, dest_file, dest_rank):
		# swap pieces
		board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
		# capture piece
		if board.data[piece_rank][piece_file].code:
			board.data[piece_rank][piece_file] = Piece(0)

	def can_move(self, game, piece_file, piece_rank, dest_file, dest_rank):
		if not game.board.data[dest_rank][dest_file]: return False
		move_list = self.valid_moves(game.board, piece_file, piece_rank)
		dest_idx = (dest_rank, dest_file)
		if dest_idx in move_list[0]:
			return self.check_path(game.board, move_list[0], dest_idx)
		elif dest_idx in move_list[1]:
			return self.check_path(game.board, move_list[1], dest_idx)
		elif dest_idx in move_list[2]:
			return self.check_path(game.board, move_list[2], dest_idx)
		elif dest_idx in move_list[3]:
			return self.check_path(game.board, move_list[3], dest_idx)
		return False

	def check_path(self, board, move_list, dest_idx):
		# iterate through list, add to path until we reach an inhabited spot. If that spot is occupied by an opp, we can land there too; if the space is occupied by an ally piece, cannot move onto tile
		for move in move_list:
			other_piece = board.data[move[0]][move[1]]
			if move == dest_idx:
				if not other_piece.code:
					return True
				else:
					if self.is_opponent(other_piece):
						return True
					else:
						return False
			elif not other_piece.code:
				continue
			else:
				return False