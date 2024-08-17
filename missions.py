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
