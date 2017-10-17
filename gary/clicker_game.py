import os
import sys
import random

# parsing txt file for variable values
# execfile(file_content)

breakout = 1

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def game():
    print("Let the game begin.")

def welcome():
    print("welcome to the game.")
    start = input("Press enter/return to start or Q to quit.\n> ").lower()
    
    if start == 'q':
        print("Bye!")
        breakout = 0
        return False
    else:
        return True
        breakout = 1

while True:
    clear()
    welcome()
    if breakout == 0:
        break
    else:
        game()



#
#
# while( quit == false ):
#   if( scene == "menu" ):
#     menu(stuff)
#   if( scene == "game" ):
#     game(stuff)
#
#