from game_config import X, Y
TEMPO = [15, 35, 80, 170]

def adjust_image(image:(list), replace_:bool = False) -> (list):
    n_image = []
    for line in image:
        if replace_:
            n_image.append(list(line.replace(" ", "&")))
        else:
            n_image.append(list(line))
    return n_image

base_card = [f"+{'-'*34}+",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"|{' '*34}|",
             f"+{'-'*34}+"]
base_card = adjust_image(base_card)

campo = [
'     /  \\        /  \\        /  \\        /  \\        /  \\        /  \\'*3,
'__/        \\__/        \\__/        \\__/        \\__/        \\__/      '*3,  
'  \\        /  \\        /  \\        /  \\        /  \\        /  \\      '*3,  
'     \\__/        \\__/        \\__/        \\__/        \\__/        \\__/'*3]

for i in range(len(campo)):
    campo[i] = campo[i][:X-1] + "\n"

temp_campo = campo.copy()
while len(campo) < Y:
    campo.extend(temp_campo)
campo = campo[:Y]

n = 0
for i in range(len(campo) - 11, len(campo)):
    if n == 0:
        campo[i] = f"+{(X-3)*'-'}+\n"
    else:
        campo[i] = f"|{(X-3)*' '}|\n"
    n += 1

campo = "".join(campo)
campo = list(campo)

rolando_dado = """
(( _______
  /\\O    O\\
 /  \\      \\
/ O  \\O____O\\ ))
\\    /O     /
 \\  /   O  /
  \\/_____O/
          ))
""".split("\n")
rolando_dado = adjust_image(rolando_dado, replace_ = False)

dados = [adjust_image("""
+-------+
|       |
|       |
|       |
+-------+
""".split("\n")),adjust_image("""
+-------+
|       |
|   0   |
|       |
+-------+
""".split("\n")), adjust_image("""
+-------+
|  0    |
|       |
|    0  |
+-------+
""".split("\n")), adjust_image("""
+-------+
| 0     |
|   0   |
|     0 |
+-------+
""".split("\n")), adjust_image("""
+-------+
| 0   0 |
|       |
| 0   0 |
+-------+
""".split("\n")), adjust_image("""
+-------+
| 0   0 |
|   0   |
| 0   0 |
+-------+
""".split("\n")), adjust_image("""
+-------+
| 0   0 |
| 0   0 |
| 0   0 |
+-------+
""".split("\n"))]

soma_dado = adjust_image("""
+-------+
|   |   |
| --+-- |
|   |   |
+-------+
""".split("\n"))

subtracao_dado = adjust_image("""
+-------+
|       |
| ----- |
|       |
+-------+
""".split("\n"))

animacao_espada = ["#",
                   "  #",
                   "   #",
                   "    #",
                   "     #",
                   "      #",
                   "       #",
                   "         #",
                   "           #",
                   "            ##",
                   "              ##",
                   "                ###",
                   "                   #"]
animacao_espada = adjust_image(animacao_espada, replace_ = True)

seta_cima = ["   /\\",
             "  /  \\",
             " /    \\",
             "/      \\",
             " -|  |-",
             "  |  |",
             "  |  |",
             "   --"]
seta_cima = adjust_image(seta_cima, replace_ = False)

escudo = """|`-._/\_.-`|
|    ||    |
|___o()o___|
|__((<>))__|
\   o\/o   /
 \   ||   /
  \  ||  /
   '.||.'""".split("\n")
escudo = adjust_image(escudo, replace_ = False)

impacto_fraco = """  #      #    #
#    #
  
 #       #
      #
   #     #
   #  #""".split("\n")
impacto_fraco = adjust_image(impacto_fraco, replace_ = True)

caveira = """
   .-"      "-.
  /            \
 |              |
 |,  .-.  .-.  ,|
 | )(__/  \__)( |
 |/     /\     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`⠀⠀
""".split("\n")
caveira = adjust_image(caveira, replace_ = False)

