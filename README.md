## Description
Reinforced Chess is a Chess simulator that supports artificially intelligent opponents. It is written in Python and uses reinforcement q-learning. The AI agent runs the [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm with [alpha-beta pruning techniques](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

### Working with the Chess engine
This project contains a basic chess implementation that can be seeded with a binary board state.

### Encoding the pieces
|		 | White  | Black  |
| :---	 | :----: | :----: |
| Pawn 	 |	6 	  |	12	   |
| Knight |	2	  |	8	   |	
| Bishop |	3	  |	9	   |
| Rook	 |	1	  |	7	   |
| King	 |	5	  |	11	   |
| Queen	 |	4	  |	10	   |
| Empty  |  0	  | 0	   |

### Encoding the board state

A binary board state consists of 65 bytes of data - 64 bytes for the board configuration and an additional byte for the current player (White is 0x00, Black is 0x01).

A binary board state is loaded into the ```Game``` object like so:

```python
game = Game(player1, player2, b'\x07\x08\x09\x0a\x0b\x09\x08\x07\x0c...')
```

Below is the initial board state for a fresh game of chess.

|      |  A   |  B   |  C   |  D   |  E   |  F   |  G   |  H   |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  **8**   |  7   |  8   |  9   |  10  |  11  |  9   |  8   |  7   |
|  **7**   |  12  |  12  |  12  |  12  |  12  |  12  |  12  |  12  |
|  **6**   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
|  **5**   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
|  **4**   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
|  **3**   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
|  **2**   |  6   |  6   |  6   |  6   |  6   |  6   |  6   |  6   |
|  **1**   |  1   |  2   |  3   |  4   |  5   |  3   |  2   |  1   |
