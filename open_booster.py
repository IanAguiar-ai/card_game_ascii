from engine_card_game import CARTAS
from threading import Thread
from random import random
from game_config import *
from arts import *
from time import sleep, time
from choose_deck import to_list, animation_image, put_color, clear, put_color_life, put_color_class, put_color_tipo, put_color_rarity, ajustar_descricao
from auxiliary_functions import criar_save, ler_save, adicionar_save, clear_all
from pure_engine_ascii import Screen
from translator import translate

def abrir_pacote(chances:list = [0.02, 0.08, 0.30, 0.60]) -> None:
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

def abrir_pacote_com_carta(chances:list = [0.02, 0.08, 0.30, 0.60], moedas:int = 100, exp:int = 0) -> None:
    game = Screen(x = X, y = Y, fps = FPS, campo = campo)      

    game.buffer_text = translate(f"Aperte qualquer tecla para abrir o pacote...")
    
    game_t = Thread(target = game.run)
    game_t.start()

    #game.effects = {}
    raridade, carta = abrir_pacote(chances)

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
    
    game.add_effects(x = x_ + 1, y = y_ + 19, image = [*put_color_rarity([list(f"{translate(carta_descoberta['raridade']).title().center(34,'=')}")], rarity = carta_descoberta['raridade'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 5, y = y_ + 1, image = [*put_color_class([list(f"{translate(carta_descoberta['classe']).title().center(23)}")], class_ = carta_descoberta['classe'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 29, y = y_ + 1, image = [list("HP:")], frames = frames, wait = espera)
    game.add_effects(x = x_ + 32, y = y_ + 1, image = [*put_color_life([list(f"{carta_descoberta['hp']:3}")], life = carta_descoberta['hp'])], frames = 1, wait = espera)
    game.add_effects(x = x_ + 1, y = y_ + 18, image = [list(f"{translate(carta_descoberta['nome']).center(34)}")], frames = frames, wait = espera)
    game.add_effects(x = x_ + 2, y = y_ + 1, image = [*put_color_rarity([list(f"({carta_descoberta['preco']})")], rarity = carta_descoberta['raridade'])], frames = 1, wait = espera)
    pos = 21
    for t in carta_descoberta["ataques"]:
        if t["tipo"] == "ataque":
            game.add_effects(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(translate(f"{t['nome']} ({t['dado']}) ({t['tipo'].title()})"))], tipo = t['tipo']), frames = 1, wait = espera)
            descricao = ajustar_descricao(t["descricao"])
            game.add_effects(x = x_ + 2, y = y_ + pos + 2, image = descricao, frames = frames, wait = espera)
        else:
            game.add_effects(x = x_ + 2, y = y_ + pos, image = put_color_tipo([list(translate(f"{t['nome']} ({t['tipo'].title()})"))], tipo = t['tipo']), frames = 1, wait = espera)
            descricao = ajustar_descricao(t["descricao"])
            game.add_effects(x = x_ + 2, y = y_ + pos + 2, image = descricao, frames = frames, wait = espera)
        pos += 3 + len(descricao)
    
    if carta_descoberta['arte'] != None:
        game.add_effects(x = x_ + 1, y = y_ + 2, image = carta_descoberta['arte'], frames = frames, wait = espera)

    game.buffer_text = "".join(put_color_rarity([list(translate(f"Desbloqueado {carta[1]}!"))], rarity = carta_descoberta['raridade'])[0])
    game.buffer_text += translate("\n\nAperte ENTER para sair...")

    #Salvando a carta desbloqueada:
    save_atual = ler_save()
    if save_atual == None:
        criar_save()
    else:
        if not carta[0] in save_atual["cartas"]:
            save_atual["cartas"].append(carta[0])
        else:
            if carta_descoberta['raridade'] == "comum":
                save_atual["exp"] += 5
            elif carta_descoberta['raridade'] == "raro":
                save_atual["exp"] += 10
            elif carta_descoberta['raridade'] == "epico":
                save_atual["exp"] += 25
            elif carta_descoberta['raridade'] == "lendario":
                save_atual["exp"] += 60
        save_atual["moedas"] -= moedas
        save_atual["exp"] -= exp
        adicionar_save(save_atual)
            
    input()

    game.close()
    game_t.join()
    del game
    return carta

if __name__ == "__main__":
    abrir_pacote_com_carta()
        
