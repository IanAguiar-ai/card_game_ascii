from colors_terminal import colors
from time import sleep, time
from arts import *
from threading import Thread
from game_config import *
from random import random
from engine_card_game import CARTAS, jogar, buffer_, cl
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
        self.morto = False
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
        
    def estats_animation(self) -> bool:
        continua = False
        x__ = 0
        for x_ in DISPOSITION_X_CARDS:
            y__ = 0
            for y_ in DISPOSITION_Y_CARDS[:1]:
                if not "x" in self.TIMES[y__][x__]:
                    self.TIMES[y__][x__]["x"] = x_
                if not "y" in self.TIMES[y__][x__]:
                    self.TIMES[y__][x__]["y"] = y_
    
                if not "hp_temp" in self.TIMES[y__][x__]:
                    self.TIMES[y__][x__]["hp_temp"] = self.TIMES[y__][x__]["hp"]
                if self.TIMES[y__][x__]["hp"] < self.TIMES[y__][x__]["hp_temp"]:
                    self.TIMES[y__][x__]["hp_temp"] -= 1
                    continua = True
                elif self.TIMES[y__][x__]["hp"] > self.TIMES[y__][x__]["hp_temp"]:
                    self.TIMES[y__][x__]["hp_temp"] += 1
                    continua = True

                #Cartas:
                self.add_temporary(Element(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{self.TIMES[y__][x__]['raridade'].title().center(34,'=')}")], rarity = self.TIMES[y__][x__]['raridade'])]))
                self.add_temporary(Element(x = x_ + 5, y = y_ + 1, image = [*put_color_class([list(f"{self.TIMES[y__][x__]['classe'].title().center(23)}")], class_ = self.TIMES[y__][x__]['classe'])]))
                self.add_temporary(Element(x = x_ + 29, y = y_ + 1, image = [list("HP:")]))
                self.add_temporary(Element(x = x_ + 32, y = y_ + 1, image = [*put_color_life([list(f"{self.TIMES[y__][x__]['hp_temp']:3}")], life = self.TIMES[y__][x__]['hp_temp'])]))
                self.add_temporary(Element(x = x_ + 1, y = y_ + 18, image = [list(f"{self.TIMES[y__][x__]['nome'].center(34)}")]))
                self.add_temporary(Element(x = x_ + 2, y = y_ + 1, image = [*put_color_rarity([list(f"({self.TIMES[y__][x__]['preco']})")], rarity = self.TIMES[y__][x__]['raridade'])]))
                #if "espinho" in self.TIMES[y__][x__]:
                #    self.add_temporary(Element(x = x_ + 1, y = y_ + 38, image = [*put_color_tipo([list(translate(f"Espinhos: {self.TIMES[y__][x__]['espinho']}"))], tipo = "espinho")]))

                pos = 21
                for t in self.TIMES[y__][x__]["ataques"]:
                    if t["tipo"] == "ataque":
                        self.add_temporary(Element(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['dado']}) ({t['tipo'].title()})")], tipo = t['tipo'])))
                        descricao = ajustar_descricao(t["descricao"])
                        self.add_temporary(Element(x = x_ + 2, y = y_ + pos + 2, image = descricao))
                    else:
                        self.add_temporary(Element(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['tipo'].title()})")], tipo = t['tipo'])))
                        descricao = ajustar_descricao(t["descricao"])
                        self.add_temporary(Element(x = x_ + 2, y = y_ + pos + 2, image = descricao))
                    pos += 3 + len(descricao)

                if "volta" in self.TIMES[y__][x__]:
                    self.add_temporary(Element(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(translate(f"{self.TIMES[y__][x__]['volta']['nome']} (Volta)"))], tipo = "volta")))
                    descricao = ajustar_descricao(self.TIMES[y__][x__]["volta"]["descricao"])
                    self.add_temporary(Element(x = x_ + 2, y = y_ + pos + 2, image = descricao))
                
                if self.TIMES[y__][x__]['arte'] != None:
                    if not "arte_morto" in self.TIMES[y__][x__]:
                        self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = self.TIMES[y__][x__]['arte']))
                    else:
                        if not self.morto:
                            self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = self.TIMES[y__][x__]['arte']))
                        else:
                            self.add_temporary(Element(x = x_ + 1, y = y_ + 2, image = self.TIMES[y__][x__]['arte_morto']))

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
    
    def run(self):
        """
        Roda o jogo
        """       
        self.estats_animation()
        while self.in_run:
            if self.animation or self.estats_animation() or not "hp_temp" in self.TIMES[0][0]:
                #Empty space:
                #buffer = ["\n" if i % self.x == 0 else " " for i in range(self.x * self.y)]
                buffer = campo.copy()
                
                #Print buffer:
                self.add_temporary(Element(x = DISPOSITION_X_TEXT, y = DISPOSITION_Y_TEXT, image = to_list(self.buffer_text)))
                
                self.put(buffer)        
                clear()
                print("".join(buffer)) #NÃO TIRAR ESSE PRINT
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

