from copy import deepcopy
from src.board import Board
from src.coords import compute_coord

class Game:
	def __init__(self, player_1, player_2, board):
		if not ((player_1.color == 0 and  player_2.color == 1) or (player_1.color == 1 and player_2.color == 0)):
			raise ValueError('Incorrect player enumeration.')
		self.board = board
		self.player = 0
		self.players = [player_1, player_2]
		self.last_move = None
		self.winner = None
	
	def play(self):
		''' Run the chess game '''
		# look for checks
		self.board.find_check(self)
		while not self.is_over():
			# display board
			self.display()
			# turn control to user; receive input
			piece_rank, piece_file, dest_rank, dest_file = self.get_move()
			# move piece
			self.execute_move(piece_rank, piece_file, dest_rank, dest_file)
			# look for checks
			self.board.find_check(self)
		# print endgame board state
		self.display()
		if self.winner == 0 or self.winner == 1:
			if not self.winner:
				print(f'Black was checkmated!\nWhite won!')
			else:
				print(f'White was checkmated!\nBlack won!')
		else:
			print(f'Players reached a stalemate!')

	def display(self):
		''' Print out the board to CLI or send JSON payload to client '''
		print(self.board)

	def get_move(self):
		# prompt the user for a move
		piece_idx, dest_idx = self.players[self.player].get_move()
		# compute the file and rank of the source and destination pieces
		piece_rank, piece_file = compute_coord(piece_idx)
		dest_rank, dest_file = compute_coord(dest_idx)
		return piece_rank, piece_file, dest_rank, dest_file

	def execute_move(self, piece_rank, piece_file, dest_rank, dest_file):
		# grab current piece
		current_piece = self.board.data[piece_rank][piece_file]
		# check for a valid move
		if current_piece.color == self.players[self.player].color and current_piece.code and current_piece.can_move(self, dest_rank, dest_file):
			# move the piece
			current_piece.move(self.board, dest_rank, dest_file)
			# save previous move (for en passant)
			self.last_move = (dest_rank, dest_file)
			# update player pieces
			self.board.update_pieces()
			# find any checking scenario
			self.board.find_check(self)
			# alternate current player
			self.alternate_player()
		else:
			print(f'Could not perform move\n')

	def alternate_player(self):
		''' Alternate the current player '''
		self.player = (self.player + 1) % 2

	def checkmate(self, king, pieces):
		king_piece = self.board.data[king[0]][king[1]]
		if king_piece.in_check:
			# check if pieces can block or capture attacking pieces
			for piece in pieces:
				# pull piece from the board
				p = self.board.data[piece[0]][piece[1]]
				# retrieve the list of moves for that piece
				p_moves = p.valid_moves(self)
				# test every move the piece can make
				for p_move in p_moves:
					# copy the game state to test moves
					new_state = deepcopy(self)
					# pull new piece
					new_piece = new_state.board.data[piece[0]][piece[1]]
					# test move the piece in the new game state
					new_piece.move(new_state.board, p_move[0], p_move[1])					
					# check for king
					if new_piece.code in [5, 11]:
						# piece is a king that's now located at (p_move[0], p_move[1])
						new_king_piece = new_state.board.data[p_move[0]][p_move[1]]
						if not new_king_piece.checkable(new_state, p_move[0], p_move[1]):
							return False
					else:
						# piece is a king that's now located at (p_move[0], p_move[1])
						new_king_piece = new_state.board.data[king[0]][king[1]]
						# get the kings new moves after moving it
						new_moves = new_king_piece.valid_moves(new_state)
						for new_move in new_moves:
							check = new_king_piece.checkable(new_state, new_move[0], new_move[1])
							if not check:
								return False
			# no possible move allows the king to escape; king is checkmated
			return True
		# king is not in check
		return False
	
	def at_checkmate(self):
		checkmated = self.checkmate(self.board.blk_king, self.board.blk_pieces)
		if checkmated:
			self.winner = 0
		return checkmated
		checkmated = self.checkmate(self.board.wht_king, self.board.wht_pieces)
		if checkmated: 
			self.winner = 1
		return checkmated

	def stalemate(self, king, pieces):
		moves = []
		king_piece = self.board.data[king[0]][king[1]]
		if not king_piece.in_check:
			for piece_idx in pieces:
				piece = self.board.data[piece_idx[0]][piece_idx[1]]					
				valid = piece.valid_moves(self)
				# only filter the move set if the piece is a king
				if piece.code == 5 or piece.code == 11:
					for val in valid:
						if not king_piece.checkable(self, val[0], val[1]):
							moves += [val]
				else:
					moves += valid
			return not moves
		return False

	def at_stalemate(self):
		''' Check current player for a stalemate '''
		if self.player == 0:
			return self.stalemate(self.board.wht_king, self.board.wht_pieces)
		elif self.player == 1:
			return self.stalemate(self.board.blk_king, self.board.blk_pieces)

	def is_over(self):
		''' check the board for terminating condition (checkmate or stalemate) '''
		# check for a stalemate or checkmate scenario
		return self.at_checkmate() or self.at_stalemate()