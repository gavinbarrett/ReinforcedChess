class Piece:
	def __init__(self, code):
		self.code = code
		if code == 0:
			# piece is an empty tile
			self.color = None
		elif code < 7:
			# piece is white
			self.color = 0
		elif code > 6:
			# piece is black
			self.color = 1

	def get_proximity(self, board, piece_file, piece_rank):
		return []

	def move(self, board, piece_file, piece_rank, dest_file, dest_rank):
		pass

	def can_move(self, game, piece_file, piece_rank, dest_file, dest_rank):
		pass

	def is_opponent(self, piece_2):
		''' Return true if other tile contains an opponent piece '''
		return piece_2.color != None and self.color != piece_2.color
	
	def valid_moves(self, game, piece_file, piece_rank):
		# return set of valid moves (diagonals and forward position); include next forward space if first move	
		return list(filter(game.board.in_bounds, self.get_proximity(game, piece_file, piece_rank)))