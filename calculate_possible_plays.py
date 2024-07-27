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
    for p in posibilidades:
        temp = qnt_cartas[p[0]] * qnt_cartas[p[1]] * qnt_cartas[p[2]]
        combinacoes += temp
        print(f"\t{str(p):10} -> {temp}")

    print(f"\n\nCombinações totais: {combinacoes}")
    print(f"{combinacoes/(len(CARTAS.keys()) * (len(CARTAS.keys()) - 1) * (len(CARTAS.keys()) - 2)) * 100:2.02f}% de todas as possibilidades...")
    print(f"Total de cartas no jogo: {len(CARTAS.keys())}")
    
        
