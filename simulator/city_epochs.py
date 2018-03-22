#!/usr/bin/env python3

import random
import time
import os
import sys

class counters:
	epoch_counter = 0
	earthquake_counter = 0
	fire_counter = 0
	flood_counter = 0
	plague_counter = 0
	current_pop = 200

class bools:
    earthquake_bool = False
    fire_bool = False
    flood_bool = False
    plague_bool = False

class constants:
	earthquake_constant = 2
	earthquake_dmg = 0
	fire_constant = 8
	fire_dmg = 0
	flood_constant = 6
	flood_dmg = 0
	plague_constant = .01
	plague_dmg = 0

class rolls:
	epoch_roll: 0
	pop_gain: 0
	earthquake_roll: 0
	fire_roll: 0
	flood_roll: 0
	plague_roll: 0

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def epoch():
	rolls.epoch_roll = random.randint(1,50)

def earthquake():
	rolls.earthquake_roll = random.randint(1,100)

	if rolls.earthquake_roll > constants.earthquake_constant:
		bools.earthquake_bool = True
	else:
		bools.earthquake_bool = False

def fire():
	rolls.fire_roll = random.randint(1,100)

	if rolls.fire_roll > constants.fire_constant:
		bools.fire_bool = True
	else:
		bools.fire_bool = False

def flood():
	rolls.flood_roll = random.randint(1,100)

	if rolls.flood_roll > constants.flood_constant:
		bools.flood_bool = True
	else:
		bools.flood_bool = False

def plague():
	rolls.plague_roll = random.randint(1,100)

	if rolls.plague_roll > constants.plague_constant:
		bools.plague_bool = True
	else:
		bools.plague_bool = False

def new_pop():
	rolls.pop_gain = random.randint(10,80)

def dmg_roll():
	constants.earthquake_dmg = random.randint(10, 80)
	constants.fire_dmg = random.randint(1, 100)
	constants.flood_dmg = random.randint(15, 50)
	constants.plague_dmg = random.randint(1, counters.current_pop)
	

def run():
	earthquake()
	fire()
	flood()
	new_pop()
	dmg_roll()

	t = 0
	for t in range(0,5):
		print(".")
		time.sleep(0.8)
		t += 1

# ================================================
	print("\n=======================================")
	print("current century: " + str(counters.epoch_counter + 1))
	print("epoch length: " + str(rolls.epoch_roll))
	print("current population: " + str(counters.current_pop))
	if counters.epoch_counter > 0:
		print("new citizens: " + str(rolls.pop_gain))
		counters.current_pop += rolls.pop_gain
#///// DEBUG ////////////
#	print("-----------------------\n")
#	print("earthquake roll: " + str(rolls.earthquake_roll) + "/" + str(constants.earthquake_constant))
#	print("fire roll: " + str(rolls.fire_roll) + "/" + str(constants.fire_constant))
#	print("flood roll: " + str(rolls.flood_roll) + "/" + str(constants.flood_constant))
#	print("plague roll: " + str(rolls.plague_roll) + "/" + str(constants.plague_constant))
#///// DEBUG ////////////
	print("=======================================\n")
# ================================================
	if bools.earthquake_bool == True:
#		print("Earthquake: Yes")
		print("Earthquake: {} casualties\n".format(constants.earthquake_dmg))
		counters.current_pop -= 20
		counters.earthquake_counter += 1
		bools.earthquake_bool = False
	else:
		print("Earthquake: No casualties.\n")
# ================================================
	if bools.fire_bool == True:
#		print("Fire: Yes")
		print("Fire: {} casualties\n".format(constants.fire_dmg))
		counters.current_pop -= 15
		counters.fire_counter += 1
		bools.fire_bool = False
	else:
		print("Fire: No casualties.\n")
# ================================================
	if bools.flood_bool == True:
#		print("Flood: Yes")
		print("Flood: {} casualties\n".format(constants.flood_dmg))
		counters.current_pop -= 30
		counters.flood_counter += 1
		bools.flood_bool = False
	else:
		print("Flood: No casualties.\n")
# ================================================
	if bools.plague_bool == True:
#		print("Plague: Yes")
		print("Plague: {} casualties\n".format(constants.plague_dmg))
		counters.current_pop -= 30
		counters.plague_counter += 1
		bools.plague_bool = False
	else:
		print("Plague: No casualties.\n")
# ================================================

def play():
	epoch()

	while counters.current_pop > 0 and counters.epoch_counter < rolls.epoch_roll:
		run()
		counters.epoch_counter += 1

	if counters.epoch_counter > 1:
		print("The City survived for {} centuries.".format(counters.epoch_counter))
	elif counters.epoch_counter == 1:
		print("The City survived for {} century.".format(counters.epoch_counter))
	else:
		print("Epic Fail.")

clear()
play()