coroa = """      
       o 
    o^/|\\^o
 o_^|\\/*\\/|^_o
o\*`'.\\|/.'`*/o
 \\\\\\\\\\\\|//////
  {><><@><><}
  `*********`
""".split("\n")
coroa = adjust_image(coroa, replace_ = True)

cruz = """
      _.--._
      \\ ** /
       (<>)
.      )  (      .
)\\_.._/ /\\ \\_.._/(
(*_<>_      _<>_*)
)/ '' \\ \\/ / '' \\(
'      )  (      '
       (  ) 
       )  (
       (<>)
      / ** \\
     /.-..-.\\
""".split("\n")
cruz = adjust_image(cruz, replace_ = False)

luz = """
     /\\
   .'  `.
 .'      `.
<          >
 `.      .'
   `.  .'
     \/
""".split("\n")
luz = adjust_image(luz, replace_ = True)

cemiterio = """
       ______
 _____/      \\_____
|                  ||
|  _     ___   _   ||
| | \     |   | \  ||
| |  |    |   |  | ||
| |_/     |   |_/  ||
| | \     |   |    ||
| |  \    |   |    ||
| |   \. _|_. | .  ||
|                  ||
| *   **    * **   |**
""".split("\n")
cemiterio = adjust_image(cemiterio, replace_ = False)

soco = """    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""".split("\n")
soco = adjust_image(soco, replace_ = False)

pocao = [adjust_image("""
  |~|
  | |
.'   `.
`.___.'
""".split("\n"), replace_ = False), adjust_image("""
 |~|
 | |
.' `.
`._.' 
""".split("\n"), replace_ = False)]

imagem_profeta_das_arreias = adjust_image("""                        .
              /^\\     .
         /\\   "V"
        /__\\   I      O  o
       //..\\\\  I     .
       \\].`[/  I
       /l\\/j\\  (]    .  O
      /. ~~ ,\\/I          .
      \\\L__j^\\/I       o
       \\/--v}  I     o   .
       |    |  I   _________
       |    |  I c(`       ')o
       |    l  I   \.     ,/
     _/j  L l\\_!  _//^---^\\\\_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""".split("\n"))

imagem_mago_suporte = adjust_image(""" . ' .  ' . '  ' O   . '  '   '
   . .   '    '  .  '   . '  '
    . .'..' . ' ' . . '.  . '
     `.':.'        ':'.'.'
      `\\\\_  |     _//'
        \\(  |\\    )/
        //\\ |_\\  /\\\\
       (/ /\\(" )/\\ \\)
        \\/\\ (  ) /\\/
           |(  )|
           | \( \\
           |  )  \\
           |      \\
           |       \\
           /  / /\\ \\
----------------------------------
""".split("\n"))

imagem_assasina_de_quadrilha = adjust_image("""
                  #
             .-"-. / #,_
            / /\\_ \\  `#|\\
           / /')'\\ \\  /#/
          (  \\ = /  )/\\/#
           )  ) (  (/  \\
          (_.;`"`;._)  |
         / (  \\|/  )   |
        /  /\\-'^'-/\\   |
       |  \\| )=@=(  \\_/
       |  /\\/     \\
       | /\\ \\      ;
       \\(// /'     |
          \\/       |
           |     / /""".split("\n"))

imagem_assasino_laranja = adjust_image("""
         /\______  __
        /-~     ,^~ / __n
       / ,---x /_.-"L/__,\\
      /-".---.\\_.-'/!"  \\ \\
      0\\/0___/   x' /    ) |
      \\.______.-'_.{__.-"_.^
       `x____,.-",-~( .-"
          _.-| ,^.-~ "\\
     __.-~_,-|/\\/     `i
    / u.-~ .-{\\/     .-^--.
    \\/   v~ ,-^x.____}--r |
        / /"            | |
      _/_/              !_l_
    o~_//)             (_\\\\_~o
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""".split("\n"))

