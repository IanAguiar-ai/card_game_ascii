"""
Lista com textos das missões

Existem 3 tipos de missões:
'inicio' <- confere sempre ao iniciar o 'jogo'
'jogo' <- confere todo turno ; (desativado por enquanto)
'vitoria' <- confere se tiver ganho
'derrota' <- confere se tiver perdido
'loja' <- confere sempre que entrar na loja

Todos retornos de missão devem retornar True ou False

A missoes é uma lista de listas onde os elementos são:

0: Nome da missão
1: Função para conferir missão
2: Aonde a missão pode ser desbloqueada
3: tipo de premio, pode ser "carta", "item" ou "moeda"
4: O nome da carta ou do item a ser ganho, ou a quantidade de moedas
"""
from missions import *
from auxiliary_functions import criar_save, ler_save, adicionar_save

missoes = [("Estou rico!", missao_moedas, "loja", "carta", "mr_money"),
           ("Derrotado", missao_o_derrotado, "loja"),
           ("Vitorioso", missao_o_vitorioso, "loja"),
           ("Mestre do Jogo", missao_lenda_das_cartas, "loja"),
           ("Dono da loja", missao_dono_da_loja, "loja", "carta", "dono_da_loja"),
           ("Somos lendários", missao_somos_lendarios, "loja"),
           ("Homem comum", missao_homem_comum, "loja"),
           ("Duelo especial", missao_duelo_especial, "inicio"),
           ("Massacre", missao_massacre, "vitoria"),
           ("Parece impossível", missao_parece_impossivel, "vitoria"),
           ("Zerado", missao_zerado, "loja"),
           ("Livro cheio", missao_livro_cheio, "loja"),
           ("Reviravolta", missao_reviravolta, "vitoria"),
           ("Primeira vez", missao_primeira_vez, "vitoria", "moeda", 100),
           ("Esfregue a lâmpada", missao_genio_da_lampada, "loja", "carta", "genio_da_lampada"),
           ("Por um triz", missao_por_um_triz, "vitoria", "moeda", 300),
           ("Passando o tempo", missao_passando_o_tempo, "loja", "carta", "mestre_das_horas"),
           ("De dia", missao_de_dia, "loja", "carta", "o_sol"),
           ("De noite", missao_de_noite, "loja", "carta", "a_lua"),
           ("Nome funcao 19", None),
           ("Nome funcao 20", None),
           ("Nome funcao 21", None),
           ("Nome funcao 22", None),
           ("Nome funcao 23", None),
           ("Nome funcao 24", None),
           ("Nome funcao 25", None),
           ("Nome funcao 26", None),
           ("Nome funcao 27", None),
           ("Nome funcao 28", None),
           ("Nome funcao 29", None),
           ("Nome funcao 30", None),
           ("Nome funcao 31", None),
           ("Nome funcao 32", None),
           ("Nome funcao 33", None),
           ("Nome funcao 34", None),
           ("Nome funcao 35", None),
           ("Nome funcao 36", None),
           ("Nome funcao 37", None),
           ("Nome funcao 38", None),
           ("Nome funcao 39", None),
           ("Nome funcao 40", None),
           ("Nome funcao 41", None),
           ("Nome funcao 42", None),
           ("Nome funcao 43", None),
           ("Nome funcao 44", None),
           ("Nome funcao 45", None),
           ("Nome funcao 46", None),
           ]

missoes = sorted(missoes, key = lambda x : x[0])

#=============================================================================

def conferir_missoes(tipo:str, save:dict, **variaveis) -> dict:
    """
    Separa todas missões que serão conferidas e confere
    Desbloqueia os itens das missões

    Retorna o novo save
    """

    #Confere quais missões serão conferidas:
    missoes_validas = [missao if len(missao) >= 3 and missao[2] == tipo and (not missao[0] in save["missoes"]) else None for missao in missoes]
    while None in missoes_validas:
        missoes_validas.remove(None)

    #Confere se as missões são válidas:
    nova_missao = []
    for missao in missoes_validas:
        if missao[1] != None and missao[1](save, **variaveis):
            nova_missao.append(missao[0])
            if len(missao) >= 5:
                if missao[3] == "carta":
                    if not missao[4] in save["cartas"]:
                        save["cartas"].append(missao[4])
                elif missao[3] == "item":
                    if not missao[4] in save["inventario"]:
                        save["inventario"].append(missao[4])
                elif missao[3] == "moeda":
                    save["moedas"] = int(save["moedas"]) + int(missao[4])

    #Adiciona a missão comprida, se tiver alguma, no save
    if nova_missao != []:
        save["missoes"].extend(nova_missao)
        adicionar_save(save)

    return save

if __name__ == "__main__":
    #Debug:
    a = ler_save()
    b = conferir_missoes(tipo = "vitoria", save = a)