def choose_deck_animation() -> None:
    #Object definitions:
    cards_base = []
    for x_ in DISPOSITION_X_CARDS:
        for y_ in DISPOSITION_Y_CARDS[:1]:
            cards_base.append(Element(x_, y_, base_card_complete))

    morto = False

    nomes_cartas = []
    for key in CARTAS.keys():
        nomes_cartas.append([key, CARTAS[key]["hp"], CARTAS[key]["classe"], CARTAS[key]["preco"]])

    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
    else:
        cartas_usuario = memoria_save["cartas"]

    nomes_cartas = sorted(sorted(sorted(nomes_cartas, key = lambda x : x[1]), key = lambda x : x[3]), key = lambda x : x[2], reverse = True)
    nomes_cartas = [nome[0] for nome in nomes_cartas]
    nomes_cartas = [carta if carta in cartas_usuario else None for carta in nomes_cartas]
    while None in nomes_cartas:
        nomes_cartas.remove(None)

    #Tem que deixar ele escolher só as cartas que o usuário tem
    if memoria_save != None and len(memoria_save["deck"]) == 3:
        escolhas = [nomes_cartas.index(memoria_save["deck"][0]),
                    nomes_cartas.index(memoria_save["deck"][1]),
                    nomes_cartas.index(memoria_save["deck"][2])]
    else:
        escolhas = [nomes_cartas[0],
                    nomes_cartas[1],
                    nomes_cartas[2]]

    #print(CARTAS[nomes_cartas[escolhas[0]]])
    TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]

    #Tela:
    game = Screen(x = X, y = Y, fps = FPS)
    game.add([*cards_base, ])
    game.TIMES = TIMES
    game.buffer_text = f"Aperte:\n(q, w) para escolher a primeira carta\n(a, s) para escolher a segunda carta\n(z, x) para escolher a terceira carta"
    game_t = Thread(target = game.run)
    game_t.start()

    while True:
        resp = input()
        game.animation = True
        
        if resp.lower() == "w":
            escolhas[0] = (escolhas[0] + 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]
        elif resp.lower() == "q":
            escolhas[0] = (escolhas[0] - 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]
        elif resp.lower() == "s":
            escolhas[1] = (escolhas[1] + 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]
        elif resp.lower() == "a":
            escolhas[1] = (escolhas[1] - 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]
        elif resp.lower() == "x":
            escolhas[2] = (escolhas[2] + 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]
        elif resp.lower() == "z":
            escolhas[2] = (escolhas[2] - 1) % len(nomes_cartas)
            game.TIMES = [[CARTAS[nomes_cartas[escolhas[0]]].copy(),
              CARTAS[nomes_cartas[escolhas[1]]].copy(),
              CARTAS[nomes_cartas[escolhas[2]]].copy()]]

        elif resp.lower() == "h" or resp.lower() == "m":
            if game.morto:
                game.morto = False
            else:
                game.morto = True

        elif resp.lower() == "":
            if CARTAS[nomes_cartas[escolhas[0]]]["preco"] + CARTAS[nomes_cartas[escolhas[1]]]["preco"] + CARTAS[nomes_cartas[escolhas[2]]]["preco"] <= 5:
                #Tem que colocar em um json o deck escolhido
                game.buffer_text = "Deck Escolhido!"
                sleep(1)
                memoria_save["deck"] = [nomes_cartas[escolhas[0]], nomes_cartas[escolhas[1]], nomes_cartas[escolhas[2]]]
                adicionar_save(memoria_save)
                game.close()
                break
            else:
                game.buffer_text = "O deck não pode ter mais de 5 de custo!"
                sleep(2)
                game.buffer_text = f"Aperte:\n(q, w) para escolher a primeira carta\n(a, s) para escolher a segunda carta\n(z, x) para escolher a terceira carta"
                
        sleep(0.25)
        game.animation = True
    
if __name__ == "__main__":
    choose_deck_animation()
