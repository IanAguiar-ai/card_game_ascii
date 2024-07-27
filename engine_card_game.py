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

As habilidades podem ser ativas em uma ou mais situações:
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

def buffer_(texto:str, end:str = "\n") -> None:
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
            game.buffer_text += f"{texto}{end}"
            game.animation = True

def jogar(TIMES:list):
    """
    Função principal com a lógica dos turnos, só termina quando o jogo acaba
    """
    #Valores de turno:
    globals()["TIMES"] = TIMES
    globals()["PARTIDA"] = 0 #Partida
    globals()["TABULEIRO"] = 0 #Tabuleiro
    globals()["ESCOLHIDO"] = [0, 0] #Personagem escolhido por tabuleiro

    for time in TIMES:
        for p in time:
            p["hp_inicial"] = p["hp"]
    
    ###Vendo habilidades globais:
    
    while True:

        time_atacante = TIMES[globals()["TABULEIRO"]]
        time_atacado = TIMES[(globals()["TABULEIRO"] + 1) % 2]
        globals()["time_atacante"] = time_atacante
        globals()["time_atacado"] = time_atacado
        
        #Escolhedo o personagem que atacara nesse round
        personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]

        n = 0
        while personagem_atual["hp"] <= 0 and n < 3:
            buffer_(f"Pulando personagem {personagem_atual['nome']}...")
            globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
            personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
            n += 1

        if n >= 3: #Termina o jogo
            buffer_("O JOGO TERMINOU!")
            break
             
        buffer_(f"Turno {globals()['PARTIDA']} do {personagem_atual['nome']} | TABULEIRO: {globals()['TABULEIRO']} - POSIÇÃO: {globals()['ESCOLHIDO'][globals()['TABULEIRO']]}")

        ###Vendo se tem alguma habilidade passiva de começo de turno:
        conferir_habilidade(tempo = "comeco", ataque = True, time = time_atacante)
        conferir_habilidade(tempo = "comeco", defesa = True, time = time_atacado)

        numero_dado = jogar_dado()
        ###ANIMACAO DO DADO

        ###Vendo ataques do personagem:
        verificar_ataques(personagem_atual, numero_dado)
        cl()

        ###Vendo se tem alguma habilidade passiva de final de turno:
        conferir_habilidade(tempo = "final", ataque = True, time = time_atacante)
        conferir_habilidade(tempo = "final", defesa = True, time = time_atacado)

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
    dado = min(max(dado, globals()["LIMITES_DADO"][0]), globals()["LIMITES_DADO"][1])
    game.add_effects(x = 125,
                     y = 42,
                     image = rolando_dado,
                     frames = 1,
                     wait = 30,
                     to_start = 0,
                     tipe = "aleatorio")
    game.add_effects(x = 127,
                     y = 44,
                     image = dados[dado-1],
                     frames = 4,
                     wait = 80,
                     to_start = 30,
                     tipe = "aleatorio")
    return dado
        
def escolha_inimigo(inimigos:list, aleatorio:bool = False, vivo:bool = True) -> dict:
    """
    Função para escolher inimigo
    """
    def criterio(inimigo, vivo:bool):
        if vivo:
            if inimigo["hp"] > 0:
                return True
        else:
            if inimigo["hp"] <= 0:
                return True
        return False
    
    possiveis = []
    n = 1
    for inimigo in inimigos:
        if criterio(inimigo, vivo):
            possiveis.append(inimigo)
            if globals()["DEBUG"]:
                buffer_(f"({n}): {inimigo['nome']:25} {inimigo['hp']:3}hp")
            else:
                if not aleatorio:
                    buffer_(f"({n}): {inimigo['nome']}")
            n += 1
    if n == 1: #Modo que ele já ataca um lacaio morto só para acabar com o turno
        if vivo:
            return inimigos[0]
        else:
            return None

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

