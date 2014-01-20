#!/usr/bin/python
# coding=UTF-8

class Piece:
    """Pieces present on the board (including those pertaining to the agent)"""
    def __init__(self, name=None, image=None, row=0, column=0, actions=[]):
        self.name = name
        self.image = image
	self.row = row
	self.column = column
        self.actions = actions

    def get_actions():
        return self.actions
