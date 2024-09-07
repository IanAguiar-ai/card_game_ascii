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
                       "Para escolher entre itens": "To choose between items",
                       "Para escolher o deck": "To choose the deck",
                       "Para comprar booster": "To buy booster",
                       "Inventário": "Inventory",
                       "Para sair da loja": "To leave the store",
                       "moedas": "coins",
                       "Essa xícara de café fumegante, tem um aroma rico e o sabor robusto do Café proporcionam um bônus de moral. Ideal para aqueles momentos em que um impulso extra é necessário para superar desafios difíceis.": "This steaming cup of coffee has a rich aroma and robust flavor that provides a morale boost. Ideal for those times when an extra boost is needed to overcome difficult challenges.",
                       "Em uma noite silenciosa, uma torta apareceu misteriosamente na mesa, sua superfície brilhando sob a luz suave das velas. Ninguém sabia de onde vinha, mas todos sentiam uma presença poderosa e enigmática no ar. Quando a torta foi cortada, um aroma irresistível se espalhou, e em um piscar de olhos, ela desapareceu, deixando apenas migalhas e um leve rastro de magia no ar. Quem teria sido capaz de tal feito? A resposta permanece envolta em mistério, assim como a identidade do ser que a degustou.": "One silent night, a pie mysteriously appeared on the table, its surface glowing in the soft candlelight. No one knew where it came from, but everyone felt a powerful and enigmatic presence in the air. When the pie was cut, an irresistible aroma spread, and in the blink of an eye, it disappeared, leaving only crumbs and a faint trail of magic in the air. Who could have done such a feat? The answer remains shrouded in mystery, as does the identity of the being who tasted it.",
                       "Em uma noite envolta em mistério, um drink apareceu no balcão, sua cor profunda e cintilante refletindo segredos antigos. Criado por um alquimista? O elixir exalava um aroma de especiarias exóticas e frutas raras, atraindo olhares curiosos. Quando alguém ousou provar, o sabor era uma explosão de complexidade, em um instante, o copo estava vazio, e uma presença invisível parecia ter se retirado, deixando apenas um sussurro. O criador da bebida? A resposta permanece oculta nas sombras, alguns dizem de sobre alquimista misterioso.": "On a night shrouded in mystery, a drink appeared on the bar, its deep, shimmering color reflecting ancient secrets. Created by an alchemist? The elixir exuded an aroma of exotic spices and rare fruits, attracting curious glances. When someone dared to taste it, the flavor was an explosion of complexity; in an instant, the glass was empty, and an invisible presence seemed to have withdrawn, leaving only a whisper. Who created the drink? The answer lies hidden in the shadows, some say about a mysterious alchemist.",
                       "Em uma noite fria e silenciosa no deserto, um viajante encontrou uma antiga lâmpada de bronze enterrada na areia. O paradeiro do viajante nunca foi descoberto. A lâmpada foi vendida várias vezes, mas sempre retornava misteriosamente. Seus donos, muitos ao longo dos anos, nunca mais foram vistos nas redondezas. A lâmpada parecia carregar consigo um enigma sombrio, envolvendo todos que ousavam possuí-la em um destino incerto.": "One cold, silent night in the desert, a traveler found an ancient bronze lamp buried in the sand. The traveler's whereabouts were never discovered. The lamp was sold several times, but always returned mysteriously. Its owners, many over the years, were never seen in the area again. The lamp seemed to carry with it a dark enigma, enveloping all who dared to possess it in an uncertain fate.",
                       "Um biscoito raro e enigmático, criado por um cozinheiro cujas habilidades são lendárias. Dizem que suas criações culinárias podem curar feridas profundas ou infligir dores terríveis, além de serem extremamente apetitosas. Apenas os mais corajosos se atrevem a experimentar seus efeitos, sabendo que uma simples mordida pode mudar seu destino para sempre.": "A rare and enigmatic cookie created by a chef whose skills are legendary. It is said that his culinary creations can heal deep wounds or inflict excruciating pain, and are also extremely appetizing. Only the bravest dare to try its effects, knowing that a simple bite could change their destiny forever.",
                       "Essa é maior que o normal.": "This one is larger than normal.",
                       "Faz parte de um conjunto de poções misteriosas, cujo dono ninguém conhece. Dizem que os anões do norte sabem algo sobre a origem dessas poções. Talvez, investigando mais, você possa descobrir histórias intrigantes sobre essas poções e seus segredos.": "It is part of a set of mysterious potions, whose owner is unknown. It is said that the dwarves of the north know something about the origin of these potions. Perhaps, by investigating further, you will discover intriguing stories about these potions and their secrets.",
                       "Essa é menorzinha.": "This one is smaller.",
                       "Café": "Coffee",
                       "Torta": "Pie",
                       "Lâmpada Mágica": "Magic Lamp",
                       "Biscoito": "Cookie",
                       "Poção Grande": "Big Potion",
                       "Poção Pequena": "Small Potion",
                       "Para escolher entre os itens": "To choose between items",
                       "Para comprar": "To buy",
                       "NOME": "NAME",
                       "PRECO": "PRICE",
                       "CLASSE": "CLASS",
                       "ARTE": "ART",
                       "RARIDADE": "RARITY",
                       "ATAQUES": "ATTACKS",
                       "LIMPAR ATAQUES": "CLEAN ATTACKS"}

dict_translate_reorganized = sorted(dict_translate_text.keys(),
                                     key = lambda x: len(x), reverse=True)

dict_translate = {}
for key in dict_translate_reorganized:
    dict_translate[key] = dict_translate_text[key]

del dict_translate_reorganized
del dict_translate_text

#Ajustar dicionário da maior key para a menor

def translate(text:str, dict_translate:dict = dict_translate) -> str:
    """
    Traduz o texto de acordo com o dicionario conhecido
    """
    if type(text) == str:
        if LANGUAGE == "pt":
            return text
        
        elif LANGUAGE == "ing":
            for key in dict_translate:
                if key in text:
                    text = text.replace(key, dict_translate[key])

            return text
    return text

if __name__ == "__main__":
    print(dict_translate)
    texto = f"Aperte:\n(1) Jogar\n(2) Ir a loja\n(3) Construtor de cartas"
    novo_texto = translator(texto)
    print(novo_texto)
