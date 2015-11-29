from piece import Piece
import movements
import copy

class BoardState():
	def __init__(self, turn = "white"):
		self.pieces = {}
		self.board = [[0 for x in range(8)] for x in range(8)] 
		self.turn = turn
		self.possible = 0
		self.children = list()
		self.heuristic = 0

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

		if (self.turn is "white" and neighbour.isKingInCheck(self.turn)):
			return False, 0

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
		if (len(self.children) is not 0):
			return self.children
		else:
			children = set()
			for row in range (0,8):
				for column in range (0,8):
					piece = self.board[row][column]
					if (piece > 1 and self.pieces[piece].color is self.turn):
						for move in movements.GetValidMovements(self, row, column):
							newrow = move[0]
							newcolumn = move[1]
							neighbour= self.MakeNeighbour(row, column, newrow, newcolumn)
							if (not neighbour.isKingInCheck(self.turn)):
								children.add(neighbour)
			self.possible = len(children)
			self.children = children
			return children

	def isCheckMate(self):
		for child in self.getNeighbours():
			if(not child.isKingInCheck(self.turn)):
				return False
		return True

	def isKingInCheck(self, color):
		moves = list()
		king_coords = (0,0)
		for row in range (0,8):
			for column in range (0,8):
				piece = self.board[row][column]
				if (piece > 1 and self.pieces[piece].type is "king" and self.pieces[piece].color is color):
					king_coords = self.pieces[piece].coords
				if (piece > 1 and self.pieces[piece].color is not color):
					for move in movements.GetValidMovements(self, row, column, check = True):
						newrow = move[0]
						newcolumn = move[1]
						moves.append((newrow, newcolumn))

		if (king_coords not in moves):
			return False
		else:
			return True


	def getPieces(self):
		white = 0
		black = 0

		for row in range (0,8):
			for column in range (0,8):
				piece = self.board[row][column]
				if (piece > 1 and self.pieces[piece].color is "white"):
					kind = self.pieces[piece].type
					if (kind is "pawn"):
						white += 1
					elif (kind is "queen"):
						white += 20
					elif (kind is "rook"):
						white += 5
					elif (kind is "bishop"):
						white += 3
					elif (kind is "knight"):
						white += 3

				elif (piece > 1 and self.pieces[piece].color is "black"):
					kind = self.pieces[piece].type
					if (kind is "pawn"):
						black += 1
					elif (kind is "queen"):
						black += 20
					elif (kind is "rook"):
						black += 5
					elif (kind is "bishop"):
						black += 3
					elif (kind is "knight"):
						black += 3

		if (self.turn is "white" and self. isKingInCheck("white") and self.isCheckMate()):
			black += 10000
		if (self.turn is "black" and self. isKingInCheck("black") and self.isCheckMate()):
			white += 10000

		#print white
		#print black
		return (black-white)


	def getHeuristic(self):
		if (self.heuristic is not 0):
			return self.heuristic
		else:
			self.heuristic = self.getPieces()
			return self.heuristic

	def toString(self):
		a = ""
		for row in range (0,8):
			for column in range (0,8):
				piece = self.board[row][column]
				if (piece > 1):
					a += self.pieces[piece].color + self.pieces[piece].type
				else:
					a += "0"
		return a

