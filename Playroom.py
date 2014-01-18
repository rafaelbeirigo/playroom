#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Board import *
from Piece import *

def move_piece(piece, direction):
    if direction == 'north':
        piece.row -= 1
    elif direction == 'south':
        piece.row += 1
    elif direction == 'east':
        piece.column += 1
    elif direction == 'west':
        piece.column -= 1

    if piece.row < 0:
        piece.row = 0
    if piece.row > board.rows - 1:
        piece.row = board.rows - 1
    if piece.column < 0:
        piece.column = 0
    if piece.column > board.columns - 1:
        piece.column = board.columns - 1

def key(event):
    action = ''
    if event.keysym == 'Up':
        action = 'north'
    if event.keysym == 'Down':
        action = 'south'
    if event.keysym == 'Left':
        action = 'west'
    if event.keysym == 'Right':
        action = 'east'

    piece = target
    move_piece(piece, action)
    board.placepiece(piece)
    
root = tk.Tk()
root.bind_all('<Key>', key)

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
board.addpiece(play)
board.addpiece(stop)
board.addpiece(switch)
board.addpiece(toy_monkey)

board.addpiece(eye)
board.addpiece(hand)
board.addpiece(target)

root.mainloop()
