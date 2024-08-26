"""
Lista de itens que são vendidos nas lojas
"""
from arts import *

def add_espaco(imagem:list, espaco:int) -> list:
    """
    Adiciona espaco para centralizar a imagem no quadrado
    """
    for i in range(len(imagem)):
        if len(imagem[i]) > 0:
            imagem[i] = [*[" " for _ in range(espaco)], *imagem[i]]
    return imagem

itens = {"cafe":{"imagem":item_cafe, "nome":"Café", "preco":150,
                 "descricao":"Essa xícara de café fumegante, tem um aroma rico e o sabor robusto do Café proporcionam um bônus de moral. Ideal para aqueles momentos em que um impulso extra é necessário para superar desafios difíceis."},
         "torta":{"imagem":item_torta, "nome":"Torta", "preco":150,
                  "descricao":"Em uma noite silenciosa, uma torta apareceu misteriosamente na mesa, sua superfície brilhando sob a luz suave das velas. Ninguém sabia de onde vinha, mas todos sentiam uma presença poderosa e enigmática no ar. Quando a torta foi cortada, um aroma irresistível se espalhou, e em um piscar de olhos, ela desapareceu, deixando apenas migalhas e um leve rastro de magia no ar. Quem teria sido capaz de tal feito? A resposta permanece envolta em mistério, assim como a identidade do ser que a degustou."},
         "drink":{"imagem":item_drink, "nome":"Lâmpada Mágica", "preco":500,
                  "descricao":"Em uma noite envolta em mistério, um drink apareceu no balcão, sua cor profunda e cintilante refletindo segredos antigos. Criado por um alquimista? O elixir exalava um aroma de especiarias exóticas e frutas raras, atraindo olhares curiosos. Quando alguém ousou provar, o sabor era uma explosão de complexidade, em um instante, o copo estava vazio, e uma presença invisível parecia ter se retirado, deixando apenas um sussurro. O criador da bebida? A resposta permanece oculta nas sombras, alguns dizem de sobre alquimista misterioso."},
         "lampada_magica":{"imagem":item_lampada_magica, "nome":"Drink", "preco":150,
                           "descricao":"Em uma noite fria e silenciosa no deserto, um viajante encontrou uma antiga lâmpada de bronze enterrada na areia. O paradeiro do viajante nunca foi descoberto. A lâmpada foi vendida várias vezes, mas sempre retornava misteriosamente. Seus donos, muitos ao longo dos anos, nunca mais foram vistos nas redondezas. A lâmpada parecia carregar consigo um enigma sombrio, envolvendo todos que ousavam possuí-la em um destino incerto."},
         "biscoito":{"imagem":item_biscoito, "nome":"Biscoito", "preco":300,
                     "descricao":"Um biscoito raro e enigmático, criado por um cozinheiro cujas habilidades são lendárias. Dizem que suas criações culinárias podem curar feridas profundas ou infligir dores terríveis, além de serem extremamente apetitosas. Apenas os mais corajosos se atrevem a experimentar seus efeitos, sabendo que uma simples mordida pode mudar seu destino para sempre."},
         "pocao_grande":{"imagem":add_espaco(pocao[0], espaco = 2), "nome":"Poção Grande", "preco": 150,
                         "descricao":"Essa é maior que o normal. Faz parte de um conjunto de poções misteriosas, cujo dono ninguém conhece. Dizem que os anões do norte sabem algo sobre a origem dessas poções. Talvez, investigando mais, você possa descobrir histórias intrigantes sobre essas poções e seus segredos."},
         "pocao_pequena":{"imagem":add_espaco(pocao[1], espaco = 3), "nome":"Poção Pequena", "preco": 150,
                          "descricao":"Essa é menorzinha. Faz parte de um conjunto de poções misteriosas, cujo dono ninguém conhece. Dizem que os anões do norte sabem algo sobre a origem dessas poções. Talvez, investigando mais, você possa descobrir histórias intrigantes sobre essas poções e seus segredos."}}

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
