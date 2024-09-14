"""
Jogo, parte lógica e gráfica que faz a interseção entre todas as telas do jogo
"""

from random import random
from threading import Thread
from time import sleep, time
from copy import deepcopy
from random import sample
from game_config import *
from arts import *
from auxiliary_functions import *
from pure_engine_ascii import Screen
from translator import translate

def animacao_mapa(memoria:dict, debug:bool = True) -> None:
    pos_ondas = [(1, 1), (10, 2), (20, 10), (1, 14), (112, 1), (122, 5), (102, 7), (102, 32), (125, 40), (80, 40),
                 (55, 42), (10, 12), (112, 6), (132, 1), (135, 7), (91, 36), (68, 40), (114, 37), (135, 38)]

    iteracao = 0
    while True:
        game.add_effects(x = 1, y = 0,
                         image = mapa_base,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        #Ondas:
        if iteracao % 8 == 0:
            pos_ondas = sample(pos_ondas, len(pos_ondas))
        k = 0
        for x, y in pos_ondas:
            game.add_effects(x = x, y = y,
                             image = mapa_ondas[k],
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
            k += 1


        #Monumentos
        game.add_effects(x = 55, y = 22,
                         image = mapa_piramide,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        if "varios_piratas" in memoria["missoes"] or debug:
            game.add_effects(x = 5, y = 11,
                             image = mapa_navio,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

                    
        sleep(1/FPS_MAPA)
        iteracao += 1
        iteracao %= 4096

if __name__ == "__main__":
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
        
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_MAPA)
    texto_principal = translate(f"(A, W, S, D) para escolher entre missões")
    game.buffer_text = texto_principal
    game_t = Thread(target = game.run)
    game_t.start()

    animacao_mapa(memoria_save)
