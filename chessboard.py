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

		#print neighbour.getHeuristic()
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
				if (piece > 1):
					if (self.pieces[piece].color is "white"):
						kind = self.pieces[piece].type
						white += values(self.pieces[piece])
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
						kind = self.pieces[piece].type
						black += values(self.pieces[piece])
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

		if (self.turn is "white" and self. isKingInCheck("white") and self.isCheckMate()):
			black += 10000
		if (self.turn is "black" and self. isKingInCheck("black") and self.isCheckMate()):
			white += 10000

		return black-white


	def getHeuristic(self):
		if (self.heuristic is not 0):
			return self.heuristic
		else:
			self.heuristic = self.getPieces()
			return self.heuristic

def chunks(l):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), 8):
        yield l[i:i+8]

def values(piece):
		color = piece.color
		kind = piece.type
		row = piece.coords[0]
		column = piece.coords[1]


		white_pawn = [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 5, -5,-10, 0, 0,-10, -5, 5, 5, 10, 10,-20,-20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0]
		white_knight = [-50,-40,-30,-30,-30,-30,-40,-50, -40,-20, 0, 0, 0, 0,-20,-40, -30, 0, 10, 15, 15, 10, 0,-30, -30, 5, 15, 20, 20, 15, 5,-30, -30, 0, 15, 20, 20, 15, 0,-30, -30, 5, 10, 15, 15, 10, 5,-30, -40,-20, 0, 5, 5, 0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50]
		white_bishop = [-20,-10,-10,-10,-10,-10,-10,-20, -10, 0, 0, 0, 0, 0, 0,-10, -10, 0, 5, 10, 10, 5, 0,-10, -10, 5, 5, 10, 10, 5, 5,-10, -10, 0, 10, 10, 10, 10, 0,-10, -10, 10, 10, 10, 10, 10, 10,-10, -10, 5, 0, 0, 0, 0, 5,-10, -20,-10,-10,-10,-10,-10,-10,-20]
		white_rook = [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 5, 5, 0, 0, 0]
		white_queen = [-20,-10,-10, -5, -5,-10,-10,-20, -10, 0, 0, 0, 0, 0, 0,-10, -10, 0, 5, 5, 5, 5, 0,-10, -5, 0, 5, 5, 5, 5, 0, -5, 0, 0, 5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0,-10, -10, 0, 5, 0, 0, 0, 0,-10, -20,-10,-10, -5, -5,-10,-10,-20]
		white_king = [-30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20]
		
		black_pawn  = white_pawn[::-1]
		black_knight= white_knight[::-1]
		black_bishop = white_bishop[::-1]
		black_rook = white_rook[::-1]
		black_queen = white_queen[::-1]
		black_king= white_king[::-1]

		values = {
		"white_pawn": list(chunks(white_pawn)), 
		"white_knight": list(chunks(white_knight)), 
		"white_bishop": list(chunks(white_bishop)), 
		"white_rook": list(chunks(white_rook)), 
		"white_queen": list(chunks(white_queen)), 
		"white_king": list(chunks(white_king)),
		"black_pawn": list(chunks(black_pawn)), 
		"black_knight": list(chunks(black_knight)), 
		"black_bishop": list(chunks(black_bishop)), 
		"black_rook": list(chunks(black_rook)), 
		"black_queen": list(chunks(black_queen)), 
		"black_king": list(chunks(black_king))}

		return values[color+"_"+kind][row][column]