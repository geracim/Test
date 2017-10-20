#!/usr/bin/env python3

import os
import sys
import random

class vars:
    keep_playing = True
    current_score = 0
    p_lvl = 1
    multiplier = 5
    lvl_1_cap = 500
    lvl_2_cap = 1200
   

def lvl_check():
    if vars.current_score < vars.lvl_1_cap:
        vars.p_lvl = 1
    elif vars.current_score > vars.lvl_1_cap and vars.current_score < vars.lvl_2_cap:
        vars.p_lvl = 2

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def calculate_score():
    vars.current_score = vars.current_score + (vars.p_lvl * vars.multiplier)

def game():
    print("""Keep tapping enter to earn points.
------------------""")

    start = input("Tap Enter to play or 'q' to quit.\n> ").lower()
    clear()

    if start == 'q':
        print("Your final score was {}. \nHope to see you again soon!".format(vars.current_score))
        vars.keep_playing = False
    else:
        calculate_score()
        print("Your score is: {}.".format(vars.current_score))
        print("Your level is: {}.".format(vars.p_lvl))

clear()

while vars.keep_playing == True:
    game()