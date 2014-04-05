#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Piece import *

class Board(tk.Frame):
    """Board where the pieces are put"""
    def __init__(self, parent, rows=5, columns=5, size=150, color1="white", color2="blue", update_screen=True):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color1
        self.pieces = []
        self.update_screen = update_screen

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def updatepieceimage(self, piece):
        self.canvas.delete(piece.name)
        self.canvas.create_image(0,0, image=piece.image, tags=(piece.name, "peça"), anchor="c")
        self.placepiece(piece)
    
    def addpiece(self, piece):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=piece.image, tags=(piece.name, "peça"), anchor="c")
        self.placepiece(piece)
        self.pieces.append(piece)

    def placepiece(self, piece):
        '''Place a piece at the given row/column'''
        if self.update_screen:
            print 'vou plaçar as piça'
            x0 = (piece.column * self.size) + int(self.size/2)
            y0 = (piece.row * self.size) + int(self.size/2)
            self.canvas.coords(piece.name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for piece in self.pieces:
            self.placepiece(piece)
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


if __name__ == "__main__":
    root = tk.Tk()
    board = Board(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    ball = Piece(name = "ball", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif"))
    bell = Piece(name = "bell", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif"), row=0, column=1)
    eye = Piece(name = "eye", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif"), row=0, column=2)
    hand = Piece(name = "hand", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif"), row=0, column=3)
    blue_block = Piece(name = "blue_block", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/blue_block.gif"), row=0, column=4)
    red_block = Piece(name = "red_block", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/red_block.gif"), row=1, column=0)
    switch = Piece(name = "switch", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif"), row=1, column=1)
    marker = Piece(name = "marker", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), row=1, column=2)
    toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), row=1, column=3)

    board.addpiece(ball)
    board.addpiece(bell)
    board.addpiece(eye)
    board.addpiece(hand)
    board.addpiece(blue_block)
    board.addpiece(red_block)
    board.addpiece(switch)
    board.addpiece(marker)
    board.addpiece(toy_monkey)
    
    root.mainloop()
