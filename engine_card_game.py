"""
Funcionamento das cartas

classes:
    - guerreiros
    - monstros
    - paladinos
    - noturnos
    - piratas
    - lendas

Abilidades podem ser:
    - comeco: começo do turno
    - final: fim do turno
    - global: ao iniciar o jogo

As abilidades podem ser ativas em uma ou mais situações:
    - vivo: enquanto vivo
    - morto: enquanto morto

"""

from time import sleep
from random import random
from card_game import Screen
from game_config import *
from arts import *

game = Screen(x = X, y = Y, fps = FPS)
DEBUG = False
#=====================================================================================
#Engine do jogo:

def cl() -> None:
    """
    Limpa o texto do buffer
    """
    buffer_("§")

def buffer_(texto:str) -> None:
    """
    Coloca o texto no buffer_ ou printa o texto
    """
    if DEBUG:
        print(texto)
    else:
        #sleep(1/FPS)
        if texto.find("§") > -1:
            game.buffer_text = ""
            game.animation = True
        else:
            game.buffer_text += f"{texto}\n"
            game.animation = True

def jogar(TIMES:list): 
    #Valores de turno:
    globals()["TIMES"] = TIMES
    globals()["PARTIDA"] = 0 #Partida
    globals()["TABULEIRO"] = 0 #Tabuleiro
    globals()["ESCOLHIDO"] = [0, 0] #Personagem escolhido por tabuleiro

    for time in TIMES:
        for p in time:
            p["hp_inicial"] = p["hp"]
    
    ###Vendo abilidades globais:
    
    while True:
        cl()

        time_atacante = TIMES[globals()["TABULEIRO"]]
        time_atacado = TIMES[(globals()["TABULEIRO"] + 1) % 2]
        
        #Escolhedo o personagem que atacara nesse round
        personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]

        n = 0
        while personagem_atual["hp"] <= 0 and n < 3:
            buffer_(f"Pulando personagem {personagem_atual['nome']}...")
            globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
            personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
            n += 1

        if n >= 3: #Termina o jogo
            buffer_("O JOGO TERMINOL!")
            break
             
        buffer_(f"Turno {globals()['PARTIDA']} do {personagem_atual['nome']} | TABULEIRO: {globals()['TABULEIRO']} - POSIÇÃO: {globals()['ESCOLHIDO'][globals()['TABULEIRO']]}")

        ###Vendo se tem alguma abilidade passiva de começo de turno:
        conferir_abilidade(tempo = "comeco", ataque = True, time = time_atacante)
        conferir_abilidade(tempo = "comeco", defesa = True, time = time_atacado)

        numero_dado = jogar_dado()
        ###ANIMACAO DO DADO

        ###Vendo ataques do personagem:
        verificar_ataques(personagem_atual, numero_dado)

        ###Vendo se tem alguma abilidade passiva de final de turno:
        conferir_abilidade(tempo = "final", ataque = True, time = time_atacante)
        conferir_abilidade(tempo = "final", defesa = True, time = time_atacado)

        #Ajustando valores de turno:      
        globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
        globals()["TABULEIRO"] = (globals()["TABULEIRO"] + 1) % 2
        globals()["PARTIDA"] += 1

        reset_globais()

#=====================================================================================
#Funções base:
def verificar_ataques(personagem:dict, dado:int) -> None:
    """
    Verifica quais ataques podem acontecer de acordo com o número do dado
    """
    #Confere quais ataques são validos de acordo com o número do dado que caiu:
    ataques_validos = []
    n = 1
    for ataque in personagem["ataques"]:
        if ataque["tipo"] == "ataque":
            if ataque["dado"] <= dado:
                ataques_validos.append(ataque)
                buffer_(f"({n}) {ataque['nome']}: {ataque['descricao']}")
                n += 1

    #Permite que o jogador escolha um dos ataques:
    if len(ataques_validos) > 0:
        while True:
            escolha = input()
            try:
                escolha = int(escolha)
                if 1 <= escolha < len(ataques_validos) + 1:
                    ataque = ataques_validos[escolha - 1]
                    break
            except:
                pass

        #Atacando usando os argumentos passados e os argumentos globais que estão em 'jogar()'
        ataque["funcao"](**ataque["argumentos"])

