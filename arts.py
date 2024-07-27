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
seta_cima = adjust_image(seta_cima, replace_ = True)

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
caveira = adjust_image(caveira, replace_ = True)

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
cruz = adjust_image(cruz, replace_ = True)

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
cemiterio = adjust_image(cemiterio, replace_ = True)

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
