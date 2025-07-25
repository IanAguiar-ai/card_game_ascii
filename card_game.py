"""
Card game from terminal
"""

from colors_terminal import colors
from time import sleep, time
from arts import *
from threading import Thread
from game_config import *
from random import random
from auxiliary_functions import *
from translator import translate

class Screen:
    def __init__(self, x:int, y:int, fps:int = 30):
        self.x = x
        self.y = y
        self.fps = fps
        self.elements = []
        self.temporary = []
        self.size = x*y
        self.buffer_text = ""
        self.animation = True
        self.effects = {}
        self.in_run = True

    def close(self):
        self.in_run = False

    def add_effects(self, x:int, y:int, image:list, frames:int = 8, tipe:str = None, wait:int = 16, to_start:int = 0) -> None:
        self.effects[str(random()*1_000_000)] = {"x":x,
                                                 "y":y,
                                                 "frames":frames,
                                                 "tipe":tipe,
                                                 "image":image,
                                                 "animation":[["" for i in range(len(image[j]))] for j in range(len(image))],
                                                 "wait":wait + frames + 1,
                                                 "to_start":to_start}
        
    def estats_animation(self, TIMES) -> bool:
        continua = False
        x__ = 0
        for x_ in DISPOSITION_X_CARDS:
            y__ = 0
            for y_ in DISPOSITION_Y_CARDS:
                if not "x" in TIMES[y__][x__]:
                    TIMES[y__][x__]["x"] = x_
                if not "y" in TIMES[y__][x__]:
                    TIMES[y__][x__]["y"] = y_
    
                if not "hp_temp" in TIMES[y__][x__]:
                    TIMES[y__][x__]["hp_temp"] = TIMES[y__][x__]["hp"]
                if TIMES[y__][x__]["hp"] < TIMES[y__][x__]["hp_temp"]:
                    TIMES[y__][x__]["hp_temp"] -= 1
                    continua = True
                elif TIMES[y__][x__]["hp"] > TIMES[y__][x__]["hp_temp"]:
                    TIMES[y__][x__]["hp_temp"] += 1
                    continua = True

                #Cartas:
                self.add_temporary(Element(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(translate(f"{TIMES[y__][x__]['raridade'].title().center(34,'=')}"))], rarity = TIMES[y__][x__]['raridade'])]))
                self.add_temporary(Element(x = x_ + 5, y = y_ + 1, image = [*put_color_class([list(translate(f"{TIMES[y__][x__]['classe'].title().center(23)}"))], class_ = TIMES[y__][x__]['classe'])]))
                self.add_temporary(Element(x = x_ + 29, y = y_ + 1, image = [list("HP:")]))
                self.add_temporary(Element(x = x_ + 32, y = y_ + 1, image = [*put_color_life([list(f"{TIMES[y__][x__]['hp_temp']:3}")], life = TIMES[y__][x__]['hp_temp'])]))
                self.add_temporary(Element(x = x_ + 1, y = y_ + 18, image = [list(translate(f"{TIMES[y__][x__]['nome'].center(34)}"))]))
                self.add_temporary(Element(x = x_ + 2, y = y_ + 1, image = [*put_color_rarity([list(f"({TIMES[y__][x__]['preco']})")], rarity = TIMES[y__][x__]['raridade'])]))
                if TIMES[y__][x__]['arte'] != None:
                    if not "arte_morto" in TIMES[y__][x__]:
                        self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = TIMES[y__][x__]['arte']))
                    else:
                        if TIMES[y__][x__]["hp"] > 0:
                            self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = TIMES[y__][x__]['arte']))
                        else:
                            self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = TIMES[y__][x__]['arte_morto']))
                            
                if "veneno" in TIMES[y__][x__]:
                    self.add_temporary(Element(x = x_ + 32, y = y_ + 2, image = [*put_color_tipo([list(f"-{TIMES[y__][x__]['veneno']}")], tipo = "veneno")]))
                if "buff_cura" in TIMES[y__][x__]:
                    self.add_temporary(Element(x = x_ + 36, y = y_ + 1, image = [*put_color_tipo([list(f"+{TIMES[y__][x__]['buff_cura']}")], tipo = "cura")]))
                if "buff_dano" in TIMES[y__][x__]:
                    self.add_temporary(Element(x = x_ + 36, y = y_ + 2, image = [*put_color_tipo([list(f"+{TIMES[y__][x__]['buff_dano']}")], tipo = "dano")]))
                if "buff_escudo" in TIMES[y__][x__]:
                    self.add_temporary(Element(x = x_ + 36, y = y_ + 3, image = [*put_color_tipo([list(f"-{TIMES[y__][x__]['buff_escudo']}")], tipo = "escudo")]))
                #if "espinho" in TIMES[y__][x__]:
                #    self.add_temporary(Element(x = x_ - 3, y = y_ + 1, image = [*put_color_tipo([list(f"-{TIMES[y__][x__]['espinho']}")], tipo = "espinho")]))
                            

                #Animacoes:
                to_pop = []
                for animation in self.effects.keys():
                    if self.effects[animation]["to_start"] > 0:
                        self.effects[animation]["to_start"] -= 1
                    else:
                        if self.effects[animation]["image"] != self.effects[animation]["animation"] or self.effects[animation]["wait"] > 0:
                            animation_image(self.effects[animation], self.effects[animation]["frames"])
                            self.add_temporary(Element(x = self.effects[animation]["x"], y = self.effects[animation]["y"], image = self.effects[animation]["animation"]))
                            continua = True
                            self.effects[animation]["wait"] -= 1
                        else:
                            to_pop.append(animation)

                for key in to_pop:
                    del self.effects[key]
                
                y__ += 1
            x__ += 1
            
        return continua

    def run(self, TIMES):
        self.estats_animation(TIMES)
        while self.in_run or self.animation:
            if self.animation or self.estats_animation(TIMES) or not "hp_temp" in TIMES[0][0]:
                #Empty space:
                #buffer = ["\n" if i % self.x == 0 else " " for i in range(self.x * self.y)]
                buffer = campo.copy()
                
                #Print buffer:
                self.add_temporary(Element(x = DISPOSITION_X_TEXT, y = DISPOSITION_Y_TEXT, image = to_list(translate(self.buffer_text))))
                
                self.put(buffer)        
                clear()
                print("".join(buffer))
                self.animation = False
            sleep(1/self.fps)

    def put(self, buffer) -> list:
        """
        Coloca a imagem na tela
        """
        for subs in [self.elements, self.temporary]:
            for element in subs:
                y = 0
                for list_values in element.image:
                    x = 0
                    for value in list_values:
                        if value != "" and value != "&":
                            try:
                                buffer[((element.y + y) * (self.x)) + (element.x + x)] = value
                            except:
                                pass
                        x += 1
                    y += 1

        self.temporary = []

    def add(self, elements:"Elements") -> None:
        """
        Adiciona fixo
        """
        self.elements = elements

    def add_temporary(self, elements:"Elements") -> None:
        """
        Adiciona temporariamente
        """
        if "§" in self.temporary:
            self.temporary = []
        else:
            self.temporary.append(elements)
            

