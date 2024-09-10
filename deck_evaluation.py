"""
Código que dá dados para a avaliação de decks quebrados
Por enquanto descontinuado por causa da quantidade muito grande de combinações de batalhas
"""
from engine_card_game import jogar, precos, CARTAS


class Fake_Screen:
    """
    Imita a função screen mas para que nada seja ativado durante o jogo
    """
    
    def __init__(self):
        self.buffer_text = 0
        game.animation = 0

    def close(self):
        pass

    def add_effects(self, **args):
        pass

    
if __name__ == "__main__":
    combinacoes = []
    for a, b, c in [[0, 0, 5], [0, 1, 4], [1, 1, 3], [0, 2, 3], [1, 2, 2]]:
        i_ = 0
        for i in range(len(precos[a])):
            j_ = 0
            for j in range(i, len(precos[b])):
                k_ = 0
                for k in range(j, len(precos[c])):
                    if i != j != k:
                        #print(f"{precos[a][i]} {precos[b][j]} {precos[c][k]}")
                        combinacoes.append([precos[a][i], precos[b][j], precos[c][k]])
                    k_ += 1
                j_ += 1
            i_ += 1

    times = []
    for i in range(len(combinacoes) - 1):
        for j in range(i +1, len(combinacoes)):
            times.append([combinacoes[i], combinacoes[j]])

    for batalha in times:
        print(batalha)
    #jogar(TIMES = times, graphic = Fake_Screen)
