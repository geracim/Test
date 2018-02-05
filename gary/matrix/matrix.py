#!/usr/bin/env python3

import random
import time
import os
import sys

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class vars:
	play = False
	n = 1

def play():
	clear()

	play = input("Begin? Y/n \n> ").lower()

	if play == "y":
		play = True
		print("let's play!")
		while play == True:
			for vars.n in range(7,random.randint(8, 16)):
				bar = ("|" * vars.n)
				print((str(len(bar)) + ": " + bar))
				time.sleep(.25)
				vars.n += 1
	else:
		clear()
		print("Bye!")
		play = False	

play()