imagem_vinganca_da_noite = adjust_image("""
              _____
          ,-~"     "~-. 
        ,^         ___ ^.
       / .^\\___. .^   ^. \\
      Y  l   O ! l   O !  Y
      l_ `.___.' `.___.' _[
      l^~"VVVVVVVVVVVVV"~^I
      !\\,               ,/!
       \\ ~-.,AAAAAAA,.-~ /
        ^.             .^
          "-.._____.,-"
""".split("\n"))

imagem_esqueleto_insano = adjust_image("""         /         # ".
         `   #        l
         |'._  ,._ l/"\\
         |  _J<__/.v._/
          \\( ,~._,,,,-)
           `-\\' \\`,,j|
              \\_,____J
         .--.__)--(__.--.
        /  `-----..--'. j
        '.- '`--` `--' \\\\
       //  '`---'`  `-' \\\\
      //   '`----'`.-.-' \\\\
    _//     `--- -'   \\' | \\______
   |  |         ) (      `.__.----
    \\7          \\`-(
    ||       _  /`-(""".split("\n"))

imagem_cacador_de_feras = adjust_image('''                _..__
              .' I   '.
              |.-"""-.|
             _;.-"""-.;_
         _.-' _..-.-.._ '-._
        ';--.-(_o_I_o_)-.--;'
         `. | |  | |  | | .`  _
           `-\\|  | |  |/-'   //
              |  | |  |   __//
              |  \_/  |  (_//\\
           _.'; ._._. ;'._//\\\\
      _.-'`; | \\  -  / | ;'-.\\\\
    .' :  /  |  |   |  |  \\  '.
   /   : /__ \\  \\___/  / __\\ : `.
  /    |   /  '._/_\\_.'  \\   :
'''.split("\n"))

imagem_cacador_iniciante = adjust_image("""         ....
       .'   ,:
     .'      \\.___..
   .'      .-'   _.'
   '.\\  \\/...-''`\\
     :.'    _  _  :
      :  \\ (o) (o) /
      (_ .  /--\\ ':        .':
        / |_\\-- .'       .'.'
        \   \\  .'_\\    .'.'
       .|__  \\/_/:   .'.'
      /          :\\.',;'
     .' -./      .'{\\|))
     '.   ',_,-.',;'--:
     / '../_   \\,;'_.'
     :.   ,''-'-'  \\""".split("\n"))

imagem_fantasma_solitario = adjust_image("""
      .-.
    .'   `.               __
    :g g   :             /  \\
    : o    `.            \\__/
   :         ``.    
  :             `.
 :  :         .   `.
 :   :          ` . `.
  `.. :            `. ``;
     `:;             `:'
        :              `.
         `.              `.     .
           `'`'`'`---..,___`;.-'
""".split("\n"))

imagem_milicia_fantasma = adjust_image("""
       .'``'.      ...
      :o  o `....'`  ;
      `. O         :'
   /__\\ `':          `.
  /    \\  `:.          `.
 |  - - |  : `.         `.
 |  ,O  | ,`..'`...       `.
 |\\/    \\/          `...     `.
 |      /    .-.       ``...  `.
  \\   _/    ( " )          `````.
   \\_/   /\\_.' '._/\\
         |         |
          \\       /
""".split("\n"))

imagem_dono_do_cassino = adjust_image("""             ,.--""-._
          __/         `.
     _,**"   "*-.       `.
   ,'            `.       \\
  ;    _,.---._    \\  ,'\\  \\
  :   ,'   ,-.. `.   \\'   \\ :
  |  ;_\\  (___)`  `-..__  : |
  ;-'`*'"  `*'    `--._ ` | ;
 /,-'/  -.        `---.`  |"
  /_,'`--='.       `-.._,-" _
  (/\\\\,--. \\    ___-.`:   //___
     /\\'''\\ '  |   |-`|  ( -__,'
    '. `--'    ;   ;  ; ;/_/
      `. `.__,/   /_,' /`.~;
      _.-._|_/_,'.____/   /
 ..--" /  =/  \\=  \\      /""".split("\n"))

