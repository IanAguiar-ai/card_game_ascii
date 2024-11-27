"""
Jogo, parte lógica e gráfica que faz a interseção entre todas as telas do jogo
"""

from random import random
from threading import Thread
from time import sleep, time
from game_config import *
from engine_card_game import CARTAS
from arts import *
from auxiliary_functions import *
from card_game import run_the_game
from pure_engine_ascii import Screen
from card_builder import card_builder
from translator import translate

def animacao_menu() -> None:
    pos_n = [0, 50, 0]
    posicoes = [i for i in range(0, 50)]
    posicoes.extend(i for i in range(49, 0, -1))
    
    while globals()["gatilho_menu"]:
        game.add_effects(x = 65, y = 3,
                        image = castelo_menu,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
    

        game.add_effects(x = 3, y = 3,
                        image = nome,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)
        
        game.add_effects(x = 20 + posicoes[pos_n[0]], y = 18,
                        image = nuvem_1,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)        

        game.add_effects(x = 50 + posicoes[pos_n[1]], y = 12,
                        image = nuvem_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        game.add_effects(x = 70 + posicoes[pos_n[2]], y = 20,
                        image = nuvem_2,
                        frames = 1,
                        tipe = None,
                        wait = 0,
                        to_start = 0)

        for i in range(len(pos_n)):
            if random() > 0.8:
                pos_n[i] = (pos_n[i]+1)%len(posicoes)
        
        sleep(0.5)

def entrar_loja() -> None:
    """
    Animação da loja
    """

    from choose_deck import choose_deck_animation
    from open_booster import abrir_pacote_com_carta
    from text_mission import missoes
    from text_mission import conferir_missoes
    
    def animacao_loja() -> None:
        em_fala = 0
        em_fala_montar_deck = 0
        em_fala_criar_deck = 0
        while globals()["gatilho_loja"]:
            game.add_effects(x = 85, y = 3,
                            image = loja,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            game.add_effects(x = 5, y = 3,
                            image = caixa_ferramentas,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            game.add_effects(x = 20, y = 26,
                            image = mesa_simples,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            game.add_effects(x = 124, y = 24,
                            image = vela,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)           

            if random() < 0.05:
                game.add_effects(x = 112, y = 16,
                            image = piscando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)

            if random() < 0.3:
                game.add_effects(x = 125, y = 24,
                            image = fumaca_vela,
                            frames = 1,
                            tipe = None,
                            wait = 0,
                            to_start = 0)

            if (memoria_save["moedas"] == 0 and memoria_save["deck"] == None) or em_fala_montar_deck > 0:
                if em_fala_montar_deck <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala_montar_deck = 30
                    
                game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                game.add_effects(x = 96, y = 6,
                                    image = instrucoes_textos[1],
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)
                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)
                    
                em_fala_montar_deck -= 1

            elif memoria_save["cartas"] == [] or em_fala_criar_deck > 0:
                if em_fala_criar_deck <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala_criar_deck = 30
                    
                game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                game.add_effects(x = 96, y = 6,
                                    image = instrucoes_textos[0],
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)
                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)
                    
                em_fala_criar_deck -= 1

            elif random() < 0.005 or em_fala > 0:
                if em_fala <= 0:
                    texto_vendedor = textos_aleatorios[int(len(textos_aleatorios)*random())]
                    em_fala = 30

                if random() < 0.2:
                    game.add_effects(x = 113, y = 18,
                            image = falando,
                            frames = 1,
                             tipe = None,
                            wait = 0,
                            to_start = 0)

                if len(texto_vendedor) > 3:
                    game.add_effects(x = 94, y = 4,
                                    image = balao_medio,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 6,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                elif len(texto_vendedor) > 2:
                    game.add_effects(x = 94, y = 8,
                                    image = balao_pequeno,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 10,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                elif len(texto_vendedor) > 1:
                    game.add_effects(x = 94, y = 9,
                                    image = balao_menor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 11,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                else:
                    game.add_effects(x = 94, y = 10,
                                    image = balao_unico,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)

                    game.add_effects(x = 96, y = 12,
                                    image = texto_vendedor,
                                    frames = 1,
                                    tipe = None,
                                    wait = 0,
                                    to_start = 0)


                em_fala -= 1
            
            sleep(0.2)

    def animacao_inventario() -> None:
        from itens import itens

        memoria_save = ler_save()
        pag = 0
        pos_inventario = 0
        missoes_por_pag = 7
        texto_aleatorio = ["-- --- -",
                           "--- - ----",
                           "- -- --- --",
                           "-- -- - --",
                           "--- --- -- -",
                           "---- -- - ----",
                           "--- ---- -- -",
                           "----- ---- -",
                           "---- ----- -- --",
                           "--- --- -- ---",
                           "- -- - -- ----",
                           "--- -- - ---- - -",
                           "- ----- - --- - ---",
                           "-- - --- - --- - -- --",
                           "-- -- ---- -- -- -",
                           "-- - - --- - - ----",
                           "--- --- - --- --- --"]

        while True:
            try:
                game.buffer_text = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n({itens[memoria_save['inventario'][pos_inventario]]['nome']})\n\nAperte:\n(Z, X) Para alternar entre páginas\n(A, W, S, D) Para escolher entre itens")
            except:
                game.buffer_text = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(Z, X) Para alternar entre páginas\n(A, W, S, D) Para escolher entre itens")

            #Inventario:
            for x in range(5):
                for y in range(5):
                    game.add_effects(x = 4 + x*16, y = 0 + y*8,
                                     image = caixa_simples,
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                    if len(memoria_save["inventario"]) > x+y*5:
                        game.add_effects(x = 5 + x*16, y = 1 + y*8,
                                     image = itens[memoria_save["inventario"][x+y*5]]["imagem"],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

            game.add_effects(x = 4 + (pos_inventario%5)*16, y = 0 + (pos_inventario//5)*8,
                             image = caixa_pontilhada,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            if len(memoria_save["inventario"]) > pos_inventario and "descricao" in itens[memoria_save["inventario"][pos_inventario]]:
                game.add_effects(x = 86, y = 28,
                                 image = caixa_texto(itens[memoria_save["inventario"][pos_inventario]]["descricao"], limite = 57),
                                 frames = 1,
                                 tipe = None,
                                 wait = 0,
                                 to_start = 0)
                
            #Missões:
            game.add_effects(x = 84, y = 6,
                             image = livro_aberto_grande,
                             frames = 1,
                             tipe = None,
                             wait = 0,
                             to_start = 0)

            x_, y_ = 0, 0
            for missao in missoes[pag*(missoes_por_pag*2 + 2):(pag+1)*(missoes_por_pag*2 + 2)]:
                x, y =  94 + x_ * 27,  9 + y_*2
                if missao[0] in memoria_save["missoes"]:
                    game.add_effects(x = x, y = y,
                                     image = put_color([list(missao[0])], color = (x_*7 + y_*32+3) % 200),
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                else:
                    game.add_effects(x = x, y = y,
                                     image = [list(missao[0])],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)
                    
                game.add_effects(x = x, y = y+1,
                                     image = [list(texto_aleatorio[(pag*x*y+x+y) % len(texto_aleatorio)])[:19]],
                                     frames = 1,
                                     tipe = None,
                                     wait = 0,
                                     to_start = 0)

                y_ += 1
                if y_ > missoes_por_pag:
                    x_ = 1
                    y_ = 0

            resp = input()
            if resp.lower() == "z":
                pag = max(pag - 1, 0)
            elif resp.lower() == "x":
                pag = min(pag + 1, len(missoes)//(missoes_por_pag*2 + 2))
            elif resp.lower() == "a" or resp.lower() == "q":
                pos_inventario = max(0, pos_inventario - 1)
            elif resp.lower() == "d" or resp.lower() == "e":
                pos_inventario = min(24, pos_inventario + 1)
            elif resp.lower() == "w":
                pos_inventario = max(0, pos_inventario - 5)
            elif resp.lower() == "s":
                pos_inventario = min(24, pos_inventario + 5)
            elif resp == "":
                break


    booster_do_dia = BOOSTER_DO_DIA()
    globals()["gatilho_loja"] = True
    memoria_save = ler_save()

    #Conferir as missões da loja:
    conferir_missoes(tipo = "loja", save = memoria_save)
    
    texto_loja = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m | EXP: \033[94m{memoria_save['exp']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar booster \033[93m(100 moedas)\033[0m\n(3) Para comprar booster especial ({booster_do_dia['nome']}) (Preço: {booster_do_dia['moedas']} moedas + {booster_do_dia['exp']} exp)\n(4) Inventário\n(5) Para sair da loja")
    game.buffer_text = texto_loja
    thread_animacao_loja = Thread(target = animacao_loja)
    thread_animacao_loja.start()

    while True:
        game.buffer_text = texto_loja
        
        resposta = input()
        
        try:
            resposta = int(resposta)
        except:
            pass
        if type(resposta) == int and 1 <= resposta <= 5:
                
            if resposta == 1 and len(memoria_save["cartas"]) >= 3: #Escolher o deck
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                choose_deck_animation()
            
                globals()["gatilho_loja"] = True
                clear_all()
                memoria_save = ler_save()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
                
            elif resposta == 2 and memoria_save["moedas"] >= 100: #Comprar um booster
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                abrir_pacote_com_carta()

                globals()["gatilho_loja"] = True
                clear_all()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
                memoria_save = ler_save()
                texto_loja = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m | EXP: \033[94m{memoria_save['exp']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar booster \033[93m(100 moedas)\033[0m\n(3) Para comprar booster especial ({booster_do_dia['nome']}) (Preço: {booster_do_dia['moedas']} moedas + {booster_do_dia['exp']} exp)\n(4) Inventário\n(5) Para sair da loja")
            elif resposta == 3 and memoria_save["moedas"] >= booster_do_dia["moedas"] and memoria_save["exp"] >= booster_do_dia["exp"]:
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                abrir_pacote_com_carta(chances = booster_do_dia["chances"], moedas = booster_do_dia["moedas"], exp = booster_do_dia["exp"])

                globals()["gatilho_loja"] = True
                clear_all()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
                memoria_save = ler_save()
                texto_loja = translate(f"MOEDAS: \033[93m{memoria_save['moedas']}\033[0m | EXP: \033[94m{memoria_save['exp']}\033[0m\nCARTAS OBTIDAS: {len(memoria_save['cartas'])}/{len(CARTAS)}\n\nAperte:\n(1) Para escolher o deck\n(2) Para comprar booster \033[93m(100 moedas)\033[0m\n(3) Para comprar booster especial ({booster_do_dia['nome']}) (Preço: {booster_do_dia['moedas']} moedas + {booster_do_dia['exp']} exp)\n(4) Inventário\n(5) Para sair da loja")

            elif resposta == 4:
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)

                animacao_inventario()
                
                globals()["gatilho_loja"] = True
                clear_all()
                thread_animacao_loja = Thread(target = animacao_loja)
                thread_animacao_loja.start()
            
            elif resposta == 5: #Sair da loja
                globals()["gatilho_loja"] = False
                thread_animacao_loja.join()
                del thread_animacao_loja
                sleep(1/FPS_LOJA)
                break

if __name__ == "__main__":
    memoria_save = ler_save()
    if memoria_save == None:
        memoria_save = criar_save()
        
    clear_all()
    game = Screen(x = X, y = Y, fps = FPS_LOJA)
    texto_principal = translate(f"Aperte:\n(1) Jogar\n(2) Ir a loja\n(3) Construtor de cartas")
    game.buffer_text = texto_principal
    game_t = Thread(target = game.run)
    game_t.start()

    gatilho_menu = True
    animacao_menu_thread = Thread(target = animacao_menu)
    animacao_menu_thread.start()

    while True:
        resposta = input()
        try:
            resposta = int(resposta)
        except:
            pass
        if type(resposta) == int and 1 <= resposta <= 3:
            gatilho_menu = False
            animacao_menu_thread.join()
            del animacao_menu_thread

            if resposta == 1: #Ir para o jogo
                run_the_game()
                gatilho_menu = True
                game.buffer_text = texto_principal
                animacao_menu_thread = Thread(target = animacao_menu)
                animacao_menu_thread.start()

            elif resposta == 2: #Ir para a loja
                entrar_loja()
                gatilho_menu = True
                game.buffer_text = texto_principal
                animacao_menu_thread = Thread(target = animacao_menu)
                animacao_menu_thread.start()

            elif resposta == 3:
                card_builder()
                gatilho_menu = True
                game.buffer_text = texto_principal
                animacao_menu_thread = Thread(target = animacao_menu)
                animacao_menu_thread.start()

    game.close()
    game_t.join()

    del game
