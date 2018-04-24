#!/usr/bin/env python3

import os
import sys
import random
import time
from datetime import datetime

#################################################################################
########################### OBJECTS #############################################
#################################################################################

class bools:
    journal = True
    show_menu = True

class input_vars:
    menu_input = ""

#################################################################################
########################### FUNCTIONS ###########################################
#################################################################################

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load():
    try: 
        print("Reading your secrets")
        t = 0
        for t in range(0,5):
            print(".")
            time.sleep(0.3)
            t += 1
        file = open("journal.txt","r")
        game_vars.current_score = int(file.readline())
        file.close()
        clear()
        print("Found your previous score: {}!".format(game_vars.current_score))
    except:
        clear()
        print("Couldn't load! Check save file.\npro-tip: If this is your first time, try saving something first.")
        pass

def save():
    try:
        print("Saving your thoughts.")
        t = 0
        for t in range(0,5):
            print(".")
            time.sleep(0.3)
            t += 1    
        file = open("journal.txt","w")
        file.write(str(game_vars.current_score))
        file.close()
        clear()
        print("Save successful!")
    except:
        clear()
        print("Couldn't save. Check save file.")
        pass

def menu():
    print("-----------------")
    input_vars.menu_input = input("Type 'n' to begin a new entry.\nType 's' to save.\nType 'l' to load.\nType 'q' to quit.\n>> ").lower()

    if input_vars.menu_input == "n":
        print("new")
        
    elif input_vars.menu_input == "s":
        print("save")
        
    elif input_vars.menu_input == "l":
        print("load")
        
    elif input_vars.menu_input == "q":
        print("quit")
        bools.journal = False

    else:
        print("error")
        bools.journal = False

    prompts()

def prompts():
    print("prompts")
    menu()

def ux():
    if bools.show_menu == True:
        print("Welcome to your journal.")
        print(str(datetime.now())[:-7])
        menu()
        bools.show_menu = False

    else:
        print(str(datetime.now())[:-7])
        prompts()

#################################################################################
########################### MAIN LOOP ###########################################
#################################################################################

while bools.journal == True:
    clear()
    ux()


