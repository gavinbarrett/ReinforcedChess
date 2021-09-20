from src.piece import Piece
from src.bishop import Bishop
from src.knight import Knight
from src.queen import Queen
from src.rook import Rook

class Pawn(Piece):
	def __init__(self, code):
		super().__init__(code)
		self.has_moved = False
	
	def promote(self, board, dest_idx):
		promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		while promotion not in ['Q', 'R', 'B', 'N']:
			promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		if promotion == 'Q':
			if self.color == 0:
				board[dest_idx] = Queen(4)
			elif self.color == 1:
				board[dest_idx] = Queen(10)
		elif promotion == 'R':
			if self.color == 0:
				board[dest_idx] = Rook(1)
			elif self.color == 1:
				board[dest_idx] = Rook(7)
		elif promotion == 'B':
			if self.color == 0:
				board[dest_idx] = Bishop(3)
			elif self.color == 1:
				board[dest_idx] = Bishop(9)
		elif promotion == 'N':
			if self.color == 0:
				board[dest_idx] = Knight(2)
			elif self.color == 1:
				board[dest_idx] = Knight(8)

	def get_proximity(self, piece_idx):
		''' Return the valid indices for the pawn, depending on class and location '''
		# white piece orientation
		if self.color == 0:
			if not piece_idx % 8:
				# piece is on the left edge of the board
				return [piece_idx - 7, piece_idx - 8, piece_idx - 16] if not self.has_moved else [piece_idx - 7, piece_idx - 8]
			elif piece_idx % 8 == 7:
				# piece is on the right edge of the board
				return [piece_idx - 8, piece_idx - 9, piece_idx - 16] if not self.has_moved else [piece_idx - 8, piece_idx - 9]
			return [piece_idx - 9, piece_idx - 8, piece_idx - 7, piece_idx - 16] if not self.has_moved else [piece_idx - 9, piece_idx - 8, piece_idx - 7]
		# black piece orientation
		elif self.color == 1:
			if not piece_idx % 8:
				# piece is on the left edge of the board
				return [piece_idx + 8, piece_idx + 9, piece_idx + 16] if not self.has_moved else [piece_idx + 8, piece_idx + 9]
			elif piece_idx % 8 == 7:
				# piece is on the right edge of the board
				return [piece_idx + 7, piece_idx + 8, piece_idx + 16] if not self.has_moved else [piece_idx + 7, piece_idx + 8]
			return [piece_idx + 7, piece_idx + 8, piece_idx + 9, piece_idx + 16] if not self.has_moved else [piece_idx + 7, piece_idx + 8, piece_idx + 9]

	def valid_moves(self, board, piece_idx):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		return list(filter(board.in_bounds, self.get_proximity(piece_idx)))

	def move(self, board, piece_idx, dest_idx):
		''' Move pawn to position. Capture opponents on diagonal tiles, or adjacent tiles if using en passant '''
		if self.color == 1:
			if piece_idx + 8 == dest_idx or piece_idx + 16 == dest_idx:
				# piece is being moved forward; swap pieces
				board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
			else:
				# pawn is capturing
				if board.array[dest_idx].code:
					# normal capture; swap pieces
					board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
					# delete old piece
					board.array[piece_idx] = Piece(0)
				else:
					# en passant capture
					board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
					board.array[dest_idx - 8] = Piece(0)
			# FIXME: if pawn gets to other side (lands on a tile 55 < x < 64), it can be promoted
			# promote the black pieces if they reach the other side
			if 55 < dest_idx < 64: self.promote(board.array, dest_idx)
		elif self.color == 0:
			if piece_idx - 8 == dest_idx or piece_idx - 16 == dest_idx:
				# piece is being moved forward
				board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
			else:
				# pawn is capturing
				if board.array[dest_idx].code:
					# normal capture; swap pieces
					board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
					# delete old piece
					board.array[piece_idx] = Piece(0)
				else:
					# en passant capture
					board.array[piece_idx], board.array[dest_idx] = board.array[dest_idx], board.array[piece_idx]
					board.array[dest_idx + 8] = Piece(0)
			# FIXME: if pawn gets to other side (lands on a tile 0 =< x < 8), it can be promoted
			# promote the black pieces if they reach the other side
			if 0 <= dest_idx < 8: self.promote(board.array, dest_idx)

	def can_move(self, board, last_move, piece_idx, dest_idx):
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
		if dest_idx in moves:
			if self.color == 1:
				# check for a move forward
				if piece_idx + 8 == dest_idx and not board.array[dest_idx].code:
					# pawn is trying to move one space forward and the space is clear
					return True
				elif piece_idx + 16 == dest_idx and not self.has_moved and not board.array[dest_idx].code and not board.array[piece_idx + 8].code:
					# pawn is trying to move two spaces forward and they're clear
					return True
				# check for a diagonal move; also check for the en passant scenario
				elif piece_idx + 9 == dest_idx:
					# try and move diagonally to the left
					if board.array[dest_idx].code and self.is_opponent(board.array[dest_idx]):
						# opponent piece can be captured
						return True
					elif not board.array[dest_idx].code and board.array[piece_idx + 1].code and self.is_opponent(board.array[piece_idx + 1] and last_move == piece_idx + 1):
						# opponent piece can be captured by en passant
						return True
				elif piece_idx + 7 == dest_idx:
					# try and move diagonally to the left
					if board.array[dest_idx].code and self.is_opponent(board.array[dest_idx]):
						# opponent piece can be captured
						return True
					elif not board.array[dest_idx].code and board.array[piece_idx - 1].code and self.is_opponent(board.array[piece_idx - 1] and (31 < dest_idx < 40) and last_move == piece_idx - 1): #FIXME: opp must be on rank 5
						# opponent piece can be captured by en passant
						return True
			elif self.color == 0:
				# check for a move forward
				if piece_idx - 8 == dest_idx and not board.array[dest_idx].code:
					# pawn is trying to move one space forward and the space is clear
					return True
				elif piece_idx - 16 == dest_idx and not self.has_moved and not board.array[dest_idx].code and not board.array[piece_idx - 8].code:
					# pawn is trying to move two spaces forward and 
					return True
				# check for a diagonal move; also check for the en passant scenario
				elif piece_idx - 9 == dest_idx:
					# try and move diagonally to the left
					if board.array[dest_idx].code and self.is_opponent(board.array[dest_idx]):
						# opponent piece can be captured
						return True
					elif not board.array[dest_idx].code and board.array[piece_idx - 1].code and self.is_opponent(board.array[piece_idx - 1]) and last_move == piece_idx - 1:
						# opponent piece can be captured by en passant
						return True
				elif piece_idx - 7 == dest_idx:
					# try and move diagonally to the left
					if board.array[dest_idx].code and self.is_opponent(board.array[dest_idx]):
						# opponent piece can be captured
						return True
					elif not board.array[dest_idx].code and board.array[piece_idx + 1].code and self.is_opponent(board.array[piece_idx + 1] and (39 < dest_idx < 48) and last_move == piece_idx + 1): # FIXME: opp must be on rank 4
						# opponent piece can be captured by en passant
						return True
		return False