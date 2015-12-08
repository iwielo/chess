from piece import Piece
import movements
import copy



class BoardState():
	def __init__(self, turn = "white"):
		'''
		pieces zamienic na liste zawierajaca pionki i figury bedace w grze
		board ustawic na 0 albo referencje do pionka stojacym na odpowiednim polu, 
		w zaleznosci, czy pole jest puste, czy jakis pionek na nim stoi
		'''
		self.pieces = {}
		self.board = [[0 for x in range(8)] for x in range(8)] 
		self.turn = turn
		self.children = list()
		self.heuristic = 0
		'''
		cala logike zwiazana ze sprawdzaniem prawidlowosci ruchow przeniesc do movements.py,
		wlacznie z metodami IsCheckmate, IsKingInCheck
		
		zostawic MakeMove w postaci
		
		MakeMove(self, begin, end):
			if not begin:
				return
			if end:
				pieces.remove(end)
			end = begin
			begin = 0
			
			zostawic metode MakeNeighbour() i przepisac metode:
						
			GetNeighbours(moves_list):
			return [MakeNeighbour(move) for move in moves_list]
			
			jest wywolywana tylko na potrzeby obliczen AI, dla listy wszystkich mozliwych ruchow 
			
		'''

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
			'''
			ponizsze petle uproscic, iterujac po pionkach o okreslonym kolorze:
				for piece in pieces:
					if pieces.color == self.turn
					...
			'''
			for row in range (0,8):
				for column in range (0,8):
					piece = self.board[row][column]
					if (piece > 1 and self.pieces[piece].color is self.turn):
						for move in movements.GetValidMovements(self, row, column):
							newrow = move[0]
							newcolumn = move[1]
							'''zmienne pomocnicze newrow, newcolumn sa zbedne'''
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
		'''			
		ponizsza iteracje zastepujemy iterowaniem po liscie pieces:
		
		king = next(piece for piece in pieces if piece.type == "king" and pieces.color == color)
		for piece in pieces:
			if piece.color != color:
				if [king.row, king.column] in GetValidMovements(self, piece, check = True):
					return False
		return True
		'''
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
		'''
		ta funkcje usunac;
		wartosci z if-ow wydzielic z klasy jako slownik postaci:
		
		heuristic_values = {
			"type":  value
		}
		
		iteracje zastepujaca cialo funkcji:
		
		result = {"white": 0, "black": 0}
		for piece in pieces:
			result[piece.color] += piece.values()
			result[piece.color] += heuristic_values[piece.type]
		
		wlaczyc do funkcji getHeuristic()
		
		slownik heuristic_values i funkcję getHeuristic przeniesc do ai.py
		'''
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
