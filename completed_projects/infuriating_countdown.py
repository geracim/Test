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
			for vars.n in range(7,random.randint(8, 46)):
				bar = (' ' * (20-vars.n) + '|' * (vars.n*2+1))
				if vars.n < 10:
					print("0" + (str(len(bar)) + ": " + bar))
				else:
					print((str(len(bar)) + ": " + bar))
				time.sleep(.25)
				vars.n += 1
	else:
		clear()
		print("Bye!")
		play = False

play()