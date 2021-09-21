from src.board import Board

class Game:
	def __init__(self, player_1, player_2, board=Board()):
		if not ((player_1.color == 0 and  player_2.color == 1) or (player_1.color == 1 and player_2.color == 0)):
			raise ValueError('Incorrect player enumeration.')
		self.board = board
		self.player = 0
		self.players = [player_1, player_2]
		self.last_move = None
	
	def play(self):
		''' Run the chess game '''
		print(self.board)
		while not self.is_over():
			# prompt the user for a move
			piece_idx, dest_idx = self.players[self.player].get_move()
			# compute the file and rank of the source and destination pieces
			piece_rank, piece_file = self.board.compute_coord(piece_idx)
			dest_rank, dest_file = self.board.compute_coord(dest_idx)
			# grab current piece
			current_piece = self.board.data[piece_rank][piece_file]
			# check for a valid move
			if current_piece.can_move(self, piece_file, piece_rank, dest_file, dest_rank):
				# move the piece
				self.board.data[piece_rank][piece_file].move(self.board, piece_file, piece_rank, dest_file, dest_rank)
				# emit new board state to output (stdout, or UI interface)
				print(self.board)
				# save previous move (for en passant)
				self.last_move = (dest_rank, dest_file)
				# alternate current player
				self.alternate()
			else:
				print(f'Could not perform move\n')
				print(self.board)
			
	def alternate(self):
		''' Alternate the current player '''
		self.player = (self.player + 1) % 2

	def is_over(self):
		''' FIXME: check the board for terminating condition (checkmate | draw) '''
		return False