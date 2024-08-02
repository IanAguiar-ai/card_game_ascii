from engine_card_game import CARTAS
from random import random
from game_config import *
from threading import Thread
from arts import *
from time import sleep, time
from colors_terminal import colors
from choose_deck import to_list, animation_image, put_color, clear, put_color_life, put_color_class, put_color_tipo, put_color_rarity, ajustar_descricao

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

    def close(self) -> None:
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
            
        return continua
    
    def run(self):
        """
        Roda o jogo
        """
        self.estats_animation()
        while self.in_run:
            if self.animation or self.estats_animation():
                #Empty space:
                buffer = ["\n" if i % self.x == 0 else " " for i in range(self.x * self.y)]
                #buffer = campo[].copy()
                
                #Print buffer:
                self.add_temporary(Element(x = DISPOSITION_X_TEXT, y = DISPOSITION_Y_TEXT, image = to_list(self.buffer_text)))
                
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

def abrir_pacote() -> None:
    chances = [0.02, 0.08, 0.25, 0.65]
    chances = [sum(chances[0:i+1]) for i in range(0, len(chances))]
    raridade = ["lendario", "epico", "raro", "comum"]

    num_aleat = random()
    for i in range(len(chances)):
        if num_aleat < chances[i] and not "abrir" in locals():
            abrir = raridade[i]

    possiveis = []
    for key in CARTAS.keys():
        if CARTAS[key]["raridade"] == abrir:
            possiveis.append([key, CARTAS[key]["nome"]])

    escolher = int(len(possiveis)*random())
    carta = possiveis[escolher]

    return abrir, carta

if __name__ == "__main__":
    game = Screen(x = X, y = Y, fps = FPS)      

    game.buffer_text = f"Aperte:\n(1) Para jogar\n(2) Para ir até a loja"
    
    game_t = Thread(target = game.run)
    game_t.start()

    pos_n = [0, 50, 0]
    posicoes = [i for i in range(0, 50)]
    posicoes.extend(i for i in range(49, 0, -1))
    
    while True:
        game.add_effects(x = 65, y = 3,
                        image = castelo_menu,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
    

        game.add_effects(x = 3, y = 3,
                        image = nome,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        
        game.add_effects(x = 20 + posicoes[pos_n[0]], y = 18,
                        image = nuvem_1,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)        

        game.add_effects(x = 50 + posicoes[pos_n[1]], y = 12,
                        image = nuvem_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        game.add_effects(x = 70 + posicoes[pos_n[2]], y = 20,
                        image = nuvem_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        for i in range(len(pos_n)):
            if random() > 0.8:
                pos_n[i] = (pos_n[i]+1)%len(posicoes)
        
        sleep(0.5)
    
    game.close()
    game_t.join()
    del game
        