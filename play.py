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
    """
    Animação da loja
    """
    
    def animacao_loja() -> None:
        em_fala = 0
        em_fala_montar_deck = 0
        em_fala_criar_deck = 0
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

            game.add_effects(x = 20, y = 26,
                            image = mesa_simples,
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

            if (memoria_save["moedas"] == 0 and memoria_save["deck"] == None) or em_fala_montar_deck > 0:
                if em_fala_montar_deck <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala_montar_deck = 30
                    
                game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                game.add_effects(x = 96, y = 6,
                                    image = instrucoes_textos[1],
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)
                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)
                    
                em_fala_montar_deck -= 1

            elif memoria_save["cartas"] == [] or em_fala_criar_deck > 0:
                if em_fala_criar_deck <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala_criar_deck = 30
                    
                game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                game.add_effects(x = 96, y = 6,
                                    image = instrucoes_textos[0],
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)
                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)
                    
                em_fala_criar_deck -= 1

            elif random() < 0.005 or em_fala > 0:
                if em_fala <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala = 30

                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)

                if len(texto_vendedor) > 3:
                    game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 6,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                elif len(texto_vendedor) > 2:
                    game.add_effects(x = 94, y = 8,
                                    image = balao_pequeno,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 10,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                elif len(texto_vendedor) > 1:
                    game.add_effects(x = 94, y = 9,
                                    image = balao_menor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 11,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                else:
                    game.add_effects(x = 94, y = 10,
                                    image = balao_unico,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 12,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)


                em_fala -= 1
            
            sleep(0.2)

    def animacao_inventario() -> None:
        memoria_save = ler_save()
        game.buffer_text = f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(Q) Para voltar uma página\n(W) Para passar uma página"
        pag = 0
        while True:
            #Inventario:

            for x in range(5):
                for y in range(4):
                    game.add_effects(x = 2 + x*12, y = 2 + y*8,
                                     image = caixa_simples,
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)
            
##            x_, y_ = 0, 0
##            for iten in memoria_save["inventario"]:
##
##                y_ += 1
##                if y_ > 15:
##                    x_ = 1
##                    y_ = 0



            #Missões:
            game.add_effects(x = 84, y = 6,
                             image = livro_aberto_grande,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            x_, y_ = 0, 0
            for missao in missoes[pag*32:(pag+1)*32]:
                if missao in memoria_save["missoes"]:
                    game.add_effects(x = 94 + x_ * 27, y = 9 + y_,
                                     image = put_color([list(missao)], color = x_*7 + y_*32),
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                else:
                    game.add_effects(x = 94 + x_ * 27, y = 9 + y_,
                                     image = [list(missao)],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                y_ += 1
                if y_ > 15:
                    x_ = 1
                    y_ = 0

            resp = input()
            if resp == "q":
                pag = max(pag - 1, 0)
            elif resp == "w":
                pag = min(pag + 1, len(missoes)//32)


    globals()["gatilho_loja"] = True
    memoria_save = ler_save()
    texto_loja = f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar boster \033[93m(100 moedas)\033[0m\n(3) Inventário\n(4) Para sair da loja"
    game.buffer_text = texto_loja
    thread_animacao_loja = Thread(target = animacao_loja)
    thread_animacao_loja.start()

    while True:
        game.buffer_text = texto_loja
        
        resposta = input()
        
        try:
            resposta = int(resposta)
        except:
            pass
        if type(resposta) == int and 1 <= resposta <= 4:
                
            if resposta == 1 and len(memoria_save["cartas"]) >= 3: #Escolher o deck
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                choose_deck_animation()
            
                globals()["gatilho_loja"] = True
                clear_all()
                memoria_save = ler_save()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
                
            elif resposta == 2 and memoria_save["moedas"] >= 100: #Comprar um booster
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                abrir_pacote_com_carta()

                globals()["gatilho_loja"] = True
                clear_all()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
                memoria_save = ler_save()
                texto_loja = f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar boster \033[93m(100 moedas)\033[0m\n(3) Inventário\n(4) Para sair da loja"

            elif resposta == 3:
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                animacao_inventario()
                
                globals()["gatilho_loja"] = True
                clear_all()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
            
            elif resposta == 4: #Sair da loja
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)
                break

if __name__ == "__main__":
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
        
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    texto_principal = f"Aperte:\n(1) Para jogar\n(2) Para ir até a loja"
    game.buffer_text = texto_principal
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
            animacao_menu_thread.join()
            del animacao_menu_thread

            if resposta == 1: #Ir para o jogo
                run_the_game()
                gatilho_menu = True
                game.buffer_text = texto_principal
                animacao_menu_thread = Thread(target = animacao_menu)
                animacao_menu_thread.start()

            elif resposta == 2: #Ir para a loja
                entrar_loja()
                gatilho_menu = True
                game.buffer_text = texto_principal
                animacao_menu_thread = Thread(target = animacao_menu)
                animacao_menu_thread.start()

    game.close()
    game_t.join()

    del game
