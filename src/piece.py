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

	def can_move(self, board, piece_idx, dest_idx):
		pass

	def is_opponent(self, piece_2):
		''' Return true if other tile contains an opponent piece '''
		return piece_2.color != None and self.color != piece_2.color