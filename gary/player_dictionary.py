#!/usr/bin/env python3

import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def player_card():
    player = {
    "pName": "Jubei", 
    "pClass": "samurai", 
    "pLevel" : "1"
    }


clear()
player_card()