def conferir_habilidade(tempo:str, ataque:bool = False, defesa:bool = False, time = None):
    for personagem in time:
        for habilidade in personagem["ataques"]:
            if habilidade["tipo"] == "habilidade":

                if not "ataque" in habilidade:
                    habilidade["ataque"] = False
                if not "defesa" in habilidade:
                    habilidade["defesa"] = False
        
                if habilidade["tempo"] == tempo and habilidade["ataque"] == ataque and habilidade["defesa"] == defesa:
                    if (habilidade["vivo"] and personagem["hp"] > 0) or (habilidade["morto"] and personagem["hp"] <= 0):
                        buffer_(f"{habilidade['nome']}: ", end = "")
                        habilidade["funcao"](**habilidade["argumentos"], personagem = personagem)

#-------------------------------------------------------------------------------------
#Funções de dano:

def dano_(dano:int, image:dict, aleatorio:bool = False, animacao:str = None, vezes:int = 1, todos:bool = False, amigos_e_inimigos:bool = False) -> None:
    """
    Causa dano em um personagem inimigo, pode ser aleatorio ou não
    """
    if not amigos_e_inimigos:
        for _ in range(vezes):
            time_inimigo = (globals()["TABULEIRO"] + 1) % 2
            if todos:
                personagens_inimigos = globals()["TIMES"][time_inimigo]
            else:
                personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

            for personagem_inimigo in personagens_inimigos:
                buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
                personagem_inimigo["hp"] = max(personagem_inimigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)

                printar(personagem_inimigo, image)

    else:
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        personagens_inimigos = globals()["TIMES"][time_inimigo]
        for personagem_inimigo in personagens_inimigos:
            buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
            personagem_inimigo["hp"] = max(personagem_inimigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)

            printar(personagem_inimigo, image)

        time_amigo = (globals()["TABULEIRO"]) % 2
        personagens_amigos = globals()["TIMES"][time_amigo]
        for personagem_amigo in personagens_amigos:
            buffer_(f"Atacando {personagem_amigo['nome']} em {dano}...")
            personagem_amigo["hp"] = max(personagem_amigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)

            printar(personagem_amigo, image)

def assasinato_(image:dict, aleatorio:bool = False, animacao:str = None, vezes:int = 1, todos:bool = False):
    for _ in range(vezes):
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        if todos:
            personagens_inimigos = globals()["TIMES"][time_inimigo]
        else:
            personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

        for personagem_inimigo in personagens_inimigos:
            buffer_(f"Destruindo {personagem_inimigo['nome']}...")
            personagem_inimigo["hp"] = 0

            printar(personagem_inimigo, image)

def cura_(cura:int, image:dict, aleatorio:bool = False, animacao:str = None, vezes:int = 1, todos:bool = False) -> None:
    """
    Cura um personagem amigo, pode ser aleatorio ou não
    """
    for _ in range(vezes):
        time_amigo = globals()["TABULEIRO"]
        if todos:
            personagens_amigos = globals()["TIMES"][time_amigo]
        else:
            personagens_amigos = [escolha_inimigo(globals()["TIMES"][time_amigo], aleatorio = aleatorio)]

        for personagem_amigo in personagens_amigos:
            buffer_(f"Curando {personagem_amigo['nome']} em {cura}...")
            personagem_amigo["hp"] = min(personagem_amigo["hp"] + cura + globals()["BUFF_CURA"], personagem_amigo["hp_inicial"])

            printar(personagem_amigo, image)             

#-------------------------------------------------------------------------------------
#Funções de cura:


#-------------------------------------------------------------------------------------
#Funções de habilidade:

