#!/usr/bin/python
# coding=UTF-8

import classes
import Tkinter as tk

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=5, columns=5, size=150, color1="white", color2="blue"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color1
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

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
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    ball = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif")
    bell = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif")
    eye = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif")
    hand = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif")
    play = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/play.gif")
    stop = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/stop.gif")
    switch = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif")
    marker = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif")
    toy_monkey = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif")

    board.addpiece("ball", ball, 0,0)
    board.addpiece("bell", bell, 0,1)
    board.addpiece("eye", eye, 0,2)
    board.addpiece("hand", hand, 0,3)
    board.addpiece("play", play, 0,4)
    board.addpiece("stop", stop, 1,0)
    board.addpiece("switch", switch, 1,1)
    board.addpiece("marker", marker, 1,2)
    board.addpiece("toy-monkey", toy_monkey, 1,3)
    
    root.mainloop()
