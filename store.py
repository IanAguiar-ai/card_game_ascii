"""
Parte gráfica e lógica da loja
"""

from random import random
from threading import Thread
from game_config import *
from arts import *
from auxiliary_functions import *
from itens import itens
from pure_engine_ascii import Screen
from translator import translate

def store(itens:list):
    """
    Printa a loja
    O usuário pode comprar itens nela
    """
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()

    pos_caixa = 0
    
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    
    game_t = Thread(target = game.run)
    game_t.start()

    while True:
        try:
            texto_principal = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\n\nAperte:\n(A, W, S, D) Para escolher entre os itens\n(C) Para comprar {itens[pos_caixa]['nome'].lower()}")
        except:
            texto_principal = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\n\nAperte:\n(A, W, S, D) Para escolher entre os itens\n(C) Para comprar")
        game.buffer_text = texto_principal
        
        game.add_effects(x = 85, y = 0,
                         image = estante,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 95, y = 22,
                         image = teia_de_aranha,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 1, y = 0,
                         image = teia_de_aranha_3,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 105, y = 20,
                         image = poutrona,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        for x in range(2):
            for y in range(2):
                if pos_caixa == x + y*2:
                    game.add_effects(x = 14 + x*36, y = 6 + y*16,
                                 image = caixa_maior,
                                 frames = 1,
                                 tipe = None,
                                 wait = 0,
                                 to_start = 0)
                
                game.add_effects(x = 15 + x*36, y = 7 + y*16,
                                 image = caixa_simples,
                                 frames = 1,
                                 tipe = None,
                                 wait = 0,
                                 to_start = 0)

                if len(itens) > x + y*2:
                    game.add_effects(x = 16 + x*36, y = 8 + y*16,
                                     image = itens[x+y*2]["imagem"],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                    preco_ = list("$" + str(itens[x+y*2]["preco"]))
                    preco_[0] = "\033[93m" + preco_[0]
                    preco_[-1] = preco_[-1] + "\033[0m"
                    game.add_effects(x = 20 + x*36, y = 14 + y*16,
                                     image = [preco_],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                    if itens[x+y*2]["id"] in memoria_save["inventario"]:
                        game.add_effects(x = 16 + x*36, y = 8 + y*16,
                                     image = caixa_simples_fechada,
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

        if "descricao" in itens[pos_caixa]:
            game.add_effects(x = 4, y = 32,
                             image = caixa_texto(itens[pos_caixa]["descricao"], limite = 70),
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
                    
        resp = input()
        if resp.lower() == "w":
            pos_caixa = max(0, pos_caixa - 2)
        elif resp.lower() == "a" or resp.lower() == "q":
            pos_caixa = max(0, pos_caixa - 1)
        elif resp.lower() == "s":
            pos_caixa = min(3, pos_caixa + 2)
        elif resp.lower() == "d" or resp.lower() == "e":
            pos_caixa = min(3, pos_caixa + 1)
        elif resp.lower() == "c":
            if len(itens) > pos_caixa and memoria_save["moedas"] >= itens[pos_caixa]["preco"] and not itens[pos_caixa]["id"] in memoria_save["inventario"]:
                memoria_save["inventario"].append(itens[pos_caixa]["id"])
                memoria_save["moedas"] -= itens[pos_caixa]["preco"]
                adicionar_save(memoria_save)

    game_t.join()
    game.close()

if __name__ == "__main__":
    store(itens = [itens["pocao_pequena"],
                   itens["torta"],
                   itens["drink"],
                   itens["biscoito"]])
