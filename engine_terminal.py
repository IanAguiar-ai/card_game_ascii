"""
Using ANSI for terminal
"""

from colors_terminal import colors
from time import sleep

#########################################################################################
#Classes:

class Screen:
    def __init__(self, name:str):
        self.name = name
        self.elements = []

    def add(self, elements:list) -> None:
        if type(elements) == list:
            for element in elements:
                self.add(element)

        else:
            self.elements.append(element)

#########################################################################################
#Functions:

def put_color(color:int = 190, back_color:int = 232,text:str = "", style:int = 0, end = "\n") -> None:
    if style == 0:
        return f"\033[48;5;{back_color}m\033[38;5;{color}m{text}\033[0m"
    else:
        style = f"\033[{style}m"
        return f"{style}\033[48;5;{back_color}m\033[38;5;{color}m{text}\033[0m"

def clear():
    print("\033c", end="")

if __name__ == "__main__":
    a = ""
    for i in range(232, 256):
        for j in range(1):
            sleep(0.1)
            clear()
            print(put_color(i, 232, f"{i}-{j}: teste", style = 0))