def jogar_dado() -> int:
    """
    Joga o dado considerando os limites inferiores e superiores
    """
    dado = int((random() * globals()["LIMITES_DADO"][1]) + globals()["LIMITES_DADO"][0]) - globals()["NERF_DADO"] + globals()["BUFF_DADO"]
    return dado
        
def escolha_inimigo(inimigos:list, aleatorio = False) -> dict:
    """
    Função para escolher inimigo
    """
    possiveis = []
    n = 1
    for inimigo in inimigos:
        if inimigo["hp"] > 0:
            possiveis.append(inimigo)
            buffer_(f"({n}): {inimigo['nome']:25} {inimigo['hp']:3}hp")

    if aleatorio:
        escolha = int(random()*len(possiveis))

    else:
        while True:
            buffer_("(ESCOLHA O NÚMERO DO INIMIGO QUE DESEJA ATACAR)")
            escolha = input("")
            try:
                escolha = int(escolha) - 1
                if 0 <= escolha < len(possiveis):
                    break
            except:
                pass

    return possiveis[escolha]

def conferir_abilidade(tempo:str, ataque:bool = False, defesa:bool = False, time = None):
    for personagem in time:
        for abilidade in personagem["ataques"]:
            if abilidade["tipo"] == "abilidade":

                if not "ataque" in abilidade:
                    abilidade["ataque"] = False
                if not "defesa" in abilidade:
                    abilidade["defesa"] = False
        
                if abilidade["tempo"] == tempo and abilidade["ataque"] == ataque and abilidade["defesa"] == defesa:
                    abilidade["funcao"](**abilidade["argumentos"], personagem = personagem)

#-------------------------------------------------------------------------------------
#Funções de dano:

def dano_(dano:int, aleatorio:bool = False, animacao:str = None) -> None:
    """
    Causa dano em um personagem inimigo, pode ser aleatorio ou não
    """
    time_inimigo = (globals()["TABULEIRO"] + 1) % 2
    personagem_inimigo = escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)
    buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
    personagem_inimigo["hp"] = max(personagem_inimigo["hp"] - dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0)

    if "x" in personagem_inimigo:
        game.add_effects(x = personagem_inimigo["x"] + 10, y = personagem_inimigo["y"] + 3, image = animacao_espada, frames = 8, tipe = animacao, wait = 5)

def cura_(cura:int, aleatorio:bool = False) -> None:
    """
    Cura um personagem amigo, pode ser aleatorio ou não
    """
    time_amigo = globals()["TABULEIRO"]
    personagem_inimigo = escolha_inimigo(globals()["TIMES"][time_amigo], aleatorio = aleatorio)
    buffer_(f"Curando {personagem_inimigo['nome']} em {cura}...")
    personagem_inimigo["hp"] = max(personagem_inimigo["hp"] + cura + globals()["BUFF_CURA"], personagem_inimigo["hp_inicial"])

#-------------------------------------------------------------------------------------
#Funções de cura:


#-------------------------------------------------------------------------------------
#Funções de abilidade:

def abilidade_buff_global_dano(buff:int, personagem):
    globals()["BUFF_TEMPORARIO"] += buff
    buffer_(f"(ABILIDADE) Buff no dano de +{globals()['BUFF_TEMPORARIO']}")
 
    if "x" in personagem:
        game.add_effects(x = personagem["x"] + 14, y = personagem["y"] + 5, image = seta_cima, frames = 6, tipe = "aleatorio", wait = 50, to_start = 60)

def abilidade_nerf_global_dano(buff:int, personagem):
    globals()["NERF_TEMPORARIO"] += buff
    buffer_(f"(ABILIDADE) Nerf no dano de -{globals()['NERF_TEMPORARIO']}")

    if "x" in personagem:
        game.add_effects(x = personagem["x"] + 12, y = personagem["y"] + 5, image = escudo, frames = 6, tipe = "aleatorio", wait = 50, to_start = 60)


#=====================================================================================
#=====================================================================================


