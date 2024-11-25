"""
Funções de missões

Padrão de input:
    save, **resto

O "save" é um dicionário, sua estrutura pode ser encontrada em ./save/save.json
O "resto" depende de onde a missão será ativada, por exemplo, se for no inicio, durante ou no final do jogo em "resto" estará os times

As cartas liberadas pelas missões estão em ./play.py na função 'animacao_inventario'
"""
from engine_card_game import CARTAS, raridades, classes
from datetime import datetime

def missao_moedas(save, **resto) -> bool:
    """
    Se o usuário tiver mais de 10000 moedas
    Libera: Mr.Money
    """
    if save["moedas"] > 10_000:
        return True
    return False

def missao_o_derrotado(save, **resto) -> bool:
    """
    Se o usuário perde mais de 100 partidas
    Libera: "Zé Mão de Alface"
    """
    if save["derrotas"] > 100:
        return True
    return False
        
def missao_o_vitorioso(save, **resto) -> bool:
    """
    Se o usuário ganha mais de 100 partidas
    Libera: ???
    """
    if save["vitorias"] > 100:
        return True
    return False

def missao_lenda_das_cartas(save, **resto) -> bool:
    """
    Se o usuário ganha mais de 1000 partidas
    Libera: ???
    """
    if save["vitorias"] > 1000:
        return True
    return False

def missao_dono_da_loja(save, **resto) -> bool:
    """
    Confere se o usuário tem pelo menos 40 cartas raras, comuns, épicas e lendárias da loja
    Libera: Dono da Loja
    """
    cartas_compradas = set()
    for categoria in raridades.keys():
        cartas_compradas = (set(raridades[categoria]) & set(save["cartas"])) | cartas_compradas
    if len(cartas_compradas) >= 40:
        return True
    return False

def missao_somos_lendarios(save, **resto) -> bool:
    """
    Se o usuário tem 8 ou mais cartas lendas
    Libera: ???
    """
    if len(set(save["cartas"]) | set(classes["lenda"])) >= 8:
        return True
    return False

def missao_homem_comum(save, **resto) -> bool:
    """
    Se o usuário tiver 15 ou mais cartas comuns
    Libera: ???
    """
    if len(set(save["cartas"]) | set(raridades["comum"])) >= 15:
        return True
    return False

def missao_duelo_especial(save, **resto) -> bool:
    """
    Se o deck do usuário é composto por cartas lendas
    Libera: ???
    """
    if len(set(save["deck"]) | set(classes["lenda"])) == 3:
        return True
    return False

def missao_massacre(save, **resto) -> bool:
    """
    Se o time ganhou e todos os personagens aliados estão vivos
    Libera: ???
    """
    if min([personagem["hp"] for personagem in resto["TIMES"][1]]) > 0:
        return True
    return False

def missao_parece_impossivel(save, **resto) -> bool:
    """
    Se o você ganhou usando um deck de 0 de mana vs um deck de 5 de mana
    Libera: ???
    """
    if sum([personagem["preco"] for personagem in resto["TIMES"][1]]) == 0 and sum([personagem["preco"] for personagem in resto["TIMES"][0]]) == 5:
        return True
    return False

def missao_zerado(save, **resto) -> bool:
    """
    Tenha exatamente 0 moedas
    Libera: ???
    """
    if save["moedas"] == 0:
        return True
    return False

def missao_livro_cheio(save, **resto) -> bool:
    """
    Tenha 30 ou mais missões concluidas
    Libera: ???
    """
    if len(save["missoes"]) >= 30:
        return True
    return False

def missao_reviravolta(save, **resto) -> bool:
    """
    Se o você ganhou usando o zé mão de alface
    Libera: ???
    """
    if "ze_mao_de_alface" in [personagem["preco"] for personagem in resto["TIMES"][0]]:
        return True
    return False

def missao_primeira_vez(save, **resto) -> bool:
    """
    Ganhe uma partida
    Libera: 100 moedas
    """
    return True

def missao_genio_da_lampada(save, **resto) -> bool:
    """
    Tenha a lâmpada mágica no inventário
    Libera: genio_da_lampada
    """
    if "lampada_magica" in save["inventario"]:
        return True
    return False

def missao_por_um_triz(save, **resto) -> bool:
    """
    Se o você ganhou por 10 de vida ou menos na soma dos seus personagens
    Libera: 300 moedas
    """
    if sum([personagem["hp"] for personagem in resto["TIMES"][1]]) <= 10:
        return True
    return False

def missao_passando_o_tempo(save, **resto) -> bool:
    """
    Se o usuário tem mais de 100 (vitorias + derrotas) e 10 ou mais itens no iventário
    Libera: "Zé Mão de Alface"
    """
    if save["vitorias"] + save["derrotas"] > 100 and len(save) >= 10:
        return True
    return False

def missao_de_dia(save, **resto) -> bool:
    """
    Se o usuário acessa a loja ao meio dia
    Libera: "O Sol"
    """
    try:
        if datetime.now().hour == 12:
            return True
    except:
        pass
    return False

def missao_de_noite(save, **resto) -> bool:
    """
    Se o usuário acessa a loja a meia noite
    Libera: "A Lua"
    """
    try:
        if datetime.now().hour == 0:
            return True
    except:
        pass
    return False

def missao_ovni(save, **resto) -> bool:
    """
    Se o usuário ganha do alien no mapa
    Libera: "Alien"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "alien":
            return True
    return False

def missao_duelo_na_neve(save, **resto) -> bool:
    """
    Se o usuário ganha do boneco de neve no mapa
    Libera: "Boneco de Neve"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "boneco_de_neve":
            return True
    return False

def missao_cavalo_alado(save, **resto) -> bool:
    """
    Se o usuário ganha do pegasus no mapa
    Libera: "Pegasus"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "pegasus":
            return True
    return False

def missao_tempestade(save, **resto) -> bool:
    """
    Se o usuário acessa o mapa em momento tempestoso e de noite
    Libera: "Senhor Trovão"
    """
    if resto["tipo_clima"] == "tempestade" and com_sol == False:
        return True
    return False

def missao_detetive(save, **resto) -> bool:
    """
    Se o usuário ganha do Detetive no mapa
    Libera: "Detetive"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "detetive":
            return True
    return False

def missao_rei_carangueijo(save, **resto) -> bool:
    """
    Se o usuário ganha do Rei Carangueijo no mapa
    Libera: "Rei Carangueijo"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "rei_carangueijo":
            return True
    return False

def missao_barba_negra(save, **resto) -> bool:
    """
    Se o usuário ganha do Barba Negra no mapa
    Libera: "Barba Negra"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "barba_negra":
            return True
    return False

def missao_grifo(save, **resto) -> bool:
    """
    Se o usuário ganha do Grifo no mapa
    Libera: "grifo"
    """
    for personagem in TIMES[0]:
        if personagem["id"] == "grifo":
            return True
    return False
