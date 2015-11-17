from piece import Piece
import movements

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

		if (endsquare is not 0):
			del self.pieces[endsquare]

		neighbour = BoardState()


		neighbour.parent = self
		neighbour.board = [x[:] for x in self.board]
		neighbour.pieces = self.pieces.copy()
		neighbour.turn = "black" if self.turn is "white" else "white"
		neighbour.board[startrow][startcolumn] = 0
		neighbour.board[endrow][endcolumn] = startsquare
		neighbour.pieces[startsquare].moved+=1

		return neighbour, endsquare

	def getNeighbours():
		pass

