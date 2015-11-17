import Tkinter as tk
from PIL import Image, ImageTk
class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.type = kind
		self.coords = (0,0)
		self.moved = 0
		path = color + "_" + kind + ".gif"
		self.image = ImageTk.PhotoImage(file = path)

	def ChangePawnToQueen(self):
		self.type = "queen"
		path = self.color + "_" + "queen" + ".gif"
		self.image = ImageTk.PhotoImage(file = path)
		return self.image
