from src.piece import Piece
from src.indices import Indices
from src.colors import BLUE, YELLOW, END

class Player:
	def __init__(self, color):
		self.color = color
		self.indices = Indices().idxs

	def get_move(self):
		''' Give input control to user (real or AI) '''
		src_piece = None
		dest_tile = None
		color = BLUE if self.color else YELLOW
		while src_piece not in self.indices:
			src_piece = input(f'What to move? {color}>{END} ')
		while dest_tile not in self.indices:
			dest_tile = input(f'Where to move? {color}>{END} ')
		return self.indices[src_piece], self.indices[dest_tile]