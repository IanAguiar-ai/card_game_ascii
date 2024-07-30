from engine_card_game import CARTAS
from random import random

def abrir_pacote() -> None:
    chances = [0.02, 0.08, 0.25, 0.65]
    chances = [sum(chances[0:i+1]) for i in range(0, len(chances))]
    raridade = ["lendario", "epico", "raro", "comum"]

    num_aleat = random()
    for i in range(len(chances)):
        if num_aleat < chances[i] and not "abrir" in locals():
            abrir = raridade[i]

    possiveis = []
    for key in CARTAS.keys():
        if CARTAS[key]["raridade"] == abrir:
            possiveis.append(CARTAS[key]["nome"])

    escolher = int(len(possiveis)*random())
    carta = possiveis[escolher]

    return abrir, carta
                
if __name__ == "__main__":
    cartas = {}
    nomes_tirados = set()
    while len(nomes_tirados) < 34:
        raridade, carta = abrir_pacote()
        print(f"{raridade:10} {carta}")
        if not raridade in cartas:
            cartas[raridade] = 1
        else:
            cartas[raridade] += 1
        nomes_tirados.add(carta)

    print(cartas)
    print(f"Cartas diferentes: {len(nomes_tirados)}")
