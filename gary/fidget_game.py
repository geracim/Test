#!/usr/bin/env python3

import os
import sys
import random
import time

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
    lvl_5_cap = 1200
    lvl_6_cap = 1800
    lvl_7_cap = 2600
    lvl_8_cap = 3300
    lvl_9_cap = 4500
    lvl_10_cap = 6000


def lvl_check():
    if game_vars.current_score < lvl_vars.lvl_1_cap:
        game_vars.p_lvl = 1
    elif game_vars.current_score > lvl_vars.lvl_1_cap and game_vars.current_score < lvl_vars.lvl_2_cap:
        game_vars.p_lvl = 2
    elif game_vars.current_score > lvl_vars.lvl_2_cap and game_vars.current_score < lvl_vars.lvl_3_cap:
        game_vars.p_lvl = 3
    elif game_vars.current_score > lvl_vars.lvl_3_cap and game_vars.current_score < lvl_vars.lvl_4_cap:
        game_vars.p_lvl = 4
    elif game_vars.current_score > lvl_vars.lvl_4_cap and game_vars.current_score < lvl_vars.lvl_5_cap:
        game_vars.p_lvl = 5
    elif game_vars.current_score > lvl_vars.lvl_5_cap and game_vars.current_score < lvl_vars.lvl_6_cap:
        game_vars.p_lvl = 6
    elif game_vars.current_score > lvl_vars.lvl_6_cap and game_vars.current_score < lvl_vars.lvl_7_cap:
        game_vars.p_lvl = 7
    elif game_vars.current_score > lvl_vars.lvl_7_cap and game_vars.current_score < lvl_vars.lvl_8_cap:
        game_vars.p_lvl = 8
    elif game_vars.current_score > lvl_vars.lvl_8_cap and game_vars.current_score < lvl_vars.lvl_9_cap:
        game_vars.p_lvl = 9
    elif game_vars.current_score > lvl_vars.lvl_9_cap and game_vars.current_score < lvl_vars.lvl_10_cap:
        game_vars.p_lvl = 10

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def calculate_score():
    game_vars.current_score += int((game_vars.multiplier**game_vars.p_lvl / game_vars.p_lvl))

def save():
    try:
        print("Saving your score.")
        t = 0
        for t in range(0,5):
            print(".")
            time.sleep(1)
            t += 1    
        file = open("fidget_game_score.txt","w")
        file.write(str(game_vars.current_score))
        file.close()
        clear()
        print("Save successful!")
    except:
        clear()
        print("Couldn't save. Check save file.")
        pass

def load():
    try: 
        print("Attempting to load previous score.")
        t = 0
        for t in range(0,5):
            print(".")
            time.sleep(1)
            t += 1
        file = open("fidget_game_score.txt","r")
        game_vars.current_score = int(file.readline())
        file.close()
        clear()
        print("Found your previous score: {}!".format(game_vars.current_score))
    except:
        clear()
        print("Couldn't load! Check save file.\nIf this is your first time, you must save the game to create save file.")
        pass

def game():
    print("------------------")
    print("""To load previous game, enter: 'l'.
To save, enter: 's'.
To quit, enter: 'q'
------------------""")

    play = input("Keep tapping enter to earn points.\n> ").lower()
    clear()

    if play == 'q':
        save()
        print("Your final score was {}.".format(game_vars.current_score))
        print("Your final level was: {}.".format(game_vars.p_lvl))
        print("Hope to see you again soon!")
        game_vars.keep_playing = False
    elif play == 's':
        save()
    elif play == 'score':
        print(game_vars.current_score)
    elif play == 'l':
        load()
    else:
        calculate_score()
        lvl_check()
        calculate_score()
        print("Your score is: {}.".format(game_vars.current_score))
        print("Your level is: {}.".format(game_vars.p_lvl))

clear()

while game_vars.keep_playing == True:
    game()