imagem_orc_rejeitado = adjust_image("""
           ___
         .';:;'.
        /_' _' /\\   __
        ;a/ e= J/-'"  '.
        \\ ~_   (  -'  ( ;_ ,.
         L~"'_.    -.  \\ ./  )
         ,'-' '-._  _;  )'   (
       .' .'   _.'")  \\  \\(  |
      /  (  .-'   __\{`', \\  |
     / .'  /  _.-'   "  ; /  |
    / /    '-._'-,     / / \\ (
 __/ (_    ,;' .-'    / /  /_'-._
`"-'` ~`  ccc.'   __.','     \\j\\L\\
                 .='/|\\7      
                    ' `""".split("\n"))

imagem_curandeiro_da_vila = adjust_image("""                    /       |
               ___,'        |
             <  -'          :
              `-.__..--'``-,_\\_
                 |o/ ` :,.)_`>
                 :/ `     ||/)
                 (_.).__,-` |\\
                 /( `.``   `| :
                 \\'`-.)  `  ; ;
                 | `       /-<
                 |     `  /   `.
 ,-_-..____     /|  `    :__..-'\\
(\,'-.__\\\\  ``-./ :`      ;     
`\\ `\\   `\\\\  \\ :  (   `  /  , 
  \\` \\    \\\\   |  | `   :  :   
   \\ `\\_  ))  :  ;     |  |""".split("\n"))

imagem_guerreiro_preparado = adjust_image("""             _.-;-._
            ;_.JL___; 
            F"-/\\_-7L
            | a/ e | \\
           ,L,c;,.='/;,
        _,-;;S:;:S;;:' '--._
       ;. \\;;s:::s;;: .'   /\\
      /  \\  ;::::;;  /    /  \\
     / ,  k ;S';;'S.'    j __,l
  ,---/| /  /S   /S '.   |'   ;
 ,Ljjj |/|.' s .' s   \\  L    |
 LL,_ ]( \\    /    '.  '.||   ;
 ||\ > /  ;-.'_.-.___\\.-'(|=="(
 JJ," /   |_  [   ]     _]|   /
  LL\\/   ,' '--'-'-----'  \\  ( 
  ||     ;      |          |  >""".split("\n"))

imagem_arqueiro = adjust_image("""                  .;;,.
                 ; '" ;\\ \\//
                \\|a (a|7 \\//
                j| ..  | ||/
               //'.--.')\\-,/
             .-||- '' ||/  `-.
            ;  | \\ |/ |/ L.  ,|
            f\\ |\\| Y  || \\ '._\\
           j | \\|     (| |   | |
          |  L_\\         L.__: |
           \\(  '-.,-,    |   ; |
            |'-.'.L_rr>  f--f  |
-=,,______,--------- J-. ;  ;__ 
  ``"-,__   |  |      h  |  f  '--
      `--;;--,_       h  f-j   |
           / `-''-,,__J,'  \\_..--""".split("\n"))

imagem_soldado_novato = adjust_image("""             ,sSSSSs,
             sS';:'`Ss
            ;K e (e s7
             S, ''  SJ 
             sL_~~_;(S_) 
 |,          'J)_.-' />'-'
 j J         /-;-A'-'|'--'-j\\
  L L        )  |/   :    /  \\
   \\ \\       | | |    '._.'|  L
    \\ \\      | | |       | \\  J
     \\ \\    _/ | |       |  ',|
      \\ L.,' | | |       |   |/
     _;-r-<_.| \=\    __.;  _/
       {_}"  L-'  '--'   / /|
             |   ,      |  \\|
             |   |      |   ")""".split("\n"))

