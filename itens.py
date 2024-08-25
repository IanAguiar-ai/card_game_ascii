"""
Lista de itens que são vendidos nas lojas
"""
from arts import *

itens = {"cafe":{"imagem":item_cafe, "nome":"Café", "preco":150},
         "torta":{"imagem":item_torta, "nome":"Torta", "preco":150},
         "drink":{"imagem":item_lampada_magica, "nome":"Lâmpada Mágica", "preco":500},
         "lampada_magica":{"imagem":item_drink, "nome":"Drink", "preco":150},
         "biscoito":{"imagem":item_biscoito, "nome":"Biscoito", "preco":200},}

for key in itens.keys():
    itens[key]["id"] = key
