#!/usr/bin/env python3

import os
import sys
import random

keep_playing = True
current_score = 0
multiplier = 5

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def game():
    global current_score
    global multiplier
    
    start = input("Press any key to start and when you're ready to quit, tap 'q'.\n> ").lower()
    clear()

    if start == 'q':
        print("Your final score was {}. \n Hope to see you again soon!".format(current_score))
        global keep_playing
        keep_playing = False
    else:
        current_score = current_score + multiplier
        print("Your score is: {}.".format(current_score))

clear()
print("Welcome to the fidget game. \n\nYou play by repeatedly and compulsively tapping any key on your keyboard.\n\n Press any key to begin. 'q' to quit.")

while keep_playing == True:
    game()