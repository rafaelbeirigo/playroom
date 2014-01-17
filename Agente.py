#!/usr/bin/python
# coding=UTF-8
import random

class Agente:
    """Classe referente ao agente aprendiz"""
    def __init__(self, pecas):
        self.acoes_disponiveis = [
            "move_olho_uma_celula_norte",
            "move_olho_uma_celula_sul",
            "move_olho_uma_celula_leste",
            "move_olho_uma_celula_oeste"
        ]
        self.pecas = pecas

if __name__ == "__main__":
    agente = Agente()
    
    acao_aleatoria = random.randint(0, len(agente.acoes_disponiveis) - 1)
    print "Ação aleatória escolhida: " + agente.acoes_disponiveis[acao_aleatoria]
