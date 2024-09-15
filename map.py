"""
Jogo, parte lógica e gráfica que faz a interseção entre todas as telas do jogo
"""

from random import random
from threading import Thread
from time import sleep, time
from datetime import datetime
from copy import deepcopy
from random import sample
from game_config import *
from arts import *
from auxiliary_functions import *
from pure_engine_ascii import Screen
from translator import translate
from text_mission import conferir_missoes

def animacao_mapa(game, memoria:dict, debug:bool = True) -> None:
    pos_ondas = [(1, 1), (10, 2), (20, 10), (1, 14), (112, 1), (122, 5), (102, 7), (102, 32), (125, 40), (80, 40),
                 (55, 42), (10, 12), (112, 6), (132, 1), (135, 7), (91, 36), (68, 40), (114, 37), (135, 38)]

    #Nuvens
    pos_nuvem = []
    for i in range(clima[tipo_clima]["nuvem"] * 3):
        pos_nuvem.append([int(random() * 125) + 1, int(random() * 35) + 1])

    if random() < .1:
        ovni = True
    else:
        ovni = False

    conferir_missoes(tipo = "mapa", save = memoria, tipo_clima = tipo_clima)

    iteracao = 0
    while True:
        game.add_effects(x = 1, y = 0,
                         image = mapa_base,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        #Ondas ===================================================
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

        #Sol e Lua ===================================================
        if iteracao == 0:
            if 6 <= datetime.now().hour < 18:
                com_sol = True
            else:
                com_sol = False

        if com_sol:
            game.add_effects(x = 130, y = 3,
                             image = mapa_sol,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
        else:
            game.add_effects(x = 130, y = 3,
                             image = mapa_lua,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)        

        #Monumentos ===================================================
        game.add_effects(x = 55, y = 20,
                         image = mapa_piramide,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 92, y = 0,
                         image = mapa_farol,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 28, y = 0,
                         image = mapa_castelo,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 45, y = 0,
                         image = mapa_castelo_2,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 65, y = 27,
                         image = mapa_cidade_3,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 73, y = 30,
                         image = mapa_cidade_2,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)
        
        game.add_effects(x = 70, y = 32,
                         image = mapa_cidade_1,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 40, y = 33,
                         image = mapa_fazenda,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 18, y = 22,
                         image = mapa_trem,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 58, y = 5,
                         image = mapa_montanha,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 47, y = 8,
                         image = mapa_boneco_de_neve,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 32, y = 26,
                         image = mapa_maquina_escavar,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 86, y = 21,
                         image = mapa_pegasus,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 122, y = 26,
                         image = mapa_vulcao,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)
    
        if "terra_a_vista" in memoria["missoes"] or debug:
            game.add_effects(x = 5, y = 11,
                             image = mapa_navio,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        if "ovni" in memoria["missoes"] or debug:
            game.add_effects(x = 12, y = 30,
                             image = mapa_espaconave,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        if "castelo_flutuante" in memoria["missoes"] or debug:
            game.add_effects(x = 100, y = 33,
                             image = mapa_castelo_voador,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)


        if (ovni and not com_sol) or debug:
            game.add_effects(x = 136, y = 14,
                             image = mapa_ovni,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        #Palmeiras ===============================================

        for x, y in ((114, 14), (122, 16), (130, 15)):
            game.add_effects(x = x, y = y,
                             image = mapa_palmeira_1,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        for x, y in ((111, 19), (117, 17), (126, 18)):
            game.add_effects(x = x, y = y,
                             image = mapa_palmeira_2,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        #Nuvem ===================================================
        for i in range(len(pos_nuvem)):
            if random() < 0.1:
                if random() > .5:
                    pos_nuvem[i][0] = min(pos_nuvem[i][0] + 1, 125)
                else:
                    pos_nuvem[i][0] = max(pos_nuvem[i][0] - 1, 1)
                                
        for x, y in pos_nuvem[:clima[tipo_clima]["nuvem"]]:
            game.add_effects(x = x, y = y,
                             image = mapa_nuvem_1,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        for x, y in pos_nuvem[clima[tipo_clima]["nuvem"]:clima[tipo_clima]["nuvem"]*2]:
            game.add_effects(x = x, y = y,
                             image = mapa_nuvem_2,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        for x, y in pos_nuvem[clima[tipo_clima]["nuvem"]*2:]:
            game.add_effects(x = x, y = y,
                             image = mapa_nuvem_3,
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

    animacao_mapa(game, memoria_save)
