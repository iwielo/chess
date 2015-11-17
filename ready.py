import Tkinter as tk
from PIL import Image, ImageTk
from piece import Piece
from chessboard import BoardState
import ai
class GameBoard(tk.Frame):
    def __init__(self, parent, size=70):
        self.size = size
        self.board_state = BoardState()
        self.move_data = {"x": 0, "y": 0, "item": None}
        self.order = 2
        self.images = list()

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=8*size, height=8*size)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.ActivateBindings()

    def ActivateBindings(self):
        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.OnPieceButtonPress)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.OnPieceButtonRelease)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.OnPieceMotion)

    def OnPieceButtonPress(self, event):
        self.move_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y

    def OnPieceMotion(self, event):
        counter = self.move_data["item"]
        if (counter < 2):
            return
        
        delta_x = event.x - self.move_data["x"]
        delta_y = event.y - self.move_data["y"]
        self.canvas.move(self.move_data["item"], delta_x, delta_y)
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y

    def OnPieceButtonRelease(self, event):
        counter = self.move_data["item"]
        if (counter < 2):
            return

        startrow = self.board_state.pieces[counter].coords[0]
        startcolumn = self.board_state.pieces[counter].coords[1]

        endrow = int(self.move_data["y"]/self.size)
        endcolumn = int(self.move_data["x"]/self.size)
        self.UserMove(startrow, startcolumn, endrow, endcolumn)

    def UserMove(self, startrow, startcolumn, endrow, endcolumn):
        valid, occupied = self.board_state.Move(startrow, startcolumn, endrow, endcolumn)
        counter = self.board_state.board[startrow][startcolumn]

        if (valid is not False):
            if (occupied  is not 0):
                self.canvas.delete(occupied) 
            self.board_state = valid
            self.MovePiece(counter, endrow, endcolumn)
        else:
            self.MovePiece(counter, startrow, startcolumn)

        if (self.board_state.turn is "black"):
            ai.MakeMove(self.board_state, self)


    def AddPiece(self, piece, row=0, column=0):
        if (self.board_state.board[row][column] is not 0):
            print "you cannot add a piece here"
            return
        else:
            piece.number = self.order
            self.order +=1 

            self.board_state.pieces[piece.number] = piece
            self.board_state.board[row][column] = piece.number

            image = ImageTk.PhotoImage(file = piece.path)
            self.images.append(image)

            self.canvas.create_image(0,0, image=image, tags=(piece.number, "piece"), anchor="c")
            self.canvas.tag_raise(piece.number)
            self.MovePiece(piece.number, row, column)
            self.board_state.pieces[piece.number].coords = (row,column)

    def MovePiece(self, counter, row, column):
        x0 = (column * self.size) + self.size/2
        y0 = (row * self.size) + self.size/2
        self.canvas.coords(counter, x0, y0)
        self.CheckSpecial(counter, row, column)

    def CheckSpecial(self, counter, row, column):
        piece = self.board_state.pieces[counter]
        if (piece.type is "pawn"):
            if (piece.color is "black" and row is 7
            or piece.color is "white" and row is 0):
                piece.type = "queen"
                path = piece.color + "_queen" + ".gif"
                image = ImageTk.PhotoImage(file = path)
                self.images.append(image)
                self.canvas.itemconfig(counter, image = image )


    def FillBoard(self):
        for i in range(8):
            self.AddPiece(Piece("black", "pawn"), 1, i)
            self.AddPiece(Piece("white", "pawn"), 6, i)

        self.AddPiece(Piece("black", "rook"), 0, 0)
        self.AddPiece(Piece("black", "rook"), 0, 7)
        self.AddPiece(Piece("black", "knight"), 0, 1)
        self.AddPiece(Piece("black", "knight"), 0, 6)
        self.AddPiece(Piece("black", "bishop"), 0, 2)
        self.AddPiece(Piece("black", "bishop"), 0, 5)
        self.AddPiece(Piece("black", "queen"), 0, 3)
        self.AddPiece(Piece("black", "king"), 0, 4)

        self.AddPiece(Piece("white", "rook"), 7, 0)
        self.AddPiece(Piece("white", "rook"), 7, 7)
        self.AddPiece(Piece("white", "knight"), 7, 1)
        self.AddPiece(Piece("white", "knight"), 7, 6)
        self.AddPiece(Piece("white", "bishop"), 7, 2)
        self.AddPiece(Piece("white", "bishop"), 7, 5)
        self.AddPiece(Piece("white", "queen"), 7, 3)
        self.AddPiece(Piece("white", "king"), 7, 4)


def setup():
    root = tk.Tk()
    root.resizable(width = False, height = False)
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true")

    path = "chessboard.jpg"
    chessboard = Image.open(path)
    chessboard = chessboard.resize((board.size*8, board.size*8), Image.ANTIALIAS)
    chessboard = ImageTk.PhotoImage(chessboard)
    board.canvas.create_image(board.size*4,board.size*4,image=chessboard)
    board.FillBoard()
    root.mainloop()

if __name__ == "__main__":
    setup()

