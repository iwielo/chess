import Tkinter as tk
from PIL import Image, ImageTk
from piece import Piece
class GameBoard(tk.Frame):
    def __init__(self, parent, size=64):
        self.size = size
        self.pieces = {}
        self._drag_data = {"x": 0, "y": 0, "item": None}
        canvas_width = 8 * size
        canvas_height = 8 * size
        self.board = [[0 for x in range(8)] for x in range(8)] 

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.ActivateBindings()

    def ActivateBindings(self):
        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.OnPieceButtonPress)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.OnPieceButtonRelease)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.OnPieceMotion)

    def OnPieceButtonPress(self, event):
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnPieceMotion(self, event):
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnPieceButtonRelease(self, event):
        counter = self._drag_data["item"]

        row = int(self._drag_data["y"]/self.size)
        column = int(self._drag_data["x"]/self.size)

        if (row < 0 or column < 0 or row > 7 or column > 7 or self.board[row][column] is not 0):
            print"you cannot move to that square"
            row = self.pieces[counter].coords[0]
            column = self.pieces[counter].coords[1]
        else:
            x = self.pieces[counter].coords[0]
            y = self.pieces[counter].coords[1]
            self.board[x][y] = 0
            self.board[row][column] = counter
        self.movepiece(counter, row,column)

    def addpiece(self, piece, row=0, column=0):
        if (self.board[row][column] is not 0):
            print "you cannot add a piece here"
            return
        else:
            self.board[row][column] = piece.number
            self.canvas.create_image(0,0, image=piece.image, tags=(piece.number, "piece"), anchor="c")
            self.pieces[piece.number] = piece
            self.movepiece(piece.number, row, column)

    def movepiece(self, counter, row, column):
        self.pieces[counter].coords = (row,column)
        x0 = (column * self.size) + self.size/2
        y0 = (row * self.size) + self.size/2
        self.canvas.coords(counter, x0, y0)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width = False, height = False)
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    path = "chessboard.jpg"
    chessboard = Image.open(path)
    chessboard = chessboard.resize((board.size*8, board.size*8), Image.ANTIALIAS)
    chessboard = ImageTk.PhotoImage(chessboard)
    board.canvas.create_image(board.size*4,board.size*4,image=chessboard)

    counter = 2


    piece1 = Piece("black", "pawn", counter)
    counter +=1
    board.addpiece(piece1, 1,1)

    piece2 = Piece("black", "pawn", counter)
    counter +=1
    board.addpiece(piece2, 5,5)

    root.mainloop()