#=====================================================================================
#=====================================================================================
#Globais:
def reset_globais():
    globals()["LIMITES_DADO"] = [1, 6]
    globals()["NERF_DADO"] = 0
    globals()["BUFF_DADO"] = 0
    globals()["BUFF_TEMPORARIO"] = 0
    globals()["NERF_TEMPORARIO"] = 0
    globals()["BUFF_CURA"] = 0

BUFF_TEMPORARIO = 0
NERF_TEMPORARIO = 0
BUFF_CURA = 0

PARTIDA = 0
TABULEIRO = 0
ESCOLHIDO = [0, 0]

LIMITES_DADO = [1, 6]
NERF_DADO = 0
BUFF_DADO = 0

GUERREIRO_PREPARADO_DANO_1 = 10
GUERREIRO_PREPARADO_DANO_2 = 30

GENIO_MALUCO_DANO_1 = 50
GENIO_MALUCO_BUFF_DANO = 20

GUERREIRA_EXPERIENTE_DANO_1 = 40
GUERREIRA_EXPERIENTE_BUFF_DEFESA = 20

CARTAS = {"guerreiro_preparado":{"nome":"Guerreiro Preparado",
                                 "hp":90,
                                 "preco":1,
                                 "classe":"guerreiro",
                                 "arte":None,
                                 "ataques":[{"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":1,
                                             "argumentos":{"dano":GUERREIRO_PREPARADO_DANO_1, "aleatorio": True, "animacao": "espada"},
                                             "nome":"Manopla de choque",
                                             "descricao":f"De {GUERREIRO_PREPARADO_DANO_1} de dano em um lacaio aleatório."},
                                            {"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":3,
                                             "argumentos":{"dano":GUERREIRO_PREPARADO_DANO_2, "aleatorio": True, "animacao": "espada"},
                                             "nome":"Fuzil Tesla",
                                             "descricao":f"De {GUERREIRO_PREPARADO_DANO_2} de dano em um lacaio aleatório"}]
                                 },          
          "genio_maluco":{"nome":"Gênio Maluco",
                          "hp":100,
                          "preco":2,
                          "classe":"guerreiro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":GENIO_MALUCO_DANO_1, "aleatorio": True, "animacao": "espada"},
                                      "nome":"Manopla de choque",
                                      "descricao":f"De {GUERREIRO_PREPARADO_DANO_1} de dano em um lacaio aleatório."},
                                     {"tipo":"abilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":abilidade_buff_global_dano,
                                      "argumentos":{"buff":GENIO_MALUCO_BUFF_DANO},
                                      "nome":"Suporte Pesado",
                                      "descricao":f"Enquanto vivo, todos os outros guerreiros no seu lado do campo ganham +{GENIO_MALUCO_BUFF_DANO} dano durante todo o jogo."}]
                          },
          "escudeira_experiente":{"nome":"Escudeira Experiente",
                                  "hp":110,
                                  "preco":3,
                                  "classe":"guerreiro",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":GUERREIRA_EXPERIENTE_DANO_1, "aleatorio": True, "animacao": "espada"},
                                              "nome":"Manopla de choque",
                                              "descricao":f"De {GUERREIRO_PREPARADO_DANO_1} de dano em um lacaio aleatório."},
                                             {"tipo":"abilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":abilidade_nerf_global_dano,
                                              "argumentos":{"buff":GUERREIRA_EXPERIENTE_BUFF_DEFESA},
                                              "nome":"Meu escudo primeiro",
                                              "descricao":f"Enquanto vivo, todos os outros guerreiros no seu lado do campo ganham +{GUERREIRA_EXPERIENTE_BUFF_DEFESA} defesa."}]
                                 },         
          }

if __name__ == "__main__":
    DEBUG = True
    TIMES = [[CARTAS["guerreiro_preparado"].copy(),
              CARTAS["guerreiro_preparado"].copy(),
              CARTAS["guerreiro_preparado"].copy()],
             [CARTAS["guerreiro_preparado"].copy(),
              CARTAS["guerreiro_preparado"].copy(),
              CARTAS["guerreiro_preparado"].copy()]]
    
    jogar(TIMES)
