#!/usr/bin/python
# coding=UTF-8

class Piece:
    """Pieces present on the board (including those pertaining to the agent)"""
    def __init__(self, name=None, image=None, row=0, column=0, inherent_actions=None):
        self.name = name
        self.image = image
	self.row = row
	self.column = column
	# TODO: As ações inerentes variam de acordo com regras do domínio
	self.inherent_actions = inherent_actions
