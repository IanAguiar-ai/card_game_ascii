from engine_card_game import CARTAS
from random import random
from game_config import *
from threading import Thread
from arts import *
from time import sleep, time
from colors_terminal import colors
from choose_deck import to_list, animation_image, put_color, clear, put_color_life, put_color_class, put_color_tipo, put_color_rarity, ajustar_descricao
from auxiliary_functions import criar_save, ler_save, adicionar_save, clear_all

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
    chances = [0.02, 0.08, 0.30, 0.60]
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

def abrir_pacote_com_carta() -> None:
    game = Screen(x = X, y = Y, fps = FPS)      

    game.buffer_text = f"Aperte qualquer tecla para abrir o pacote..."
    
    game_t = Thread(target = game.run)
    game_t.start()

    #game.effects = {}
    raridade, carta = abrir_pacote()

    if raridade == "comum":
        imagem_verso = verso_comum
        espera = 2
    if raridade == "raro":
        imagem_verso = verso_raro
        espera = 4
    if raridade == "epico":
        imagem_verso = verso_epico
        espera = 5
    if raridade == "lendario":
        imagem_verso = verso_lendario
        espera = 6

    input()
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
    for i in [5, 7, 9, 10, 13, 17, 21, 26, 32, 39, 47, 57, 68]:
        game.add_effects(x = 50, y = 2,
                        image = put_color_rarity(imagem_verso, rarity = raridade),
                        frames = 1, #espera,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        
        game.add_effects(x = 50, y = i,
                        image = abrindo_pacote_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        sleep(2/FPS)

        

    carta_descoberta = CARTAS[carta[0]].copy()
    input()
    #Cartas:
    x_, y_ = 50, 2
    frames = espera
    espera = 10000
    game.add_effects(x = 50, y = 2,
                    image = base_card_complete,
                    frames = 1,
                    tipe = None,
                    wait = espera,
                    to_start = 0)
    
    game.add_effects(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{carta_descoberta['raridade'].title().center(34,'=')}")], rarity = carta_descoberta['raridade'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{carta_descoberta['raridade'].title().center(34,'=')}")], rarity = carta_descoberta['raridade'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 5, y = y_ + 1, image = [*put_color_class([list(f"{carta_descoberta['classe'].title().center(23)}")], class_ = carta_descoberta['classe'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 29, y = y_ + 1, image = [list("HP:")], frames = frames, wait = espera)
    game.add_effects(x = x_ + 32, y = y_ + 1, image = [*put_color_life([list(f"{carta_descoberta['hp']:3}")], life = carta_descoberta['hp'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 1, y = y_ + 18, image = [list(f"{carta_descoberta['nome'].center(34)}")], frames = frames, wait = espera)
    game.add_effects(x = x_ + 2, y = y_ + 1, image = [*put_color_rarity([list(f"({carta_descoberta['preco']})")], rarity = carta_descoberta['raridade'])], frames = 1, wait = espera)
    pos = 21
    for t in carta_descoberta["ataques"]:
        if t["tipo"] == "ataque":
            game.add_effects(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['dado']}) ({t['tipo'].title()})")], tipo = t['tipo']), frames = 1, wait = espera)
            descricao = ajustar_descricao(t["descricao"])
            game.add_effects(x = x_ + 2, y = y_ + pos + 2, image = descricao, frames = frames, wait = espera)
        else:
            game.add_effects(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(f"{t['nome']} ({t['tipo'].title()})")], tipo = t['tipo']), frames = 1, wait = espera)
            descricao = ajustar_descricao(t["descricao"])
            game.add_effects(x = x_ + 2, y = y_ + pos + 2, image = descricao, frames = frames, wait = espera)
        pos += 3 + len(descricao)
    
    if carta_descoberta['arte'] != None:
        game.add_effects(x = x_ + 1, y = y_ + 2, image = carta_descoberta['arte'], frames = frames, wait = espera)

    game.buffer_text = "".join(put_color_rarity([list(f"Desbloqueado {carta[1]}!")], rarity = carta_descoberta['raridade'])[0])
    game.buffer_text += "\n\nAperte ENTER para sair..."

    #Salvando a carta desbloqueada:
    save_atual = ler_save()
    if save_atual == None:
        criar_save()
    else:
        if not carta[0] in save_atual["cartas"]:
            save_atual["cartas"].append(carta[0])
        save_atual["moedas"] -= 100
        adicionar_save(save_atual)
            
    input()

    game.close()
    game_t.join()
    del game
    return carta

if __name__ == "__main__":
    abrir_pacote_com_carta()
        
