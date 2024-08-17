"""
Funções de missões

Padrão de input:
    save, **resto
"""
from engine_card_game import CARTAS, raridades, classes

def missao_moedas(save, **resto) -> bool:
    """
    Se o usuário tiver mais de 10000 moedas
    """
    if save["moedas"] > 10_000:
        return True
    return False

def missao_o_derrotado(save, **resto) -> bool:
    """
    Se o usuário perde mais de 100 partidas
    """
    if save["derrotas"] > 100:
        return True
    return False
        
def missao_o_vitorioso(save, **resto) -> bool:
    """
    Se o usuário ganha mais de 100 partidas
    """
    if save["vitorias"] > 100:
        return True
    return False

def missao_lenda_das_cartas(save, **resto) -> bool:
    """
    Se o usuário ganha mais de 1000 partidas
    """
    if save["vitorias"] > 1000:
        return True
    return False

def missao_dono_da_loja(save, **resto) -> bool:
    """
    Confere se o usuário tem pelo menos 40 cartas raras, comuns, épicas e lendárias da loja
    """
    cartas_compradas = set()
    for categoria in raridades.keys():
        cartas_compradas = (set(raridades[categoria]) & set(save["cartas"])) | cartas_compradas
    if len(cartas_compradas) >= 40:
        return True
    return False

    
    
