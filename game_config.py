"""
Configurações do jogo
"""

X:int = 145
Y:int = 53
FPS:int = 12
FPS_LOJA:int = 8
FPS_MAPA:int = 4

DISPOSITION_X_CARDS:list = [5, 55, 105]
DISPOSITION_Y_CARDS:list = [1, 22]

DISPOSITION_X_TEXT:int = 5
DISPOSITION_Y_TEXT:int = 43

ART_WIDTH:int = 16
HEIGHT_ART:int = 34

FOLDER_SAVE:str = "save"
SAVE_SAVE:str = f"{FOLDER_SAVE}/save.json"
FOLDER_MODS:str = "mods"
FOLDER_ART:str = f"{FOLDER_MODS}/arts"
FOLDER_CARDS_MODS:str = f"{FOLDER_MODS}/cards"

CONTRA_BOT:bool = True

SLEEP_TURN:float = 2
SLEEP_BOT:float = 1.5
SLEEP_INITIAL_TURN:float = 0
SLEEP_END_TURN:float = 0
SLEEP_DICE:float = 0

USE_MODS:bool = False

LANGUAGE = "pt"

BOOSTERS_ESPECIAIS = {"comum":{"nome":"booster comum", "moedas":40, "exp":0, "chances":[0, 0, 0, 1]},
                      "raro":{"nome":"booster raro", "moedas":200, "exp":0, "chances":[0, 0, 1, 0]},
                      "epico":{"nome":"booster épico", "moedas":800, "exp":0, "chances":[0, 1, 0, 0]},
                      "sorte":{"nome":"booster da sorte", "moedas":0, "exp":100, "chances":[0.2, 0.3, 0.4, 0.1]},
                      "lendario":{"nome":"booster lendário", "moedas":1000, "exp":100, "chances":[1, 0, 0, 0]}}

DIFICULT = {"facil":{"custo":3, "nome":"Facil", "cor":45}, #\033[93m \033[0m
            "normal":{"custo":5, "nome":"Normal", "cor":154},
            "dificil":{"custo":8, "nome":"Difícil", "cor":196},
            "epico":{"custo":10, "nome":"Épico", "cor":165},
            "impossivel":{"nome":"Impossível", "cor":248}}

TIMES_MAPA = {"mapa_sol": ["balao", "o_sol", "balao"],
              "mapa_lua": ["balao", "a_lua", "balao"],
              "mapa_piramide": ["rei_carangueijo", "cactus_cowboy", "profeta_das_areias"],
              "mapa_farol": ["morcego", "morcego", "morcego"],
              "mapa_castelo": ["guerreiro_preparado", "guarda_do_rei", "guerreiro_preparado"],
              "mapa_castelo_2": ["soldado_romano", "soldado_romano", "soldado_romano"],
              "mapa_cidade": ["detetive", "mafioso_acumulador", "dono_do_cassino"],
              "mapa_fazenda": ["lobo_da_noite", "cacador_de_feras", "rei_da_vila"],
              "mapa_trem": ["hacker", "assasina_de_quadrilha", "mestre_dos_venenos"],
              "mapa_montanha": ["aranha_rainha", "protetor_do_tesouro", "morcego"],
              "mapa_boneco_de_neve": ["boneco_de_neve", "boneco_de_neve", "boneco_de_neve"],
              "mapa_maquina_escavar": ["cubo", "exterminador", "cubo"],
              "mapa_pegasus": ["pegasus", "grifo", "cavalo_xadrez"],
              "mapa_vulcao": ["senhor_trovao", "senhor_trovao", "senhor_trovao"],
              "mapa_navio": ["pirata", "barba_negra", "pirata"],
              "mapa_espaconave": ["prototipo_meca", "meca_fogueteiro", "meca_last_hope"],
              "mapa_castelo_voador": ["escudeiro_experiente", "cacador_de_feras", "curandeiro_da_vila"],
              "mapa_ovni": ["alien", "alien", "alien"],
              "mapa_oasis": ["cogumelo_venenoso", "flores_sinistras", "fenix"],
              "mapa_praia": ["curandeiro_da_vila", "campones_corajoso", "cacador_de_feras"],
              "mapa_tartaruga_gigante": ["morcego", "tartaruga_gigante", "morcego"],
              "mapa_dinossauro": ["morcego", "dinossauro", "morcego"]}
