"""
Sistema de construção de cartas
"""

from random import random
from threading import Thread
from game_config import *
from arts import *
from auxiliary_functions import *
from pure_engine_ascii import Screen
from engine_card_game import raridades, classes

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
             "arte":janela,
             "raridade":raridades[index_raridades],
             "ataques":[]
             }

    pos_ponteiro = 0

    tela = ["principal"]
    textos = {"principal":["NOME", "HP", "PRECO", "CLASSE", "ARTE", "RARIDADE", "ATAQUES"],
              "HP":[str(int(i)) for i in range(1, 21)]}
    
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    
    game_t = Thread(target = game.run)
    game_t.start()
    
    

    while True:        
        x_carta = 105
        y_carta = 0
        
        game.add_effects(x = x_carta, y = y_carta,
                         image = base_card_complete_transparent,
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

        iteracao = 0
        pos_texto_x, pos_texto_y = 3, 0
        if tela[0] == "principal":
            texto_principal = f"Use as teclas (A, W, S, D, ENTER) para iteragir"
            game.buffer_text = texto_principal

            for nivel in range(len(tela)):
                adicao_x = 0
                for texto in textos[tela[nivel]]:
                    game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 4) * len(tela),
                                     image = caixa_texto(texto, limite = len(texto) + 4),
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                    if nivel == len(tela) - 1 and iteracao == pos_ponteiro:
                        game.add_effects(x = pos_texto_x + adicao_x + (len(texto) - 1)//2, y = (pos_texto_y + 4) * len(tela) + 3,
                                         image = seta_cima_pequena,
                                         frames = 1,
                                         tipe = None,
                                         wait = 0,
                                         to_start = 0)

                    adicao_x += len(texto) + 5
                    iteracao += 1

        resp = input()
        if resp.lower() == "a" or resp.lower() == "q":
            pos_ponteiro = max(pos_ponteiro - 1, 0)
        elif resp.lower() == "d" or resp.lower() == "e":
            pos_ponteiro = min(pos_ponteiro + 1, len(textos[tela[-1]]) - 1)
        elif resp == "":
            tela.append(textos[tela[-1]][pos_ponteiro])
            pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

    game_t.join()
    game.close()

if __name__ == "__main__":
    card_builder()