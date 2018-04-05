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
    manual_bool = False

class constants:
	earthquake_chance = 0.01
	earthquake_dmg = 0
	fire_chance = 0.04
	fire_dmg = 0
	flood_chance = 0.02
	flood_dmg = 0
	plague_chance = 0.4
	plague_dmg = 0

class rolls:
	epoch_roll: 100
	pop_gain: 0
	earthquake_roll: 0
	fire_roll: 0
	flood_roll: 0
	plague_roll: 0

class choice:
	choice_manual = ""

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def epoch():
	rolls.epoch_roll = random.randint(1,50)

def earthquake():
	rolls.earthquake_roll = random.randint(1,100)

	if rolls.earthquake_roll > (100*(constants.earthquake_chance)):
		bools.earthquake_bool = True
	else:
		bools.earthquake_bool = False

def fire():
	rolls.fire_roll = random.randint(1,100)

	if rolls.fire_roll > (100*(constants.fire_chance)):
		bools.fire_bool = True
	else:
		bools.fire_bool = False

def flood():
	rolls.flood_roll = random.randint(1,100)

	if rolls.flood_roll > (100*(constants.flood_chance)):
		bools.flood_bool = True
	else:
		bools.flood_bool = False

def plague():
	rolls.plague_roll = random.randint(1,(100*(constants.plague_chance)))

	if rolls.plague_roll > constants.plague_chance:
		bools.plague_bool = True
	else:
		bools.plague_bool = False

def new_pop():
	rolls.pop_gain = random.randint(10,80)

def dmg_roll():
	constants.earthquake_dmg = random.randint(10, 80)
	constants.fire_dmg = random.randint(1, 100)
	constants.flood_dmg = random.randint(15, 50)
	constants.plague_dmg = random.randint(counters.current_pop, 150)

def run():

	t = 0
	for t in range(0,5):
		print(".")
		time.sleep(0.6)
		t += 1

# ================================================
	print("\n=======================================")
	print("current century: {}".format(counters.epoch_counter + 1))
	print("epoch length: {}".format(rolls.epoch_roll))
	print("current population: {}".format(counters.current_pop))
	if counters.epoch_counter > 0:
		print("new citizens: {}".format(rolls.pop_gain))
		counters.current_pop += rolls.pop_gain
#///// DEBUG ////////////
#	print("-----------------------\n")
#	print("earthquake roll: " + str(rolls.earthquake_roll) + "/" + str(constants.earthquake_chance))
#	print("fire roll: " + str(rolls.fire_roll) + "/" + str(constants.fire_chance))
#	print("flood roll: " + str(rolls.flood_roll) + "/" + str(constants.flood_chance))
#	print("plague roll: " + str(rolls.plague_roll) + "/" + str(constants.plague_chance))
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

	print("Total: {} casualties.".format(constants.earthquake_dmg + constants.fire_dmg + constants.flood_dmg + constants.plague_dmg))

def play():
	epoch()
	print("Welcome to the City simulator. This tool is intended \nas a fun & simple test of 'Minimum viable population'. \nEnter a starting population, a number of ticks in centuries (Epoch), \nand see if your City survives.\n")
	choice.manual = input("(M)anual or (A)uto?\n> ").lower()
	if choice.manual == "m" or choice.manual == "manual":
		counters.current_pop = int(input("Enter a starting population. (Minimum viable population)\n> "))
		rolls.epoch_roll = int(input("Enter an epoch length in centuries. (number of ticks)\n> "))

		while counters.current_pop > 0 and counters.epoch_counter < rolls.epoch_roll:
			earthquake()
			fire()
			flood()
			plague()
			new_pop()
			dmg_roll()	

			run()
			counters.epoch_counter += 1

	elif choice.manual == "a" or choice.manual == "auto":		
		
		while counters.current_pop > 0 and counters.epoch_counter < rolls.epoch_roll:
			earthquake()
			fire()
			flood()
			plague()
			new_pop()
			dmg_roll()	

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

