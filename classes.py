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
    def __init__(self, num_lin, num_col):
	self.num_lin = num_lin
	self.num_col = num_col
	
class Ambiente:
    """Ambiente, composto do tabuleiro e das peças"""


class Agente:
