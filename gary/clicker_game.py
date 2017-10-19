import os
import sys
import random

# parsing txt file for variable values
# execfile(file_content)

keep_playing = True

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def game():
    print("Let the game begin.")

def welcome(keep_playing):
    print("welcome to the game.\n -----------------")
    start = input("Press enter/return to start or Q to quit.\n> ").lower()
    clear()

    if start == 'q':
        print("Bye!")
        keep_playing = False
    else:
        print("Hi!")


while keep_playing == True:
    welcome(keep_playing)
    game()