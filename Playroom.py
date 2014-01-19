#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Board import *
from Piece import *
from random import randint

def move_piece_to_piece(piece_to_move, destination_piece):
    piece_to_move.row = destination_piece.row
    piece_to_move.column = destination_piece.column
    
    board.placepiece(piece_to_move)

def move_eye_to_random_object():
    random_index = randint(0, len(non_agent_pieces) - 1)
    move_piece_to_piece(eye, non_agent_pieces[random_index])

def move_hand_to_eye():
    move_piece_to_piece(hand, eye)

def move_marker_to_eye():
    move_piece_to_piece(marker, eye)

def move_eye_to_marker():
    move_piece_to_piece(eye, marker)

def move_eye_to_hand():
    move_piece_to_piece(eye, hand)

def move_eye_one_step_north():
    move_piece(eye, 'north')
    
def move_eye_one_step_south():
    move_piece(eye, 'south')

def move_eye_one_step_east():
    move_piece(eye, 'east')

def move_eye_one_step_west():
    move_piece(eye, 'west')

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

    board.placepiece(piece)

def move_piece_by_name(name, direction):
    if name == 'eye':
        move_piece(eye, direction)
    elif name == 'hand':
        move_piece(hand, direction)
    elif name == 'marker':
        move_piece(marker, direction)

current_piece_to_move_using_keys = 'marker'
def key(event):
    global current_piece_to_move_using_keys
    if event.keysym == 'e':
        current_piece_to_move_using_keys = 'eye'
    if event.keysym == 'h':
        current_piece_to_move_using_keys = 'hand'
    if event.keysym == 'm':
        current_piece_to_move_using_keys = 'marker'

    direction = ''
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        if event.keysym == 'Up':
            direction = 'north'
        if event.keysym == 'Down':
            direction = 'south'
        if event.keysym == 'Left':
            direction = 'west'
        if event.keysym == 'Right':
            direction = 'east'
        move_piece_by_name(current_piece_to_move_using_keys, direction)

    if event.keysym == '1':
        move_eye_to_marker()
    if event.keysym == '2':
        move_eye_to_hand()
    if event.keysym == '4':
        move_eye_to_random_object()
    if event.keysym == '5':
        move_hand_to_eye()
    if event.keysym == '6':
        move_marker_to_eye()

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
marker = Piece(name = "marker", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), row=1, column=2)
toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), row=1, column=3)

agent_pieces = [eye, hand, marker]
non_agent_pieces = [ball, bell, play, stop, switch, toy_monkey]

for piece in non_agent_pieces:
    board.addpiece(piece)
for piece in agent_pieces:
    board.addpiece(piece)

state = []

update_state()

root.bind_all('<Key>', key)
root.mainloop()
