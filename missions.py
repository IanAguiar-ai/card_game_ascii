"""
Funções de missões

Padrão de input:
    save, **resto
"""

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
