from engine_card_game import CARTAS
from random import random
from game_config import *
from threading import Thread
from arts import *
from time import sleep, time
from colors_terminal import colors
from auxiliary_functions import *
from choose_deck import choose_deck_animation
from open_booster import abrir_pacote_com_carta

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

def animacao_menu() -> None:
    pos_n = [0, 50, 0]
    posicoes = [i for i in range(0, 50)]
    posicoes.extend(i for i in range(49, 0, -1))
    
    while globals()["gatilho_menu"]:
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

def entrar_loja() -> None:
    def animacao_loja() -> None:
        while globals()["gatilho_loja"]:
            game.add_effects(x = 85, y = 3,
                            image = loja,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            game.add_effects(x = 5, y = 3,
                            image = caixa_ferramentas,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            game.add_effects(x = 124, y = 24,
                            image = vela,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)           

            if random() < 0.05:
                game.add_effects(x = 112, y = 16,
                            image = piscando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)

            if random() < 0.3:
                game.add_effects(x = 125, y = 24,
                            image = fumaca_vela,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0) 
            sleep(0.25)

    globals()["gatilho_loja"] = True
    game.buffer_text = f"Bem vindo a loja amigo!\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar"
    thread_animacao_loja = Thread(target = animacao_loja)
    thread_animacao_loja.start()

    while True:
        game.buffer_text = f"Bem vindo a loja amigo!\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar"
        
        resposta = input()
        
        try:
            resposta = int(resposta)
        except:
            pass
        if resposta == 1: #Escolher o deck
            #Animação do em balão do vendedor falando 'Muito bem, escolha seu deck na mesa...'
            sleep(0)
            globals()["gatilho_loja"] = False
            thread_animacao_loja.join()
            del thread_animacao_loja
            globals()["gatilho_loja"] = True
            choose_deck_animation()
            thread_animacao_loja = Thread(target = animacao_loja)
            thread_animacao_loja.start()
            globals()["gatilho_loja"] = True
            
        elif resposta == 2: #Comprar um booster
            globals()["gatilho_loja"] = False
            thread_animacao_loja.join()
            abrir_pacote_com_carta()
            del thread_animacao_loja
            globals()["gatilho_loja"] = True
            thread_animacao_loja = Thread(target = animacao_loja)
            thread_animacao_loja.start()

if __name__ == "__main__":
    game = Screen(x = X, y = Y, fps = FPS)      
    game.buffer_text = f"Aperte:\n(1) Para jogar\n(2) Para ir até a loja"
    game_t = Thread(target = game.run)
    game_t.start()

    gatilho_menu = True
    animacao_menu_thread = Thread(target = animacao_menu)
    animacao_menu_thread.start()
    
    while True:
        resposta = input()
        try:
            resposta = int(resposta)
        except:
            pass
        if type(resposta) == int and 1 <= resposta <= 2:
            gatilho_menu = False
            if resposta == 1:
                pass #Ir para o jogo
            elif resposta == 2:
                entrar_loja()
                pass #Ir para a loja
    
    game.close()
    game_t.join()
    
    del game
        
