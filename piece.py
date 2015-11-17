import Tkinter as tk
from PIL import Image, ImageTk
class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.type = kind
		self.coords = (0,0)
		self.moved = 0
		self.path = color + "_" + kind + ".gif"