from src.game_state.coords import compute_coord

class Piece:
	def __init__(self, code, position):
		self.code = code
		self.rank, self.file_ = compute_coord(position)
		if code == 0:
			# piece is an empty tile
			self.color = None
		elif code < 7:
			# piece is white
			self.color = 0
		elif code > 6:
			# piece is black
			self.color = 1

	def get_proximity(self, board):
		''' Return coordinates of neighbors '''
		return []

	def move(self, board, dest_rank, dest_file):
		''' Move or capture piece (dest_rank, dest_file) with (piece_rank, piece_file) '''
		pass

	def can_move(self, game, dest_rank, dest_file):
		''' Return True if piece (piece_rank, piece_file) can move to (dest_rank, dest_file) '''
		pass

	def is_opponent(self, piece_2):
		''' Return True if other tile contains an opponent piece '''
		return piece_2.color != None and self.color != piece_2.color
	
	def valid_moves(self, game):
		''' Return set of valid moves '''	
		return list(filter(game.board.in_bounds, self.get_proximity(game)))