"""
Funções de missões

Padrão de input:
    save, **resto

O "save" é um dicionário, sua estrutura pode ser encontrada em ./save/save.json
O "resto" depende de onde a missão será ativada, por exemplo, se for no inicio, durante ou no final do jogo em "resto" estará os times

As cartas liberadas pelas missões estão em ./play.py na função 'animacao_inventario'
"""
from engine_card_game import CARTAS, raridades, classes

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
    Se o você ganhou usando um deck de 0 de mana vs um deck de 5 de mana
    Libera: ???
    """
    if "ze_mao_de_alface" in [personagem["preco"] for personagem in resto["TIMES"][0]]:
        return True
    return False
