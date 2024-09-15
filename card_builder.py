"""
Sistema de construção de cartas
"""

from random import random
from threading import Thread
from os import listdir
from json import dump
from game_config import *
from arts import *
from auxiliary_functions import *
from pure_engine_ascii import Screen
from engine_card_game import raridades, classes, lista_ataques, lista_habilidades, lista_variaveis_globais, dicionario_ataques
from translator import translate

def card_builder():
    """
    Sistema de construção de carta

    O usuário pode escolher entre:

    - Classe
    - Raridade
    - HP
    - Custo
    - Nome
    - Imagem
    - Ataques
    - habilidades    
    """
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()

    descricoes_opcoes = {"NOME": "Escolha o nome da carta.",
                         "HP": "Vida da carta.",
                         "PRECO": "Custo da carta.",
                         "CLASSE": "Classe da carta.",
                         "ARTE": "Arte da carta.",
                         "RARIDADE": "Raridade da carta.",
                         "ATAQUES": "Monte um ataque ou uma habilidade para a carta.",
                         "SAVE": f"Salve a carta na pasta {FOLDER_CARDS_MODS} com o nome da carta.",
                         "LIMPAR ATAQUES": "Limpa os ataques da carta.",
                         "secreto": "Só é obtido por meio de missões ou itens.",
                         "":"",
                         "ataques": "Cria um ataque (só acontece obtendo o valor igual ou maior no dado).",
                         "habilidades": "Cria uma habilidade passiva. Você obrigatoriamente precisa passar os parâmetros (tempo, vivo, morto, ataque, defesa)",
                         "dano_": "Dá dano a um inimigo específico, os parâmetros são (dano, aleatorio, vezes, todos, amigos_e_inimigos, multiplicador, chance).",
                         "cura_": "Cura um personagem aliado, os parâmetros são (cura, aleatorio, vezes, todos, curar_todos).",
                         "assasinato_": "Destroi um personagem inimigo, os parâmetros são (aleatorio, vezes, todos).",
                         "trocar_vida": "Troca a vida de um personagem inimigo com si mesmo ou com outro personagem, os parâmetros são (si_mesmo, chance).",
                         "copiar_atributo": "Copia o atributo de um personagem inimigo, os parâmetros são (atributo, aleatorio, copia_completa).",
                         "habilidade_buff_global_dano": "Dá um buff aos persagens aliados, os parâmetros são (apenas_caracteristico, soma_por_caracteristicas, caracteristicas).",
                         "habilidade_nerf_global_dano": "Dá um nerf aos personagens inimigos, os parâmetros são (apenas_caracteristico, soma_por_caracteristicas, caracteristicas, multiplicador).",
                         "habilidade_reviver": "Revive um personagem com um limite de vida superior, os parâmetros são (chance, vida, si_mesmo, vivo)",
                         "habilidade_buff_global_dado": "Dá um buff global no dado, os parâmetros são (buff, chance).",
                         "habilidade_nerf_global_dado": "Dá um nerf global no dado, os parâmetros são (buff, chance).",
                         "adicionar_habilidade": "Adiciona uma habilidade a carta, os parâmetros são (funcao)",
                         "somar_global": "Soma ou subtrai uma variável global, os parâmetros são (variavel_global, soma).",
                         "pular_turno": "Pula o turno da carta seguinte.",
                         "tempo": "O tempo em que ocorrera a habilidade, pode ser: 'comeco' ou 'final' do turno.",
                         "vivo": "Se a habilidade acontecerá enquanto o personagem estiver vivo.",
                         "morto": "Se a habilidade acontecerá enquanto o personagem estiver morto.",
                         "ataque": "Se a habilidade acontecerá no turno de ataque do personagem.",
                         "defesa": "Se a habilidade acontecerá no turno de defesa do personagem.",
                         "si_mesmo": "Se a habilidade acontece com o próprio personagem.",
                         "chance": "Chance da habilidade ou do ataque acontecer.",
                         "buff": "Valor de buff da habilidade.",
                         "nerf": "Valor de nerf da habilidade.",
                         "todos": "Se a habilidade ou o ataque pode acontecer em qualquer lado do tabuleiro.",
                         "dano": "Quanto de dano será dado.",
                         "cura": "Quanto de cura será dado.",
                         "vezes": "Quantidade de vezes que o habilidade ou oataque acontecerá.",
                         "aleatorio": "Se a habilidade ou o ataque será aplicado de forma aleatória ou a escolha do usuário.",
                         "atributo": "Lista de itens que será copiada.",
                         "amigos_e_inimigos": "Se o ataque ou a habilidade pode ser usada nos dois lados do tabuleiro.",
                         "multiplicador": "Caso esteja usando uma variável global como valor para um ataque ou habilidade, o multiplicador multiplica essa variável pelo valor indicado.",
                         "vida": "Limite de vida para algum tipo de cura.",
                         "variavel_global": "Alguma variável global.",
                         "dado": "Quanto que tem que cair no dado para aquilo ocorrer.",
                         "apenas_caracteristico": "A habilidade só funciona com caracteristicas específicas, que é definida pelo dicionário de características",
                         "caracteristicas": "Características específicas para uma habilidade ocorrer.",
                         "soma_por_caracteristicas": "Se uma habilidade deve somar a habilidade para cada personagem com aquela característica.",
                         "voltar": "Volta para o primeiro nível de criação da carta, salvando as modificações feitas nesse nível.",
                         "nome": "Nome do ataque ou da habilidade.",
                         "copia_completa": "Se deve fazer a cópia completa de outro personagem.",
                         "variavel_global": "Qual variável global será modificada.",
                         "funcao": "Função que será adicionada a carta, essa caracteristica é bem complexa, deve ser adicionada manualmente no arquivo da carta."}

    classes, index_classes = tuple(globals()["classes"].keys()), 0
    raridades, index_raridades = tuple(globals()["raridades"].keys()), 0

    carta = {"nome":"???",
             "hp":50,
             "preco":1,
             "classe":classes[index_classes],
             "arte":None,
             "raridade":raridades[index_raridades],
             "ataques":[]
             }

    pos_ponteiro = 0

    tela = ["principal"]
    textos = {"principal":["NOME", "HP", "PRECO", "CLASSE", "ARTE", "RARIDADE", "ATAQUES", "SAVE", "LIMPAR ATAQUES"],
              "ATAQUES":["ataques", "habilidades"],
              "HP":["0 ~ 100", "100 ~ 200", "200 ~ 300", "300 ~ 400", "400 ~ 500"],
              "0 ~ 100":[str(i*10) for i in range(0, 10)],
              "100 ~ 200":[str(i*10) for i in range(10, 20)],
              "200 ~ 300":[str(i*10) for i in range(20, 30)],
              "300 ~ 400":[str(i*10) for i in range(30, 40)],
              "400 ~ 500":[str(i*10) for i in range(40, 51)],
              "~ 0 ~ 50":["0 ~ 10", "10 ~ 20", "20 ~ 30", "30 ~ 40", "40 ~ 50"],
              "0 ~ 10":[str(i) for i in range(0, 10)],
              "10 ~ 20":[str(i) for i in range(10, 20)],
              "20 ~ 30":[str(i) for i in range(20, 30)],
              "30 ~ 40":[str(i) for i in range(30, 40)],
              "40 ~ 50":[str(i) for i in range(40, 51)],
              "CLASSE":classes,
              "RARIDADE":raridades,
              "PRECO":[str(i) for i in range(6)]}

    textos = textos | dicionario_ataques
    
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    
    game_t = Thread(target = game.run)
    game_t.start()

    salvar_ataque_temporario = {"argumentos":{"image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                "nome":"???",
                                "descricao":f"???",
                                "dado":1}

    while True:
        x_carta = 105
        y_carta = 0

        if textos[tela[-1]][pos_ponteiro] in descricoes_opcoes:
            caixa_de_ajuda = caixa_texto(translate(descricoes_opcoes[textos[tela[-1]][pos_ponteiro]]), limite = 100)
            game.add_effects(x = 2, y = 38 - len(caixa_de_ajuda),
                             image = caixa_de_ajuda,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
        
        game.add_effects(x = x_carta, y = y_carta,
                         image = base_card_complete_transparent,
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = 2, y = 38,
                         image = caixa_texto(translate(f"Parâmetros base: {', '.join(list(salvar_ataque_temporario.keys()))} | Parâmetros ataque: {', '.join(list(salvar_ataque_temporario['argumentos'].keys()))}"), limite = 137),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        if carta["arte"] != None:
            game.add_effects(x = x_carta + 1, y = y_carta + 2,
                             image = carta["arte"],
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

        game.add_effects(x = x_carta + 1, y = y_carta + 19,
                         image = put_color_rarity([list(f"{translate(carta['raridade']).title().center(34,'=')}")],
                                                  rarity = carta["raridade"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 5, y = y_carta + 1,
                         image = put_color_class([list(translate(f"{carta['classe'].title().center(23)}"))],
                                                 class_ = carta["classe"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 29, y = y_carta + 1,
                         image = [list("HP:")],
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 32, y = y_carta + 1,
                         image = put_color_life([list(f"{carta['hp']:3}")],
                                                life = carta['hp']),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 1, y = y_carta + 18,
                         image = [list(translate(carta['nome'].center(34)))],
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        game.add_effects(x = x_carta + 2, y = y_carta + 1,
                         image = put_color_rarity([list(f"({carta['preco']})")],
                                                  rarity = carta["raridade"]),
                         frames = 1,
                         tipe = None,
                         wait = 0,
                         to_start = 0)

        pos = 21
        for iteracao in carta["ataques"]:
            if iteracao["tipo"] == "ataque":
                texto_descricao = [list(translate(f"{iteracao['nome']} ({iteracao['dado']}) ({iteracao['tipo'].title()})"))]
            else:
                texto_descricao = [list(translate(f"{iteracao['nome']} ({iteracao['tipo'].title()})"))]
                
            game.add_effects(x = x_carta + 2, y = y_carta + pos,
                             image = put_color_tipo(texto_descricao,
                                                    tipo = iteracao["tipo"]),
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            descricao = ajustar_descricao(translate(iteracao["descricao"]))

            game.add_effects(x = x_carta + 2, y = y_carta + pos + 2,
                             image = descricao,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            pos += 3 + len(descricao)

        pos_texto_x, pos_texto_y = 2, 0
        nivel_complementar = 0
        if tela[0] == "principal":
            texto_principal = translate(f"Use as teclas (A, S, ENTER) Para iteragir\n(E) Para sair")
            game.buffer_text = texto_principal

            for nivel in range(len(tela)):
                adicao_x = 0
                iteracao = 0
                for texto in textos[tela[nivel]]:

                    if adicao_x >= x_carta - 10:
                        adicao_x = 0
                        nivel_complementar += 1

                    try:
                        if texto in salvar_ataque_temporario or texto in salvar_ataque_temporario["argumentos"]:
                            game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 3) * (nivel + nivel_complementar),
                                             image = caixa_texto(translate(f"{texto}!"), limite = len(translate(texto)) + 4),
                                             frames = 1,
                                             tipe = None,
                                             wait = 0,
                                             to_start = 0)
                            
                        elif texto == tela[nivel + 1]:
                            game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 3) * (nivel + nivel_complementar),
                                             image = caixa_texto(translate(f"{texto}*"), limite = len(translate(texto)) + 4),
                                             frames = 1,
                                             tipe = None,
                                             wait = 0,
                                             to_start = 0)


                        else:
                            game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 3) * (nivel + nivel_complementar),
                                             image = caixa_texto(translate(texto), limite = len(translate(texto)) + 4),
                                             frames = 1,
                                             tipe = None,
                                             wait = 0,
                                             to_start = 0)
                    except IndexError:
                        game.add_effects(x = pos_texto_x + adicao_x, y = (pos_texto_y + 3) * (nivel + nivel_complementar),
                                         image = caixa_texto(translate(texto), limite = len(translate(texto)) + 4),
                                         frames = 1,
                                         tipe = None,
                                         wait = 0,
                                         to_start = 0)

                    if nivel == len(tela) - 1 and iteracao == pos_ponteiro:
                        pos_seta_x = pos_texto_x + adicao_x + (len(translate(texto)) - 1)//2
                        pos_seta_y = (pos_texto_y + 3) * (nivel + nivel_complementar) + 3

                    adicao_x += len(translate(texto)) + 5
                    iteracao += 1

            game.add_effects(x = pos_seta_x, y = pos_seta_y,
                             image = seta_cima_pequena,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)
        resp = input()
        if resp.lower() == "a" or resp.lower() == "q":
            pos_ponteiro = max(pos_ponteiro - 1, 0)
        elif resp.lower() == "s" or resp.lower() == "w" or resp.lower() == "d":
            pos_ponteiro = min(pos_ponteiro + 1, len(textos[tela[-1]]) - 1)
        elif resp == "":
            if "principal" in tela:
                if "voltar" == textos[tela[-1]][pos_ponteiro]:
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                    carta["ataques"].append(salvar_ataque_temporario)
                    salvar_ataque_temporario = {"argumentos":{"image":{"image":animacao_espada,
                                                                       "frames":6,
                                                                       "wait":5,
                                                                       "to_start":0,
                                                                       "x":10,
                                                                       "y":3}},
                                                "nome":"???",
                                                "descricao":f"???"}
                    
                elif len(tela) == 3 and "HP" in tela[1]:
                    carta["hp"] = int(textos[tela[-1]][pos_ponteiro])
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "CLASSE" in tela[1]:
                    carta["classe"] = textos[tela[-1]][pos_ponteiro]
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "RARIDADE" in tela[1]:
                    carta["raridade"] = textos[tela[-1]][pos_ponteiro]
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "PRECO" in tela[1]:
                    carta["preco"] = int(textos[tela[-1]][pos_ponteiro])
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 1 and "NOME" == textos[tela[-1]][pos_ponteiro]:
                    carta["nome"] = input("Coloque o nome: ")
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 1 and "ARTE" == textos[tela[-1]][pos_ponteiro]:
                    artes = sorted(listdir(FOLDER_ART))
                    textos["ARTE"] = artes
                    tela.append(textos[tela[-1]][pos_ponteiro])
                    pos_ponteiro = min(pos_ponteiro, len(artes) - 1)

                elif len(tela) == 1 and "SAVE" == textos[tela[-1]][pos_ponteiro]:
                    with open(f"{FOLDER_CARDS_MODS}/{carta['nome']}", "w") as salvar_carta:
                        json.dump(carta, salvar_carta, indent = 4)

                elif len(tela) == 1 and "LIMPAR ATAQUES" == textos[tela[-1]][pos_ponteiro]:
                    carta["ataques"] = []

                elif len(tela) == 4 and "nome" == textos[tela[-1]][pos_ponteiro]:
                    salvar_ataque_temporario["nome"] = input("Coloque o nome: ")
                    tela = tela[0:4]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 4 and "descricao" == textos[tela[-1]][pos_ponteiro]:
                    salvar_ataque_temporario["descricao"] = input("Coloque a descrição: ")
                    tela = tela[0:4]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif len(tela) == 2 and "ARTE" in tela[1]:
                    with open(f"{FOLDER_ART}/{textos[tela[-1]][pos_ponteiro]}") as arte_da_carta:
                        arte_final = arte_da_carta.read().split("\n")
                        arte_final = arte_final[:ART_WIDTH]
                        for i in range(len(arte_final)):
                            if len(arte_final[i]) > HEIGHT_ART:
                                arte_final[i] = arte_final[i][:HEIGHT_ART]
                    carta["arte"] = adjust_image(arte_final)
                    tela = tela[0:1]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)

                elif (not textos[tela[-1]][pos_ponteiro] in textos) and (tela[2] == "ataques" or tela[2] == "habilidades"):
                    if tela[2] == "ataques":
                        salvar_ataque_temporario["tipo"] = "ataque"

                    elif tela[2] == "habilidades":
                        salvar_ataque_temporario["tipo"] = "habilidade"
                    
                    if "copiar_atributo" in tela and "atributo" in tela:
                        if not "atributo" in salvar_ataque_temporario["argumentos"]:
                            salvar_ataque_temporario["argumentos"]["atributo"] = []
                        salvar_ataque_temporario["argumentos"]["atributo"].append(tela[5])
                        
                    elif tela[2] == "ataques":
                        salvar_ataque_temporario["funcao"] = tela[3]
                        if tela[4] == "dado":
                            salvar_ataque_temporario["dado"] = int(textos[tela[-1]][pos_ponteiro])
                        elif tela[4] == "caracteristicas":
                            if not "caracteristicas" in salvar_ataque_temporario["argumentos"]:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"] = {}
                            try:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"] = int(textos[tela[-1]][pos_ponteiro])
                            except:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"] = textos[tela[-1]][pos_ponteiro]
                        else:
                            salvar_ataque_temporario["argumentos"][tela[4]] = textos[tela[-1]][pos_ponteiro]
                        
                    elif tela[2] == "habilidades":
                        salvar_ataque_temporario["funcao"] = tela[3]
                        if "caracteristicas" in tela:
                            if not "caracteristicas" in salvar_ataque_temporario["argumentos"]:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"] = {}
                            try:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"][tela[5]] = int(textos[tela[-1]][pos_ponteiro])
                            except:
                                salvar_ataque_temporario["argumentos"]["caracteristicas"][tela[5]] = textos[tela[-1]][pos_ponteiro]
                        else:
                            salvar_ataque_temporario["argumentos"][tela[4]] = textos[tela[-1]][pos_ponteiro]
                        
                    tela = tela[0:4]
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                    
                else:
                    tela.append(textos[tela[-1]][pos_ponteiro])
                    pos_ponteiro = min(pos_ponteiro, len(textos[tela[-1]]) - 1)
                            
            else:
                pass

        elif resp.lower() == "m" or resp.lower() == "e":
            break

    game.close()
    game_t.join()

if __name__ == "__main__":
    card_builder()
