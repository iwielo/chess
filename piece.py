import Tkinter as tk
from PIL import Image, ImageTk
'''te importy sa zbedne'''

class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.type = kind
		self.coords = (0,0)
		self.moved = 0		
		self.path = "res/" + color + "_" + kind + ".gif"
		'''zamiast coords:
		self.row = row
		self.column = column
		gdzie row, column przekazywane jako argumenty
		
		self.path jest zbedne jako atrybut klasy, 
		sciezki do plikow z rysunkami figur uzywamy tylko przy wczytywaniu planszy lub zmianie pionka na krolowke,
		lepiej konstruowac je gdy sa potrzebne
		
		self.moved tez zbedne, sluzy tylko do okreslenia pierwszego ruchu pionka
		lepiej to zrobic w movements.py
		'''



	def values(self):
		color = self.color
		kind = self.type
		row = self.coords[0]
		column = self.coords[1]
		'''te zmienne pomocnicze sa zbedne'''

		'''ponizsze listy, wraz ze slownikiem values, przeniesc poza funkcje, wazna jest tylok jej ostatnia linijka
		wszystko, razem z funkcja, przeniesc do ai.py'''
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


def chunks(l):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), 8):
        yield l[i:i+8]

