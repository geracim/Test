import os
import sys
import random

# parsing txt file for variable values
# execfile(file_content)


p_level = 1
p_exp = 0
p_continue = 0
p_choice = ""

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def welcome():
    print("Welcome to the Game.\n")
    print("The purpose of this game is to reach level 10.\n")
    print("You achieve new levels by gaining enough experience points (exp) to 'level up.'\n")
    input("Press any key if you are ready to continue.\n > ")
    clear()

def game():
    clear()
    # show intro for the first time
    welcome()
    # show menu and teach user how to play
    #menu(p_choice)

game()