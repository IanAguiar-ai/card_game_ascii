"""
Sistema de construção de cartas
"""

from random import random
from threading import Thread
from os import listdir
from json import dump
from game_config import *
from arts import *
from auxiliary_functions import *
from pure_engine_ascii import Screen
from engine_card_game import raridades, classes, lista_ataques, lista_habilidades, lista_variaveis_globais, dicionario_ataques

def card_builder():
    """
    Sistema de construção de carta

    O usuário pode escolher entre:

    - Classe
    - Raridade
    - HP
    - Custo
    - Nome
    - Imagem
    - Ataques
    - Abilidades    
    """
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()

    classes, index_classes = tuple(globals()["classes"].keys()), 0
    raridades, index_raridades = tuple(globals()["raridades"].keys()), 0

    carta = {"nome":"???",
             "hp":50,
             "preco":1,
             "classe":classes[index_classes],
             "arte":None,
             "raridade":raridades[index_raridades],
             "ataques":[]
             }

    pos_ponteiro = 0

    tela = ["principal"]
    textos = {"principal":["NOME", "HP", "PRECO", "CLASSE", "ARTE", "RARIDADE", "ATAQUES", "SAVE", "LIMPAR ATAQUES"],
              "ATAQUES":["ataques", "habilidades"],
              "HP":["0 ~ 100", "100 ~ 200", "200 ~ 300", "300 ~ 400", "400 ~ 500"],
              "0 ~ 100":[str(i*10) for i in range(0, 10)],
              "100 ~ 200":[str(i*10) for i in range(10, 20)],
              "200 ~ 300":[str(i*10) for i in range(20, 30)],
              "300 ~ 400":[str(i*10) for i in range(30, 40)],
              "400 ~ 500":[str(i*10) for i in range(40, 51)],
              "~ 0 ~ 50":["0 ~ 10", "10 ~ 20", "20 ~ 30", "30 ~ 40", "40 ~ 50"],
              "0 ~ 10":[str(i) for i in range(0, 10)],
              "10 ~ 10":[str(i) for i in range(10, 20)],
              "20 ~ 30":[str(i) for i in range(20, 30)],
              "30 ~ 40":[str(i) for i in range(30, 40)],
              "40 ~ 50":[str(i) for i in range(40, 51)],
              "CLASSE":classes,
              "RARIDADE":raridades,
              "PRECO":[str(i) for i in range(6)]}

    textos = textos | dicionario_ataques
    
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    
    game_t = Thread(target = game.run)
    game_t.start()

    salvar_ataque_temporario = {"argumentos":{"image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                "nome":"???",
                                "descricao":f"???"}

    while True:
        x_carta = 105
        y_carta = 0
        
        game.add_effects(x = x_carta, y = y_carta,
                         image = base_card_complete_transparent,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        if carta["arte"] != None:
            game.add_effects(x = x_carta + 1, y = y_carta + 2,
                             image = carta["arte"],
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        game.add_effects(x = x_carta + 1, y = y_carta + 19,
                         image = put_color_rarity([list(f"{carta['raridade'].title().center(34,'=')}")],
                                                  rarity = carta["raridade"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 5, y = y_carta + 1,
                         image = put_color_class([list(f"{carta['classe'].title().center(23)}")],
                                                 class_ = carta["classe"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 29, y = y_carta + 1,
                         image = [list("HP:")],
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 32, y = y_carta + 1,
                         image = put_color_life([list(f"{carta['hp']:3}")],
                                                life = carta['hp']),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 1, y = y_carta + 18,
                         image = [list(carta['nome'].center(34))],
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 2, y = y_carta + 1,
                         image = put_color_rarity([list(f"({carta['preco']})")],
                                                  rarity = carta["raridade"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        pos = 21
        for iteracao in carta["ataques"]:
            if iteracao["tipo"] == "ataque":
                texto_descricao = [list(f"{iteracao['nome']} ({iteracao['dado']}) ({iteracao['tipo'].title()})")]
            else:
                texto_descricao = [list(f"{iteracao['nome']} ({iteracao['tipo'].title()})")]
                
            game.add_effects(x = x_carta + 2, y = y_carta + pos,
                             image = put_color_tipo(texto_descricao,
                                                    tipo = iteracao["tipo"]),
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            descricao = ajustar_descricao(iteracao["descricao"])

            game.add_effects(x = x_carta + 2, y = y_carta + pos + 2,
                             image = descricao,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            pos += 3 + len(descricao)

        pos_texto_x, pos_texto_y = 2, 0
        nivel_complementar = 0
        if tela[0] == "principal":
            texto_principal = f"Use as teclas (A, W, S, D, ENTER) para iteragir"
            game.buffer_text = texto_principal

            for nivel in range(len(tela)):
                adicao_x = 0
                iteracao = 0
                for texto in textos[tela[nivel]]:

                    if adicao_x >= x_carta - 10:
                        adicao_x = 0
                        nivel_complementar += 1
                    
                    game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 3) * (nivel + nivel_complementar),
                                     image = caixa_texto(texto, limite = len(texto) + 4),
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                    if nivel == len(tela) - 1 and iteracao == pos_ponteiro:
                        pos_seta_x = pos_texto_x + adicao_x + (len(texto) - 1)//2
                        pos_seta_y = (pos_texto_y + 3) * (nivel + nivel_complementar) + 3

                    adicao_x += len(texto) + 5
                    iteracao += 1

            game.add_effects(x = pos_seta_x, y = pos_seta_y,
                             image = seta_cima_pequena,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
        resp = input()
        if resp.lower() == "a" or resp.lower() == "q":
            pos_ponteiro = max(pos_ponteiro - 1, 0)
        elif resp.lower() == "d" or resp.lower() == "e":
            pos_ponteiro = min(pos_ponteiro + 1, len(textos[tela[-1]]) - 1)
        elif resp == "":
            if "principal" in tela:
                if "voltar" == textos[tela[-1]][pos_ponteiro]:
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                    carta["ataques"].append(salvar_ataque_temporario)
                    salvar_ataque_temporario = {"argumentos":{"image":{"image":animacao_espada,
                                                                       "frames":6,
                                                                       "wait":5,
                                                                       "to_start":0,
                                                                       "x":10,
                                                                       "y":3}},
                                                "nome":"???",
                                                "descricao":f"???"}
                    
                elif len(tela) == 3 and "HP" in tela[1]:
                    carta["hp"] = int(textos[tela[-1]][pos_ponteiro])
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "CLASSE" in tela[1]:
                    carta["classe"] = textos[tela[-1]][pos_ponteiro]
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "RARIDADE" in tela[1]:
                    carta["raridade"] = textos[tela[-1]][pos_ponteiro]
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "PRECO" in tela[1]:
                    carta["preco"] = int(textos[tela[-1]][pos_ponteiro])
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 1 and "NOME" == textos[tela[-1]][pos_ponteiro]:
                    carta["nome"] = input("Coloque o nome: ")
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 1 and "ARTE" == textos[tela[-1]][pos_ponteiro]:
                    artes = sorted(listdir(FOLDER_ART))
                    textos["ARTE"] = artes
                    tela.append(textos[tela[-1]][pos_ponteiro])
                    pos_ponteiro = min(pos_ponteiro, len(artes) - 1)

                elif len(tela) == 1 and "SAVE" == textos[tela[-1]][pos_ponteiro]:
                    with open(f"{FOLDER_CARDS_MODS}/{carta['nome']}", "w") as salvar_carta:
                        json.dump(carta, salvar_carta, indent = 4)

                elif len(tela) == 1 and "LIMPAR ATAQUES" == textos[tela[-1]][pos_ponteiro]:
                    carta["ataques"] = []

                elif len(tela) == 2 and "ARTE" in tela[1]:
                    with open(f"{FOLDER_ART}/{textos[tela[-1]][pos_ponteiro]}") as arte_da_carta:
                        arte_final = arte_da_carta.read().split("\n")
                        arte_final = arte_final[:ART_WIDTH]
                        for i in range(len(arte_final)):
                            if len(arte_final[i]) > HEIGHT_ART:
                                arte_final[i] = arte_final[i][:HEIGHT_ART]
                    carta["arte"] = adjust_image(arte_final)
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif (not textos[tela[-1]][pos_ponteiro] in textos) and (tela[2] == "ataques" or tela[2] == "habilidades"):
                    if tela[2] == "ataques":
                        salvar_ataque_temporario["funcao"] = tela[3]
                        salvar_ataque_temporario["tipo"] = "ataque"
                        if tela[4] == "dado":
                            salvar_ataque_temporario["dado"] = int(textos[tela[-1]][pos_ponteiro])
                        else:
                            salvar_ataque_temporario["argumentos"][tela[4]] = textos[tela[-1]][pos_ponteiro]
                    tela = tela[0:4]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                    print(salvar_ataque_temporario)
                    input()

                else:
                    tela.append(textos[tela[-1]][pos_ponteiro])
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                            
            else:
                pass

        elif resp.lower() == "m":
            break

    game_t.join()
    game.close()

if __name__ == "__main__":
    card_builder()
