#!/usr/bin/python
# coding=UTF-8

from classes import *
from board_game import *

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
target = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif")
toy_monkey = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif")

board.addpiece("ball", ball, 0,0)
board.addpiece("bell", bell, 0,1)
board.addpiece("eye", eye, 0,2)
board.addpiece("hand", hand, 0,3)
board.addpiece("play", play, 0,4)
board.addpiece("stop", stop, 1,0)
board.addpiece("switch", switch, 1,1)
board.addpiece("target", target, 1,2)
board.addpiece("toy-monkey", toy_monkey, 1,3)

root.mainloop()
