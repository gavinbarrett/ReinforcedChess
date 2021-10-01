from src.piece import Piece
from src.pawn import Pawn
from src.bishop import Bishop
from src.rook import Rook
from src.knight import Knight
from src.king import King
from src.queen import Queen
from src.indices import Indices
from src.colors import BLUE, YELLOW, WHITE, END
from src.coords import compute_coord

default_board = b'\x07\x08\x09\x0a\x0b\x09\x08\x07\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x06\x06\x06\x06\x06\x06\x06\x01\x02\x03\x04\x05\x03\x02\x01'

class Board:
	def __init__(self, data=default_board):
		self.data = self.construct_board(data)
		self.indices = Indices().idxs
		self.piece_map = [f'{WHITE}*', f'{YELLOW}R', f'{YELLOW}N', f'{YELLOW}B', f'{YELLOW}Q', f'{YELLOW}K', f'{YELLOW}P', f'{BLUE}R', f'{BLUE}N', f'{BLUE}B', f'{BLUE}Q', f'{BLUE}K', f'{BLUE}P']
		self.wht_pieces = []
		self.blk_pieces = []
		self.wht_king = None
		self.blk_king = None
		self.update_pieces()

	def construct_board(self, data):
		board = []
		for pos, code in enumerate(data):
			if not code: board.append(Piece(0, pos))
			elif code == 6 or code == 12: board.append(Pawn(code, pos))
			elif code == 1 or code == 7: board.append(Rook(code, pos))
			elif code == 2 or code == 8: board.append(Knight(code, pos))
			elif code == 3 or code == 9: board.append(Bishop(code, pos))
			elif code == 4 or code == 10: board.append(Queen(code, pos))
			elif code == 5 or code == 11: board.append(King(code, pos))
		return [board[i:i+8] for i in range(0, len(board), 8)]

	def update_pieces(self):
		''' Update the new set of pieces for each player '''
		self.wht_pieces = []
		self.blk_pieces = []
		for rank_idx, rank in enumerate(self.data):
			for piece_idx, piece in enumerate(rank):
				if not piece.code: continue
				elif 0 < piece.code < 7:
					self.wht_pieces.append((rank_idx, piece_idx))
					if piece.code == 5:
						self.wht_king = (rank_idx, piece_idx)
				elif 6 < piece.code < 13:
					self.blk_pieces.append((rank_idx, piece_idx))
					if piece.code == 11:
						self.blk_king = (rank_idx, piece_idx)

	def find_check(self, game):
		''' Determine if either king is now in check '''
		# iterate through blk_pieces
		blk_vector = []
		for blk_piece in game.board.blk_pieces:
			target = game.board.data[blk_piece[0]][blk_piece[1]]
			blk_vector += target.valid_moves(game)
		king = game.board.wht_king
		if king in blk_vector:
			game.board.data[king[0]][king[1]].in_check = True
			print(f'White is in check!')
		else:
			game.board.data[king[0]][king[1]].in_check = False
		wht_vector = []
		for wht_piece in game.board.wht_pieces:
			target = game.board.data[wht_piece[0]][wht_piece[1]]
			wht_vector += target.valid_moves(game)
		king = game.board.blk_king
		if king in wht_vector:
			game.board.data[king[0]][king[1]].in_check = True
			print(f'Black is in check!')
		else:
			game.board.data[king[0]][king[1]].in_check = False
	
	def compute_coord(self, piece_idx):
		''' Return the file and rank of the piece '''
		return piece_idx // 8, piece_idx % 8

	def in_bounds(self, idx):
		''' Return True if index falls inside the board '''
		return 0 <= idx[0] < 8 and 0 <= idx[1] < 8
	
	def __str__(self):
		# generate the board's binary code representation
		arr = []
		for idx, row in enumerate(self.data):
			arr += [f'{WHITE}{8 - idx} ']
			for p in row:
				arr += [f'{self.piece_map[p.code]} ']
			arr += ['\n']
		arr += [f'{WHITE}  A B C D E F G H{END}']
		return ''.join(arr)