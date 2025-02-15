from engine_card_game import CARTAS

def infos(cartas:list) -> None:
    bytes_usados = 0
    for carta in cartas.keys():
        for key in cartas[carta].keys():
            bytes_usados += cartas[carta][key].__sizeof__()
    print(f"\nEstão sendo usados {bytes_usados/1024:4.02f} Kilo Bytes para armazenar as cartas.\n")
    info_ = f"Estão sendo usados {bytes_usados/1024:4.02f} Kilo Bytes para armazenar as cartas."
    
    por_classe = {}
    for key in cartas:
        if not cartas[key]["classe"] in por_classe:
            por_classe[cartas[key]["classe"]] = []
        por_classe[cartas[key]["classe"]].append({"nome": cartas[key]["nome"],
                                             "hp": cartas[key]["hp"],
                                             "preco": cartas[key]["preco"]})

    for key in por_classe:
        print(f"{key.title()} ({len(por_classe[key])}):")
        info_ += f"\n\n{key.title()} ({len(por_classe[key])}):"
        for personagem in sorted(sorted(por_classe[key], key = lambda x: x["hp"]), key = lambda x: x["preco"]):
            print(f"\t{personagem['nome']:25} {personagem['hp']:3} {personagem['preco']}")
            info_ += f"\n\t{personagem['nome']:25} {personagem['hp']:3} {personagem['preco']}"

    raridades = {"comum":0,
                 "raro":0,
                 "epico":0,
                 "lendario":0,
                 "secreto":0}

    for i in cartas.keys():
        raridades[cartas[i]['raridade']] += 1

    print("Raridades:")
    info_ += "\n\nRaridades:"
    for i in raridades.keys():
        print(f"\t({i}) {raridades[i]}")
        info_ += f"\n\t({i}) {raridades[i]}"

    with open("infos.txt", "w") as arq:
        arq.write(info_)
    
    return por_classe

def ajustar(cartas) -> dict:
    final = {}
    for i in cartas:
        final[i["nome"]] = {"preco":i["preco"],
                            "hp":i["hp"]}
    return final

def dicionario_mana(cartas:list) -> dict:
    dicionario = {-1:0,
                  0:0,
                  1:0,
                  2:0,
                  3:0,
                  4:0,
                  5:0}
    for key in cartas.keys():
        dicionario[cartas[key]["preco"]] += 1

    print(f"\nQuantidade de cartas:")
    print(f"\tMANA{' '*3}QUANTIDADE")
    for key in dicionario:
        print(f"\t{key}:    {dicionario[key]:2}")

    return dicionario

if __name__ == "__main__":
    cartas_por_classe = infos(CARTAS)
    qnt_cartas = dicionario_mana(CARTAS)

    divisao = [6, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2,
               6, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 6, 2, 2, 2]

    posibilidades = [(-1, -1, -1), 
                     (-1, -1, 0), 
                     (-1, -1, 1), 
                     (-1, -1, 2), 
                     (-1, -1, 3), 
                     (-1, -1, 4), 
                     (-1, -1, 5), 
                     (-1, 0, 0), 
                     (-1, 0, 1), 
                     (-1, 0, 2), 
                     (-1, 0, 3), 
                     (-1, 0, 4), 
                     (-1, 0, 5), 
                     (-1, 1, 1), 
                     (-1, 1, 2), 
                     (-1, 1, 3), 
                     (-1, 1, 4), 
                     (-1, 1, 5), 
                     (-1, 2, 2), 
                     (-1, 2, 3), 
                     (-1, 2, 4), 
                     (-1, 3, 3), 
                     (0, 0, 0),
                     (0, 0, 1),
                     (0, 0, 2),
                     (0, 0, 3),
                     (0, 0, 4),
                     (0, 0, 5),
                     (0, 1, 1),
                     (0, 1, 2),
                     (0, 1, 3),
                     (0, 1, 4),
                     (0, 2, 2),
                     (0, 2, 3),
                     (1, 1, 1),
                     (1, 1, 2),
                     (1, 1, 3),
                     (1, 2, 2)]

    info_ = "\n\nCOMBINAÇÕES POSSÍVEIS COM AS CARTAS DO JOGO:"
    print("\n\nCOMBINAÇÕES POSSÍVEIS COM AS CARTAS DO JOGO:")
    combinacoes = 0
    combinacoes_unicas = 0
    n = 0
    for p in posibilidades:
        temp = qnt_cartas[p[0]] * qnt_cartas[p[1]] * qnt_cartas[p[2]]
        combinacoes += temp

        temp_ = 1
        qnt_temp = qnt_cartas.copy()
        temp_ *= qnt_temp[p[0]]
        qnt_temp[p[0]] -= 1
        temp_ *= qnt_temp[p[1]]
        qnt_temp[p[1]] -= 1
        temp_ *= qnt_temp[p[2]]/divisao[n]
        qnt_temp[p[2]] -= 1
        combinacoes_unicas += temp_
        n += 1
        
        print(f"\t{str(p):10} -> {temp:4} | {int(temp_):4}")
        info_ += f"\n\t{str(p):10} -> {temp:4} | {int(temp_):4}"

    print(f"\n\nCombinações totais: {combinacoes}")
    print(f"Combinações únicas: {int(combinacoes_unicas)}")
    print(f"Total de cartas no jogo: {len(CARTAS.keys())}")
    info_ += f"\n\nCombinações totais: {combinacoes}\nCombinações únicas: {int(combinacoes_unicas)}\nTotal de cartas no jogo: {len(CARTAS.keys())}"

    with open("infos.txt", "a") as arq:
        arq.write(info_)

    for classe in cartas_por_classe.keys():
        print(f"\n\n{'='*30}({classe.center(16):16}){'='*30}")
        CARTAS = ajustar(cartas_por_classe[classe])
        qnt_cartas = dicionario_mana(CARTAS)
        
        print(f"\nCOMBINAÇÕES POSSÍVEIS COM AS CARTAS {classe.upper()} NO JOGO:")
        combinacoes = 0
        combinacoes_unicas = 0
        n = 0
        for p in posibilidades:
            temp = qnt_cartas[p[0]] * qnt_cartas[p[1]] * qnt_cartas[p[2]]
            combinacoes += temp

            temp_ = 1
            qnt_temp = qnt_cartas.copy()
            temp_ *= qnt_temp[p[0]]
            qnt_temp[p[0]] -= 1
            temp_ *= qnt_temp[p[1]]
            qnt_temp[p[1]] -= 1
            temp_ *= qnt_temp[p[2]]/divisao[n]
            qnt_temp[p[2]] -= 1
            combinacoes_unicas += temp_
            n += 1
            
            print(f"\t{str(p):10} -> {temp:4} | {int(temp_):4}")

        print(f"\n\nCombinações totais de {classe}: {combinacoes}")
        print(f"Combinações únicas de {classe}: {int(combinacoes_unicas)}")
        print(f"Total de {classe} no jogo: {len(CARTAS.keys())}")
    
        
