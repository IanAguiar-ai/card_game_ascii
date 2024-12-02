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
from card_game import run_the_game, build_cards
from engine_card_game import CARTAS

class Selecionar:
    def __init__(self, pos:tuple, time:list = None):
        self.pos:tuple = pos
        self.time:list = None
        self.tipo:str = "jogo" #loja
        self.nome:str = None
        self.dificuldade:str = None
        self.r = None
        self.l = None
        self.u = None
        self.d = None

def animacao_mapa(game, memoria:dict, memoria_input:list, gatilho_terminar:list, debug:bool = True) -> None:
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
                  "mapa_oasis": {"x":40, "y":22},
                  "mapa_praia": {"x":122, "y":16}}

    #Nuvens
    pos_nuvem = []
    for i in range(clima[tipo_clima]["nuvem"] * 3):
        pos_nuvem.append([int(random() * 125) + 1, int(random() * 35) + 1])

    #Existencia dos itens no mapa
    jogos = {}
    for locais in pos_locais.keys():
        xy = (pos_locais[locais]["x"], pos_locais[locais]["y"])
        jogos[locais] = Selecionar(pos = xy)
        jogos[locais].time = TIMES_MAPA[locais]
        jogos[locais].nome = locais[locais.find("_")+1:].replace("_"," ").title()
        if TIMES_MAPA[locais] != None:
            dificuldade = sum([int(CARTAS[personagem]["preco"]) for personagem in TIMES_MAPA[locais]])
            if dificuldade <= 3:
                jogos[locais].dificuldade = "Facil"
            elif dificuldade <= 5:
                jogos[locais].dificuldade = "Normal"
            elif dificuldade <= 8:
                jogos[locais].dificuldade = "Difícil"
            else:
                jogos[locais].dificuldade = "Épico"

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

    jogos["mapa_boneco_de_neve"].r = jogos["mapa_montanha"]
    jogos["mapa_boneco_de_neve"].u = jogos["mapa_castelo_2"]
    jogos["mapa_boneco_de_neve"].d = jogos["mapa_oasis"]

    jogos["mapa_trem"].l = jogos["mapa_espaconave"]
    jogos["mapa_trem"].d = jogos["mapa_espaconave"]
    jogos["mapa_trem"].r = jogos["mapa_maquina_escavar"]
    jogos["mapa_trem"].u = jogos["mapa_oasis"]

    jogos["mapa_espaconave"].u = jogos["mapa_trem"]
    jogos["mapa_espaconave"].r = jogos["mapa_trem"]

    jogos["mapa_maquina_escavar"].u = jogos["mapa_oasis"]
    jogos["mapa_maquina_escavar"].l = jogos["mapa_trem"]
    jogos["mapa_maquina_escavar"].d = jogos["mapa_fazenda"]
    jogos["mapa_maquina_escavar"].r = jogos["mapa_cidade"]

    jogos["mapa_fazenda"].u = jogos["mapa_maquina_escavar"]
    jogos["mapa_fazenda"].l = jogos["mapa_espaconave"]
    jogos["mapa_fazenda"].r = jogos["mapa_cidade"]

    jogos["mapa_cidade"].u = jogos["mapa_piramide"]
    jogos["mapa_cidade"].l = jogos["mapa_fazenda"]
    jogos["mapa_cidade"].r = jogos["mapa_pegasus"]

    jogos["mapa_pegasus"].l = jogos["mapa_piramide"]
    jogos["mapa_pegasus"].d = jogos["mapa_cidade"]
    jogos["mapa_pegasus"].r = jogos["mapa_vulcao"]
    jogos["mapa_pegasus"].u = jogos["mapa_montanha"]

    jogos["mapa_vulcao"].l = jogos["mapa_pegasus"]
    jogos["mapa_vulcao"].u = jogos["mapa_praia"]

    jogos["mapa_praia"].d = jogos["mapa_vulcao"]
    jogos["mapa_praia"].l = jogos["mapa_pegasus"]

    #Especiais
    jogos["mapa_ovni"].d = jogos["mapa_praia"]
    
    jogos["mapa_sol"].u = jogos["mapa_ovni"]
    jogos["mapa_lua"].u = jogos["mapa_ovni"]

    jogos["mapa_navio"].u = jogos["mapa_castelo"]
    jogos["mapa_navio"].d = jogos["mapa_trem"]
    jogos["mapa_navio"].r = jogos["mapa_oasis"]

    jogos["mapa_castelo_voador"].l = jogos["mapa_cidade"]
    jogos["mapa_castelo_voador"].r = jogos["mapa_vulcao"]
    jogos["mapa_castelo_voador"].u = jogos["mapa_pegasus"]

    posicao_atual = jogos["mapa_farol"]
    
    if random() < .1:
        ovni = True
    else:
        ovni = False

    if 6 <= datetime.now().hour < 18:
        com_sol = True
        jogos["mapa_ovni"].u = jogos["mapa_sol"]
        jogos["mapa_sol"].d = jogos["mapa_ovni"]
    else:
        com_sol = False
        jogos["mapa_ovni"].u = jogos["mapa_lua"]
        jogos["mapa_lua"].d = jogos["mapa_ovni"]

    if "terra_a_vista" in memoria["missoes"] or debug:
        terra_a_vista = True
        jogos["mapa_trem"].u = jogos["mapa_navio"]
        jogos["mapa_oasis"].u = jogos["mapa_navio"]
        jogos["mapa_boneco_de_neve"].l = jogos["mapa_navio"]
    else:
        terra_a_vista = False

    if "ovni" in memoria["missoes"] or debug:
        ovni_ = True
        jogos["mapa_praia"].r = jogos["mapa_ovni"]
        jogos["mapa_praia"].u = jogos["mapa_ovni"]
    else:
        ovni_ = False

    if "castelo_flutuante" in memoria["missoes"] or debug:
        castelo_flutuante = True
        jogos["mapa_cidade"].d = jogos["mapa_castelo_voador"]
        jogos["mapa_vulcao"].d = jogos["mapa_castelo_voador"]
    else:
        castelo_flutuante = False


    #Conferindo missões
    conferir_missoes(tipo = "mapa", save = memoria, tipo_clima = tipo_clima, com_sol = com_sol)

    iteracao = 0
    while not gatilho_terminar[0]:
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

        for x, y in ((114, 14), (122, 16), (130, 15), (49, 18)):
            game.add_effects(x = x, y = y,
                             image = mapa_palmeira_1,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        for x, y in ((111, 19), (117, 17), (126, 18), (46, 17), (43, 18)):
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
            elif andar == "":
                if posicao_atual.tipo == "jogo" and posicao_atual.time != None:
                    memoria_input[0] = posicao_atual.time[0]
                    memoria_input[1] = posicao_atual.time[1]
                    memoria_input[2] = posicao_atual.time[2]
                    gatilho_terminar[0] = True


        #Parte da escolha
        x_:int = max(1, posicao_atual.pos[0] - 10)
        y_:int = max(1, posicao_atual.pos[1] - 3)
        game.add_effects(x = x_, y = y_,
                         image = seta_diagonal,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        texto_principal = translate(f"(A, W, S, D) para escolher entre missões\n(E) para sair\n(ENTER) PARA entrar em {posicao_atual.nome}")
        game.buffer_text = texto_principal

        sleep(1/FPS_MAPA)
        iteracao += 1
        iteracao %= 4096

def mapa_completo(game, memoria_save):
    texto_principal = translate(f"(A, W, S, D) para escolher entre missões\n(E) para sair")
    game.buffer_text = texto_principal
    
    memoria_input:list = [None, None, None, None]
    gatilho_terminar:list = [False]
    thread_animacao = Thread(target = animacao_mapa, args = (game, memoria_save, memoria_input, gatilho_terminar))
    thread_animacao.start()

    while True:
        direcao = input()

        if type(direcao) == str and direcao.lower() == "e":
            gatilho_terminar[0] = True
            thread_animacao.join()
            return None
        elif type(direcao) == str and direcao != "": #Para andar
            memoria_input[0] = direcao.lower()
        elif type(direcao) == str and direcao == "": #Para entrar em jogo ou loja
            memoria_input[0] = direcao
            while memoria_input[2] == None:
                sleep(1/FPS_MAPA)
            gatilho_terminar[0] = True
            sleep(1/FPS_MAPA)
            run_the_game(time_inimigo = build_cards(memoria_input[:3]))            
        
if __name__ == "__main__":
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
        
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_MAPA)
    game_t = Thread(target = game.run)
    game_t.start()

    mapa_completo(game, memoria_save)

    
