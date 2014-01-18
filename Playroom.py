#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Board import *
from Piece import *

root = tk.Tk()
board = Board(root)
board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

ball = Piece(name = "ball", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif"))
bell = Piece(name = "bell", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif"), row=0, column=1)
eye = Piece(name = "eye", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif"), row=0, column=2)
hand = Piece(name = "hand", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif"), row=0, column=3)
play = Piece(name = "play", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/play.gif"), row=0, column=4)
stop = Piece(name = "stop", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/stop.gif"), row=1, column=0)
switch = Piece(name = "switch", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif"), row=1, column=1)
target = Piece(name = "target", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), row=1, column=2)
toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), row=1, column=3)

board.addpiece(ball)
board.addpiece(bell)
board.addpiece(eye)
board.addpiece(hand)
board.addpiece(play)
board.addpiece(stop)
board.addpiece(switch)
board.addpiece(target)
board.addpiece(toy_monkey)

root.mainloop()
