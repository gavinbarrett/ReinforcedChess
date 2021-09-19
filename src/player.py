from src.piece import Piece
from src.indices import Indices
from src.colors import BLUE, YELLOW, END

class Player:
	def __init__(self, color):
		self.color = color
		self.indices = Indices().idxs

	def get_move(self):
		''' Give input control to user (real or AI) '''
		p = 'x'
		move = 'x'
		color = YELLOW if self.color else BLUE
		while p not in self.indices:
			p = input(f'What piece to move? {color}>{END} ')
		while move not in self.indices:
			move = input(f'Where to move? {color}>{END} ')
		return self.indices[p], self.indices[move]
	
	def make_move(self, board, piece_idx, dest_idx):
		if not board[dest_idx].code:
			# piece is an empty tile; simply swap the pieces
			board[piece_idx], board[dest_idx] = board[dest_idx], board[piece_idx]
		else:
			# swap pieces
			board[piece_idx], board[dest_idx] = board[dest_idx], board[piece_idx]
			# capture the opponent's piece
			board[piece_idx] = Piece(0)