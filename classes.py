#!/usr/bin/python
# coding=UTF-8

class Peca:
    """Peças presentes no tabuleiro incluindo as relativas ao agente (
    Mão, sino, olho, etc.)"""
    def __init__(self, imagem=None, linha=0, coluna=0, acoes_inerentes=None):
        self.imagem = imagem
	self.linha = linha
	self.coluna = coluna
	# TODO: As ações inerentes variam de acordo com regras do domínio
	self.acoes_inerentes = acoes_inerentes

class Tabuleiro:
    """Tabuleiro onde as peças são posicionadas"""
    def __init__(self, linhas, colunas):
	self.linhas = linhas
	self.colunas = colunas
	
class Ambiente:
    """Ambiente, composto do tabuleiro e das peças"""


class Agente:
    """Classe referente ao agente aprendiz"""
