from src.piece import Piece
from src.bishop import Bishop
from src.knight import Knight
from src.queen import Queen
from src.rook import Rook

class Pawn(Piece):
	def __init__(self, code):
		super().__init__(code)
	
	def promote(self, board, dest_rank, dest_file):
		promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		while promotion not in ['Q', 'R', 'B', 'N']:
			promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		if promotion == 'Q':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Queen(4)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Queen(10)
		elif promotion == 'R':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Rook(1)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Rook(7)
		elif promotion == 'B':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Bishop(3)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Bishop(9)
		elif promotion == 'N':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Knight(2)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Knight(8)

	def get_proximity(self, piece_file, piece_rank):
		''' Return the valid move indices for the pawn '''
		if self.color == 1:
			neighbors = [(piece_rank + 1, piece_file), (piece_rank + 1, piece_file - 1), (piece_rank + 1, piece_file + 1)]
			if piece_rank == 1: neighbors.append((piece_rank + 2, piece_file))
			return neighbors
		elif self.color == 0:
			neighbors = [(piece_rank - 1, piece_file), (piece_rank - 1, piece_file - 1), (piece_rank - 1, piece_file + 1)]
			if piece_rank == 6: neighbors.append((piece_rank - 2, piece_file))
			return neighbors

	def move(self, board, piece_file, piece_rank, dest_file, dest_rank):
		''' Move pawn to position. Capture opponents on diagonal tiles, or adjacent tiles if using en passant '''
		if self.color == 1:
			if piece_file == dest_file:
				# move pawn
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
			elif board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
				# capture opponent piece
				board.data[piece_rank][piece_file] = Piece(0)
			elif not board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
				# en passant capture
				board.data[piece_rank][dest_file] = Piece(0)
			if dest_rank == 7: self.promote(board, dest_rank, dest_file)
		elif self.color == 0:
			if piece_file == dest_file:
				# move pawn
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
			elif board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
				# capture opponent piece
				board.data[piece_rank][piece_file] = Piece(0)
			elif not board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
				# en passant capture
				board.data[piece_rank][dest_file] = Piece(0)
			if dest_rank == 0: self.promote(board, dest_rank, dest_file)

	def can_move(self, game, piece_file, piece_rank, dest_file, dest_rank):
		''' Return True if the piece can move onto the specified space '''
		# check if the destination index falls outside of the board
		if not game.board.in_bounds((dest_rank, dest_file)): return False
		# get list of valid moves
		move_list = self.valid_moves(game.board, piece_file, piece_rank)
		if (dest_rank, dest_file) in move_list:
			if self.color == 1:
				if piece_file == dest_file:
					# pawn is moving forward
					if piece_rank + 1 == dest_rank and not game.board.data[dest_rank][dest_file].code:
						return True
					elif piece_rank + 2 == dest_rank and not game.board.data[dest_rank][dest_file].code and not game.board.data[piece_rank + 1][dest_file].code:
						# pawn is moving two spaces forward
						return True
				else:
					# pawn is moving diagonally to capture
					other_piece = game.board.data[dest_rank][dest_file]
					if other_piece.code and self.is_opponent(other_piece):
						return True
					elif not other_piece.code and self.is_opponent(game.board.data[piece_rank][dest_file]) and game.board.data[piece_rank][dest_file].code == 6 and game.last_move == (piece_rank, dest_file):
						# en passant
						return True
			elif self.color == 0:
				if piece_file == dest_file:
					# pawn is moving forward
					if piece_rank - 1 == dest_rank and not game.board.data[dest_rank][dest_file].code:
						return True
					elif piece_rank - 2 == dest_rank and not game.board.data[dest_rank][dest_file].code and not game.board.data[piece_rank - 1][dest_file].code:
						# pawn is moving two spaces forward
						return True
				else:
					# pawn is moving diagonally to capture
					other_piece = game.board.data[dest_rank][dest_file]
					if other_piece.code and self.is_opponent(other_piece):
						return True
					elif not other_piece.code and self.is_opponent(game.board.data[piece_rank][dest_file]) and game.board.data[piece_rank][dest_file].code == 12 and game.last_move == (piece_rank, dest_file):
						# en passant
						return True
		return False