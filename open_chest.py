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
        while True:
            if self.animation or self.estats_animation():
                #Empty space:
                #buffer = ["\n" if i % self.x == 0 else " " for i in range(self.x * self.y)]
                buffer = campo.copy()
                
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
            possiveis.append(CARTAS[key]["nome"])

    escolher = int(len(possiveis)*random())
    carta = possiveis[escolher]

    return abrir, carta

game = Screen(x = X, y = Y, fps = FPS)      
if __name__ == "__main__":
##    cartas = {}
##    nomes_tirados = set()
##    while len(nomes_tirados) < 1:
##        raridade, carta = abrir_pacote()
##        print(f"{raridade:10} {carta}")
##        if not raridade in cartas:
##            cartas[raridade] = 1
##        else:
##            cartas[raridade] += 1
##        nomes_tirados.add(carta)
##
##    print(cartas)
##    print(f"Cartas diferentes: {len(nomes_tirados)}")

    game.buffer_text = f"Aperte qualquer tecla para abrir o pacote..."
    
    game_t = Thread(target = game.run)
    game_t.start()

    while True:
        input()
        raridade, carta = abrir_pacote()
        game.add_effects(x = 50, y = 1,
                        image = pacote,
                        frames = 2,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        input()
        game.add_effects(x = 50, y = 1,
                        image = abrindo_pacote_1,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        input()
        game.add_effects(x = 50, y = 2,
                        image = abrindo_pacote_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        if raridade == "comum":
            imagem_verso = verso_comum
        if raridade == "raro":
            imagem_verso = verso_raro
        if raridade == "epico":
            imagem_verso = verso_epico
        if raridade == "lendario":
            imagem_verso = verso_lendario
        input()
        game.add_effects(x = 50, y = 2,
                        image = imagem_verso,
                        frames = 2,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        
        
