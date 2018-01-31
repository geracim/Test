#!/usr/bin/env python3

import random
import time
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class vars:
	play = True
	n = 1

def run():
	while vars.play == True:
		clear()
		random_num = random.randint(1, 100)
		print("Run number: {}\n________".format(vars.n))
		if random_num > 5:
			vars.t = 0
			for vars.t in range(1,random_num):
				print(str(random_num-vars.t) + ": " + (random_num-vars.t)*"*")
				time.sleep(0.13)
				vars.t += 1
		else:
			print("quit on {} after {} runs.".format(random_num,vars.n))
			vars.play = False
		vars.n += 1

run()