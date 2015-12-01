from chessboard import BoardState
from ready import GameBoard
import piece
import sys
import time

def MakeMove(board_state, gameboard):
	'''Get all the possible moves, decide which one is best and alter the gameboard'''

	start = time.time()
	move = abSearch(board_state)
	gameboard.UserMove(move.startrow, move.startcolumn, move.endrow, move.endcolumn)
	end = time.time()
	print str(end - start) + " seconds"


def abSearch(board_state):
	v = maxValue(board_state, -999999, 999999, 2)
	print v
	for option in board_state.GetNeighbours():
		for option2 in option.GetNeighbours():
			if (option2.getHeuristic() is v):
				return option

	options  = board_state.GetNeighbours()
	return options.pop()


def maxValue(board_state, a, b, depth):
	if (depth is 0):
		return board_state.getHeuristic()
	
	v = -999999
	for neighbour in board_state.GetNeighbours():
		v = max(v, minValue(neighbour, a, b, depth-1))
		if (v >= b):
			return v
		a = max(a, v)
	return v

def minValue(board_state, a, b, depth):
	if (depth is 0):
		return board_state.getHeuristic()
	
	v = 999999
	for neighbour in board_state.GetNeighbours():
		v = min(v, maxValue(neighbour, a, b, depth-1))
		if (v <= a):
			return v
		b = min(b, v)
	return v
