colors = {"d_red": 52,
          "red": 1,
          "orange": 9,
          "cian": 14,
          "dd_blue": 17,
          "d_blue": 21,
          "blue": 39,
          "l_blue": 45,
          "ll_blue": 51,
          "dd_green": 22,
          "d_green": 34,
          "green": 40,
          "l_green": 46,
          "red_purple": 53,
          "purple": 57,
          "blue_purple": 63,
          "light": 159,
          "black": 232,
          "white": 255,
          "yellow": 226}

for i in range(255):
    print(f"\033[38;5;{i}m" + str(i) + "\033[0m")
