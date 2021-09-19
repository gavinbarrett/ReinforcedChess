from src.game import Game
from src.board import Board
from src.player import Player

board = Board()
player_1 = Player(0)	# white
player_2 = Player(1)	# black

game = Game(player_1, player_2, board)

game.start()