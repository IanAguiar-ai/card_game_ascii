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

class Selecionar:
    def __init__(self, pos:tuple, time:list = None):
        self.pos:tuple = pos
        self.time:list = None
        self.r = None
        self.l = None
        self.u = None
        self.d = None

def animacao_mapa(game, memoria:dict, memoria_input:list, debug:bool = True) -> None:
    pos_ondas = [(1, 1), (10, 2), (20, 10), (1, 14), (112, 1), (122, 5), (102, 7), (102, 32), (125, 40), (80, 40),
                 (55, 42), (10, 12), (112, 6), (132, 1), (135, 7), (91, 36), (68, 40), (114, 37), (135, 38)]

    pos_locais = {"mapa_sol": {"x":130, "y":3},
                  "mapa_lua": {"x":130, "y":3},
                  "mapa_piramide": {"x":55, "y":20},
                  "mapa_farol": {"x":92, "y":0},
                  "mapa_castelo": {"x":28, "y":0},
                  "mapa_castelo_2": {"x":45, "y":0},
                  "mapa_cidade": {"x":73, "y":30},
                  "mapa_fazenda": {"x":40, "y":33},
                  "mapa_trem": {"x":18, "y":22},
                  "mapa_montanha": {"x":58, "y":5},
                  "mapa_boneco_de_neve": {"x":47, "y":8},
                  "mapa_maquina_escavar": {"x":32, "y":26},
                  "mapa_pegasus": {"x":86, "y":21},
                  "mapa_vulcao": {"x":122, "y":26},
                  "mapa_navio": {"x":5, "y":11},
                  "mapa_espaconave": {"x":12, "y":30},
                  "mapa_castelo_voador": {"x":100, "y":33},
                  "mapa_ovni": {"x":136, "y":14},
                  "mapa_oasis": {"x":45, "y":20},}

    #Nuvens
    pos_nuvem = []
    for i in range(clima[tipo_clima]["nuvem"] * 3):
        pos_nuvem.append([int(random() * 125) + 1, int(random() * 35) + 1])

    #Existencia dos itens no mapa
    jogos = {}
    for locais in pos_locais.keys():
        xy = (pos_locais[locais]["x"], pos_locais[locais]["y"])
        jogos[locais] = Selecionar(pos = xy)

    jogos["mapa_sol"].time = None
    jogos["mapa_lua"].time = None
    jogos["mapa_piramide"].time = None
    jogos["mapa_farol"].time = None
    jogos["mapa_castelo"].time = None
    jogos["mapa_castelo_2"].time = None
    jogos["mapa_cidade"].time = None
    jogos["mapa_fazenda"].time = None
    jogos["mapa_trem"].time = None
    jogos["mapa_montanha"].time = None
    jogos["mapa_boneco_de_neve"].time = None
    jogos["mapa_maquina_escavar"].time = None
    jogos["mapa_pegasus"].time = None
    jogos["mapa_vulcao"].time = None
    jogos["mapa_navio"].time = None
    jogos["mapa_espaconave"].time = None
    jogos["mapa_castelo_voador"].time = None
    jogos["mapa_ovni"].time = None

    jogos["mapa_farol"].l = jogos["mapa_castelo_2"]
    jogos["mapa_farol"].d = jogos["mapa_montanha"]

    jogos["mapa_castelo_2"].r = jogos["mapa_farol"]
    jogos["mapa_castelo_2"].l = jogos["mapa_castelo"]
    jogos["mapa_castelo_2"].d = jogos["mapa_boneco_de_neve"]

    jogos["mapa_castelo"].r = jogos["mapa_castelo_2"]
    jogos["mapa_castelo"].d = jogos["mapa_boneco_de_neve"]

    jogos["mapa_montanha"].u = jogos["mapa_farol"]
    jogos["mapa_montanha"].l = jogos["mapa_boneco_de_neve"]
    jogos["mapa_montanha"].d = jogos["mapa_piramide"]

    jogos["mapa_piramide"].l = jogos["mapa_oasis"]
    jogos["mapa_piramide"].r = jogos["mapa_pegasus"]
    jogos["mapa_piramide"].d = jogos["mapa_cidade"]
    jogos["mapa_piramide"].u = jogos["mapa_montanha"]

    jogos["mapa_oasis"].u = jogos["mapa_boneco_de_neve"]
    jogos["mapa_oasis"].r = jogos["mapa_piramide"]
    jogos["mapa_oasis"].l = jogos["mapa_trem"]
    jogos["mapa_oasis"].d = jogos["mapa_maquina_escavar"]

    jogos["mapa_trem"].l = jogos["mapa_espaconave"]
    jogos["mapa_trem"].d = jogos["mapa_espaconave"]
    jogos["mapa_trem"].r = jogos["mapa_maquina_escavar"]
    jogos["mapa_trem"].u = jogos["mapa_oasis"]

    jogos["mapa_maquina_escavar"].u = jogos["mapa_oasis"]
    jogos["mapa_maquina_escavar"].l = jogos["mapa_trem"]
    jogos["mapa_maquina_escavar"].d = jogos["mapa_fazenda"]
    jogos["mapa_maquina_escavar"].r = jogos["mapa_cidade"]

    posicao_atual = jogos["mapa_farol"]
    
    if random() < .1:
        ovni = True
    else:
        ovni = False

    if 6 <= datetime.now().hour < 18:
        com_sol = True
    else:
        com_sol = False

    if "terra_a_vista" in memoria["missoes"]:
        terra_a_vista = True
    else:
        terra_a_vista = False

    if "ovni" in memoria["missoes"]:
        ovni_ = True
    else:
        ovni_ = False

    if "castelo_flutuante" in memoria["missoes"]:
        castelo_flutuante = True
    else:
        castelo_flutuante = False


    #Conferindo missões
    conferir_missoes(tipo = "mapa", save = memoria, tipo_clima = tipo_clima, com_sol = com_sol)

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
            game.add_effects(x = pos_locais["mapa_sol"]["x"], y = pos_locais["mapa_sol"]["y"],
                             image = mapa_sol,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
        else:
            game.add_effects(x = pos_locais["mapa_lua"]["x"], y = pos_locais["mapa_sol"]["y"],
                             image = mapa_lua,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        #Monumentos ===================================================
        game.add_effects(x = pos_locais["mapa_piramide"]["x"], y = pos_locais["mapa_piramide"]["y"],
                         image = mapa_piramide,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_farol"]["x"], y = pos_locais["mapa_farol"]["y"],
                         image = mapa_farol,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_castelo"]["x"], y = pos_locais["mapa_castelo"]["y"],
                         image = mapa_castelo,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_castelo_2"]["x"], y = pos_locais["mapa_castelo_2"]["y"],
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

        game.add_effects(x = pos_locais["mapa_cidade"]["x"], y = pos_locais["mapa_cidade"]["y"],
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

        game.add_effects(x = pos_locais["mapa_fazenda"]["x"], y = pos_locais["mapa_fazenda"]["y"],
                         image = mapa_fazenda,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_trem"]["x"], y = pos_locais["mapa_trem"]["y"],
                         image = mapa_trem,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_montanha"]["x"], y = pos_locais["mapa_montanha"]["y"],
                         image = mapa_montanha,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_boneco_de_neve"]["x"], y = pos_locais["mapa_boneco_de_neve"]["y"],
                         image = mapa_boneco_de_neve,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_maquina_escavar"]["x"], y = pos_locais["mapa_maquina_escavar"]["y"],
                         image = mapa_maquina_escavar,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_pegasus"]["x"], y = pos_locais["mapa_pegasus"]["y"],
                         image = mapa_pegasus,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = pos_locais["mapa_vulcao"]["x"], y = pos_locais["mapa_vulcao"]["y"],
                         image = mapa_vulcao,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)
    
        if terra_a_vista or debug:
            game.add_effects(x = pos_locais["mapa_navio"]["x"], y = pos_locais["mapa_navio"]["y"],
                             image = mapa_navio,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        if ovni_ or debug:
            game.add_effects(x = pos_locais["mapa_espaconave"]["x"], y = pos_locais["mapa_espaconave"]["y"],
                             image = mapa_espaconave,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        if castelo_flutuante or debug:
            game.add_effects(x = pos_locais["mapa_castelo_voador"]["x"], y = pos_locais["mapa_castelo_voador"]["y"],
                             image = mapa_castelo_voador,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)


        if (ovni and not com_sol) or debug:
            game.add_effects(x = pos_locais["mapa_ovni"]["x"], y = pos_locais["mapa_ovni"]["y"],
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

        if memoria_input[0] != None:
            andar, memoria_input[0] = memoria_input[0], None

            if andar == "a":
                if posicao_atual.l != None:
                    posicao_atual = posicao_atual.l
            elif andar == "d":
                if posicao_atual.r != None:
                    posicao_atual = posicao_atual.r
            elif andar == "s":
                if posicao_atual.d != None:
                    posicao_atual = posicao_atual.d
            elif andar == "w":
                if posicao_atual.u != None:
                    posicao_atual = posicao_atual.u


        #Parte da escolha
        x_:int = max(1, posicao_atual.pos[0] - 10)
        y_:int = max(1, posicao_atual.pos[1] - 3)
        game.add_effects(x = x_, y = y_,
                         image = seta_diagonal,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)
                    
        sleep(1/FPS_MAPA)
        iteracao += 1
        iteracao %= 4096

def mapa_completo():
    memoria_input = [None]
    thread_animacao = Thread(target = animacao_mapa, args = (game, memoria_save, memoria_input))
    thread_animacao.start()

    while True:
        direcao = input()

        if type(direcao) == str:
            memoria_input[0] = direcao.lower()
        
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

    mapa_completo()

    
