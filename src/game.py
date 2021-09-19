from src.board import Board

class Game:
	def __init__(self, player_1, player_2, board=Board()):
		if not ((player_1.color == 0 and  player_2.color == 1) or (player_1.color == 1 and player_2.color == 0)):
			raise ValueError('Incorrect player enumeration.')
		self.board = board
		self.player = 0
		self.players = [player_1, player_2]
	
	def start(self):
		# run game until checkmate, draw, or exit
		print(self.board)
		while not self.is_over():
			# prompt the user for a move
			piece_idx, dest_idx = self.players[self.player].get_move()

			# FIXME make sure there is a piece at the space and that it's owned by the current player
			# FIXME check to see if we can make the move with the piece we have
			
			if self.board.array[piece_idx].can_move(self.board, piece_idx, dest_idx):
				
				self.players[self.player].make_move(self.board.array, piece_idx, dest_idx)

				# FIXME: emit new board state to output (stdout, or UI interface)
				print(self.board)
				#self.board.array[dest_idx].promote(self.board.array, dest_idx)
				# alternate player
				self.alternate()
			else:
				print(f'Could not perform move')
			
	def alternate(self):
		''' Alternate the current player '''
		self.player = (self.player + 1) % 2

	def is_over(self):
		''' FIXME: check the board for terminating condition (checkmate | draw) '''
		return False