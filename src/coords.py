def compute_coord(piece_idx):
	''' Return the file and rank of the piece '''
	return piece_idx // 8, piece_idx % 8