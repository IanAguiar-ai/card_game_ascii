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

BOOSTERS_ESPECIAIS = {"comum":{"nome":"bosster comum", "moedas":40, "exp":0, "chances":[0, 0, 0, 1]},
                      "raro":{"nome":"booster raro", "moedas":200, "exp":0, "chances":[0, 0, 1, 0]},
                      "epico":{"nome":"booster épico", "moedas":800, "exp":0, "chances":[0, 1, 0, 0]},
                      "sorte":{"nome":"booster da sorte", "moedas":0, "exp":100, "chances":[0.2, 0.3, 0.4, 0.1]},
                      "lendario":{"nome":"booster lendário", "moedas":1000, "exp":100, "chances":[1, 0, 0, 0]}}

TIMES_MAPA = {"mapa_sol": ["balao", "o_sol", "balao"],
              "mapa_lua": ["balao", "a_lua", "balao"],
              "mapa_piramide": None,
              "mapa_farol": None,
              "mapa_castelo": None,
              "mapa_castelo_2": None,
              "mapa_cidade": None,
              "mapa_fazenda": None,
              "mapa_trem": None,
              "mapa_montanha": None,
              "mapa_boneco_de_neve": None,
              "mapa_maquina_escavar": None,
              "mapa_pegasus": None,
              "mapa_vulcao": None,
              "mapa_navio": None,
              "mapa_espaconave": None,
              "mapa_castelo_voador": None,
              "mapa_ovni": None,
              "mapa_oasis": None,
              "mapa_praia": None}