imagem_acumulador_de_almas = adjust_image("""     ;::::; :;
   ;:::::'   :;
  ;:::::;     ;.
 ,:::::'       ;           OOO\\
 ::::::;       ;          OOOOO\\
 ;:::::;       ;         OOOOOOOO
,;::::::;     ;'         / OOOOOOO
::::::::`. ,,,;.        /  / DOOOO
::::::::::::::::;,     /  /     DO
::;::::::;;;;::::;,   /  /
::`'::::::;;;::::: ,#/  /
:::`;::::::;;::: ;::#  /
::::`;:::::::: ;::::# /
::::`;:::::: ;::::::#/
::::::`;; ;:::::::::## 
:::::::`;::::::::;:::#""".split("\n"))

imagem_rei_da_vila = adjust_image("""                       ____
                      / ___`\\
          /|         ( (   \ \\
     |^v^v  V|        \\ \\/) ) )
     \\  ____ /         \\_/ / /
     ,Y`    `,            / /
     ||  -  -)           { }
     \\\\   _\\ |           | |
      \\\\ / _`\\_         / /
      / |  ~ | ``\\     _|_|
   ,-`  \    |  \\ \\  ,//(_}
  /      |   |   | \\/  \\| |
 |       |   |   | '   ,\\ \\
 |     | \\   /  /\\  _/`  | |
 \\     |  | |   | ``     | |
  |    \\  \\ |   |        | |""".split("\n"))

imagem_guarda_do_rei = adjust_image("""         _,.
       ,` -.)
      ( _/-\\\\-._
     /,|`--._,-^|            ,
     \\_| |`-._/||          ,'|
       |  `-, / |         /  /
       |     || |        /  /
        `r-._||/   __   /  /
    __,-<_     )`-/  `./  /
   '  \\   `---'   \\   /  /
       |           |./  /
       /           //  /
   \\_/' \\         |/  /
    |    |   _,^-'/  /
    |    , ``  (\\/  /_
     \\,.->._    \\X-=/^""".split("\n"))

imagem_mestre_da_lamina = adjust_image("""
             _,._
           ,'   ,`-.
|.        /     |\\  `.
\\ \\      (  ,/,-` ). `-._ __
 \\ \\      \|\\,' ,    `\\  /'  `\\
. \\ \\      ` |, /  /  \\ \\     \\
|  \\ \\         `,_/`, /\\,`-.__/`.
.   \\ \\            | ` /    /    `
     \\\\\\           `-/'    / 
      \\\\`/ _______,-/_   /'
     ---'`|       |`  ),' `---.  ,
.     \\..-`--..___|_,/          /
                 |    |`,-,...,/  
.                \\    | |_|   /   
                  |___|/  |, /""".split("\n"))

imagem_escudeiro_experiente = adjust_image("""         /   | |  \\
        |  __|_|___|
        |' |||  --
        |(   _L   ||
        \\|`-'__`-'|'
        _| \\      |-.
    .-'| |  \\     /  `-.
   /   | |\\     .'  ##  `-.
  /    | | `''''           \
 J     | |      #    # _____|
 |  |  J J         .-'   ___ `-.
 |  \\   L L #    .'  .-'  |  `-.`.
 | \\|   | |     /  .'|    |    |\\
 |  |   J J   .' .'  |    |    | \\
 |  |    L L J  /    |    |    |
/   |     \\ \\F J|    |    |    |
|   |      \\J F | () | () | () | (""".split("\n"))

imagem_gigante = adjust_image("""      /.'.'               '.\\
      |.'    _.--...--._     |
      \\    `._.-.....-._.'   /
      |     _..- .-. -.._   |
   .-.'    `.   ((@))  .'   '.-.
  ( ^ \\      `--.   .-'     / ^ )
   \\  /         .   .       \\  /
   /          .'     '.  .-    \\
  ( _.\\    \\ (_`-._.-'_)    /._\\)
   `-' \\   ' .--.          / `-'
       |  / /|_| `-._.'\\   |
       |   |       |_| |   /-.._
   _..-\\   `.--.______.'  |
        \\       .....     |
         `.  .'      `.  /
           \\           .'""".split("\n"))

