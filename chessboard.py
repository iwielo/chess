from piece import Piece
import movements
import copy

class BoardState():
	def __init__(self, turn = "white"):
		self.pieces = {}
		self.board = [[0 for x in range(8)] for x in range(8)] 
		self.turn = turn
		self.children = list()
		self.heuristic = 0

	def Move(self, startrow, startcolumn, endrow, endcolumn):
		'''This method checks if the move is valid and then creates a new BoardState'''
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

		if (self.turn is "white" and neighbour.IsKingInCheck(self.turn)):
			return False, 0

		return neighbour, endsquare

	def MakeNeighbour(self, startrow, startcolumn, endrow, endcolumn):
		'''This method generates the new boardstate based on the current one'''
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

	def GetNeighbours(self):
		'''This method gets all the possible movements for a given state'''
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
							if (not neighbour.IsKingInCheck(self.turn)):
								children.add(neighbour)
			self.children = children
			return children

	def IsCheckmate(self):
		'''Scans all the neighbours - if every neighbouring state is in check, the game ends'''
		for child in self.GetNeighbours():
			if(not child.IsKingInCheck(self.turn)):
				return False
		return True

	def IsKingInCheck(self, color):
		'''Very simple - if the position of the king is on a spot that can be attacked, he is in check'''
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
		'''This method helps us evaluate the value of each state to help the AI decide what to do'''
		white = 0
		black = 0

		for row in range (0,8):
			for column in range (0,8):
				piece = self.board[row][column]
				if (piece > 1):
					piece = self.pieces[piece]
					if (piece.color is "white"):
						kind = piece.type
						white += piece.values()
						if (kind is "pawn"):
							white += 100
						elif (kind is "queen"):
							white += 900
						elif (kind is "rook"):
							white += 500
						elif (kind is "bishop"):
							white += 330
						elif (kind is "knight"):
							white += 320

					else :
						kind = piece.type
						black += piece.values()
						if (kind is "pawn"):
							black += 100
						elif (kind is "queen"):
							black += 900
						elif (kind is "rook"):
							black += 500
						elif (kind is "bishop"):
							black += 330
						elif (kind is "knight"):
							black += 320

		if (self.turn is "white" and self. IsKingInCheck("white") and self.IsCheckmate()):
			black += 10000
		if (self.turn is "black" and self. IsKingInCheck("black") and self.IsCheckmate()):
			white += 10000

		return black-white


	def getHeuristic(self):
		'''Returns the value of the boardstate'''
		if (self.heuristic is not 0):
			return self.heuristic
		else:
			self.heuristic = self.getPieces()
			return self.heuristic
