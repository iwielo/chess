from chessboard import BoardState
from ready import GameBoard
import piece
import sys
import time

def MakeMove(board_state, gameboard):
	#start = time.time()
	options = board_state.getNeighbours()
	if (board_state.isCheckMate(options)):
		sys.exit()


	DFS(board_state)
	move = options.pop()
	#print move.isKingInCheck("black")
	gameboard.UserMove(move.startrow, move.startcolumn, move.endrow, move.endcolumn)


	#end = time.time()
	#print end - start


def DFS(board_state):
	visited = set()
	visited.add(board_state.toString())
	i = DFSRecur(board_state, 1, visited)
	#print i 

def DFSRecur(board_state, height, visited):
	if (height is 0):
		i = board_state.getHeuristic()
		return i
	else:
		temp = sys.maxint
		children = board_state.getNeighbours()
		for child in children:
			string = child.toString()
			if (string not in visited):
				temp = min(DFSRecur(child, height-1, visited), temp)
				visited.add(string)
			else:
				pass
		return temp