from src.piece import Piece
from src.bishop import Bishop
from src.knight import Knight
from src.queen import Queen
from src.rook import Rook

class Pawn(Piece):
	def __init__(self, code):
		super().__init__(code)
		self.has_moved = False
		self.passing = False
	
	def promote(self, board, piece_idx):
		promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		while promotion not in ['Q', 'R', 'B', 'N']:
			promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		if promotion == 'Q':
			if self.color == 0:
				board[piece_idx] = Queen(4)
			elif self.color == 1:
				board[piece_idx] = Queen(10)
		elif promotion == 'R':
			if self.color == 0:
				board[piece_idx] = Rook(1)
			elif self.color == 1:
				board[piece_idx] = Rook(7)
		elif promotion == 'B':
			if self.color == 0:
				board[piece_idx] = Bishop(3)
			elif self.color == 1:
				board[piece_idx] = Bishop(9)
		elif promotion == 'N':
			if self.color == 0:
				board[piece_idx] = Knight(2)
			elif self.color == 1:
				board[piece_idx] = Knight(8)

	def get_proximity(self, piece_idx):
		''' Return the valid indices for the pawn, depending on class and location '''
		# white piece orientation
		if self.color == 0:
			if not piece_idx % 8:
				# piece is on the left edge of the board
				return [piece_idx - 7, piece_idx - 8, piece_idx - 16]
			elif piece_idx % 8 == 7:
				# piece is on the right edge of the board
				return [piece_idx - 8, piece_idx - 9, piece_idx - 16]
			return [piece_idx - 9, piece_idx - 8, piece_idx - 7, piece_idx - 16]
				# black piece orientation
		elif self.color == 1:
			if not piece_idx % 8:
				# piece is on the left edge of the board
				return [piece_idx + 8, piece_idx + 9, piece_idx + 16]
			elif piece_idx % 8 == 7:
				# piece is on the right edge of the board
				return [piece_idx + 7, piece_idx + 8, piece_idx + 16]
			return [piece_idx + 7, piece_idx + 8, piece_idx + 9, piece_idx + 16]

	def valid_moves(self, board, piece_idx):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		return list(filter(board.in_bounds, self.get_proximity(piece_idx)))

	def can_move(self, board, piece_idx, dest_idx):
		''' FIXME: determine whether or not piece_idx can move onto dest_idx
			We need to ensure:
				1) piece_idx and dest_idx correspond to indices in the board array
				2) the move is in the particular piece's moveset
				3) the space is either empty or contains an opponent's piece
			Make sure the index is somewhere on the board.
			For a pawn, we either want to move two spaces forward, one space forward, or a space diagonally
			We can only move to an empty diagonal space if we're performing en passant
		'''
		# check that the destination index is in bounds of the array
		# then, check that it is either:
			# 1) directly in front of the pawn (move)
				# if it's the player's first move, allow them to either move one or two steps, as long as there is no piece along the path
				# otherwise, allow them to move one space forward, provided it is not occupies by another piece
			# 2) diagonal to the pawn (capture)

		# check if the destination index falls outside of the board
		if not board.in_bounds(dest_idx): return False
		# get moveset for pawns
		moves = self.valid_moves(board, piece_idx)
		print(moves)
		#if dest_idx in moves:
			# check for a move forward

			# check for a diagonal move; also check for the en passant scenario
		return True