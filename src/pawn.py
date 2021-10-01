from src.piece import Piece
from src.bishop import Bishop
from src.knight import Knight
from src.queen import Queen
from src.rook import Rook

class Pawn(Piece):
	def __init__(self, code, position):
		super().__init__(code, position)
		self.value = 1
	
	def promote(self, board, dest_rank, dest_file):
		promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		while promotion not in ['Q', 'R', 'B', 'N']:
			promotion = input('How would you like to promote your pawn?\n(Q)ueen, (R)ook, (B)ishop, or K(N)ight? ')
		if promotion == 'Q':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Queen(4, (dest_rank * 8) + dest_file)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Queen(10, (dest_rank * 8) + dest_file)
		elif promotion == 'R':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Rook(1, (dest_rank * 8) + dest_file, True)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Rook(7, (dest_rank * 8) + dest_file, True)
		elif promotion == 'B':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Bishop(3, (dest_rank * 8) + dest_file)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Bishop(9, (dest_rank * 8) + dest_file)
		elif promotion == 'N':
			if self.color == 0:
				board.data[dest_rank][dest_file] = Knight(2, (dest_rank * 8) + dest_file)
			elif self.color == 1:
				board.data[dest_rank][dest_file] = Knight(8, (dest_rank * 8) + dest_file)

	def get_proximity(self, game):
		''' Return the valid move indices for the pawn '''
		rank, file_ = self.rank, self.file_
		length = len(game.board.data)
		if self.color == 1:
			# add first tile before it
			neighbors = [(rank + 1, file_)]
			# pawn's first move; add second tile before it
			if rank == 1: neighbors.append((rank + 2, file_))
			if 0 <= rank + 1 < length and 0 <= file_ + 1 < length:
				left_diag = game.board.data[rank + 1][file_ + 1]
				# add left diagonal tile
				if left_diag.code and self.is_opponent(left_diag):
					neighbors.append((rank + 1, file_ + 1))
				# en passant case
				elif not left_diag.code and self.is_opponent(game.board.data[rank][file_ + 1]) and game.last_move == (rank, file_ + 1) and rank == 4:
					neighbors.append((rank + 1, file_ + 1))
			if 0 <= rank + 1 < length and 0 <= file_ - 1 < length:
				right_diag = game.board.data[rank + 1][file_ - 1]
				# add right diagonal tile
				if right_diag.code and self.is_opponent(right_diag):
					neighbors.append((rank + 1, file_ - 1))
				# en passant case
				elif not right_diag.code and self.is_opponent(game.board.data[rank][file_ - 1]) and game.last_move == (rank, file_ - 1) and rank == 4:
					neighbors.append((rank + 1, file_ - 1))
			return list(filter(game.board.in_bounds, neighbors))
		elif self.color == 0:
			neighbors = [(rank - 1, file_)]
			if rank == 6: neighbors.append((rank - 2, file_))
			if 0 <= rank - 1 < length and 0 <= file_ - 1 < length:
				left_diag = game.board.data[rank - 1][file_ - 1]
				# add left diagonal tile
				if left_diag.code and self.is_opponent(left_diag):
					neighbors.append((rank - 1, file_ - 1))
				# en passant case
				elif not left_diag.code and self.is_opponent(game.board.data[rank][file_ - 1]) and game.last_move == (rank, file_ - 1) and rank == 3:
					neighbors.append((rank - 1, file_ - 1))
			if 0 <= rank - 1 < length and 0 <= file_ + 1 < length:
				right_diag = game.board.data[rank - 1][file_ + 1]
				# add right diagonal tile
				if right_diag.code and self.is_opponent(right_diag):
					neighbors.append((rank - 1, file_ + 1))
				# en passant case
				elif not right_diag.code and self.is_opponent(game.board.data[rank][file_ + 1]) and game.last_move == (rank, file_ + 1) and rank == 3:
					neighbors.append((rank - 1, file_ + 1))
			return list(filter(game.board.in_bounds, neighbors))

	def move(self, board, dest_rank, dest_file):
		''' Move pawn to position. Capture opponents on diagonal tiles, or adjacent tiles if using en passant '''
		rank, file_ = self.rank, self.file_
		if self.color == 1:
			if file_ == dest_file:
				# move pawn
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
			elif board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
				# capture opponent piece
				board.data[rank][file_] = Piece(0, (rank * 8) + file_)
			elif not board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
				# en passant capture
				board.data[rank][dest_file] = Piece(0, (rank * 8) + dest_file)
			# check for promotion
			if dest_rank == 7: self.promote(board, dest_rank, dest_file)
		elif self.color == 0:
			if file_ == dest_file:
				# move pawn
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
			elif board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
				# capture opponent piece
				board.data[rank][file_] = Piece(0, (rank * 8) + file_)
			elif not board.data[dest_rank][dest_file].code:
				# swap pieces
				board.data[rank][file_], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[rank][file_]
				# en passant capture
				board.data[rank][file_] = Piece(0, (rank * 8) + file_)
			# check for promotion
			if dest_rank == 0: self.promote(board, dest_rank, dest_file)
			# update piece coordinates
		self.rank = dest_rank
		self.file_ = dest_file

	def can_move(self, game, dest_rank, dest_file):
		''' Return True if the piece can move onto the specified space '''
		# check if the destination index falls outside of the board
		if not game.board.in_bounds((dest_rank, dest_file)): return False
		rank, file_ = self.rank, self.file_
		# get list of valid moves
		move_list = self.valid_moves(game)
		if (dest_rank, dest_file) in move_list:
			if self.color == 1:
				if file_ == dest_file:
					# pawn is moving forward
					if rank + 1 == dest_rank and not game.board.data[dest_rank][dest_file].code:
						return True
					elif rank + 2 == dest_rank and not game.board.data[dest_rank][dest_file].code and not game.board.data[rank + 1][dest_file].code:
						# pawn is moving two spaces forward
						return True
				else:
					# pawn is moving diagonally to capture
					other_piece = game.board.data[dest_rank][dest_file]
					if other_piece.code and self.is_opponent(other_piece):
						return True
					elif not other_piece.code and self.is_opponent(game.board.data[rank][dest_file]) and game.board.data[rank][dest_file].code == 6 and game.last_move == (rank, dest_file):
						# en passant
						return True
			elif self.color == 0:
				if file_ == dest_file:
					# pawn is moving forward
					if rank - 1 == dest_rank and not game.board.data[dest_rank][dest_file].code:
						return True
					elif rank - 2 == dest_rank and not game.board.data[dest_rank][dest_file].code and not game.board.data[rank - 1][dest_file].code:
						# pawn is moving two spaces forward
						return True
				else:
					# pawn is moving diagonally to capture
					other_piece = game.board.data[dest_rank][dest_file]
					if other_piece.code and self.is_opponent(other_piece):
						return True
					elif not other_piece.code and self.is_opponent(game.board.data[rank][dest_file]) and game.board.data[rank][dest_file].code == 12 and game.last_move == (rank, dest_file):
						# en passant
						return True
		return False