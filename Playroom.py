#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Tabuleiro import *
from Peca import *

root = tk.Tk()
tabuleiro = Tabuleiro(root)
tabuleiro.pack(side="top", fill="both", expand="true", padx=4, pady=4)

ball = Peca(nome = "bola", imagem=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif"))
bell = Peca(nome = "sino", imagem=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif"), linha=0, coluna=1)
eye = Peca(nome = "eye", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif"), linha=0, coluna=2)
hand = Peca(nome = "hand", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif"), linha=0, coluna=3)
play = Peca(nome = "play", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/play.gif"), linha=0, coluna=4)
stop = Peca(nome = "stop", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/stop.gif"), linha=1, coluna=0)
switch = Peca(nome = "switch", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif"), linha=1, coluna=1)
target = Peca(nome = "target", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), linha=1, coluna=2)
toy_monkey = Peca(nome = "toy_monkey", imagem = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), linha=1, coluna=3)

tabuleiro.addpiece(ball)
tabuleiro.addpiece(bell)
tabuleiro.addpiece(eye)
tabuleiro.addpiece(hand)
tabuleiro.addpiece(play)
tabuleiro.addpiece(stop)
tabuleiro.addpiece(switch)
tabuleiro.addpiece(target)
tabuleiro.addpiece(toy_monkey)

root.mainloop()
