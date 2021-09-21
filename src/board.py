from src.piece import Piece
from src.pawn import Pawn
from src.bishop import Bishop
from src.rook import Rook
from src.knight import Knight
from src.king import King
from src.queen import Queen
from src.indices import Indices
from src.colors import BLUE, YELLOW, WHITE, END

class Board:
	def __init__(self):
		self.data = [
			[Rook(7), Knight(8), Bishop(9), Queen(10), King(11), Bishop(9), Knight(8), Rook(7)],
			[Pawn(12), Pawn(12), Pawn(12), Pawn(12), Pawn(12), Pawn(12), Pawn(12), Pawn(12)],
			[Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
			[Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
			[Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
			[Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0), Piece(0)],
			[Pawn(6), Pawn(6), Pawn(6), Piece(0), Pawn(6), Pawn(6), Pawn(6), Pawn(6)],
			[Rook(1), Knight(2), Bishop(3), Queen(4), King(5), Bishop(3), Knight(2), Rook(1)]
		]
		self.indices = Indices().idxs
		self.piece_map = [f'{WHITE}*', f'{YELLOW}R', f'{YELLOW}N', f'{YELLOW}B', f'{YELLOW}Q', f'{YELLOW}K', f'{YELLOW}P', f'{BLUE}R', f'{BLUE}N', f'{BLUE}B', f'{BLUE}Q', f'{BLUE}K', f'{BLUE}P']
		self.blk_pieces = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		self.wht_pieces = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]

	def __str__(self):
		# generate the board's binary code representation
		binary_board = [self.piece_map[p.code] for row in self.data for p in row] + [END]
		# format into a string with appropraite line breaks
		return ''.join([' '.join(binary_board[c:c+8]) + '\n' for c in range(0, len(binary_board), 8)])
	
	def compute_coord(self, piece_idx):
		''' Return the file and rank of the piece '''
		return piece_idx // 8, piece_idx % 8

	def in_bounds(self, idx):
		''' Return True if index falls inside the board '''
		return 0 <= idx[0] < 8 and 0 <= idx[1] < 8