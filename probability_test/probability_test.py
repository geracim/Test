#!/usr/bin/env python3

import random
import time
import json
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class state:
	play = True
	t = 1
	jsonList = []
	num_runs = 10000
	object_weight = 100

def load():
    try:
        with open ('probs.json', 'r') as in_file:
            rawStringContents = in_file.read()
            state.jsonList = json.loads(rawStringContents)
    except:
    	print("error")

def run():
	# load from json file
	load()
	
	return random.randint(0, len(state.jsonList)-1)

	# print a specific thing for debugging
	# print(state.jsonList[0]["weight"])

clear()
counts = {}

while state.t < state.num_runs:
	random_choice = run()
	if not random_choice in counts:
		counts[random_choice] = 1
	else:
		counts[random_choice] += 1
	state.t += 1

print(counts)


"""

((state.jsonList[random_choice]["weight"]) * 10)

"""
