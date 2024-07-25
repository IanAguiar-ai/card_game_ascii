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
