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
from card_game import run_the_game
from text_mission import missoes
from text_mission import conferir_missoes
from itens import itens

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
            texto_principal = f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\n\nAperte:\n(A, W, S, D) Para andar entre os itens\n(C) Para comprar {itens[pos_caixa]['nome'].lower()}"
        except:
            texto_principal = f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\n\nAperte:\n(A, W, S, D) Para andar entre os itens\n(C) Para comprar"
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
            game.add_effects(x = 14, y = 32,
                             image = caixa_texto(itens[pos_caixa]["descricao"], limite = 50),
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
    store(itens = [itens["cafe"],
                   itens["torta"],
                   itens["drink"],
                   itens["lampada_magica"]])
