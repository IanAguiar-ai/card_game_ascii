"""
Lista com textos das missões

Existem 3 tipos de missões:
'inicio' <- confere sempre ao iniciar o jogo
'jogo' <- confere todo turno
'loja' <- confere sempre que entrar na loja

Todos retornos de missão devem retornar True ou False
"""

missoes = [("Nome funcao 1", None, "jogo"),
           ("Nome funcao 2", None),
           ("Nome funcao 3", None),
           ("Nome funcao 4", None),
           ("Nome funcao 5", None),
           ("Nome funcao 6", None),
           ("Nome funcao 7", None),
           ("Nome funcao 8", None),
           ("Nome funcao 9", None),
           ("Nome funcao 10", None),
           ("Nome funcao 11", None),
           ("Nome funcao 12", None),
           ("Nome funcao 13", None),
           ("Nome funcao 14", None),
           ("Nome funcao 15", None),
           ("Nome funcao 16", None),
           ("Nome funcao 17", None),
           ("Nome funcao 18", None),
           ("Nome funcao 19", None),
           ("Nome funcao 20", None),
           ("Nome funcao 21", None),
           ("Nome funcao 22", None),
           ("Nome funcao 23", None),
           ("Nome funcao 24", None),
           ("Nome funcao 25", None),
           ("Nome funcao 26", None),
           ("Nome funcao 27", None),
           ("Nome funcao 28", None),
           ("Nome funcao 29", None),
           ("Nome funcao 30", None),
           ("Nome funcao 31", None),
           ("Nome funcao 32", None),
           ("Nome funcao 33", None),
           ("Nome funcao 34", None),
           ("Nome funcao 35", None),
           ("Nome funcao 36", None),
           ("Nome funcao 37", None),
           ("Nome funcao 38", None),
           ("Nome funcao 39", None),
           ("Nome funcao 40", None),
           ("Nome funcao 41", None),
           ("Nome funcao 42", None),
           ("Nome funcao 43", None),
           ("Nome funcao 44", None),
           ("Nome funcao 45", None),
           ("Nome funcao 46", None),
           ]

def conferir_missoes(tipo:str, save:dict, **variaveis) -> dict:
    """
    Separa todas missões que serão conferidas e confere

    Retorna o novo save
    """

    #Confere quais missões serão conferidas:
    missoes_validas = [missao[:2] if len(missao) == 3 and missao[2] == tipo and (not missao[0] in save["missoes"]) else None for missao in missoes]
    while None in missoes_validas:
        missoes_validas.remove(None)

    #Confere se as missões são válidas:
    nova_missao = []
    for missao in missoes_validas:
        if missao[1] != None and missao[1](**variaveis):
            nova_missao.append(missao[0])

    #Adiciona a missão comprida, se tiver alguma, no save
    if nova_missao != []:
        save["missoes"].extend(nova_missao)
        adicionar_save(save)

    return save

