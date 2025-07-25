"""
Funcionamento das cartas

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
from inspect import signature
from card_game import Screen
from os import listdir
from json import load
from game_config import *
from arts import *
from auxiliary_functions import criar_save, ler_save, adicionar_save, put_color_text
from threading import Thread

game = Screen(x = X, y = Y, fps = FPS)
DEBUG = False
#=====================================================================================
#Engine do jogo:

def cl() -> None:
    """
    Limpa o texto do buffer
    """
    buffer_("§")
    #sleep(1/FPS)
    #game.animation = True

def buffer_(texto:str, end:str = "\n") -> None:
    globals()["BUFFER_TEXTO"] += f"{texto}{end}"

    i = len(globals()["BUFFER_TEXTO"]) + 1
    texto = globals()["BUFFER_TEXTO"][:i]
    globals()["BUFFER_TEXTO"] = globals()["BUFFER_TEXTO"][i:]
    
    if DEBUG:
        print(texto)
    else:
        game.buffer_text += f"{texto.replace('§', '')}"
        if len(game.buffer_text.split("\n")) > 9:
            game.buffer_text = game.buffer_text[game.buffer_text.find("\n") + 1:]
            game.animation = True
            

def loop_buffer_() -> None:
    """
    Coloca o texto no buffer_ ou printa o texto
    """
    while not globals()["QUEBRA_LOOP_TEXTO"]:
        if globals()["BUFFER_TEXTO"] != "":
            i = len(globals()["BUFFER_TEXTO"]) + 1 #min(10 + int((len(globals()["BUFFER_TEXTO"])*0.8)), len(globals()["BUFFER_TEXTO"]) + 1)
            texto = globals()["BUFFER_TEXTO"][:i]
            globals()["BUFFER_TEXTO"] = globals()["BUFFER_TEXTO"][i:]
            
            if DEBUG:
                print(texto)
            else:
                game.buffer_text += f"{texto.replace('§', '')}"
                if len(game.buffer_text.split("\n")) > 9:
                    game.buffer_text = game.buffer_text[game.buffer_text.find("\n") + 1:]
                    game.animation = True
                    
        sleep(1/FPS)
                

def jogar(TIMES:list, graphic:bool = True) -> None:
    """
    Função principal com a lógica dos turnos, só termina quando o jogo acaba
    """
    from text_mission import conferir_missoes
    globals()["BUFFER_TEXTO"] = ""
    globals()["QUEBRA_LOOP_TEXTO"] = False
    #thread_texto = Thread(target = loop_buffer_)
    #thread_texto.start()

    if graphic == True:
        if not "game" in globals():
            globals()["game"] = Screen(x = X, y = Y, fps = FPS)
    else:
        globals()["game"] = graphic() #graphic deve ser uma classe falsa para que não seja ativado os gráficos
        for VARIAVEL_CONFIGURACAO in ["SLEEP_TURN", "SLEEP_BOT", "SLEEP_INITIAL_TURN", "SLEEP_END_TURN", "SLEEP_DICE"]:
            globals()[VARIAVEL_CONFIGURACAO] = 0

    globals()["game"].in_run = True

    #Valores de turno:
    globals()["TIMES"] = TIMES
    globals()["PARTIDA"] = 0 #Partida
    globals()["TABULEIRO"] = 0 #Tabuleiro
    globals()["ESCOLHIDO"] = [0, 0] #Personagem escolhido por tabuleiro

    for time in TIMES:
        for p in time:
            p["hp_inicial"] = p["hp"]

    #Conferindo as missões antes do jogo começar:
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
    conferir_missoes(tipo = "inicio", save = memoria_save)

    while globals()["PARTIDA"] < 100: #Caso o jogo demore mais de 100 partidas ele termina
        time_atacante = TIMES[globals()["TABULEIRO"]]
        time_atacado = TIMES[(globals()["TABULEIRO"] + 1) % 2]
        globals()["time_atacante"] = time_atacante
        globals()["time_atacado"] = time_atacado

        #Escolhedo o personagem que atacara nesse round
        personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
        globals()["personagem_atual"] = personagem_atual

        n = 0
        while personagem_atual["hp"] <= 0 and n < 3:
            buffer_(f"Pulando personagem {personagem_atual['nome']}...")
            globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
            personagem_atual = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
            globals()["personagem_atual"] = personagem_atual
            n += 1
        
        if n >= 3: #Termina o jogo
            buffer_(f"O JOGO TERMINOU!")
            if sum([TIMES[1][i]["hp"] for i in range(3)]) > 0:
                venceu = True
            else:
                venceu = False
            break

        printar(personagem_atual, {"image":base_card_2, "frames":6, "wait":80, "to_start":0, "x":-1, "y":-1})

        buffer_(f"Turno {globals()['PARTIDA']} do {personagem_atual['nome']} | TABULEIRO: {globals()['TABULEIRO']} - POSIÇÃO: {globals()['ESCOLHIDO'][globals()['TABULEIRO']]}")
        globals()["turno_atual"][0] = globals()['PARTIDA']

        ###Vendo se tem alguma habilidade passiva de começo de turno:
        conferir_habilidade(tempo = "comeco", ataque = True, time = time_atacante)
        conferir_habilidade(tempo = "comeco", defesa = True, time = time_atacado)
        conferir_habilidade(tempo = "comeco", ataque = True, defesa = True, time = time_atacante)
        conferir_habilidade(tempo = "comeco", ataque = True, defesa = True, time = time_atacado)
        sleep(SLEEP_INITIAL_TURN)

        personagem_atual["buff_cura"] = globals()["BUFF_CURA"]
        personagem_atual["buff_dano"] = globals()["BUFF_TEMPORARIO"]
        personagem_atual["buff_escudo"] = globals()["NERF_TEMPORARIO"]

        numero_dado = jogar_dado()
        globals()["numero_dado"][0] = numero_dado
        sleep(SLEEP_DICE)

        ###Vendo ataques do personagem:
        verificar_ataques(personagem_atual, numero_dado)
        sleep(SLEEP_TURN)
        cl()

        ###Vendo se tem alguma habilidade passiva de final de turno:
        conferir_habilidade(tempo = "final", ataque = True, time = time_atacante)
        conferir_habilidade(tempo = "final", defesa = True, time = time_atacado)
        conferir_habilidade(tempo = "final", ataque = True, defesa = True, time = time_atacante)
        conferir_habilidade(tempo = "final", ataque = True, defesa = True, time = time_atacado)

        personagem_atual["buff_cura"] = globals()["BUFF_CURA"]
        personagem_atual["buff_dano"] = globals()["BUFF_TEMPORARIO"]
        personagem_atual["buff_escudo"] = globals()["NERF_TEMPORARIO"]
        
        sleep(SLEEP_END_TURN)

        ### Vendo se o personagem está envenenado:
        conferir_veneno(time = [*time_atacante, *time_atacado])

        #Ajustando valores de turno:      
        globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
        globals()["TABULEIRO"] = (globals()["TABULEIRO"] + 1) % 2
        globals()["PARTIDA"] += 1

        reset_globais()

        #Conferindo missões
        #conferir_missoes(tipo = "jogo", save = memoria_save)
    
    if venceu:
        memoria_save = ler_save()
        if memoria_save == None:
            memoria_save = criar_save()

        memoria_save["exp"] += 3
        memoria_save["moedas"] += 40
        memoria_save["vitorias"] += 1
        adicionar_save(memoria_save)
        
        game.add_effects(x = 50,
                     y = 20,
                     image = vitoria,
                     frames = 4,
                     wait = 200,
                     to_start = 0,
                     tipe = "aleatorio")

        conferir_missoes(tipo = "vitoria", save = memoria_save, TIMES = TIMES)

    else:
        memoria_save = ler_save()
        if memoria_save == None:
            memoria_save = criar_save()

        memoria_save["exp"] += 1
        memoria_save["moedas"] += 10
        memoria_save["derrotas"] += 1
        adicionar_save(memoria_save)

        conferir_missoes(tipo = "derrota", save = memoria_save, TIMES = TIMES)

    sleep(3)
    globals()["game"].close()

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
                if "usos" in ataque:
                    if ataque["usos"] > 0:
                        ataques_validos.append(ataque)
                        buffer_(f"({n}) {ataque['nome']}: {ataque['descricao']}")
                        n += 1
                else:
                    ataques_validos.append(ataque)
                    buffer_(f"({n}) {ataque['nome']}: {ataque['descricao']}")
                    n += 1

    #Permite que o jogador escolha um dos ataques:
    if len(ataques_validos) > 0:
        while True:
            if CONTRA_BOT and globals()["turno_atual"][0] % 2 == 0:
                escolha = int(random()*len(ataques_validos) + 1)
                sleep(SLEEP_BOT)
            else:
                escolha = input()
            try:
                escolha = int(escolha)
                if 1 <= escolha < len(ataques_validos) + 1:
                    ataque = ataques_validos[escolha - 1]
                    break
            except:
                pass

        #Atacando usando os argumentos passados e os argumentos globais que estão em 'jogar()'
        if "usos" in ataque:
            ataque["usos"] -= 1
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
                     image = dados[dado],
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
            if CONTRA_BOT and globals()["turno_atual"][0] % 2 == 0:
                buffer_("(BOT ESCOLHENDO O NÚMERO DO INIMIGO QUE DESEJA ATACAR)")
                escolha = int(random()*len(possiveis) + 1)
                sleep(1)
            else:
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
        
                if habilidade["tempo"] == tempo and (habilidade["ataque"] == ataque and habilidade["defesa"] == defesa):
                    if (habilidade["vivo"] and personagem["hp"] > 0) or (habilidade["morto"] and personagem["hp"] <= 0):
                        buffer_(f"{habilidade['nome']}: ", end = "")
                        habilidade["funcao"](**habilidade["argumentos"], personagem = personagem)

def conferir_veneno(time:list):
    for personagem in time:
        if ("veneno" in personagem) and personagem["hp"] > 0:
            personagem["hp"] = max(personagem["hp"] - personagem["veneno"], 0)
            buffer_(f"{personagem['nome']} sofrendo {personagem['veneno']} de dano de veneno...")

#-------------------------------------------------------------------------------------
#Funções de dano:

def base_ataque(personagem_inimigo:dict, dano:int):
    """
    Base do ataque
    """
    if type(dano) == list:
        dano = dano[0]
        
    globals()["ultimo_ataque"][0] = dano

    if globals()["menor_ataque"][0] == None:
        globals()["menor_ataque"][0] = dano
    elif globals()["maior_ataque"][0] < dano:
        globals()["maior_ataque"][0] = dano
    elif globals()["menor_ataque"][0] > dano:
        globals()["menor_ataque"][0] = dan

    if dano == None:
        dano = 0

    if ("volta" in personagem_inimigo) and (dano > 0) and (personagem_inimigo != globals()["personagem_atual"]):
        personagem_inimigo["volta"]["funcao"](personagem = globals()["personagem_atual"], **personagem_inimigo["volta"]["argumentos"])

    return max(personagem_inimigo["hp"] - max(dano + globals()["BUFF_TEMPORARIO"] - globals()["NERF_TEMPORARIO"], 0), 0)
    
def dano_(dano:int, image:dict, aleatorio:bool = False, vezes:int = 1, todos:bool = False, amigos_e_inimigos:bool = False, personagem = None, multiplicador:int = None, chance:float = 1) -> None:
    """
    Causa dano em um personagem inimigo, pode ser aleatorio ou não
    """
    if type(vezes) == list:
        vezes:int = vezes[0]

    if type(multiplicador) == list:
        multiplicador:int = multiplicador[0]
    
    if random() < chance:
        if type(dano) == list: #Casos que recebem listas com variáveis
            if dano[0] != None:
                if multiplicador != None:
                    dano = dano[0] * multiplicador
                else:
                    dano = dano[0]

        if personagem != None:
            buffer_(put_color_text(f"Atacando {personagem['nome']} em {dano}...", tipo = "ataque"))
            personagem["hp"] = base_ataque(personagem, dano)
            printar(personagem, image)
            return None
            
        if not amigos_e_inimigos:
            for _ in range(vezes):
                time_inimigo = (globals()["TABULEIRO"] + 1) % 2
                if todos:
                    personagens_inimigos = globals()["TIMES"][time_inimigo]
                else:
                    personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

                for personagem_inimigo in personagens_inimigos:
                    buffer_(put_color_text(f"Atacando {personagem_inimigo['nome']} em {dano}...", tipo = "ataque"))
                    personagem_inimigo["hp"] = base_ataque(personagem_inimigo, dano)

                    printar(personagem_inimigo, image)

        else:
            buffer_(put_color_text(f"Atacando todos os personagens em {dano}...", tipo = "ataque"))
            time_inimigo = (globals()["TABULEIRO"] + 1) % 2
            personagens_inimigos = globals()["TIMES"][time_inimigo]
            for personagem_inimigo in personagens_inimigos:
                personagem_inimigo["hp"] = base_ataque(personagem_inimigo, dano)

                printar(personagem_inimigo, image)

            time_amigo = (globals()["TABULEIRO"]) % 2
            personagens_amigos = globals()["TIMES"][time_amigo]
            for personagem_amigo in personagens_amigos:
                personagem_amigo["hp"] = base_ataque(personagem_amigo, dano) #max(personagem_amigo["hp"] - max(dano + globals()["BUFF_TEMPORARIO"] - globals()["NERF_TEMPORARIO"], 0), 0)

                printar(personagem_amigo, image)

    else:
        buffer_(f"Nada aconteceu!")

def veneno_(dano:int, image:dict, aleatorio:bool = False, vezes:int = 1, todos:bool = False, amigos_e_inimigos:bool = False, personagem = None, multiplicador:int = None, chance:float = 1) -> None:
    """
    Causa dano em um personagem inimigo, pode ser aleatorio ou não
    """
    if type(vezes) == list:
        vezes:int = vezes[0]

    if type(multiplicador) == list:
        multiplicador:int = multiplicador[0]
    
    if random() < chance:
        if type(dano) == list: #Casos que recebem listas com variáveis
            if dano[0] != None:
                if multiplicador != None:
                    dano = dano[0] * multiplicador
                else:
                    dano = dano[0]

        if personagem != None:
            buffer_(put_color_text(f"Envenenando {personagem['nome']} em {dano}...", tipo = "veneno"))
            if not "veneno" in personagem:
                personagem["veneno"] = 0
            personagem["veneno"] += dano
            printar(personagem, image)
            return None
                
        if not amigos_e_inimigos:
            for _ in range(vezes):
                time_inimigo = (globals()["TABULEIRO"] + 1) % 2
                if todos:
                    personagens_inimigos = globals()["TIMES"][time_inimigo]
                else:
                    personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

                for personagem_inimigo in personagens_inimigos:
                    buffer_(put_color_text(f"Envenenando {personagem_inimigo['nome']} em {dano}...", tipo = "veneno"))
                    if not "veneno" in personagem_inimigo:
                        personagem_inimigo["veneno"] = 0
                    personagem_inimigo["veneno"] += dano

                    printar(personagem_inimigo, image)

        else:
            buffer_(put_color_text(f"Envenenando todos os personagens em {dano}...", tipo = "veneno"))
            time_inimigo = (globals()["TABULEIRO"] + 1) % 2
            personagens_inimigos = globals()["TIMES"][time_inimigo]
            for personagem_inimigo in personagens_inimigos:
                if not "veneno" in personagem_inimigo:
                    personagem_inimigo["veneno"] = 0
                personagem_inimigo["veneno"] += dano

                printar(personagem_inimigo, image)

            time_amigo = (globals()["TABULEIRO"]) % 2
            personagens_amigos = globals()["TIMES"][time_amigo]
            for personagem_amigo in personagens_amigos:
                if not "veneno" in personagem_amigo:
                    personagem_amigo["veneno"] = 0
                personagem_amigo["veneno"] += dano
                
                printar(personagem_amigo, image)

    else:
        buffer_(f"Nada aconteceu!")

def assasinato_(image:dict, aleatorio:bool = False, vezes:int = 1, chance:float = 1, todos:bool = False, personagem = None):
    if random() < chance:
        if type(vezes) == list:
            vezes:int = vezes[0]
            
        for _ in range(vezes):
            time_inimigo = (globals()["TABULEIRO"] + 1) % 2
            if todos:
                personagens_inimigos = globals()["TIMES"][time_inimigo]
            else:
                personagens_inimigos = [escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)]

            for personagem_inimigo in personagens_inimigos:
                buffer_(put_color_text(f"Destruindo {personagem_inimigo['nome']}...", tipo = "ataque"))
                personagem_inimigo["hp"] = 0

                printar(personagem_inimigo, image)

def cura_(cura:int, image:dict, aleatorio:bool = False, vezes:int = 1, todos:bool = False, chance:float = 1, si_mesmo:bool = False, curar_todos:bool = False, multiplicador:int = None, personagem = None) -> None:
    """
    Cura um personagem amigo, pode ser aleatorio ou não
    """
    if random() < chance:
        if type(vezes) == list:
            if vezes[0] == None:
                vezes = 1
            else:
                vezes:int = vezes[0]

        if type(cura) == list:
            if cura[0] == None:
                cura = 0
            else:
                cura = cura[0]

        if type(multiplicador) == list:
            multiplicador:int = multiplicador[0]

        if multiplicador != None:
            cura *= multiplicador
            
        if curar_todos:
            buffer_(put_color_text(f"Curando todos...", tipo = "cura"))
            for i in range(len(TIMES)):
                for j in range(len(TIMES[i])):
                    TIMES[i][j]["hp"] = min(TIMES[i][j]["hp"] + cura + globals()["BUFF_CURA"], TIMES[i][j]["hp_inicial"])
                    printar(TIMES[i][j], image)
        else:
            for _ in range(vezes):
                time_amigo = globals()["TABULEIRO"]
                if todos:
                    personagens_amigos = globals()["TIMES"][time_amigo]
                elif si_mesmo:
                    personagens_amigos = [personagem]
                else:
                    personagens_amigos = [escolha_inimigo(globals()["TIMES"][time_amigo], aleatorio = aleatorio)]

                for personagem_amigo in personagens_amigos:
                    buffer_(put_color_text(f"Curando {personagem_amigo['nome']} em {cura}...", tipo = "cura"))
                    personagem_amigo["hp"] = min(personagem_amigo["hp"] + cura + globals()["BUFF_CURA"], personagem_amigo["hp_inicial"])

                    printar(personagem_amigo, image)             

def trocar_vida(image:dict, si_mesmo:bool = False, chance:float = 1):
    """
    Troca a vida de um personagem inimigo com si mesmo ou com outro personagem
    """
    if si_mesmo:
        personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        personagem_inimigo = escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = True)
            
        if random() <= chance:
            buffer_(f"Trocando a vida do {personagem_inimigo['nome']} com {personagem['nome']}...")
            personagem["hp"], personagem["hp_inicial"], personagem_inimigo["hp"], personagem_inimigo["hp_inicial"] = personagem_inimigo["hp"], personagem_inimigo["hp_inicial"], personagem["hp"], personagem["hp_inicial"]
            printar(personagem, image)
            printar(personagem_inimigo, image)
        else:
            buffer_(f"Nenhuma iteração...")
    else:
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        personagem_inimigo = escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = False)
            
        time_amigo = (globals()["TABULEIRO"]) % 2
        personagem_amigo = escolha_inimigo(globals()["TIMES"][time_amigo], aleatorio = True)
        
        if random() <= chance:
            buffer_(f"Trocando a vida do {personagem_inimigo['nome']} com {personagem_amigo['nome']}...")
            personagem_amigo["hp"], personagem_amigo["hp_inicial"], personagem_inimigo["hp"], personagem_inimigo["hp_inicial"] = personagem_inimigo["hp"], personagem_inimigo["hp_inicial"], personagem_amigo["hp"], personagem_amigo["hp_inicial"]
            printar(personagem_amigo, image)
            printar(personagem_inimigo, image)
        else:
            buffer_("Nenhuma iteração...")

def copiar_atributo(image:dict, atributo:list ,aleatorio:bool = False, copia_completa:bool = False):
    time_inimigo = (globals()["TABULEIRO"] + 1) % 2
    personagem_inimigo = escolha_inimigo(globals()["TIMES"][time_inimigo], aleatorio = aleatorio)
    
    if copia_completa:
        x_temp, y_temp = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]["x"], TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]["y"]
        TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]] = personagem_inimigo.copy()
        TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]["x"] = x_temp
        TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]["y"] = y_temp
    else:
        personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
        for key in atributo:
            personagem[key] = personagem_inimigo[key]

    personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]            
    printar(personagem, image)
    printar(personagem_inimigo, image)

#-------------------------------------------------------------------------------------
#Funções de habilidade:

def habilidade_buff_global_dano(buff:int, personagem, image:dict, multiplicador:int = 1, apenas_caracteristico:bool = False, soma_por_caracteristicas:bool = False, caracteristicas:dict = None, chance:float = 1) -> None:
    """
    Da um buff...

    Se usar as caracteristicas devem ser passados:
        {"key":"classe",
        "valor":"humano",
        "time_atacante":True,
        "time_atacado":False}
    """
    if not (random() < chance):
        buffer_(f"Nada aconteceu!")
        return None

    if type(buff) == list:
        buff = buff[0]
    if type(multiplicador) == list:
        multiplicador:int = multiplicador[0]
    buff *= multiplicador
    
    if not soma_por_caracteristicas:
        if not apenas_caracteristico:
            globals()["BUFF_TEMPORARIO"] += buff
            buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Buff no dano de +{buff}", tipo = "habilidade"))
        else:
            if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
                globals()["BUFF_TEMPORARIO"] += buff
                buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Buff no dano de +{buff}", tipo = "habilidade"))
            else:
                buffer_(f"Nada aconteceu!")
    else:
        buffer_("Conferindo iterações...")
        if "time_atacante" in caracteristicas and caracteristicas["time_atacante"]:
            for personagem_ in globals()["time_atacante"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["BUFF_TEMPORARIO"] += buff
                    buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} buff no dano de +{buff}", tipo = "habilidade"))
        
        if "time_atacado" in caracteristicas and caracteristicas["time_atacado"]:
            for personagem_ in globals()["time_atacado"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["BUFF_TEMPORARIO"] += buff
                    buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} buff no dano de +{buff}", tipo = "habilidade"))
        
    if not apenas_caracteristico:
        printar(personagem, image)
    else:
        if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
            printar(personagem, image)


def habilidade_nerf_global_dano(buff:int, personagem, image:dict, apenas_caracteristico:bool = False, soma_por_caracteristicas:bool = False, caracteristicas:dict = None, multiplicador:int = 1, chance:float = 1) -> None:
    """
    Da um nerf...

    Se usar as caracteristicas devem ser passados:
        {"key":"classe",
        "valor":"humano",
        "time_atacante":True,
        "time_atacado":False}
    """
    if not (random() < chance):
        buffer_(f"Nenhuma iteração...")
        return None
        
    if type(buff) == list:
        buff = buff[0]
    if type(multiplicador) == list:
        multiplicador:int = multiplicador[0]
    buff *= multiplicador
        
    if not soma_por_caracteristicas:
        if not apenas_caracteristico:
            globals()["NERF_TEMPORARIO"] += buff
            buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Nerf no dano de -{buff}", tipo = "habilidade"))
        else:
            if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
                globals()["NERF_TEMPORARIO"] += buff
                buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Nerf no dano de -{buff}", tipo = "habilidade"))
            else:
                buffer_(f"Nada aconteceu!")
    else:
        buffer_("Conferindo iterações...")
        if "time_atacante" in caracteristicas and caracteristicas["time_atacante"]:
            for personagem_ in globals()["time_atacante"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["NERF_TEMPORARIO"] += buff
                    buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} nerf no dano de -{buff}", tipo = "habilidade"))
        
        if "time_atacado" in caracteristicas and caracteristicas["time_atacado"]:
            for personagem_ in globals()["time_atacado"]:
                if personagem_[caracteristicas["key"]] == caracteristicas["valor"]:
                    globals()["NERF_TEMPORARIO"] += buff
                    buffer_(put_color_text(f"(HABILIDADE:{personagem['nome']}) Sinergia com {personagem_['nome']} nerf no dano de -{buff}", tipo = "habilidade"))
        
    if not apenas_caracteristico:
        printar(personagem, image)
    else:
        if globals()["personagem_atual"][caracteristicas["key"]] == caracteristicas["valor"]:
            printar(personagem, image)


def habilidade_reviver(personagem, chance:float, image:dict, vida:int, si_mesmo:bool = False, vivo:bool = True):
    """
    Revive a sim mesmo ou a um personagem aleatório do mesmo time
    """
    if si_mesmo:
        if random() <= chance and personagem["hp"] <= 0:
            buffer_(put_color_text(f"Revivendo {personagem['nome']}...", tipo = "reviver"))
            personagem["hp"] = min(personagem["hp_inicial"], vida)
            printar(personagem, image)
        else:
            buffer_(f"Nenhuma iteração...")
    else:
        time_amigo = (globals()["TABULEIRO"]) % 2
        personagens_amigos = globals()["TIMES"][time_amigo]
        personagem_reviver = escolha_inimigo(personagens_amigos, aleatorio = True, vivo = vivo)
        if personagem_reviver != None and random() <= chance:
            buffer_(put_color_text(f"Revivendo {personagem_reviver['nome']}...", tipo = "reviver"))
            personagem_reviver["hp"] = min(personagem_reviver["hp_inicial"], vida)
            printar(personagem_reviver, image)
            printar(personagem, image)
        else:
            buffer_("Nenhuma iteração...")    

def habilidade_acao(funcao, argumentos_funcao:dict, personagem, image:dict) -> None:
    """
    Chama uma ação e possibilita um print extra no personagem que emite a ação
    """
    buffer_(f"(HABILIDADE) habilidade de {personagem['nome']}")

    printar(personagem, image)

    funcao(**argumentos_funcao)

def habilidade_buff_global_cura(personagem, buff:int, image:dict, chance:float = 1) -> None:
    """
    Buffa de cura
    """
    if random() < chance:
        buffer_(f"Buff de cura de +{buff}...")
        globals()["BUFF_CURA"] += buff
        printar(personagem, image)
    else:
        buffer_(f"Nenhuma iteração...")

def habilidade_buff_global_dado(personagem, buff:int, image:dict, chance:float = 1) -> None:
    """
    Buffa o dado
    """
    if random() < chance:
        buffer_(f"Somando {buff} ao dado...")
        globals()["BUFF_DADO"] += buff
        printar(personagem, image)
    else:
        buffer_(f"Nenhuma iteração...")

def habilidade_nerf_global_dado(personagem, buff:int, image:dict, chance:float = 1) -> None:
    """
    Nerfa o dado
    """
    if random() < chance:
        buffer_(f"Subtraindo {buff} ao dado...")
        globals()["NERF_DADO"] -= buff
        printar(personagem, image)
    else:
        buffer_(f"Nenhuma iteração...")

def adicionar_habilidade(funcao:dict, image:dict, chance:float = 1) -> None:
    """
    Adiciona uma abilidade a uma carta
    """
    if random() < chance:
        personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
        personagem["ataques"].append(funcao)
        printar(personagem, image)
    else:
        buffer_(f"Nenhuma iteração...")

def somar_global(variavel_global:list, soma:int, image:dict) -> None:
    """
    Soma ou subtrai uma variável global
    """
    personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
    variavel_global[0] = variavel_global[0] + soma 
    printar(personagem, image)

def pular_turno(image:dict):
    """
    Pula o turno do inimigo
    """
    personagem = TIMES[globals()["TABULEIRO"]][globals()["ESCOLHIDO"][globals()["TABULEIRO"]]]
    globals()["ESCOLHIDO"][globals()["TABULEIRO"]] = (globals()["ESCOLHIDO"][globals()["TABULEIRO"]] + 1) % 3
    globals()["TABULEIRO"] = (globals()["TABULEIRO"] + 1) % 2
    globals()["PARTIDA"] += 1
    printar(personagem, image)
    

#=====================================================================================
#=====================================================================================

def printar(personagem, image) -> None:
    if "x" in personagem:
        game.add_effects(x = personagem["x"] + image["x"],
                         y = personagem["y"] + image["y"],
                         image = image["image"],
                         frames = image["frames"],
                         wait = image["wait"],
                         to_start = image["to_start"],
                         tipe = "aleatorio" if not "tipe" in image else image["tipe"])
        
#=====================================================================================
#=====================================================================================

def dano_e_cura_acumulador(dano:int, buff:int, image:dict, aleatorio:bool = False, vezes:int = 1, todos:bool = False, amigos_e_inimigos:bool = False) -> None:
    """
    Ataque específico do acumulador
    """
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
                personagem_inimigo["hp"] = base_ataque(personagem_inimigo, dano)
                personagem["hp"] = min(personagem["hp"] + dano + globals()["BUFF_CURA"], personagem["hp_inicial"])
                personagem["ataques"][0]["argumentos"]["dano"] += buff
                personagem["ataques"][0]["descricao"] = f"De {personagem['ataques'][0]['argumentos']['dano']} de dano a um personagem inimigo aleatório e se cure nesse valor."

                printar(personagem_inimigo, image)

    else:
        time_inimigo = (globals()["TABULEIRO"] + 1) % 2
        personagens_inimigos = globals()["TIMES"][time_inimigo]
        for personagem_inimigo in personagens_inimigos:
            buffer_(f"Atacando {personagem_inimigo['nome']} em {dano}...")
            personagem_inimigo["hp"] = base_ataque(personagem_inimigo, dano)
            personagem["hp"] = min(personagem["hp"] + dano + globals()["BUFF_CURA"], personagem["hp_inicial"])
            personagem["ataques"][0]["argumentos"]["dano"] += buff
            personagem["ataques"][0]["descricao"] = f"De {personagem['ataques'][0]['argumentos']['dano']} de dano a um personagem inimigo aleatório e se cure nesse valor."

            printar(personagem_inimigo, image)

        time_amigo = (globals()["TABULEIRO"]) % 2
        personagens_amigos = globals()["TIMES"][time_amigo]
        for personagem_amigo in personagens_amigos:
            buffer_(f"Atacando {personagem_amigo['nome']} em {dano}...")
            personagem_amigo["hp"] = max(personagem_amigo["hp"] - max(dano + globals()["BUFF_TEMPORARIO"] - globals()["NERF_TEMPORARIO"], 0), 0)
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

numero_dado = [1]
turno_atual = [0]
BUFF_TEMPORARIO = 0
NERF_TEMPORARIO = 0
BUFF_CURA = 0

PARTIDA = 0 #GLOBAL = turno_atual
TABULEIRO = 0
ESCOLHIDO = [0, 0]

LIMITES_DADO = [1, 6]
NERF_DADO = 0
BUFF_DADO = 0

ultimo_ataque = [0]
maior_ataque = [0]
menor_ataque = [None]

CARTAS = {"guerreiro_preparado":{"nome":"Guerreiro Preparado",
                                 "hp":80,
                                 "preco":1,
                                 "classe":"guerreiro",
                                 "arte":imagem_guerreiro_preparado,
                                 "raridade":"comum",
                                 "ataques":[{"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":1,
                                             "argumentos":{"dano":10, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                             "nome":"Machadada Erronêa",
                                             "descricao":f"Dá 10 de dano a um personagem inimigo aleatório."},
                                            {"tipo":"ataque",
                                             "funcao":dano_,
                                             "dado":3,
                                             "argumentos":{"dano":30, "aleatorio": True, "image":{"image":martelo, "frames":4, "wait":50, "to_start":0, "x":0, "y":3}},
                                             "nome":"Machadada Certeira",
                                             "descricao":f"Dá 30 de dano a um personagem inimigo aleatório."}]
                                 },          
          "guarda_do_rei":{"nome":"Guarda do Rei",
                          "hp":100,
                          "preco":2,
                          "classe":"guerreiro",
                          "arte":imagem_guarda_do_rei,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":50, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Defesa Real",
                                      "descricao":f"Dá 50 de dano a um personagem inimigo aleatório."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":10, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Soldados em Posição",
                                      "descricao":f"Enquanto vivo, todos os outros personagens do seu lado do campo ganham +10 de dano."}]
                          },
          "escudeiro_experiente":{"nome":"Escudeiro Experiente",
                                  "hp":110,
                                  "preco":3,
                                  "classe":"guerreiro",
                                  "arte":imagem_escudeiro_experiente,
                                  "raridade":"comum",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":40, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Empurrão",
                                              "descricao":f"Dá 40 de dano a um personagem inimigo aleatório."},
                                             {"tipo":"habilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_nerf_global_dano,
                                              "argumentos":{"buff":10, "image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                              "nome":"Meu escudo primeiro",
                                              "descricao":f"Enquanto vivo, todos os outros personagens do seu lado do campo ganham +10 de defesa."}]
                                  },
          "cacador_iniciante":{"nome":"Caçador Iniciante",
                                  "hp":50,
                                  "preco":0,
                                  "classe":"guerreiro",
                                  "arte":imagem_cacador_iniciante,
                                  "arte_morto":imagem_cacador_iniciante_morto,
                                  "raridade":"comum",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":10, "aleatorio": True, "image":{"image":impacto_fraco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Tiro de Chumbo",
                                              "descricao":f"Dá 10 de dano a um personagem inimigo aleatório."}]
                                  },
          "arqueiro":{"nome":"Arqueiro",
                                  "hp":90,
                                  "preco":1,
                                  "classe":"guerreiro",
                                  "arte":imagem_arqueiro,
                                  "raridade":"comum",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":30, "aleatorio": False, "image":{"image":flecha, "frames":4, "wait":50, "to_start":0, "x":-5, "y":6}},
                                              "nome":"Ponta da Lamina",
                                              "descricao":f"Dá 30 de dano a um personagem inimigo à sua escolha."}]
                                  },
          "soldado_novato":{"nome":"Soldado Novato",
                                  "hp":80,
                                  "preco":1,
                                  "classe":"guerreiro",
                                  "arte":imagem_soldado_novato,
                                  "raridade":"comum",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":2,
                                              "argumentos":{"dano":30, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Espadada Torta",
                                              "descricao":f"Dá 30 de dano a um personagem inimigo aleatório."}]
                                  },
          "cacador_de_feras":{"nome":"Caçador de Feras",
                                  "hp":70,
                                  "preco":3,
                                  "classe":"humano",
                                  "arte":imagem_cacador_de_feras,
                                  "arte_morto":imagem_cacador_de_feras_morto,
                                  "raridade":"raro",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":5,
                                              "argumentos":{"dano":30, "todos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Preparação de Guerra",
                                              "descricao":f"Dá 30 de dano em todos os personagens inimigos."},
                                             {"tipo":"ataque",
                                              "funcao":assasinato_,
                                              "dado":6,
                                              "argumentos":{"aleatorio": True, "image":{"image":caveira, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
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
                                              "descricao":f"Enquanto vivo, todos os outros personagens do seu lado do campo ganham +10 de defesa."}]
                              },
          "rei_da_vila":{"nome":"Rei da Vila",
                                  "hp":70,
                                  "preco":3,
                                  "classe":"humano",
                                  "arte":imagem_rei_da_vila,
                                  "raridade":"raro",
                                  "ataques":[{"tipo":"habilidade",
                                              "ataque":True,
                                              "defesa":False,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_buff_global_dano,
                                              "argumentos":{"buff":25, "image":{"image":coroa, "frames":4, "wait":50, "to_start":TEMPO[1], "x":10, "y":5}},
                                              "nome":"Bençãos do Rei",
                                              "descricao":f"Enquanto vivo, todos os outros personagens do seu lado do campo ganham +25 de ataque."}]
                              },
          "curandeiro_da_vila":{"nome":"Curandeiro da Vila",
                                  "hp":40,
                                  "preco":1,
                                  "classe":"humano",
                                  "arte":imagem_curandeiro_da_vila,
                                  "raridade":"raro",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":2,
                                              "argumentos":{"dano":10, "todos":True, "image":{"image":impacto_fraco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Explosão de Luz",
                                              "descricao":f"Dá 10 de dano em todos os personagens inimigos."},
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
                                              "descricao":f"Enquanto vivo, no final do seu turno, cure um personagem aliado aleatório em 30."}]
                              },
          "campones_corajoso":{"nome":"Camponês Corajoso",
                          "hp":80,
                          "preco":1,
                          "classe":"humano",
                          "arte":imagem_campones_corajoso,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":3,
                                      "argumentos":{"dano":20, "aleatorio": False, "image":{"image":mao, "frames":6, "wait":25, "to_start":0, "x":10, "y":3}},
                                      "nome":"Pá Leve, Mão Pesada",
                                      "descricao":f"Dá 20 de dano a um personagem inimigo à sua escolha."},
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
                                      "descricao":f"Enquanto vivo, todos os personagens no seu lado do campo ganham +10 de dano para cada guerreiro aliado."}]
                          },
          "esqueleto_insano":{"nome":"Esqueleto Insano",
                          "hp":80,
                          "preco":1,
                          "classe":"monstro",
                          "arte":imagem_esqueleto_insano,
                          "arte_morto":imagem_esqueleto_insano_morto,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":30, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Caçada a Carne",
                                      "descricao":f"Dá 30 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_reviver,
                                      "argumentos":{"chance":0.25, "si_mesmo":True, "vida":40, "image":{"image":cemiterio, "frames":4, "wait":50, "to_start":TEMPO[1], "x":7, "y":2}},
                                      "nome":"Saindo da Terra",
                                      "descricao":f"Enquanto morto, no início de cada turno inimigo, tem 25% de chance de reviver com 40 de vida."}]
                          },
          "orc_rejeitado":{"nome":"Orc Rejeitado",
                          "hp":100,
                          "preco":1,
                          "classe":"monstro",
                          "arte":imagem_orc_rejeitado,
                           "arte":imagem_orc_rejeitado_morto,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":20, "amigos_e_inimigos":True, "image":{"image":impacto_fraco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Baba Acida",
                                      "descricao":f"Dá 20 de dano em todos os personagens."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":6,
                                      "argumentos":{"dano":60, "aleatorio":True, "vezes":2, "image":{"image":garra, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Pulo nas Costas",
                                      "descricao":f"Dá 60 de dano a dois personagens inimigos aleatórios."}]
                          },
          "fantasma_solitario":{"nome":"Fantasma Solitario",
                          "hp":100,
                          "preco":2,
                          "classe":"monstro",
                          "arte":imagem_fantasma_solitario,
                          "raridade":"raro",                                
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":3,
                                      "argumentos":{"dano":30, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Assombração",
                                      "descricao":f"Dá 30 de dano a um personagem inimigo aleatório."},
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
                                      "descricao":f"Enquanto vivo, todos os personagens aliados do seu lado do campo ganham -10 de dano para cada lacaio morto."}]
                          },
          "milicia_fantasma":{"nome":"Milicia Fantasma",
                          "hp":110,
                          "preco":2,
                          "classe":"monstro",
                          "arte":imagem_milicia_fantasma,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":10, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Estou na Porta",
                                      "descricao":f"Dá 10 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":30, "aleatorio": True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Impostos ou Saque",
                                      "descricao":f"Dá 30 de dano a um personagem aleatório 3 vezes."}],
                          },
          "gigante":{"nome":"Gigante",
                          "hp":170,
                          "preco":4,
                          "classe":"monstro",
                          "arte":imagem_gigante,
                          "arte_morto":imagem_gigante_morto,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":30, "aleatorio":False, "vezes":2, "image":{"image":soco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Soco Bruto",
                                      "descricao":f"Dá 30 de dano a dois personagens inimigos à sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":70, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Pisada Terremoto",
                                      "descricao":f"Dá 70 de dano em todos os personagens."}]
                          },
          "protetor_do_tesouro":{"nome":"Protetor do Tesouro",
                          "hp":160,
                          "preco":4,
                          "classe":"noturno",
                          "arte":imagem_protetor_do_tesouro,
                          "arte_morto":imagem_protetor_do_tesouro_morto,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":100, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Sombra da Caverna",
                                      "descricao":f"Dá 100 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":True,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_reviver,
                                      "argumentos":{"chance":0.15,  "vida":60, "vivo":False, "image":{"image":cemiterio, "frames":4, "wait":50, "to_start":TEMPO[1], "x":7, "y":2}},
                                      "nome":"Mito das Sombras",
                                      "descricao":f"Morto ou vivo, no início de cada turno aliado, tem 15% de chance de reviver com até 60 de vida um personagem morto."}]
                          },
          "acumulador_de_almas":{"nome":"Acumulador de Almas",
                          "hp":100,
                          "preco":2,
                          "classe":"noturno",
                          "arte":imagem_acumulador_de_almas,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_e_cura_acumulador,
                                      "dado":3,
                                      "argumentos":{"dano":20, "buff":10, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Roubar Vida",
                                      "descricao":f"Dá 20 de dano a um personagem inimigo aleatório e se cura nesse valor."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":False,
                                      "funcao":None,
                                      "nome":"Lâmina Sugadora",
                                      "descricao":f"Cada vez que esse lacaio usar o ataque 'Roubar Vida', ele ganha um bônus de 10 de dano que se acumula."}]
                          },
          "dono_do_cassino":{"nome":"Dono do Cassino",
                          "hp":90,
                          "preco":3,
                          "classe":"noturno",
                          "arte":imagem_dono_do_cassino,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":30, "aleatorio": False, "image":{"image":guarda_chuva, "frames":6, "wait":50, "to_start":0, "x":0, "y":7}},
                                      "nome":"Não Pode Anotar",
                                      "descricao":f"Dá 30 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dado,
                                      "argumentos":{"buff":1, "image":{"image":soma_dado, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Dono Legal",
                                      "descricao":f"Enquanto vivo, some 1 aos seus dados."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_nerf_global_dado,
                                      "argumentos":{"buff":1, "image":{"image":subtracao_dado, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Dono Chato",
                                      "descricao":f"Enquanto vivo, subtraia 1 aos dados dos inimigos."}]
                          },
          "vinganca_da_noite":{"nome":"Vingança da Noite",
                          "hp":80,
                          "preco":1,
                          "classe":"noturno",
                          "arte":imagem_vinganca_da_noite,
                          "arte_morto":imagem_vinganca_da_noite_morto,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":40, "aleatorio": True, "image":{"image":soco, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Mão das Profundezas",
                                      "descricao":f"Dá 40 de dano a um personagem inimigo aleatório."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":20, "amigos_e_inimigos":True, "image":{"image":garra, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Sequestro Total",
                                      "descricao":f"Dá 20 de dano em todos os personagens."}],
                          },
          "mestre_dos_venenos":{"nome":"Mestre dos Venenos",
                          "hp":80,
                          "preco":3,
                          "classe":"assassino",
                          "arte":imagem_mestre_dos_venenos,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":40, "aleatorio": True, "vezes":2, "image":{"image":pocao[0], "frames":6, "wait":45, "to_start":0, "x":14, "y":7}},
                                      "nome":"Vai um Suco?",
                                      "descricao":f"Dá 40 de dano a dois personagens inimigos aleatórios."},
                                     {"tipo":"habilidade",
                                      "funcao":dano_,
                                      "tempo":"final",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "argumentos":{"dano":10, "amigos_e_inimigos":True, "image":{"image":pocao[1], "frames":6, "wait":40, "to_start":TEMPO[2], "x":15, "y":7}},
                                      "nome":"Todos Envenenados!",
                                      "descricao":f"Dá 10 de dano a todos os personagens no início de cada turno aliado."}],
                        },
          "assasina_de_quadrilha":{"nome":"Assasina de Quadrilha",
                          "hp":90,
                          "preco":3,
                          "classe":"assassino",
                          "arte":imagem_assasina_de_quadrilha,
                          "arte_morto":imagem_assasina_de_quadrilha_morto,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":30, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Facada nas costas",
                                      "descricao":f"Dá 30 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":20, "soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"assassino", "time_atacante":True, "time_atacado":False},
                                                   "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Caos na Cidade",
                                      "descricao":f"Enquanto vivo, todos os personagens do seu lado do campo ganham +20 para cada assassino aliado."}]
                        },
          "mestre_da_lamina":{"nome":"Mestre da Lamina",
                          "hp":70,
                          "preco":1,
                          "classe":"assassino",
                          "arte":imagem_mestre_da_lamina,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":6,
                                      "argumentos":{"dano":60, "aleatorio": False, "image":{"image":faca_2, "frames":6, "wait":50, "to_start":0, "x":-3, "y":10}},
                                      "nome":"Espionagem",
                                      "descricao":f"Dá 60 de dano a um personagem inimigo à sua escolha"},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":6,
                                      "argumentos":{"dano":120, "aleatorio": True, "image":{"image":faca_1, "frames":6, "wait":50, "to_start":0, "x":-3, "y":10}},
                                      "nome":"Atrás de Você",
                                      "descricao":f"Dá 120 de dano a um personagem inimigo aleatório."}],
                          },
          "assasino_laranja":{"nome":"Assassino Laranja",
                          "hp":40,
                          "preco":2,
                          "classe":"assassino",
                          "arte":imagem_assasino_laranja,
                          "arte_morto":imagem_assasino_laranja_morto,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":20, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Olhem pra mim",
                                      "descricao":f"Dá 20 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":20, "soma_por_caracteristicas":True, "caracteristicas":{"key":"hp", "valor":0, "time_atacante":True, "time_atacado":False},
                                                   "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Sacrificio da Ordem",
                                      "descricao":f"Enquanto morto, todos os personagens do seu lado do campo ganham +20 de dano para cada personagem aliado morto."}]
                        },
          "profeta_das_areias":{"nome":"Profeta das Areias",
                          "hp":60,
                          "preco":3,
                          "classe":"humano",
                          "arte":imagem_profeta_das_arreias,
                          "arte_morto":imagem_profeta_das_arreias_morto,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":40, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Ilusão do Deserto",
                                      "descricao":f"Dá 40 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":cura_,
                                      "dado":2,
                                      "argumentos":{"cura":80, "aleatorio": False, "image":{"image":cruz, "frames":4, "wait":70, "to_start":0, "x":8, "y":2}},
                                      "nome":"Oásis",
                                      "descricao":f"Cure 80 de vida de um personagem aliado à sua escolha."},],
                          },
          "quan_o_equilibro":{"nome":"Guardião do Equilibrio",
                          "hp":50,
                          "preco":2,
                          "classe":"lenda",
                          "arte":imagem_quan,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":cura_,
                                      "dado":5,
                                      "argumentos":{"cura":120, "aleatorio": False, "vezes":2, "image":{"image":cruz, "frames":4, "wait":70, "to_start":0, "x":8, "y":2}},
                                      "nome":"Redenção",
                                      "descricao":f"Cure 120 de dano de dois personagem aliados à sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":assasinato_,
                                      "dado":6,
                                      "argumentos":{"aleatorio": True, "image":{"image":caveira, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Queda",
                                      "descricao":f"Destrua um personagem inimigo aleatório."},
                                     ],
                          },
          "mago_suporte":{"nome":"Mago Suporte",
                          "hp":50,
                          "preco":3,
                          "classe":"humano",
                          "arte":imagem_mago_suporte,
                          "arte_morto":imagem_mago_suporte_morto,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":10, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Bola de Fogo",
                                      "descricao":f"Dá 10 de dano a um personagem inimigo a sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":20, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Suporte Completo",
                                      "descricao":f"Enquanto vivo, todos os personagens do seu lado do campo ganham +30 de dano."}]
                        },
          "fenix":{"nome":"Fenix",
                          "hp":50,
                          "preco":2,
                          "classe":"lenda",
                          "arte":imagem_fenix,
                          "arte_morto":ovo_fenix,
                          "raridade":"lendario",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":20, "aleatorio": True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Revoada Flamejante",
                                      "descricao":f"Dá 20 de dano a três personagens inimigos aleatórios."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_reviver,
                                      "argumentos":{"chance":1, "si_mesmo":True, "vida":20, "image":{"image":fogo, "frames":4, "wait":40, "to_start":TEMPO[1], "x":1, "y":7}},
                                      "nome":"Reviver da Fenix",
                                      "descricao":f"Sempre que morrer, no seu próximo turno, reviva com 20 de vida."}]
                          },
          "cactus_cowboy":{"nome":"Cactus Cowboy",
                          "hp":130,
                          "preco":4,
                          "classe":"lenda",
                          "arte":imagem_cactus_cowboy,
                          "arte_morto":imagem_cactus_cowboy_morto,
                          "raridade":"epico",
                           "volta":{"funcao":dano_,
                                    "argumentos":{"dano":20, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                    "nome":"Espinhos",
                                    "descricao":f"Dá 20 de dano no lacaio."},
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":10, "aleatorio": True, "vezes":3, "image":{"image":tnt_1, "frames":4, "wait":50, "to_start":0, "x":3, "y":8}},
                                      "nome":"Duelo aceito!",
                                      "descricao":f"Dá 10 de dano a 3 personagens inimigos aleatórios."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":True,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":20, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Cuidado, espinho!",
                                      "descricao":f"Enquanto vivo, todos os personagens do jogo ganham +20 de dano."}]
                        },
          "cubo":{"nome":"Cubo",
                          "hp":60,
                          "preco":1,
                          "classe":"lenda",
                          "arte":imagem_cubo,
                          "raridade":"lendario",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":0,
                                      "argumentos":{"dano":numero_dado, "aleatorio": False, "multiplicador":10, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Dado o Dado",
                                      "descricao":f"Dá 10 vezes o número que sair no dado a um personagem à sua escolha."},]
                        },
          "bandido_cinico":{"nome":"Bandido Cínico",
                          "hp":60,
                          "preco":1,
                          "classe":"assassino",
                          "arte":imagem_bandido_cinico,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":1,
                                      "argumentos":{"dano":20, "aleatorio": True, "image":{"image":faca_2, "frames":6, "wait":50, "to_start":0, "x":-3, "y":10}},
                                      "nome":"Facada Covarde",
                                      "descricao":f"Dá 20 de dano a um personagem inimigo aleatório."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":2,
                                      "argumentos":{"dano":20, "aleatorio": True, "vezes":2, "image":{"image":tnt_2, "frames":4, "wait":50, "to_start":0, "x":3, "y":12}},
                                      "nome":"Explodindo Porta!",
                                      "descricao":f"Dá 20 de dano a 2 personagens inimigos aleatórios."},]
                        },
          "mafioso_acumulador":{"nome":"Mafioso Acumulador",
                          "hp":90,
                          "preco":3,
                          "classe":"assassino",
                          "arte":imagem_mafioso_acumulador,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":turno_atual, "aleatorio": False, "multiplicador":5, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Uma Palavrinha",
                                      "descricao":f"Dá o dano do turno atual vezes 5 a um personagem à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_nerf_global_dano,
                                      "argumentos":{"buff":10, "soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"assassino", "time_atacante":False, "time_atacado":True},
                                                   "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Big Boss",
                                      "descricao":f"Os personagens do seu lado do campo recebem -10 de dano para cada assassino aliado."}
                                     ]
                        },
          "cogumelo_venenoso":{"nome":"Cogumelo Venenoso",
                          "hp":70,
                          "preco":3,
                          "classe":"monstro",
                          "arte":imagem_cogumelo_venenoso,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":5,
                                              "argumentos":{"dano":20, "todos":True, "image":{"image":fumaca, "frames":6, "wait":50, "to_start":0, "x":9, "y":6}},
                                              "nome":"Fungo Perigoso",
                                              "descricao":f"Dá 20 de dano a todos os personagens inimigos."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_nerf_global_dano,
                                      "argumentos":{"buff":turno_atual, "multiplicador":2, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Fungo Perigoso",
                                      "descricao":f"A cada turno, enquanto estiver vivo, seu time recebe -2 de dano, acumula."}
                                     ]
                        },
          "flores_sinistras":{"nome":"Flores Sinistras",
                          "hp":40,
                          "preco":0,
                          "classe":"monstro",
                          "arte":imagem_flores_sinistras,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":3,
                                              "argumentos":{"dano":10, "aleatorio":False, "vezes":2, "image":{"image":fumaca, "frames":6, "wait":50, "to_start":0, "x":9, "y":6}},
                                              "nome":"Pólen Venenoso",
                                              "descricao":f"Dá 10 de dano a dois personagens inimigos à sua escolha."}
                                     ]
                        },
          "exterminador":{"nome":"Exterminador",
                          "hp":160,
                          "preco":4,
                          "classe":"guerreiro",
                          "arte":imagem_exterminador,
                          "raridade":"lendario",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":turno_atual, "multiplicador":10, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Alto-Destruição",
                                      "descricao":f"Dá 5 vezes o número de turnos de dano a todos os personagens."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":50, "aleatorio":False, "vezes":2, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Lazer Direcionado",
                                      "descricao":f"Dá 50 de dano a dois personagens inimigos à sua escolha."}]
                          },
          "hacker":{"nome":"H@ck3r",
                          "hp":70,
                          "preco":3,
                          "classe":"lenda",
                          "arte":imagem_hacker,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":1,
                                      "argumentos":{"dano":20, "aleatorio":False, "image":{"image":cursor, "frames":10, "wait":5, "to_start":0, "x":14, "y":7, "tipe":"bug"}},
                                      "nome":"Cliquer",
                                      "descricao":f"Dá 20 de dano em um personagem inimigo à sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":trocar_vida,
                                      "dado":5,
                                      "argumentos":{"si_mesmo":False, "image":{"image":base_card_transparent, "frames":6, "wait":5, "to_start":0, "x":0, "y":2, "tipe":"bug_rapido"}},
                                      "nome":"Bug no Sistema",
                                      "descricao":f"Escolha um personagem inimigo, troque a vida dele com a de um personagem aleatório."},
                                     {"tipo":"ataque",
                                      "funcao":cura_,
                                      "dado":6,
                                      "argumentos":{"cura":1_000, "curar_todos":True, "image":{"image":seta_cima, "frames":6, "wait":5, "to_start":0, "x":13, "y":6, "tipe":"bug"}},
                                      "nome":"Reboot",
                                      "descricao":f"Todos os lacaios voltam com a vida inicial do jogo."},
                                     ]
                          },
          "o_imitador":{"nome":"O Imitador",
                          "hp":40,
                          "preco":2,
                          "classe":"noturno",
                          "arte":imagem_o_imitador,
                          "raridade":"lendario",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":copiar_atributo,
                                      "dado":4,
                                      "argumentos":{"atributo":["hp", "hp_inicial"], "image":{"image":interrogacao, "frames":6, "wait":50, "to_start":0, "x":13, "y":5, "tipe":"hacker"}},
                                      "nome":"Jogo da imitação",
                                      "descricao":f"Copie a vida de um personagem inimigo a sua escolha."},
                                     {"tipo":"ataque",
                                      "funcao":copiar_atributo,
                                      "dado":6,
                                      "argumentos":{"atributo":[None], "copia_completa":True, "image":{"image":mascarazinha, "frames":6, "wait":5, "to_start":0, "x":10, "y":5, "tipe":"bug"}},
                                      "nome":"Cópia Identica",
                                      "descricao":f"Se torne uma cópia identica de um personagem inimigo a sua escolha."},
                                     ]
                          },
          "lobo_da_noite":{"nome":"Lobo da Noite",
                          "hp":50,
                          "preco":1,
                          "classe":"noturno",
                          "arte":imagem_lobo_da_noite,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":40, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"A Espreita",
                                      "descricao":f"Dá 40 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_buff_global_dano,
                                      "argumentos":{"buff":5, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Uivo do Bando",
                                      "descricao":f"Enquanto vivo, todos os outros personagens do seu lado do campo ganham +5 de dano."}],
                          },
          "duas_faces":{"nome":"Duas Faces",
                          "hp":30,
                          "preco":1,
                          "classe":"noturno",
                          "arte":imagem_duas_faces,
                          "raridade":"epico",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":1,
                                      "argumentos":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Mudança de Expressão",
                                      "descricao":f"Dá 10 de dano a um personagem inimigo aleatório."},
                                     {"tipo":"habilidade",
                                      "tempo":"final",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                       "funcao":habilidade_acao,
                                              "argumentos":{"funcao":cura_,
                                                           "image":{"image":imagem_duas_faces_feliz, "frames":4, "wait":60, "to_start":TEMPO[1], "x":1, "y":2},
                                                            "argumentos_funcao":{"cura":10, "aleatorio":True, "image":{"image":cruz, "frames":4, "wait":60, "to_start":TEMPO[1], "x":8, "y":2}}},
                                      "nome":"Feliz",
                                      "descricao":f"Vivo, cura em 10 um personagem aliado aleatório."},
                                     {"tipo":"habilidade",
                                      "tempo":"final",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":habilidade_acao,
                                              "argumentos":{"funcao":dano_,
                                                           "image":{"image":imagem_duas_faces_triste, "frames":4, "wait":60, "to_start":TEMPO[1], "x":1, "y":2},
                                                            "argumentos_funcao":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":60, "to_start":TEMPO[1], "x":10, "y":3}}},
                                      "nome":"Triste",
                                      "descricao":f"Morto, dá 10 de dano a um personagem inimigo aleatório."},
                                     ]
                          },
          "morcego":{"nome":"Morcego",
                          "hp":30,
                          "preco":0,
                          "classe":"noturno",
                          "arte":imagem_morcego,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":10, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Susto na Caverna",
                                      "descricao":f"Dá 10 de dano três vezes em personagens inimigos aleatórios."},],
                          },
          "lesma":{"nome":"Lesma",
                          "hp":30,
                          "preco":0,
                          "classe":"noturno",
                          "arte":imagem_lesma,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":60, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Cheguei",
                                      "descricao":f"Dá 60 de dano em um personagem inimigo aleatório."},],
                          },
          "comeia":{"nome":"Comeia",
                          "hp":40,
                          "preco":2,
                          "classe":"noturno",
                          "arte":imagem_comeia,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":1,
                                      "argumentos":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Picada",
                                      "descricao":f"Dá 10 de dano em um personagem inimigo aleatório."},
                                     {"tipo":"habilidade",
                                      "funcao":dano_,
                                      "tempo":"final",
                                      "vivo":False,
                                      "morto":True,
                                      "ataque":False,
                                      "defesa":True,
                                      "argumentos":{"dano":10, "amigos_e_inimigos":True, "image":{"image":abelhas, "frames":6, "wait":50, "to_start":TEMPO[1], "x":10, "y":4}},
                                      "nome":"Enxente",
                                      "descricao":f"Enquanto morto, no final do turno inimigo, dá 10 de dano em todos os personagens no campo."}],
                          },
          "prototipo_meca":{"nome":"Protótipo Meca",
                          "hp":140,
                          "preco":2,
                          "classe":"guerreiro",
                          "arte":imagem_prototipo_meca,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":40, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Ganchado",
                                      "descricao":f"Dá 40 de dano em um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "funcao":dano_,
                                      "tempo":"final",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "argumentos":{"dano":40, "aleatorio":True, "chance":0.15, "image":{"image":animacao_espada, "frames":6, "wait":50, "to_start":TEMPO[1], "x":10, "y":4}},
                                      "nome":"Falha na Homologação",
                                      "descricao":f"No final do turno inimigo, tem 15% de chance de dar 40 de dano em um personagem aliado."}],
                          },
          "meca_fogueteiro":{"nome":"Meca Fogueteiro",
                          "hp":160,
                          "preco":4,
                          "classe":"guerreiro",
                          "arte":imagem_meca_fogueteiro,
                          "raridade":"comum",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":20, "aleatorio":True, "vezes":4, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Bombardeamento",
                                      "descricao":f"Dá 20 de dano quatro vezes em personagens inimigos aleatórios."},
                                     {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":6,
                                      "argumentos":{"dano":80, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Míssil Teleguiado",
                                      "descricao":f"Dá 80 de dano quatro em um personagem inimigo à sua escolha."},],
                          },
          "meca_last_hope":{"nome":"Meca Last Hope",
                          "hp":180,
                          "preco":5,
                          "classe":"guerreiro",
                          "arte":imagem_meca_last_hope,
                          "raridade":"raro",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":10, "vezes":10, "aleatorio":True, "image":{"image":tiros, "frames":8, "wait":0, "to_start":0, "x":10, "y":3}},
                                      "nome":"Protocolo Alpha",
                                      "descricao":f"Dá 10 de dano dez vezes em personagens inimigos aleatórios."},
                                     {"tipo":"habilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_nerf_global_dano,
                                              "argumentos":{"buff":10, "image":{"image":usa, "frames":4, "wait":70, "to_start":TEMPO[1], "x":6, "y":4}},
                                              "nome":"Protocolo Delta",
                                              "descricao":f"Enquanto vivo, todos os personagens aliados recebem -10 de dano."}],
                          },
          "senhor_balao":{"nome":"Senhor Balão",
                                  "hp":40,
                                  "preco":0,
                                  "classe":"lenda",
                                  "arte":imagem_senhor_balao,
                                  "arte_morto":imagem_senhor_balao_morto,
                                  "raridade":"raro",
                                  "ataques":[
                                      {"tipo":"habilidade",
                                       "ataque":True,
                                        "defesa":False,
                                        "tempo":"comeco",
                                        "vivo":True,
                                        "morto":False,
                                      "funcao":cura_,
                                      "argumentos":{"cura":10, "aleatorio": True, "image":{"image":cruz, "frames":4, "wait":70, "to_start":0, "x":8, "y":2}},
                                      "nome":"Gás Hélio",
                                      "descricao":f"Cure 10 de vida de um personagem aliado aleatório."}]
                              },
          "mr_money":{"nome":"Mr.Money",
                                  "hp":70,
                                  "preco":2,
                                  "classe":"lenda",
                                  "arte":imagem_mr_money,
                                  "raridade":"secreto",
                                  "ataques":[
                                      {"tipo":"habilidade",
                                       "ataque":True,
                                        "defesa":False,
                                        "tempo":"comeco",
                                        "vivo":True,
                                        "morto":False,
                                      "funcao":cura_,
                                      "argumentos":{"cura":10, "aleatorio": True, "image":{"image":cruz, "frames":4, "wait":70, "to_start":0, "x":8, "y":2}},
                                      "nome":"Gás Hélio",
                                      "descricao":f"Cure 10 de vida de um personagem aliado aleatório."}]
                              },
          "mestre_das_horas":{"nome":"Mestre das Horas",
                                  "hp":50,
                                  "preco":1,
                                  "classe":"lenda",
                                  "arte":imagem_mestre_das_horas,
                                  "raridade":"secreto",
                                  "ataques":[
                                      {"tipo":"ataque",
                                      "funcao":pular_turno,
                                      "dado":3,
                                      "argumentos":{"image":{"image":item_relogio, "frames":6, "wait":70, "to_start":0, "x":12, "y":5}},
                                      "nome":"Viagem no Tempo",
                                      "descricao":f"Pule para o turno do próximo personagem aliado."},
                                      {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":4,
                                      "argumentos":{"dano":ultimo_ataque, "aleatorio": True, "multiplicador":1, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Déjà-vu",
                                      "descricao":f"Dá o último dano da partida em um personagem inimigo aleatório."},]
                              },
          "dono_da_loja":{"nome":"Dono da Loja",
                                  "hp":40,
                                  "preco":2,
                                  "classe":"humano",
                                  "arte":imagem_dono_da_loja,
                                  "raridade":"secreto",
                                  "ataques":[
                                      {"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":40, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Vou pegar a vassoura",
                                      "descricao":f"Dá 40 de dano a um personagem inimigo à sua escolha."},
                                      {"tipo":"ataque",
                                      "funcao":adicionar_habilidade,
                                      "dado":6,
                                      "argumentos":{"funcao":{"tipo":"habilidade",
                                                  "tempo":"comeco",
                                                  "vivo":True,
                                                  "morto":False,
                                                  "ataque":True,
                                                  "defesa":False,
                                                  "funcao":habilidade_buff_global_dado,
                                                  "argumentos":{"buff":1, "image":{"image":soma_dado, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                                  "nome":"Uma Ajudinha",
                                                  "descricao":f"Enquanto vivo, some 1 aos seus dados."},
                                          "image":{"image":soma_dado, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Precisa de um Dado?",
                                      "descricao":f"Enquanto vivo, some 1 aos seus dados, acumula."},
                                      {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":False,
                                      "defesa":True,
                                      "funcao":habilidade_nerf_global_dano,
                                      "argumentos":{"buff":numero_dado, "multiplicador":4, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Sorte Nossa",
                                      "descricao":f"No turno inimigo, enquanto estiver vivo, leva menos 4 vezes o número do dado atual de dano."}]
                              },
          "senhor_dos_mapas":{"nome":"Senhor dos Mapas",
                              "hp":50,
                              "preco":3,
                              "classe":"lenda",
                              "arte":imagem_senhor_dos_mapas,
                              "raridade":"secreto",
                              "ataques":[
                                  {"tipo":"ataque",
                                   "funcao":dano_,
                                   "dado":1,
                                   "argumentos":{"dano":10, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                   "nome":"Qual o Destino?",
                                   "descricao":f"Dá 10 de dano em personagem inimigo à sua escolha."},
                                  {"tipo":"habilidade",
                                   "ataque":True,
                                   "defesa":False,
                                   "tempo":"comeco",
                                   "vivo":True,
                                   "morto":False,
                                   "funcao":habilidade_buff_global_dano,
                                   "argumentos":{"buff":turno_atual, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                   "nome":"Chegando ao Destino",
                                   "descricao":f"Enquanto vivo, a cada turno, o ataque dos personagens aliados ganham +1 em buff de ataque."}]
                              },
          "aranha_rainha":{"nome":"Aranha rainha",
                                  "hp":80,
                                  "preco":2,
                                  "classe":"monstro",
                                  "arte":imagem_aranha,
                                  "raridade":"secreto",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":assasinato_,
                                              "dado":6,
                                              "argumentos":{"aleatorio": True, "image":{"image":caveira, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Mordida Final",
                                              "descricao":f"Destrua um personagem inimigo aleatório."},
                                             {"tipo":"habilidade",
                                              "ataque":True,
                                              "defesa":False,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":dano_,
                                              "argumentos":{"dano":40, "chance":0.2, "aleatorio": True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Salto Surpreza",
                                              "descricao":f"Todo final de turno aliado, enquanto vivo, tem 20% de dar 40 de dano em um personagem inimigo aleatório."}]
                              },
          "genio_da_lampada":{"nome":"Gênio da Lâmpada",
                                  "hp":90,
                                  "preco":2,
                                  "classe":"noturno",
                                  "arte":imagem_genio_da_lampada,
                                  "raridade":"secreto",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":4,
                                              "argumentos":{"dano":menor_ataque, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"3 Desejos",
                                              "descricao":f"Dá o menor dano de ataque da partida 3 vezes em personagens inimigos aleatórios."},
                                             {"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":6,
                                              "argumentos":{"dano":maior_ataque, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Último Desejo",
                                              "descricao":f"Dá o maior dano de ataque da partida em um personagem inimigo à sua escolha."}] #ABILIDADE, chance de dar o maior ataque em um lacaio inimigo aleatório
                              },
          "balao":{"nome":"Balão",
                                  "hp":130,
                                  "preco":3,
                                  "classe":"lenda",
                                  "arte":imagem_balao,
                                  "raridade":"secreto",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":4,
                                              "argumentos":{"dano":50, "chance": 0.2, "aleatorio":True, "vezes":4, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Bombardeio Aéreo",
                                              "descricao":f"20% de chance de dar 50 de dano 4 vezes em personagens inimigos aleatórios."},
                                             {"tipo":"habilidade",
                                              "ataque":False,
                                              "defesa":True,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_nerf_global_dano,
                                              "argumentos":{"buff":50, "chance":0.2 ,"image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                              "nome":"Fulga",
                                              "descricao":f"Enquanto vivo, tem 20% de chance de que os personagens do seu lado do campo tomem -50 de dano."}]
                              },
          "o_sol":{"nome":"O Sol",
                                  "hp":240,
                                  "preco":5,
                                  "classe":"lenda",
                                  "arte":imagem_sol,
                                  "raridade":"secreto",
                                  "ataques":[
                                      {"tipo":"ataque",
                                       "funcao":dano_,
                                       "dado":3,
                                       "argumentos":{"dano":30,  "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                       "nome":"Explosão Solar",
                                       "descricao":f"Dá 30 de dano em todos os personagens."},
                                      {"tipo":"habilidade",
                                       "ataque":True,
                                        "defesa":False,
                                        "tempo":"comeco",
                                        "vivo":True,
                                        "morto":True,
                                      "funcao":dano_,
                                      "argumentos":{"dano":10, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":40, "to_start":TEMPO[2], "x":10, "y":3}},
                                      "nome":"Queimadura",
                                      "descricao":f"Todo começo de turno, dá 10 de dano em todos os personagens."}]
                              },
          "a_lua":{"nome":"A Lua",
                                  "hp":180,
                                  "preco":5,
                                  "classe":"lenda",
                                  "arte":imagem_lua,
                                  "raridade":"secreto",
                                  "ataques":[
                                      {"tipo":"ataque",
                                       "funcao":dano_,
                                       "dado":4,
                                       "argumentos":{"dano":40, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                       "nome":"Meteoros",
                                       "descricao":f"Dá 40 de dano em personagens inimigos aleatórios 3 vezes."},
                                      {"tipo":"habilidade",
                                       "ataque":True,
                                        "defesa":False,
                                        "tempo":"comeco",
                                        "vivo":True,
                                        "morto":True,
                                      "funcao":cura_,
                                      "argumentos":{"cura":10, "aleatorio":True, "vezes": 2, "image":{"image":cruz, "frames":4, "wait":40, "to_start":TEMPO[2], "x":8, "y":2}},
                                      "nome":"Descanso Norturno",
                                      "descricao":f"Todo começo de turno, cura 10 de dano de um personagens aliado aleatório 2 vezes."}]
                              },
          "senhor_trovao":{"nome":"Senhor Trovão",
                           "hp":80,
                           "preco":2,
                           "classe":"lenda",
                           "arte":imagem_senhor_trovao,
                           "raridade":"secreto",
                           "ataques":[{"tipo":"ataque",
                                       "funcao":dano_,
                                       "dado":1,
                                       "argumentos":{"dano":10, "vezes":numero_dado, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                       "nome":"Chuva Forte",
                                       "descricao":f"Dá 10 de dano vezes o número que caiu no dado em personagens inimigos aleatórios."},
                                      {"tipo":"habilidade",
                                       "ataque":True,
                                       "defesa":False,
                                       "tempo":"comeco",
                                       "vivo":True,
                                       "morto":False,
                                       "funcao":assasinato_,
                                       "argumentos":{"chance":0.1, "aleatorio":True, "image":{"image":trovao, "frames":6, "wait":60, "to_start":TEMPO[2], "x":7, "y":7}},
                                       "nome":"Raio",
                                       "descricao":f"Todo final de turno aliado, enquanto vivo, tem 10% de destruir um personagem inimigo aleatório."}]
                              },
          "grifo":{"nome":"Grifo",
                   "hp":120,
                   "preco":4,
                   "classe":"monstro",
                   "arte":imagem_grifo,
                   "raridade":"secreto",
                   "ataques":[{"tipo":"ataque",
                               "funcao":dano_,
                               "dado":3,
                               "argumentos":{"dano":menor_ataque, "multiplicador":numero_dado, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                               "nome":"Garra afiada",
                               "descricao":f"Dá o menor dano de ataque da partida vezes o número do dado em um personagem inimigo aleatório."},
                              {"tipo":"habilidade",
                               "tempo":"comeco",
                               "vivo":True,
                               "morto":False,
                               "ataque":False,
                               "defesa":True,
                               "funcao":habilidade_nerf_global_dano,
                               "argumentos":{"buff":10, "apenas_caracteristico":True, "caracteristicas":{"key":"nome", "valor":"Grifo"},
                                             "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                               "nome":"Couro grosso",
                               "descricao":f"Enquanto vivo, recebe -10 de dano de qualquer ataque."}]
                              },
          "detetive":{"nome":"Detetive",
                                  "hp":60,
                                  "preco":2,
                                  "classe":"humano",
                                  "arte":imagem_detetive,
                                  "raridade":"secreto",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":4,
                                              "argumentos":{"dano":10, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Queima Roupa",
                                              "descricao":f"Dá 10 de dano 3 vezes em personagens inimigos aleatórios."},
                                             {"tipo":"habilidade",
                                              "ataque":True,
                                              "defesa":False,
                                              "tempo":"comeco",
                                              "vivo":True,
                                              "morto":False,
                                              "funcao":habilidade_buff_global_dano,
                                              "argumentos":{"buff":30, "chance":0.25 ,"image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                              "nome":"Investigação",
                                              "descricao":f"Enquanto vivo, tem 25% de chance de que os personagens do seu lado do campo de +30 de dano."}]
                              },
          "alien":{"nome":"Alien",
                   "hp":70,
                   "preco":2,
                   "classe":"noturno",
                   "arte":imagem_aliem,
                   "raridade":"secreto",
                   "ataques":[{"tipo":"ataque",
                               "funcao":dano_,
                               "dado":3,
                               "argumentos":{"dano":20, "aleatorio":True, "vezes":2, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                               "nome":"Pistola lazer",
                               "descricao":f"Dá 20 de dano em 2 inimigos aleatórios."},
                              {"tipo":"ataque",
                               "usos":1,
                               "funcao":dano_,
                               "dado":5,
                               "argumentos":{"dano":60, "aleatorio":False, "vezes":1, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                               "nome":"Aniquilação",
                               "descricao":f"Uma vez durante a partida, dá 60 de dano em um inimigo a sua escolha."},
                              {"tipo":"ataque",
                               "usos":1,
                               "funcao":cura_,
                               "dado":3,
                               "argumentos":{"cura":40, "todos":True, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                               "nome":"Medicina Alien",
                               "descricao":f"Uma vez durante a partida, cura todos aliados em 40."},]
                              },
          "cozinheiro":{"nome":"Cozinheiro",
                                  "hp":90,
                                  "preco":2,
                                  "classe":"noturno",
                                  "arte":imagem_cozinheiro,
                                  "raridade":"secreto",
                                  "ataques":[{"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":4,
                                              "argumentos":{"dano":menor_ataque, "aleatorio":True, "vezes":3, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"3 Desejos",
                                              "descricao":f"Dá o menor dano de ataque da partida 3 vezes em personagens inimigos aleatórios."},
                                             {"tipo":"ataque",
                                              "funcao":dano_,
                                              "dado":6,
                                              "argumentos":{"dano":maior_ataque, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                              "nome":"Último Desejo",
                                              "descricao":f"Dá o maior dano de ataque da partida em um personagem inimigo à sua escolha."}]
                              },
          "rei_carangueijo":{"nome":"Rei Carangueijo",
                             "hp":80,
                             "preco":2,
                             "classe":"monstro",
                             "arte":imagem_rei_carangueijo,
                             "raridade":"secreto",
                             "ataques":[{"tipo":"ataque",
                                         "funcao":dano_,
                                         "dado":6,
                                         "argumentos":{"dano":80, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                         "nome":"Garra Agarra",
                                         "descricao":f"Dá 80 de dano em um personagem inimigo a sua escolha."},
                                        {"tipo":"habilidade",
                                         "ataque":False,
                                         "defesa":True,
                                         "tempo":"comeco",
                                         "vivo":True,
                                         "morto":False,
                                         "funcao":habilidade_nerf_global_dano,
                                         "argumentos":{"buff":10, "chance":0.3,"soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"monstro", "time_atacante":True, "time_atacado":True},
                                                       "image":{"image":escudo, "frames":4, "wait":50, "to_start":TEMPO[1], "x":12, "y":5}},
                                         "nome":"Reino Monstro",
                                         "descricao":f"Enquanto vivo, tem 40% de chance de que os personagens do seu lado do campo recebam -10 de dano para cada monstro vivo ou morto em jogo."}]
                              },
          "pirata":{"nome":"Pirata",
                    "hp":60,
                    "preco":2,
                    "classe":"assassino",
                    "arte":imagem_pirata,
                    "raridade":"raro",
                    "ataques":[{"tipo":"ataque",
                                "funcao":dano_,
                                "dado":3,
                                "argumentos":{"dano":20, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                "nome":"Passe tudo!",
                                "descricao":f"Dá o 20 de dano em um personagem inimigo aleatório."},
                               {"tipo":"habilidade",
                                "tempo":"comeco",
                                "vivo":True,
                                "morto":False,
                                "ataque":True,
                                "defesa":False,
                                "funcao":habilidade_buff_global_dano,
                                "argumentos":{"buff":5, "soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"assassino", "time_atacante":True, "time_atacado":False},
                                              "image":{"image":bandeira_pirata, "frames":4, "wait":50, "to_start":TEMPO[1], "x":2, "y":2}},
                                "nome":"Saquear",
                                "descricao":f"Enquanto vivo, todos os personagens do seu lado do campo ganham +5 de dano para cada assassino aliado."}] 
                              },
          "barba_negra":{"nome":"Barba Negra",
                         "hp":80,
                         "preco":3,
                         "classe":"assassino",
                         "arte":imagem_barba_negra,
                         "raridade":"secreto",
                         "ataques":[{"tipo":"ataque",
                                     "funcao":dano_,
                                     "dado":5,
                                     "argumentos":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                     "nome":"Para prancha!",
                                     "descricao":f"Dá 10 de dano 2 vezes em personagens inimigos aleatórios."},
                                    {"tipo":"habilidade",
                                     "tempo":"comeco",
                                     "vivo":True,
                                     "morto":False,
                                     "ataque":True,
                                     "defesa":False,
                                     "funcao":habilidade_buff_global_dano,
                                     "argumentos":{"buff":10, "soma_por_caracteristicas":True, "caracteristicas":{"key":"classe", "valor":"assassino", "time_atacante":True, "time_atacado":False},
                                                   "image":{"image":bandeira_pirata, "frames":4, "wait":50, "to_start":TEMPO[1], "x":2, "y":2}},
                                     "nome":"Ilha a vista!",
                                     "descricao":f"Enquanto vivo, todos os personagens do seu lado do campo ganham +10 de dano para cada assassino aliado."}]
                         },
          "boneco_de_neve":{"nome":"Boneco de Neve",
                         "hp":120,
                         "preco":4,
                         "classe":"lenda",
                         "arte":imagem_boneco_de_neve,
                         "raridade":"secreto",
                         "ataques":[{"tipo":"ataque",
                                     "funcao":dano_,
                                     "dado":4,
                                     "argumentos":{"dano":4, "vezes":turno_atual, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                     "nome":"Nevasca",
                                     "descricao":f"Dá 4 de dano vezes o número da partida em personagens inimigos aleatórios."},
                                    {"tipo":"habilidade",
                                     "ataque":True,
                                     "defesa":False,
                                     "tempo":"comeco",
                                     "vivo":True,
                                     "morto":False,
                                     "funcao":cura_,
                                     "argumentos":{"cura":120, "chance":0.1, "si_mesmo":True,"image":{"image":floco_neve_2, "frames":4, "wait":80, "to_start":0, "x":1, "y":0}},
                                     "nome":"Clima de natal",
                                     "descricao":f"Todo inicio de turno, enquanto vivo, tem 10% de chance de recuperar 120 de vida."}]
                         },
          "pegasus":{"nome":"Pegasus",
                     "hp":130,
                     "preco":4,
                     "classe":"lenda",
                     "arte":imagem_pegasus,
                     "raridade":"secreto",
                     "ataques":[{"tipo":"ataque",
                                 "funcao":dano_,
                                 "dado":5,
                                 "argumentos":{"dano":60, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                 "nome":"Coice terrestre",
                                 "descricao":f"Dá 60 de dano em um personagens inimigos sua escolha."},
                                {"tipo":"ataque",
                                 "funcao":dano_,
                                 "dado":5,
                                 "argumentos":{"dano":maior_ataque, "aleatorio":True, "vezes":2, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                 "nome":"Coice voador",
                                 "descricao":f"Dá o maior dano de ataque da partida 2 vezes em personagens inimigos aleatórios."}]
                     },
          "cavalo_xadrez":{"nome":"Cavalo Xadrez",
                     "hp":80,
                     "preco":2,
                     "classe":"lenda",
                     "arte":imagem_cavalo_xadrez,
                     "raridade":"epico",
                     "ataques":[{"tipo":"ataque",
                                 "funcao":dano_,
                                 "dado":4,
                                 "argumentos":{"dano":menor_ataque, "multiplicador":numero_dado, "aleatorio":True, "vezes":1, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                 "nome":"Meu Turno",
                                 "descricao":f"Dá o menor dano de ataque da partida vezes o número do dado em um personagem inimigo aleatório."},
                                {"tipo":"habilidade",
                                 "tempo":"comeco",
                                 "vivo":True,
                                 "morto":False,
                                 "ataque":True,
                                 "defesa":True,
                                 "funcao":habilidade_buff_global_dano,
                                 "argumentos":{"buff":10, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                 "nome":"Jogo Rápido",
                                 "descricao":f"Enquanto vivo, todos os personagens ganham +10 de dano."}]
                     },
          "soldado_romano":{"nome":"Soldado Romano",
                     "hp":40,
                     "preco":1,
                     "classe":"guerreiro",
                     "arte":imagem_soldado_romano,
                     "raridade":"raro",
                     "ataques":[{"tipo":"ataque",
                                 "funcao":dano_,
                                 "dado":2,
                                 "argumentos":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                 "nome":"Guerra",
                                 "descricao":f"Dá 10 de dano em um inimigo aleatório."},
                                {"tipo":"habilidade",
                                 "tempo":"comeco",
                                 "vivo":True,
                                 "morto":False,
                                 "ataque":True,
                                 "defesa":False,
                                 "funcao":habilidade_buff_global_dano,
                                 "argumentos":{"buff":5, "soma_por_caracteristicas":True, "caracteristicas":{"key":"nome", "valor":"Soldado Romano", "time_atacante":True, "time_atacado":False},
                                               "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                 "nome":"Expansão Romana",
                                 "descricao":f"Enquanto vivo, todos os personagens do seu lado do campo ganham +5 de dano para cada Soldado Romano aliado vivo ou morto."}]
                     },
          "hidrante":{"nome":"Hidrante",
                     "hp":200,
                     "preco":0,
                     "classe":"lenda",
                     "arte":imagem_hidrante,
                      "volta":{"funcao":dano_,
                               "argumentos":{"dano":70, "chance":0.01, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                               "nome":"Chute no metal",
                               "descricao":f"1% de chance de dar 60 de dano no lacaio."},
                     "raridade":"epico",
                     "ataques":[]
                     },
          "o_cozinheiro":{"nome":"O Cozinheiro",
                          "hp":60,
                          "preco":2,
                          "classe":"humano",
                          "arte":imagem_cozinheiro,
                          "raridade":"secreto",
                          "ataques":[{"tipo":"ataque",
                                      "funcao":dano_,
                                      "dado":5,
                                      "argumentos":{"dano":40, "aleatorio": False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Prato Quente",
                                      "descricao":f"Dá 40 de dano a um personagem inimigo à sua escolha."},
                                     {"tipo":"habilidade",
                                      "tempo":"comeco",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":True,
                                      "funcao":habilidade_buff_global_cura,
                                      "argumentos":{"buff":30, "chance":0.4, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Especiarias",
                                      "descricao":f"Enquanto vivo, todos tem 40% de chance de ganhar um buff em cura de +30."},
                                     {"tipo":"habilidade",
                                      "tempo":"final",
                                      "vivo":True,
                                      "morto":False,
                                      "ataque":True,
                                      "defesa":False,
                                      "funcao":cura_,
                                      "argumentos":{"cura":numero_dado, "multiplicador":5, "aleatorio": True, "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                      "nome":"Culinária Especial",
                                      "descricao":f"Enquanto vivo, no final do turno aliado, cure 5 vezes o número que caiu no dado."},]},
          "lampada_vulcao":{"nome":"Lampada Vulcao",
                            "hp":10,
                            "preco":-1,
                            "classe":"lenda",
                            "arte":imagem_lampada_vulcao,
                            "raridade":"secreto",
                            "ataques":[]
                            },
          "guardiao_da_ponte":{"nome":"Guardião da Ponte",
                               "hp":60,
                               "preco":2,
                               "classe":"humano",
                               "arte":imagem_guardiao_da_ponte,
                               "raridade":"raro",
                               "ataques":[{"tipo":"ataque",
                                           "funcao":dano_,
                                           "dado":4,
                                           "argumentos":{"dano":10, "aleatorio":True, "vezes":4,"image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                           "nome":"Para trás",
                                           "descricao":f"Dá 10 de dano 4 vezes em inimigos aleatórios."},
                                          {"tipo":"habilidade",
                                           "ataque":True,
                                           "defesa":False,
                                           "tempo":"comeco",
                                           "vivo":True,
                                           "morto":False,
                                           "funcao":habilidade_buff_global_dano,
                                           "argumentos":{"buff":numero_dado, "multiplicador":5, "chance":0.3, "apenas_caracteristico":True,
                                                         "caracteristicas":{"key":"nome", "valor":"Guardião da Ponte"},
                                                         "image":{"image":coroa, "frames":4, "wait":50, "to_start":TEMPO[1], "x":10, "y":5}},
                                           "nome":"Aura mágica",
                                           "descricao":f"Enquanto vivo, no seu turno, tem 30% de chance de que o dano desse personagem seja buffado no número do dado que cair vezes 5."}]
                               },
          "tartaruga_gigante":{"nome":"Tartaruga Gigante",
                               "hp":140,
                               "preco":4,
                               "classe":"monstro",
                               "arte":imagem_tartaruga_gigante,
                               "raridade":"secreto",
                               "ataques":[{"tipo":"ataque",
                                          "funcao":dano_,
                                          "dado":4,
                                          "argumentos":{"dano":20, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                          "nome":"Andar",
                                          "descricao":f"Dá 20 de dano em todos personagens."},
                                          {"tipo":"habilidade",
                                           "tempo":"comeco",
                                           "vivo":True,
                                           "morto":False,
                                           "ataque":False,
                                           "defesa":True,
                                           "funcao":habilidade_nerf_global_dano,
                                           "argumentos":{"buff":30, "apenas_caracteristico":True, "caracteristicas":{"key":"nome", "valor":"Tartaruga Gigante"},
                                                         "image":{"image":seta_cima, "frames":4, "wait":50, "to_start":TEMPO[1], "x":14, "y":5}},
                                           "nome":"Carapaça Gigante",
                                           "descricao":f"Enquanto vivo, este personagem recebe -30 de dano de qualquer ataque."}]
                               },
          "dinossauro":{"nome":"Dinossauro",
                        "hp":190,
                        "preco":4,
                        "classe":"monstro",
                        "arte":imagem_dinossauro,
                        "raridade":"secreto",
                        "ataques":[{"tipo":"ataque",
                                    "funcao":dano_,
                                    "dado":5,
                                    "argumentos":{"dano":30, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                    "nome":"Pisotear antigo",
                                    "descricao":f"Dá 30 de dano em todos personagens."},
                                   {"tipo":"ataque",
                                    "usos":1,
                                    "funcao":dano_,
                                    "dado":3,
                                    "argumentos":{"dano":70, "amigos_e_inimigos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                    "nome":"Meteoros",
                                    "descricao":f"Uma vez durante a partida, esse lacaio pode dar 70 de dano em todos personagens."},]
                        },
          "agua_viva":{"nome":"Agua Viva",
                       "hp":40,
                       "preco":1,
                       "classe":"noturno",
                       "arte":imagem_agua_viva,
                       "arte_morto":imagem_agua_viva,
                       "raridade":"raro",
                       "volta":{"funcao":veneno_,
                                "argumentos":{"dano":5, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                "nome":"Toque venenoso",
                                "descricao":f"Envenena o lacaio em 5."},
                       "ataques":[{"tipo":"ataque",
                                   "funcao":dano_,
                                   "dado":2,
                                   "argumentos":{"dano":10, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                   "nome":"Queimadura",
                                   "descricao":f"Dá 10 de dano em um personagem inimigo aleatório."},
                                  #{"tipo":"habilidade",
                                  # "ataque":True,
                                  # "defesa":True,
                                  # "tempo":"comeco",
                                  # "vivo":False,
                                  # "morto":True,
                                  # "funcao":dano_,
                                  # "argumentos":{"dano":10, "aleatorio":True, "image":{"image":cruz, "frames":4, "wait":70, "to_start":0, "x":8, "y":2}},
                                  # "nome":"Pisei em algo",
                                  # "descricao":f"Enquanto morto, no inicio de todo turno, de 10 de dano em um personagem aleatório, aliádo ou inimigo, todos buffs valem para esse ataque."}
                                  ]
                              },
          "cogumelo_venenoso":{"nome":"Cogumelo Venenoso",
                               "hp":40,
                               "preco":1,
                               "classe":"assassino",
                               "arte":imagem_cogumelo_venenoso,
                               "arte_morto":imagem_cogumelo_venenoso,
                               "raridade":"comum",
                               "ataques":[{"tipo":"ataque",
                                           "funcao":veneno_,
                                           "dado":4,
                                           "argumentos":{"dano":5, "aleatorio":False, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                           "nome":"Toxina da floresta",
                                           "descricao":f"Envenena um personagem inimigo a sua escolha em 5."},]
                                          },
          "cobra_rei":{"nome":"Cobra Rei",
                               "hp":80,
                               "preco":3,
                               "classe":"assassino",
                               "arte":imagem_cobra_rei,
                               "arte_morto":imagem_cobra_rei,
                               "raridade":"raro",
                               "ataques":[{"tipo":"ataque",
                                           "funcao":veneno_,
                                           "dado":5,
                                           "usos":1,
                                           "argumentos":{"dano":20, "aleatorio":False, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                           "nome":"Veneno mortal",
                                           "descricao":f"Uma vez durante a partida pode envenenar um lacaio inimigo a sua escolha em 20."},
                                          {"tipo":"ataque",
                                           "funcao":veneno_,
                                           "dado":5,
                                           "argumentos":{"dano":10, "aleatorio":True, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                           "nome":"Picada",
                                           "descricao":f"Envenene um lacaio inimigo aleatório em 10."}]
                                          },
          "revolver":{"nome":"Revolver 38",
                      "hp":40,
                      "preco":1,
                      "classe":"lenda",
                      "arte":imagem_revolver,
                      "arte_morto":imagem_revolver,
                      "raridade":"epico",
                      "ataques":[{"tipo":"ataque",
                                  "funcao":adicionar_habilidade,
                                  "dado":1,
                                  "nome":"Colocar Bala",
                                  "usos":1,
                                  "descricao":f"Uma vez na partida, coloca 6 balas no tambor. (Próximo ataque: Carregar)",
                                  "argumentos":{"image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3},
                                                "funcao":{"tipo":"ataque",
                                                          "funcao":adicionar_habilidade,
                                                          "dado":1,
                                                          "usos":1,
                                                          "nome":"Carregar",
                                                          "descricao":"Carrega e prepara o revolver. (Próximo ataque: 90 de dano 1 de custo)",
                                                          "argumentos":{"image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3},
                                                                        "funcao":{"tipo":"ataque",
                                                                                  "funcao":dano_,
                                                                                  "dado":1,
                                                                                  "usos":6,
                                                                                  "argumentos":{"dano":90, "aleatorio":False,
                                                                                                "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                                                                  "nome":"Apertar gatilho",
                                                                                  "descricao":f"Dá 90 de dano em um personagem inimigo a sua escolha."
                                                                                  }
                                                                        },
                                                          },
                                                },
                                  },]
                      },
          "espada_de_arthur":{"nome":"Espada de Arthur",
                             "hp":90,
                             "preco":2,
                             "classe":"lenda",
                             "arte":imagem_espada_de_arthur,
                             "arte_morto":imagem_espada_de_arthur,
                             "raridade":"epico",
                             "ataques":[{"tipo":"ataque",
                                         "funcao":adicionar_habilidade,
                                         "dado":6,
                                         "nome":"Tirar da pedra",
                                         "usos":1,
                                         "descricao":f"Uma vez na partida, você pode tirar a espada da pedra. (Próximo ataque: 40 de dano em todos inimigos, 4 de custo)",
                                         "argumentos":{"image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3},
                                                       "funcao":{"tipo":"ataque",
                                                                 "funcao":dano_,
                                                                 "dado":4,
                                                                 "argumentos":{"dano":40, "todos":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                                                 "nome":"Lâmida da justiça",
                                                                 "descricao":f"Dá 40 de dano em todos personagens inimigos."
                                                                 },
                                                       },
                                         },]
                             },
          "lamina_venenosa":{"nome":"Lamina Venenosa",
                             "hp":50,
                             "preco":2,
                             "classe":"assassino",
                             "arte":imagem_lamina_venenosa,
                             "arte_morto":imagem_lamina_venenosa,
                             "raridade":"epico",
                             "ataques":[{"tipo":"ataque",
                                         "funcao":veneno_,
                                         "dado":1,
                                         "argumentos":{"dano":2, "todos":True, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                         "nome":"Corte leve",
                                         "descricao":f"Envenena todos personagens inimigos em 2."},
                                        {"tipo":"ataque",
                                         "funcao":veneno_,
                                         "dado":6,
                                         "argumentos":{"dano":10, "aleatorio":False, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                         "nome":"Corte profundo",
                                         "descricao":f"Envenena em 10 um personagem inimigo a sua escolha."}]
                             },
          "lata_de_lixo":{"nome":"Lata de Lixo",
                          "hp":80,
                          "preco":2,
                          "classe":"monstro",
                          "arte":imagem_lata_de_lixo,
                          "arte_morto":imagem_lata_de_lixo,
                          "raridade":"raro",
                          "volta":{"funcao":veneno_,
                                   "argumentos":{"dano":10, "chance":0.4, "image":{"image":imagem_veneno, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                   "nome":"Tóxico",
                                   "descricao":f"Tem 40% de chance de envenenar o lacaio em 10."},
                          "ataques":[{"tipo":"ataque",
                                      "funcao":veneno_,
                                      "dado":2,
                                      "argumentos":{"dano":numero_dado, "aleatorio":False, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Reciclável",
                                      "descricao":f"Envenena um lacaio inimigo a sua escolha de acordo com o número do dado que caiu."},
                                     {"tipo":"ataque",
                                      "funcao":veneno_,
                                      "dado":6,
                                      "argumentos":{"dano":6, "aleatorio":True, "image":{"image":animacao_espada, "frames":6, "wait":5, "to_start":0, "x":10, "y":3}},
                                      "nome":"Lixo radioativo",
                                      "descricao":f"Envenena todos personagens inimigos em 4."},]
                          },
          }

for carta in CARTAS.keys():
    if len(CARTAS[carta]["arte"]) > ART_WIDTH:
        CARTAS[carta]["arte"] = CARTAS[carta]["arte"][:ART_WIDTH]
        
    for i in range(len(CARTAS[carta]["arte"])):
        if len(CARTAS[carta]["arte"][i]) > HEIGHT_ART:
            CARTAS[carta]["arte"][i] = CARTAS[carta]["arte"][i][:HEIGHT_ART - 1]

    CARTAS[carta]["id"] = carta

raridades = {}
for carta in CARTAS.keys():
    if not CARTAS[carta]["raridade"] in raridades:
        raridades[CARTAS[carta]["raridade"]] = []
    raridades[CARTAS[carta]["raridade"]].append(carta)

classes = {}
for carta in CARTAS.keys():
    if not CARTAS[carta]["classe"] in classes:
        classes[CARTAS[carta]["classe"]] = []
    classes[CARTAS[carta]["classe"]].append(carta)

precos = {}
for carta in CARTAS.keys():
    if not CARTAS[carta]["preco"] in precos:
        precos[CARTAS[carta]["preco"]] = []
    precos[CARTAS[carta]["preco"]].append(carta)

lista_ataques = [dano_, cura_, assasinato_, trocar_vida, copiar_atributo]
lista_habilidades = [dano_, cura_, assasinato_, trocar_vida, copiar_atributo, habilidade_buff_global_dano, habilidade_nerf_global_dano, habilidade_reviver, habilidade_buff_global_dado, habilidade_nerf_global_dado, adicionar_habilidade, somar_global, pular_turno]
lista_variaveis_globais = ["PARTIDA", "TABULEIRO", "ultimo_ataque", "maior_ataque", "menor_ataque", "numero_dado", "turno_atual"]
lista_opcoes_ataques = ["aleatorio", "todos", "amigos_e_inimigos", "dano", "cura", "vezes", "multiplicador", "dado", "voltar", "nome", "chance", "copia_completa"]
lista_opcoes_habilidades = ["vivo", "morto", "ataque", "defesa", "buff", "nerf", "voltar", "nome", "apenas_caracteristico", "soma_por_caracteristicas", "si_mesmo", "caracteristicas", "multiplicador", "funcao", "variavel_global"]
todos_ataques = {"nome", "voltar", "dado", "descricao"}
todos_habilidades = {"nome", "voltar", "descricao", "vivo", "morto", "ataque", "defesa"}

dicionario_ataques = {"ataques":[nome.__name__ for nome in lista_ataques],
                      "habilidades":[nome.__name__ for nome in lista_habilidades],
                      "vezes":["~ 0 ~ 50", *lista_variaveis_globais],
                      "multiplicador":["~ 0 ~ 50", *lista_variaveis_globais],
                      "variavel_global":lista_variaveis_globais,
                      "dado":[str(i) for i in range(1, 7)],
                      "chance":[f"{i/20:4}" for i in range(1, 21)],
                      "copia_completa":["True", "False"],
                      "caracteristicas":["classe", "raridade", "hp", "preco"],
                      "classe":list(classes.keys()),
                      "raridade":list(raridades.keys()),
                      "preco":[str(i) for i in range(6)],
                      "hp":["0 ~ 100", "100 ~ 200", "200 ~ 300", "300 ~ 400", "400 ~ 500"],
                      "funcao":["Adicione manualmente"],
                      "atributo":list(CARTAS["guerreiro_preparado"].keys())}

for ataque_ in lista_ataques:
    dicionario_ataques[ataque_.__name__] = sorted(list((set(lista_opcoes_ataques) & set(signature(ataque_).parameters)) | todos_ataques))

for opcoes in lista_opcoes_ataques[0:3]:
    dicionario_ataques[opcoes] = ["True", "False"]
    
for opcoes in lista_opcoes_ataques[3:5]:
    dicionario_ataques[opcoes] = ["0 ~ 100", "100 ~ 200", "200 ~ 300", "300 ~ 400", "400 ~ 500", *lista_variaveis_globais]

for opcoes in lista_opcoes_habilidades[0:4]:
    dicionario_ataques[opcoes] = ["True", "False"]

for opcoes in lista_opcoes_habilidades[8:11]:
    dicionario_ataques[opcoes] = ["True", "False"]

for habilidade_ in lista_habilidades:
    if habilidade_.__name__ in dicionario_ataques:
        dicionario_ataques[habilidade_.__name__] = sorted(set(dicionario_ataques[habilidade_.__name__]) | set(signature(ataque_).parameters) | todos_habilidades | todos_ataques)
    else:
        dicionario_ataques[habilidade_.__name__] = sorted(list((set(lista_opcoes_habilidades) & set(signature(habilidade_).parameters)) | todos_habilidades))

for opcoes in lista_opcoes_habilidades[4:6]:
    dicionario_ataques[opcoes] = ["~ 0 ~ 50"]

if USE_MODS:
    for arquivo in listdir(FOLDER_CARDS_MODS):
        with open(f"{FOLDER_CARDS_MODS}/{arquivo}") as carta:
            carta_temporaria = load(carta)
        for key in carta_temporaria.keys():
            if not key in ["nome", "descricao", "tipo", "image", "classe", "arte", "raridade", "ataques", "caracteristicas"]:
                exec(f"""carta_temporaria[key] = {str(carta_temporaria[key]).replace('"','')}""")

        for i in range(len(carta_temporaria["ataques"])):
            for key in carta_temporaria["ataques"][i].keys():
                if not key in ["nome", "descricao", "image", "classe", "tipo", "caracteristicas"]:
                    valor = str(carta_temporaria["ataques"][i][key]).replace('"','')

                    try:
                        carta_temporaria["ataques"][i][key] = eval(valor)
                    except Exception as e:
                        print(f"Erro ao avaliar {arquivo}: {e}")


        for i in range(len(carta_temporaria["ataques"])):
            for key in carta_temporaria["ataques"][i]["argumentos"].keys():
                if key not in ["nome", "descricao", "image", "classe", "tipo", "caracteristicas"]:
                    valor = str(carta_temporaria["ataques"][i]["argumentos"][key]).replace('"', '')
                    try:
                        carta_temporaria["ataques"][i]["argumentos"][key] = eval(valor)
                    except Exception as e:
                        print(f"Erro ao avaliar {arquivo}: {e}")

        CARTAS[carta_temporaria["nome"]] = carta_temporaria

if __name__ == "__main__":
    DEBUG = True
    TIMES = [[CARTAS["prototipo_meca"].copy(),
              CARTAS["protetor_do_tesouro"].copy(),
              CARTAS["fantasma_solitario"].copy()],
             [CARTAS["senhor_trovao"].copy(),
              CARTAS["tartaruga_gigante"].copy(),
              CARTAS["cubo"].copy()]]
    
    jogar(TIMES)
