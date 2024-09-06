"""
Código de tradução do jogo, todos os textos do jogo devem passar pela função de tradução
"""

from game_config import LANGUAGE

dict_translate_text = {"Aperte": "Press",
                       "Para jogar": "To play",
                       "Para ir até a loja": "To go to the store",
                       "Construtor de cartas": "Card Builder",
                       "Jogar": "Play",
                       "Ir a loja": "Go to the store",
                       "MOEDAS": "COINS",
                       "CARTAS OBTIDAS": "CARDS OBTAINED",
                       "Para alternar entre páginas": "To switch between pages",
                       "Para escolher entre itens": "To choose between items"}

dict_translate_reorganized = sorted(dict_translate_text.keys(),
                                     key = lambda x: len(x), reverse=True)

dict_translate = {}
for key in dict_translate_reorganized:
    dict_translate[key] = dict_translate_text[key]

del dict_translate_reorganized
del dict_translate_text

#Ajustar dicionário da maior key para a menor

def translator(text:str, dict_translate:dict = dict_translate) -> str:
    """
    Traduz o texto de acordo com o dicionario conhecido
    """
    if LANGUAGE == "pt":
        return text

    elif LANGUAGE == "ing":
        for key in dict_translate:
            if key in text:
                text = text.replace(key, dict_translate[key])

        return text

if __name__ == "__main__":
    print(dict_translate)
    texto = f"Aperte:\n(1) Jogar\n(2) Ir a loja\n(3) Construtor de cartas"
    novo_texto = translator(texto)
    print(novo_texto)