class Element:
    def __init__(self, x:int, y:int, image:list):
        self.x = x
        self.y = y
        self.image = image

def build_cards(time_inimigo:list) -> list:
    """
    Pega o nome das cartas e coloca elas com todas suas propriedades na lista
    """
    from engine_card_game import CARTAS
    from copy import deepcopy
    
    nova_lista = []
    for inimigo in time_inimigo:
        nova_lista.append(deepcopy(CARTAS[inimigo]))

    return nova_lista

def run_the_game(time_inimigo:list = None) -> None:
    """
    Roda o jogo, caso receba o parâmetro time_inimigo, ele roda o jogo com o time inimigo vs o time escolhido no deck que está na memória
    """
    from engine_card_game import CARTAS, jogar, game

    memoria_save = ler_save()    
        
    #Object definitions:
    cards_base = []
    for x_ in DISPOSITION_X_CARDS:
        for y_ in DISPOSITION_Y_CARDS:
            cards_base.append(Element(x_, y_, base_card))

    #Add elements in game:
    game.add([*cards_base, ])

    if time_inimigo == None:
        while True:
            aleatorios = [list(CARTAS.keys())[int(len(CARTAS.keys())*random())] for i in range(3)]
            if 4 <= CARTAS[aleatorios[0]]["preco"] + CARTAS[aleatorios[1]]["preco"] + CARTAS[aleatorios[2]]["preco"] <= 5:
                break

        TIMES = [[CARTAS[aleatorios[0]].copy(),
                  CARTAS[aleatorios[1]].copy(),
                  CARTAS[aleatorios[2]].copy()],
                 [CARTAS[memoria_save["deck"][0]].copy(),
                  CARTAS[memoria_save["deck"][1]].copy(),
                  CARTAS[memoria_save["deck"][2]].copy()]]
    else:
        TIMES = [time_inimigo,
                 [CARTAS[memoria_save["deck"][0]].copy(),
                  CARTAS[memoria_save["deck"][1]].copy(),
                  CARTAS[memoria_save["deck"][2]].copy()]]

    logica = Thread(target = jogar, args = [TIMES])
    game_ = Thread(target = game.run, args = [TIMES])

    logica.start()
    game_.start()

    logica.join()
    sleep(3)
    game.close()
    game_.join()

    del game
    del game_
    del logica

#=================================================================
#Game definitions:
if __name__ == "__main__":
    from engine_card_game import CARTAS, jogar
    
    #Object definitions:
    cards_base = []
    for x_ in DISPOSITION_X_CARDS:
        for y_ in DISPOSITION_Y_CARDS:
            cards_base.append(Element(x_, y_, base_card))

    #Add elements in game:
    game.add([*cards_base, ])

    while True:
        aleatorios = [list(CARTAS.keys())[int(len(CARTAS.keys())*random())] for i in range(3)]
        if 4 <= CARTAS[aleatorios[0]]["preco"] + CARTAS[aleatorios[1]]["preco"] + CARTAS[aleatorios[2]]["preco"] <= 5:
            break

    #Adicionado cartas
    TIMES = [[CARTAS[aleatorios[0]].copy(),
              CARTAS[aleatorios[1]].copy(),
              CARTAS[aleatorios[2]].copy()],
             [CARTAS["senhor_balao"].copy(),
              CARTAS["meca_fogueteiro"].copy(),
              CARTAS["fenix"].copy()]]

    logica = Thread(target = jogar, args = [TIMES])
    game = Thread(target = game.run, args = [TIMES])

    logica.start()
    game.start()

    game.join()
    logica.join()        
