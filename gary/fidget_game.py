#!/usr/bin/env python3

import os
import sys
import random

class game_vars:
    keep_playing = True
    current_score = 0
    p_lvl = 1
    multiplier = 5
    
class lvl_vars:
    lvl_1_cap = 100
    lvl_2_cap = 255
    lvl_3_cap = 500
    lvl_4_cap = 860


def lvl_check():
    if game_vars.current_score < lvl_vars.lvl_1_cap:
        game_vars.p_lvl = 1
    elif game_vars.current_score > lvl_vars.lvl_1_cap and game_vars.current_score < lvl_vars.lvl_2_cap:
        game_vars.p_lvl = 2
    elif game_vars.current_score > lvl_vars.lvl_2_cap and game_vars.current_score < lvl_vars.lvl_3_cap:
        game_vars.p_lvl = 3
    elif game_vars.current_score > lvl_vars.lvl_3_cap and game_vars.current_score < lvl_vars.lvl_4_cap:
        game_vars.p_lvl = 4

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def calculate_score():
    if game_vars.p_lvl > 1 and game_vars.p_lvl < 2:
        game_vars.current_score = game_vars.current_score + (game_vars.p_lvl * (game_vars.multiplier**2 / 2))
    elif game_vars.p_lvl > 2 and game_vars.p_lvl < 3:
        game_vars.current_score = game_vars.current_score + (game_vars.p_lvl * (game_vars.multiplier**3 / 2))
    else:
        game_vars.current_score = game_vars.current_score + (game_vars.p_lvl * game_vars.multiplier)

def game():
    print("""Keep tapping enter to earn points.
------------------""")

    start = input("Tap Enter to play or 'q' to quit.\n> ").lower()
    clear()

    if start == 'q':
        print("Your final score was {}.".format(game_vars.current_score))
        print("Your final level was: {}.".format(game_vars.p_lvl))
        print("Hope to see you again soon!")
        game_vars.keep_playing = False
    else:
        calculate_score()
        lvl_check()
        calculate_score()
        print("Your score is: {}.".format(game_vars.current_score))
        print("Your multiplier is {}.".format(game_vars.p_lvl * game_vars.multiplier))
        print("Your level is: {}.".format(game_vars.p_lvl))

clear()

while game_vars.keep_playing == True:
    game()