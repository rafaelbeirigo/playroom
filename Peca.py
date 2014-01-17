#!/usr/bin/python
# coding=UTF-8

class Peca:
    """Peças presentes no tabuleiro incluindo as relativas ao agente (
    Mão, sino, olho, etc.)"""
    def __init__(self, nome=None, imagem=None, linha=0, coluna=0, acoes_inerentes=None):
        self.nome = nome
        self.imagem = imagem
	self.linha = linha
	self.coluna = coluna
	# TODO: As ações inerentes variam de acordo com regras do domínio
	self.acoes_inerentes = acoes_inerentes
