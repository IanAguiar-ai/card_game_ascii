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
             "hp":999,
             "preco":1,
             "classe":classes[index_classes],
             "arte":janela,
             "raridade":raridades[index_raridades],
             "ataques":[]
             }
    
    clear_all()
    game = Screen(x = X, y = Y, fps = 1)
    
    game_t = Thread(target = game.run)
    game_t.start()

    while True:
        texto_principal = f"Use as teclas para iteragir"
        game.buffer_text = texto_principal

        x_carta = 105
        y_carta = 0
        
        game.add_effects(x = x_carta, y = y_carta,
                         image = base_card_complete,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 1, y = y_carta + 19,
                         image = [*put_color_rarity([list(f"{raridades[index_raridades].title().center(34,'=')}")], rarity = raridades[index_raridades])],
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)
##
##        self.add_temporary(Element(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{self.TIMES[y__][x__]['raridade'].title().center(34,'=')}")], rarity = self.TIMES[y__][x__]['raridade'])]))
##        self.add_temporary(Element(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{self.TIMES[y__][x__]['raridade'].title().center(34,'=')}")], rarity = self.TIMES[y__][x__]['raridade'])]))
##        self.add_temporary(Element(x = x_ + 5, y = y_ + 1, image = [*put_color_class([list(f"{self.TIMES[y__][x__]['classe'].title().center(23)}")], class_ = self.TIMES[y__][x__]['classe'])]))
##        self.add_temporary(Element(x = x_ + 29, y = y_ + 1, image = [list("HP:")]))
##        self.add_temporary(Element(x = x_ + 32, y = y_ + 1, image = [*put_color_life([list(f"{self.TIMES[y__][x__]['hp_temp']:3}")], life = self.TIMES[y__][x__]['hp_temp'])]))
##        self.add_temporary(Element(x = x_ + 1, y = y_ + 18, image = [list(f"{self.TIMES[y__][x__]['nome'].center(34)}")]))
##        self.add_temporary(Element(x = x_ + 2, y = y_ + 1, image = [*put_color_rarity([list(f"({self.TIMES[y__][x__]['preco']})")], rarity = self.TIMES[y__][x__]['raridade'])]))
##        pos = 21
##        for t in self.TIMES[y__][x__]["ataques"]:
##            if t["tipo"] == "ataque":
##                self.add_temporary(Element(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['dado']}) ({t['tipo'].title()})")], tipo = t['tipo'])))
##                descricao = ajustar_descricao(t["descricao"])
##                self.add_temporary(Element(x = x_ + 2, y = y_ + pos + 2, image = descricao))
##            else:
##                self.add_temporary(Element(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['tipo'].title()})")], tipo = t['tipo'])))
##                descricao = ajustar_descricao(t["descricao"])
##                self.add_temporary(Element(x = x_ + 2, y = y_ + pos + 2, image = descricao))
##            pos += 3 + len(descricao)

        resp = input()


    game_t.join()
    game.close()

if __name__ == "__main__":
    card_builder()
