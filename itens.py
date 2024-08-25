"""
Lista de itens que são vendidos nas lojas
"""
from arts import *

itens = {"cafe":{"imagem":item_cafe, "nome":"Café", "preco":150,
                 "descricao":"Essa xícara de café fumegante, tem um aroma rico e o sabor robusto do Café proporcionam um bônus de moral. Ideal para aqueles momentos em que um impulso extra é necessário para superar desafios difíceis."},
         "torta":{"imagem":item_torta, "nome":"Torta", "preco":150,
                  "descricao":"Teste 2"},
         "drink":{"imagem":item_lampada_magica, "nome":"Lâmpada Mágica", "preco":500},
         "lampada_magica":{"imagem":item_drink, "nome":"Drink", "preco":150},
         "biscoito":{"imagem":item_biscoito, "nome":"Biscoito", "preco":200},}

for key in itens.keys():
    itens[key]["id"] = key

if __name__ == "__main__":
    tamanho = 0
    
    for iten in itens.keys():
        size = itens[iten].__sizeof__()
        tamanho += size
        print(f"{iten:44}: {size}")
        for sub in itens[iten].keys():
            size = itens[iten][sub].__sizeof__()
            tamanho += size
            print(f"{iten:20} -> {sub:20}: {size}")

    print(f"\nTamanho total: {tamanho:7} bytes\n{' '*len('Tamanho total: ')}{tamanho/1024:7.02f} Kb")
