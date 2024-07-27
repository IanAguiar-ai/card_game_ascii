from engine_card_game import CARTAS

def dicionario_mana(cartas:list) -> dict:
    dicionario = {0:0,
                  1:0,
                  2:0,
                  3:0,
                  4:0,
                  5:0}
    for key in cartas.keys():
        dicionario[cartas[key]["preco"]] += 1

    print(f"Quantidade de cartas:")
    print(f"\tMANA{' '*3}QUANTIDADE")
    for key in dicionario:
        print(f"\t{key}:    {dicionario[key]:2}")

    return dicionario

if __name__ == "__main__":
    qnt_cartas = dicionario_mana(CARTAS)

    posibilidades = [[0, 0, 0],
                     [0, 0, 1],
                     [0, 0, 2],
                     [0, 0, 3],
                     [0, 0, 4],
                     [0, 0, 5],
                     [0, 1, 1],
                     [0, 1, 2],
                     [0, 1, 3],
                     [0, 1, 4],
                     [1, 1, 1],
                     [1, 1, 2],
                     [1, 1, 3],
                     [1, 2, 2]]

    print("\n\nCOMBINAÇÕES POSSÍVEIS COM AS CARTAS NO JOGO:")
    combinacoes = 0
    combinacoes_unicas = 0
    for p in posibilidades:
        temp = qnt_cartas[p[0]] * qnt_cartas[p[1]] * qnt_cartas[p[2]]
        combinacoes += temp

        temp_ = 1
        qnt_temp = qnt_cartas.copy()
        temp_ *= qnt_temp[p[0]]
        qnt_temp[p[0]] -= 1
        temp_ *= qnt_temp[p[1]]
        qnt_temp[p[1]] -= 1
        temp_ *= qnt_temp[p[2]]
        qnt_temp[p[2]] -= 1
        combinacoes_unicas += temp_
        
        print(f"\t{str(p):10} -> {temp:4} | {temp_:4}")

    print(f"\n\nCombinações totais: {combinacoes}")
    print(f"Combinações únicas: {combinacoes_unicas}")
    print(f"Total de cartas no jogo: {len(CARTAS.keys())}")
    
        
