from random import random
import json
import os
from game_config import *

def to_list(text:str) -> list:
    """
    Passa um texto para lista
    """
    lsts = text.split("\n")
    n_l = []
    for lst in lsts:
        n_l.append(list(lst))
    return n_l

def animation_image(image, frames:int, tipe = None) -> None:
    """
    Animação para colocar a carta
    """
    if image["tipe"] == "espada" or image["tipe"] == "aleatorio" or image["tipe"] == None:
        for i in range(len(image["image"])):
            for j in range(len(image["image"][i])):
                if random() < 1/frames:
                    image["animation"][i][j] = image["image"][i][j]

    elif image["tipe"] == "vertical": #conferir
        image["animation"][-1][-1] == image["image"][-1][-1] 
        for i in range(len(image["image"])):
            for j in range(len(image["image"][i])):
                if image["animation"][i][j] == image["image"][i][j]:
                    try:
                        image["animation"][i-1][j] == image["image"][i-1][j]
                    except:
                        pass
                        
                    try:
                        image["animation"][i][j-1] == image["image"][i][j-1]
                    except:
                        pass

    elif image["tipe"] == "hacker":
        letters = [chr(i) for i in range(48, 127)]
        for i in range(len(image["image"])):
            for j in range(len(image["image"][i])):
                if random() < 1/frames:
                    image["animation"][i][j] = image["image"][i][j]
                else:
                    if image["image"][i][j] != image["animation"][i][j]:
                        image["animation"][i][j] = letters[int(random()*len(letters))]
                        
    elif image["tipe"] == "bug":
        letters = [chr(i) for i in range(48, 127)]
        for i in range(len(image["image"])):
            for j in range(len(image["image"][i])):
                if random() < 0.9:
                    image["animation"][i][j] = image["image"][i][j]
                else:
                    image["animation"][i][j] = letters[int(random()*len(letters))]

    elif image["tipe"] == "bug_rapido":
        letters = [chr(i) for i in range(48, 127)]
        if random() < 0.99:
            for i in range(len(image["image"])):
                for j in range(len(image["image"][i])):
                    if random() < 0.8:
                        image["animation"][i][j] = image["image"][i][j]
                    else:
                        image["animation"][i][j] = letters[int(random()*len(letters))]
        else:
            for i in range(len(image["image"])):
                for j in range(len(image["image"][i])):
                    image["animation"][i][j] = image["image"][i][j]

def clear():
    print("\033c", end="")

def clear_all(lines = (Y)):
    for _ in range(lines+100):
        #print("\r", end = "")  # Retorna ao início da linha
        print("\033[F", end = "")  # Move o cursor para cima
        #print(" " * 80, end="")  
        #print("\r", end="")  # Retorna ao início da linha para prepará-la para ser reescrita
        
    print("\r", end = "")  # Retorna ao início da linha

def put_color(text: list, color: int = 190, back_color: int = None, style: int = 0, end = "\n") -> list:
    if style == 0:
        for i in range(len(text)):
            if back_color is not None:
                text[i][0] = f"\033[48;5;{back_color}m\033[38;5;{color}m" + text[i][0]
            else:
                text[i][0] = f"\033[38;5;{color}m" + text[i][0]
            text[i][-1] = text[i][-1] + f"\033[0m"
        return text
    else:
        style = f"\033[{style}m"
        if back_color is not None:
            return f"{style}\033[48;5;{back_color}m\033[38;5;{color}m{text}\033[0m"
        else:
            return f"{style}\033[38;5;{color}m{text}\033[0m"

def put_color_life(text, life) -> list:
    l = life//20
    values_color = [196, 202, 208, 214, 220, 226, 227, 228,192, 194, 195]
    try:
        color = values_color[l]
    except:
        color = 15
    return put_color(text = text, color = color)

def put_color_class(text, class_) -> list:
    colors_class = {"humano":51,
                    "guerreiro":9,
                    "monstro":3,
                    "noturno":63,
                    "assasino":8,
                    "lenda":226}
    if class_ in colors_class:
        color = colors_class[class_]
    else:
        color = 15
    return put_color(text = text, color = color)

def put_color_tipo(text, tipo) -> list:
    colors_class = {"habilidade":45,
                    "ataque":196}
    if tipo in colors_class:
        color = colors_class[tipo]
    else:
        color = 15
    return put_color(text = text, color = color)

def put_color_rarity(text, rarity) -> list:
    colors_class = {"comum":219,
                    "raro":37,
                    "epico":99,
                    "lendario":214}
    if rarity in colors_class:
        color = colors_class[rarity]
    else:
        color = 15
    return put_color(text = text, color = color)

def ajustar_descricao(desc:str):
    """
    Ajusta a descrição para mostrar no choose_deck.py
    """
    desc = desc.split(" ")
    final = []
    temp = [" ", " "]
    tamanho = 0
    
    for i in range(len(desc)):
        tamanho += len(desc[i]) + 1
        if tamanho < 32:
            temp.extend([*list(desc[i]), " "])
        else:
            final.append(temp)
            temp = [*list(desc[i]), " "]
            tamanho = len(desc[i]) + 1

    final.append(temp)
    return final

def criar_save() -> dict:
    """
    Cria o save:
    """
    data = {"cartas": [], "moedas": 1000, "deck":None}
    with open(SAVE_SAVE, "w") as json_file:
        json.dump(data, json_file, indent = 4)
    return data

def ler_save() -> dict:
    """
    Lê o save:
    """
    if os.path.exists(SAVE_SAVE):
        with open(SAVE_SAVE, "r") as json_file:
            data = json.load(json_file)
        return data
    else:
        return None

def adicionar_save(data:dict) -> None:
    """
    Adiciona ao save:
    """
    with open(SAVE_SAVE, "w") as json_file:
        json.dump(data, json_file, indent = 4)  

