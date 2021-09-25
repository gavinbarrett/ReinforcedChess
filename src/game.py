from src.board import Board

class Game:
	def __init__(self, player_1, player_2, board):
		if not ((player_1.color == 0 and  player_2.color == 1) or (player_1.color == 1 and player_2.color == 0)):
			raise ValueError('Incorrect player enumeration.')
		self.board = board
		self.player = 0
		self.players = [player_1, player_2]
		self.last_move = None
	
	def play(self):
		''' Run the chess game '''
		while not self.is_over():
			print(self.board)
			# prompt the user for a move
			piece_idx, dest_idx = self.players[self.player].get_move()
			# compute the file and rank of the source and destination pieces
			piece_rank, piece_file = self.board.compute_coord(piece_idx)
			dest_rank, dest_file = self.board.compute_coord(dest_idx)
			# look for king checks
			self.board.find_check(self)
			# move piece
			self.execute_move(piece_file, piece_rank, dest_file, dest_rank)

	def execute_move(self, piece_file, piece_rank, dest_file, dest_rank):
		# grab current piece
		current_piece = self.board.data[piece_rank][piece_file]
		# check for a valid move
		if current_piece.color == self.players[self.player].color and current_piece.code and current_piece.can_move(self, piece_file, piece_rank, dest_file, dest_rank):
			# move the piece
			self.board.data[piece_rank][piece_file].move(self.board, piece_file, piece_rank, dest_file, dest_rank)
			# save previous move (for en passant)
			self.last_move = (dest_rank, dest_file)
			# update player pieces
			self.board.update_pieces()
			# find any checking scenario
			self.board.find_check(self)
			# alternate current player
			self.alternate()
		else:
			print(f'Could not perform move\n')

	def alternate(self):
		''' Alternate the current player '''
		self.player = (self.player + 1) % 2

	def is_over(self):
		''' FIXME: check the board for terminating condition (checkmate | draw) '''
		return False