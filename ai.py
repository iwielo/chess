from chessboard import BoardState
from ready import GameBoard
import piece

def MakeMove(board_state, gameboard):
	board_state.getNeighbours()
	options = board_state.children
	print len(options)
	move = options.pop()
	gameboard.UserMove(move.startrow, move.startcolumn, move.endrow, move.endcolumn)

