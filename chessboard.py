from piece import Piece
import movements
import copy

class BoardState():
	def __init__(self, turn = "white"):
		self.pieces = {}
		self.board = [[0 for x in range(8)] for x in range(8)] 
		self.turn = turn
		self.children = set()

	def Move(self, startrow, startcolumn, endrow, endcolumn):
		if (endrow < 0 or endcolumn <0 or endcolumn > 7 or endrow >7 or endrow is startrow and endcolumn is startcolumn):
			return False, 0

		if ((endrow, endcolumn) not in movements.GetValidMovements(self, startrow, startcolumn)):
			return False, 0

		startsquare = self.board[startrow][startcolumn]
		endsquare = self.board[endrow][endcolumn]

		color = self.pieces[startsquare].color
		if (color is not self.turn):
			return False, 0

		neighbour = self.MakeNeighbour(startrow, startcolumn, endrow, endcolumn)

		return neighbour, endsquare

	def MakeNeighbour(self, startrow, startcolumn, endrow, endcolumn):

		startsquare = self.board[startrow][startcolumn]
		endsquare = self.board[endrow][endcolumn]

		neighbour = BoardState()
		neighbour.parent = self
		neighbour.board = copy.deepcopy(self.board)
		neighbour.pieces = copy.deepcopy(self.pieces)
		neighbour.turn = "black" if self.turn is "white" else "white"
		neighbour.board[startrow][startcolumn] = 0
		neighbour.board[endrow][endcolumn] = startsquare
		neighbour.pieces[startsquare].moved += 1
		neighbour.pieces[startsquare].coords = (endrow, endcolumn)

		neighbour.startrow = startrow
		neighbour.startcolumn = startcolumn
		neighbour.endrow = endrow
		neighbour.endcolumn = endcolumn

		if (endsquare is not 0):
			del neighbour.pieces[endsquare]

		return neighbour

	def getNeighbours(self):
		for row in range (0,8):
			for column in range (0,8):
				piece = self.board[row][column]
				if (piece > 1 and self.pieces[piece].color is self.turn):
					for move in movements.GetValidMovements(self, row, column):
						newrow = move[0]
						newcolumn = move[1]
						neighbour= self.MakeNeighbour(row, column, newrow, newcolumn)
						self.children.add(neighbour)

		print len(self.children)