imagem_protetor_do_tesouro = adjust_image("""                /           /
               /' .,,,,  ./
              /';'     ,/
             / /   ,,//,`'`
            ( ,, '_,  ,,,' ``
            |    /@  ,,, ;" `
           /    .   ,''/' `,``   /
          /   .     ./, `,, ` ; /
       ,./  .   ,-,',` ,,/''\\,'/#
      |   /; ./,,'`,,'' |   | /
      |     /   ','    /    |/ #
       \\___/'   '     |     |   #
         `,,'  |      /     `\\ #
              /      |        ~\\ #
             '       (
            :""".split("\n"))

imagem_campones_corajoso = adjust_image("""             :-----:
         (''' , - , ''')
         \\   ' .  , `  /
          \\  '   ^  ? /
           \\ `   -  ,'
            `j_ _,'
       ,- -`\\ \\  /f
     ,-      \\_\\/_/'-
    ,                 `,
    ,        |V|   #     ,     
         /\\          \\
   |    /      #      \\   ',
   ,   f  :           :`,  ,
   <...\\  ,       #   : ,- '
   \\,,,,\\ ;           : j  '
    \\    \\            :/^^^^'""".split("\n"))

imagem_mestre_dos_venenos = adjust_image(''' ,        `'-_.-.
/`'.       ,' _  |
    `-.  ,' ,'\\\\/
       \\, ,'  ee`-.
       / ./  ,(_   \      ,     
      (_/\\\\\\ \\__|`--'     ||
          \\|     \\        ||
          ||-./`-.}    .--||
         /     `-.__.-`_.-.|
         |      '._,-'`|___}    `;
         /   '.        |/ || ,;'`
         |     '.__,.-`   || ':,
         |       |        || ,;'
         /       /     _,.||oOoO.,
        |        |     \\-.O,o_O..-
       /         /     /'''.split("\n"))

imagem_fenix = adjust_image("""    ,,\\\\\\                     ///,,       ) (
  (\\\\\\\\//   ))            ))  \\\\////)      )
 (-(__//     ((                \\\\__)-)     (
(-(__||    ))                 ((||__)-))    ) )
-(-(_||           ```\\__        ||_)-)-))   ((
(-(/(/\\\\        ''; 9.- `      //\\)\\)-)-))    )
-(/(/(/\\\\      '';;;;-\\~      //\\)\\)\\)-)-)   (   )
(-(/(/(/\\======,:;:;:;:,======/\\)\\)\\)-)-))   )'
(-(/(/(/(//////:%%%%%%%:\\\\\\\\\\\\)\\)\\)\\)-)))`  ( (
(-(/(/(/('uuuu:WWWWWWWWW:uuuu`)\\)\\)\\)-))`    )
((-(/(/(/('|||:wwwwwwwww:|||')\\)\\)\\)-))`    ((
 '((((/(/('uuu:WWWWWWWWW:uuu`)\\)\\))))`     ))
   '':::UUUUUU:wwwwwwwww:UUUUUU:::``     ((   )
((      '''''''\\uuuuuuuu/``````         ))
 ))     ))     `JJJJJJJJJ`   ((      ((
   ((       ((   LLLLLLLLLLL         ))""".split("\n"))

for i in range(len(imagem_fenix)):
    imagem_fenix[i] = imagem_fenix[i][:34]

fogo = adjust_image("""          (  .      )
      )           (              )
             .  '   .   '  .  '  .
    (    , )       (.   )  (   ',    )
     .' ) ( . )    ,  ( ,     )   ( .
  ). , ( .   (  ) ( , ')  .' (  ,    )
(_,) . ), ) _) _,')  (, ) '. )  ,. (' )
""".split("\n"), replace_ = False)

for i in range(len(fogo)):
    fogo[i] = fogo[i][:33]
