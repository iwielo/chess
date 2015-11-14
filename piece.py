import Tkinter as tk
from PIL import Image, ImageTk
class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.type = kind
		self.coords = (0,0)

		path = color + "_" + kind + ".jpg"
		img = Image.open(path)
		img = img.resize((50, 50), Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(img)

	