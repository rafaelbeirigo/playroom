class Peca:
    """Peças presentes no tabuleiro incluindo as relativas ao agente (
    Mão, sino, olho, etc.)"""
    def __init__(self):
	self.lin = 0
	self.col = 0
	# TODO: As ações disponíveis variam de acordo com regras do domínio
	self.acoes_disponiveis = {}

class Tabuleiro:
    """Tabuleiro onde as peças são posicionadas"""
    def __init__(self, linhas, colunas):
	self.linhas = linhas
	self.colunas = colunas
	
class Ambiente:
    """Ambiente, composto do tabuleiro e das peças"""


class Agente:
