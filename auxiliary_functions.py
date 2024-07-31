from random import random

def to_list(text:str) -> list:
    lsts = text.split("\n")
    n_l = []
    for lst in lsts:
        n_l.append(list(lst))
    return n_l

def animation_image(image, frames:int, tipe = None) -> None:
    if image["tipe"] == "espada" or image["tipe"] == "aleatorio" or image["tipe"] == None:
        for i in range(len(image["image"])):
            for j in range(len(image["image"][i])):
                if random() < 1/frames:
                    image["animation"][i][j] = image["image"][i][j]

    if image["tipe"] == "vertical": #conferir
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


def clear():
    print("\033c", end="")

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