def habilidade_buff_global_dano(buff:int, personagem, image:dict, apenas_caracteristico:bool = False, soma_por_caracteristicas:bool = False, caracteristicas:dict = None) -> None:
    """
    Da um buff...

    Se usar as caracteristicas devem ser passados:
        {"key":"classe",
        "valor":"humano",
        "time_atacante":True,
        "time_atacado":False}
    """
    if not soma_por_caracteristicas:
        if not apenas_caracteristico:
            globals()["BUFF_TEMPORARIO"] += buff
            buffer_(f"(HABILIDADE:{personagem['nome']}) Buff no dano de +{buff}")
        else:
            if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
                globals()["BUFF_TEMPORARIO"] += buff
                buffer_(f"(HABILIDADE:{personagem['nome']}) Buff no dano de +{buff}")
    else:
        buffer_("Conferindo iterações...")
        if "time_atacante" in caracteristicas and caracteristicas["time_atacante"]:
            for personagem_ in globals()["time_atacante"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["BUFF_TEMPORARIO"] += buff
                    buffer_(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} buff no dano de +{buff}")
        
        if "time_atacado" in caracteristicas and caracteristicas["time_atacado"]:
            for personagem_ in globals()["time_atacado"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["BUFF_TEMPORARIO"] += buff
                    buffer_(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} buff no dano de +{buff}")
        
    if not apenas_caracteristico:
        printar(personagem, image)
    else:
        if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
            printar(personagem, image)


def habilidade_nerf_global_dano(buff:int, personagem, image:dict, apenas_caracteristico:bool = False, soma_por_caracteristicas:bool = False, caracteristicas:dict = None) -> None:
    """
    Da um nerf...

    Se usar as caracteristicas devem ser passados:
        {"key":"classe",
        "valor":"humano",
        "time_atacante":True,
        "time_atacado":False}
    """
    if not soma_por_caracteristicas:
        if not apenas_caracteristico:
            globals()["NERF_TEMPORARIO"] += buff
            buffer_(f"(HABILIDADE:{personagem['nome']}) Nerf no dano de -{buff}")
        else:
            if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
                globals()["NERF_TEMPORARIO"] += buff
                buffer_(f"(HABILIDADE:{personagem['nome']}) Nerf no dano de -{buff}")
    else:
        buffer_("Conferindo iterações...")
        if "time_atacante" in caracteristicas and caracteristicas["time_atacante"]:
            for personagem_ in globals()["time_atacante"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["NERF_TEMPORARIO"] += buff
                    buffer_(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} nerf no dano de -{buff}")
        
        if "time_atacado" in caracteristicas and caracteristicas["time_atacado"]:
            for personagem_ in globals()["time_atacado"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["NERF_TEMPORARIO"] += buff
                    buffer_(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} nerf no dano de -{buff}")
        
    if not apenas_caracteristico:
        printar(personagem, image)
    else:
        if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
            printar(personagem, image)


def habilidade_reviver(personagem, chance:float, image:dict, vida:int, si_mesmo:bool = False, vivo:bool = True):
    if si_mesmo:
        if random() <= chance:
            buffer_(f"Revivendo {personagem['nome']}...")
            personagem["hp"] = min(personagem["hp_inicial"], vida)
            printar(personagem, image)
        else:
            buffer_(f"Nenhuma iteração...")
    else:
        time_amigo = (globals()["TABULEIRO"]) % 2
        personagens_amigos = globals()["TIMES"][time_amigo]
        personagem_reviver = escolha_inimigo(personagens_amigos, aleatorio = True, vivo = vivo)
        if personagem_reviver != None and random() <= chance:
            buffer_(f"Revivendo {personagem_reviver['nome']}...")
            personagem_reviver["hp"] = min(personagem_reviver["hp_inicial"], vida)
            printar(personagem_reviver, image)
            printar(personagem, image)
        else:
            buffer_("Nenhuma iteração...")
        
    

def habilidade_acao(funcao, argumentos_funcao:dict, personagem, image:dict) -> None:
    buffer_(f"(HABILIDADE) habilidade de {personagem['nome']}")

    printar(personagem, image)

    funcao(**argumentos_funcao)

#=====================================================================================
#=====================================================================================

def printar(personagem, image):
    if "x" in personagem:
        game.add_effects(x = personagem["x"] + image["x"],
                         y = personagem["y"] + image["y"],
                         image = image["image"],
                         frames = image["frames"],
                         wait = image["wait"],
                         to_start = image["to_start"],
                         tipe = "aleatorio")
        
#=====================================================================================
#=====================================================================================

def dano_e_cura_acumulador(dano:int, buff:int, image:dict, aleatorio:bool = False, animacao:str = None, vezes:int = 1, todos:bool = False, amigos_e_inimigos:bool = False) -> None:
    personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
    
    if not amigos_e_inimigos:
        for _ in range(vezes):
            time_inimigo = (globals()["TABULEIRO"] + 1) % 2
            if todos:
                personagens_inimigos = globals()["TIMES"][time_inimigo]
            else:
                personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

            for personagem_inimigo in personagens_inimigos:
                buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
                personagem_inimigo["hp"] = max(personagem_inimigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)
                personagem["hp"] = min(personagem["hp"] + dano + globals()["BUFF_CURA"], personagem["hp_inicial"])
                personagem["ataques"][0]["argumentos"]["dano"] += buff
                personagem["ataques"][0]["descricao"] = f"De {personagem['ataques'][0]['argumentos']['dano']} de dano a um personagem inimigo aleatório e se cure nesse valor."

                printar(personagem_inimigo, image)

    else:
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        personagens_inimigos = globals()["TIMES"][time_inimigo]
        for personagem_inimigo in personagens_inimigos:
            buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
            personagem_inimigo["hp"] = max(personagem_inimigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)
            personagem["hp"] = min(personagem["hp"] + dano + globals()["BUFF_CURA"], personagem["hp_inicial"])
            personagem["ataques"][0]["argumentos"]["dano"] += buff
            personagem["ataques"][0]["descricao"] = f"De {personagem['ataques'][0]['argumentos']['dano']} de dano a um personagem inimigo aleatório e se cure nesse valor."

            printar(personagem_inimigo, image)

        time_amigo = (globals()["TABULEIRO"]) % 2
        personagens_amigos = globals()["TIMES"][time_amigo]
        for personagem_amigo in personagens_amigos:
            buffer_(f"Atacando {personagem_amigo['nome']} em {dano}...")
            personagem_amigo["hp"] = max(personagem_amigo["hp"] - max(dano - globals()["BUFF_TEMPORARIO"] + globals()["NERF_TEMPORARIO"], 0), 0)
            personagem["hp"] = min(personagem["hp"] + dano + globals()["BUFF_CURA"], personagem["hp_inicial"])
            personagem["ataques"][0]["argumentos"]["dano"] += buff
            personagem["ataques"][0]["descricao"] = f"De {personagem['ataques'][0]['argumentos']['dano']} de dano a um personagem inimigo aleatório e se cure nesse valor."

            printar(personagem_amigo, image)
    
    

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

CARTAS = {"guerreiro_preparado":{"nome":"Guerreiro Preparado",
                                 "hp":80,
                                 "preco":1,
                                 "classe":"guerreiro",
                                 "arte":None,
                                 "ataques":[{"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":1,
                                             "argumentos":{"dano":10, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                             "nome":"Espadada Erronêa",
                                             "descricao":f"De 10 de dano em um personagem inimigo aleatório."},
                                            {"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":3,
                                             "argumentos":{"dano":30, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                             "nome":"Espadada Certeira",
                                             "descricao":f"De 30 de dano em um personagem inimigo aleatório"}]
                                 },          
          "genio_maluco":{"nome":"Gênio Maluco",
                          "hp":100,
                          "preco":2,
                          "classe":"guerreiro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":50, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Manopla de choque",
                                      "descricao":f"De 50 de dano em um personagem inimigo aleatório."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":10, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Suporte Pesado",
                                      "descricao":f"Enquanto vivo, todos os outros personagens no seu lado do campo ganham +10 dano."}]
                          },
          "escudeira_experiente":{"nome":"Escudeira Experiente",
                                  "hp":110,
                                  "preco":3,
                                  "classe":"guerreiro",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":40, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Empurrão",
                                              "descricao":f"De 40 de dano em um personagem inimigo aleatório."},
                                             {"tipo":"habilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_nerf_global_dano,
                                              "argumentos":{"buff":10, "image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                              "nome":"Meu escudo primeiro",
                                              "descricao":f"Enquanto vivo, todos os outros personagens no seu lado do campo ganham +10 defesa."}]
                                  },
          "escudeiro_leal":{"nome":"Escudeiro Leal",
                                  "hp":50,
                                  "preco":0,
                                  "classe":"guerreiro",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":10, "aleatorio": True, "animacao": "espada", "image":{"image":impacto_fraco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Escudada de Madeira",
                                              "descricao":f"De 10 de dano em um personagem inimigo aleatório."}]
                                  },
          "guerreira_cetica":{"nome":"Guerreira Cética",
                                  "hp":90,
                                  "preco":1,
                                  "classe":"guerreiro",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":30, "aleatorio": False, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Ponta da Lamina",
                                              "descricao":f"De 30 de dano em um personagem inimigo a sua escolha."}]
                                  },
          "soldado_novato":{"nome":"Soldado Novato",
                                  "hp":80,
                                  "preco":1,
                                  "classe":"guerreiro",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":2,
                                              "argumentos":{"dano":30, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Espadada Torta",
                                              "descricao":f"De 30 de dano em um personagem inimigo aleatório."}]
                                  },
          "cacador_de_feras":{"nome":"Caçador de Feras",
                                  "hp":70,
                                  "preco":3,
                                  "classe":"humano",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":5,
                                              "argumentos":{"dano":30, "todos":True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Preparação de Guerra",
                                              "descricao":f"De 30 de dano em todos os personagens inimigos."},
                                             {"tipo":"ataque",
                                              "funcao":assasinato_,
                                              "dado":6,
                                              "argumentos":{"aleatorio": True, "animacao":"espada", "image":{"image":caveira, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Última Batalha",
                                              "descricao":f"Destrua um personagem inimigo aleatório."},
                                             {"tipo":"habilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_nerf_global_dano,
                                              "argumentos":{"buff":10, "image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                              "nome":"Proteção do Caçador",
                                              "descricao":f"Enquanto vivo, todos os outros personagens no seu lado do campo ganham +10 defesa."}]
                              },
          "rei_da_vila":{"nome":"Rei da Vila",
                                  "hp":70,
                                  "preco":3,
                                  "classe":"humano",
                                  "arte":None,
                                  "ataques":[{"tipo":"habilidade",
                                              "ataque":True,
                                              "defesa":False,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_buff_global_dano,
                                              "argumentos":{"buff":20, "image":{"image":coroa, "frames":4, "wait":50, "to_start":TEMPO[1], "x":10, "y":5}},
                                              "nome":"Bençãos do Rei",
                                              "descricao":f"Enquanto vivo, todos os outros personagens no seu lado do campo ganham +20 de ataque."}]
                              },
          "curandeiro_da_vila":{"nome":"Curandeiro da Vila",
                                  "hp":50,
                                  "preco":1,
                                  "classe":"humano",
                                  "arte":None,
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":2,
                                              "argumentos":{"dano":10, "todos":True, "animacao": "espada", "image":{"image":impacto_fraco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Explosão de Luz",
                                              "descricao":f"De 10 de dano em todos os personagens inimigos."},
                                             {"tipo":"habilidade",
                                              "ataque":True,
                                              "defesa":False,
                                              "tempo":"final",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_acao,
                                              "argumentos":{"funcao":cura_,
                                                            "image":{"image":luz, "frames":2, "wait":70, "to_start":TEMPO[1], "x":10, "y":3},
                                                            "argumentos_funcao":{"cura":30, "aleatorio":True ,"image":{"image":cruz, "frames":4, "wait":70, "to_start":TEMPO[2], "x":8, "y":2}}},
                                              "nome":"Seja Curado",
                                              "descricao":f"Enquanto vivo, no final de seu turno cure um presonagem aliado aleatório em 30."}]
                              },
          "fazendeiro_corajoso":{"nome":"Fazendeiro Corajoso",
                          "hp":80,
                          "preco":1,
                          "classe":"humano",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":3,
                                      "argumentos":{"dano":20, "aleatorio": False, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Pá Leve, Mão Pesada",
                                      "descricao":f"De 20 de dano em um personagem inimigo a sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":10, "soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"guerreiro", "time_atacante":True, "time_atacado":False},
                                                    "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Camponeses Unidos",
                                      "descricao":f"Enquanto vivo, todos os personagens no seu lado do campo ganham +10 para cada guerreiro aliado."}]
                          },
          "zumbi":{"nome":"Zumbi",
                          "hp":80,
                          "preco":1,
                          "classe":"monstro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":30, "aleatorio": False, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Caçada a Carne",
                                      "descricao":f"De 30 de dano em um personagem inimigo a sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_reviver,
                                      "argumentos":{"chance":0.25, "si_mesmo":True, "vida":40, "image":{"image":cemiterio, "frames":4, "wait":50, "to_start":TEMPO[1], "x":7, "y":2}},
                                      "nome":"Saindo da Terra",
                                      "descricao":f"Enquanto morto, em todo o turno inimigo, tem 25% de chance de reviver com 40 de vida."}]
                          },
          "ogro_burro":{"nome":"Ogro Burro",
                          "hp":100,
                          "preco":1,
                          "classe":"monstro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":20, "amigos_e_inimigos":True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Barrigada Desenfreiada",
                                      "descricao":f"De 20 em todos os personagens."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":6,
                                      "argumentos":{"dano":60, "aleatorio":True, "vezes":2, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Soco Baixo",
                                      "descricao":f"Dê 60 de dano em dois personagens inimigos aleatórios."}]
                          },
          "fantasma_solitario":{"nome":"Fantasma Solitario",
                          "hp":100,
                          "preco":2,
                          "classe":"monstro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":3,
                                      "argumentos":{"dano":30, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Assombração",
                                      "descricao":f"De 30 de dano em um personagem inimigo aleatorio."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_nerf_global_dano,
                                      "argumentos":{"buff":10, "soma_por_caracteristicas":True, "caracteristicas":{"key":"hp", "valor":0, "time_atacante":True, "time_atacado":True},
                                                    "image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Defesa dos Mortos",
                                      "descricao":f"Enquanto vivo, todos os personagens aliados no seu lado do campo, ganham -10 de dano para cada lacaio morto."}]
                          },
          "milicia_fantasma":{"nome":"Milicia Fantasma",
                          "hp":110,
                          "preco":2,
                          "classe":"monstro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":10, "aleatorio": False, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Estou na Porta",
                                      "descricao":f"De 10 de dano em um personagem inimigo a sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":30, "aleatorio": True, "vezes":3, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Impostos ou Saque",
                                      "descricao":f"De 30 de dano em um personagem aleatório 3 vezes."}],
                          },
          "gigante":{"nome":"Gigante",
                          "hp":180,
                          "preco":4,
                          "classe":"monstro",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":30, "aleatorio":False, "vezes":2, "animacao": "espada", "image":{"image":soco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Soco Bruto",
                                      "descricao":f"De 30 de dano em dois personagens inimigos a sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":70, "amigos_e_inimigos":True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Pisada Terremoto",
                                      "descricao":f"Dê 70 de dano em em todos os personagens."}]
                          },
          "protetor_do_tesouro":{"nome":"Protetor do Tesouro",
                          "hp":170,
                          "preco":4,
                          "classe":"noturno",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":100, "aleatorio": False, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Sombra da Caverna",
                                      "descricao":f"De 100 de dano em um personagem inimigo a sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":True,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_reviver,
                                      "argumentos":{"chance":0.15,  "vida":60, "vivo":False, "image":{"image":cemiterio, "frames":4, "wait":50, "to_start":TEMPO[1], "x":7, "y":2}},
                                      "nome":"Mito das Sombras",
                                      "descricao":f"Morto ou vivo, em todo o turno aliado, tem 15% de chance de reviver um lacaio morto com até 60 de vida."}]
                          },
          "acumulador_de_almas":{"nome":"Acumulador de Almas",
                          "hp":100,
                          "preco":2,
                          "classe":"noturno",
                          "arte":None,
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_e_cura_acumulador,
                                      "dado":3,
                                      "argumentos":{"dano":20, "buff":10, "aleatorio": True, "animacao": "espada", "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Roubar Vida",
                                      "descricao":f"De 20 de dano a um personagem inimigo aleatório e se cure nesse valor."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":False,
                                      "funcao":None,
                                      "nome":"Lâmina Sugadora",
                                      "descricao":f"Cada vez que esse lacaio usar o ataque 'Roubar Vida', ele ganha um bonûs de 10 de dano que acumula."}]
                          },
          }

if __name__ == "__main__":
    DEBUG = True
    TIMES = [[CARTAS["ogro_burro"].copy(),
              CARTAS["protetor_do_tesouro"].copy(),
              CARTAS["fantasma_solitario"].copy()],
             [CARTAS["acumulador_de_almas"].copy(),
              CARTAS["gigante"].copy(),
              CARTAS["zumbi"].copy()]]
    
    jogar(TIMES)
