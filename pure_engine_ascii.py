"""
Engine ascii para o terminal sem modificações
Em outros códigos .py no mesmo diretório tem a cópia dessa engine contudo com modificações afim de deixar um pouco mais otimizado a classe
"""
from random import random
from game_config import *
from auxiliary_functions import *
from time import sleep

class Screen:
    """
    Engine ascii crua
    Essa engine é responsável pela parte gráfica do jogo, ela deve ser rodado em paralelo a uma lógica
    O usuário faz pedidos de animação a engine e ela processa
    """
    
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
        """
        Termina o loop principal da engine
        """
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
