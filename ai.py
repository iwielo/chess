from chessboard import BoardState
from ready import GameBoard
import piece
import sys
import time

def MakeMove(board_state, gameboard):
	start = time.time()
	#options = board_state.getNeighbours()

	move = abSearch(board_state)


	gameboard.UserMove(move.startrow, move.startcolumn, move.endrow, move.endcolumn)


	end = time.time()
	print end - start


def abSearch(board_state):
	options = board_state.getNeighbours()


	for option in options:
		option.getHeuristic()

	v = maxValue(board_state, -sys.maxint-1, sys.maxint, 2)
	print v
	for option in options:
		#print option.getHeuristic()
		if (option.getHeuristic() is v):
			return option

	return options.pop()


def maxValue(board_state, a, b, depth):
	if (depth is 0):
		return board_state.getHeuristic()
	
	v = -sys.maxint-1
	for neighbour in board_state.getNeighbours():
		v = max(v, minValue(neighbour, a, b, depth-1))
		if (v >= b):
			print "prune"
			return v
		a = max(a, v)
	return v

def minValue(board_state, a, b, depth):
	if (depth is 0):
		return board_state.getHeuristic()
	
	v = sys.maxint
	for neighbour in board_state.getNeighbours():
		v = min(v, maxValue(neighbour, a, b, depth-1))
		if (v <= a):
			print "prune"
			return v
		b = min(b, v)
	return v
