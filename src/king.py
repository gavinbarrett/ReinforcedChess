from src.piece import Piece

class King(Piece):
	def __init__(self, code):
		super().__init__(code)
		self.has_moved = False
		self.in_check = False

	def get_proximity(self, game, piece_rank, piece_file):
		return list(filter(game.board.in_bounds, [
			(piece_rank - 1, piece_file - 1), (piece_rank - 1, piece_file), (piece_rank - 1, piece_file + 1),
			(piece_rank, piece_file - 1), (piece_rank, piece_file + 1),
			(piece_rank + 1, piece_file - 1), (piece_rank + 1, piece_file), (piece_rank + 1, piece_file + 1),
		]))

	def valid_moves(self, game, piece_rank, piece_file):
		# return set of valid moves (diagonals and forward position); include next forward space if first move
		move_set = self.get_proximity(game, piece_rank, piece_file)
		moves = []
		for move in move_set:
			target = game.board.data[move[0]][move[1]]
			if not target.code or (target.code and self.is_opponent(target)):
				moves.append((move[0], move[1]))
		# check for castling
		moves += self.can_castle(game, piece_rank, piece_file)
		return moves

	def checkable(self, game, piece_rank, piece_file):
		# compute the attack area of the opponent's pieces and determine if our king would get checked at location (piece_rank, piece_file)
		attacks = []
		if self.color == 0:
			# white is current player; generate the attack surface of black's pieces
			for blk_piece in game.board.blk_pieces:
				piece = game.board.data[blk_piece[0]][blk_piece[1]]
				ms = piece.valid_moves(game, blk_piece[0], blk_piece[1])
				attacks += ms
		elif self.color == 1:
			# black is current player; generate the attack surface of white's pieces
			for wht_piece in game.board.wht_pieces:
				piece = game.board.data[wht_piece[0]][wht_piece[1]]
				ms = piece.valid_moves(game, wht_piece[0], wht_piece[1])
				attacks += ms
		attacks = list(set(attacks))
		return (piece_rank, piece_file) in attacks

	def can_castle(self, game, piece_rank, piece_file):
		current_piece = game.board.data[piece_rank][piece_file]
		castles = []
		if self.color == 0:
			# make sure (piece_rank, piece_file) is in position, is an unmoved king, isn't in check, has two empty spaces between it and an original unmoved rook
			if current_piece.code == 5 and not current_piece.has_moved and not current_piece.in_check:
				# white king
				k_rook = game.board.data[piece_rank][piece_file + 3] if game.board.in_bounds((piece_rank, piece_file + 3)) else None
				q_rook = game.board.data[piece_rank][piece_file - 4] if game.board.in_bounds((piece_rank, piece_file - 4)) else None
				if k_rook and k_rook.code == 1 and not k_rook.has_moved and not k_rook.promoted:
					# check spaces between king and kingside rook
					if not game.board.data[piece_rank][piece_file + 1].code and not game.board.data[piece_rank][piece_file + 2].code:
						if not self.checkable(game, piece_rank, piece_file + 1) and not self.checkable(game, piece_rank, piece_file + 2):
							castles += [(piece_rank, piece_file + 2)]
				if q_rook and q_rook.code == 1 and not q_rook.has_moved and not q_rook.promoted:
					# check spaces between king and queenside rook
					if not game.board.data[piece_rank][piece_file - 1].code and not game.board.data[piece_rank][piece_file - 2].code and not game.board.data[piece_rank][piece_file - 3].code:
						if not self.checkable(game, piece_rank, piece_file - 1) and not self.checkable(game, piece_rank, piece_file - 2):
							castles += [(piece_rank, piece_file - 2)]
		elif self.color == 1:
			# make sure (piece_rank, piece_file) is in position, is an unmoved king, isn't in check, has two empty spaces between it and an original unmoved rook
			if current_piece.code == 11 and not current_piece.has_moved and not current_piece.in_check:
				# black king
				k_rook = game.board.data[piece_rank][piece_file + 3] if game.board.in_bounds((piece_rank, piece_file + 3)) else None
				q_rook = game.board.data[piece_rank][piece_file - 4] if game.board.in_bounds((piece_rank, piece_file - 4)) else None
				if k_rook and k_rook.code == 7 and not k_rook.has_moved and not k_rook.promoted:
					# check spaces between king and kingside rook
					if not game.board.data[piece_rank][piece_file + 1].code and not game.board.data[piece_rank][piece_file + 2].code:
						if not self.checkable(game, piece_rank, piece_file + 1) and not self.checkable(game, piece_rank, piece_file + 2):
							castles += [(piece_rank, piece_file + 2)]
				if q_rook and q_rook.code == 7 and not q_rook.has_moved and not q_rook.promoted:
					# check spaces between king and queenside rook
					if not game.board.data[piece_rank][piece_file - 1].code and not game.board.data[piece_rank][piece_file - 2].code and not game.board.data[piece_rank][piece_file - 3].code:
						if not self.checkable(game, piece_rank, piece_file - 1) and not self.checkable(game, piece_rank, piece_file - 2):
							castles += [(piece_rank, piece_file - 2)]
		return castles

	def move(self, board, piece_rank, piece_file, dest_rank, dest_file):
		# swap pieces
		board.data[piece_rank][piece_file], board.data[dest_rank][dest_file] = board.data[dest_rank][dest_file], board.data[piece_rank][piece_file]
		# check for castling scenario
		if (abs(piece_file - dest_file) == 2):
			# player is castling
			if (piece_rank, piece_file) == (7, 4) and (dest_rank, dest_file) == (7, 6):
				# white king is castling kingside
				board.data[7][5], board.data[7][7] = board.data[7][7], board.data[7][5]
			elif (piece_rank, piece_file) == (7, 4) and (dest_rank, dest_file) == (7, 2):
				# white king is castling queenside
				board.data[7][0], board.data[7][3] = board.data[7][3], board.data[7][0]
			elif (piece_rank, piece_file) == (0, 4) and (dest_rank, dest_file) == (0, 2):
				# black king is castling kingside
				board.data[0][0], board.data[0][3] = board.data[0][3], board.data[0][0]
			elif (piece_rank, piece_file) == (0, 4) and (dest_rank, dest_file) == (0, 6):
				# black king is castling queenside
				board.data[0][7], board.data[0][5] = board.data[0][5], board.data[0][7]
		# capture opponent piece
		if board.data[piece_rank][piece_file].code:
			board.data[piece_rank][piece_file] = Piece(0)
		# set moved flag
		self.has_moved = True

	def can_move(self, game, piece_rank, piece_file, dest_rank, dest_file):
		if not game.board.in_bounds((dest_rank, dest_file)): return False
		# determine valid move list
		move_list = self.valid_moves(game, piece_rank, piece_file)
		not_checkable = []
		for move in move_list:
			if not self.checkable(game, move[0], move[1]):
				not_checkable.append(move)
		return (dest_rank, dest_file) in move_list