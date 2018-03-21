#!/usr/bin/env python3

import random
import time
import os
import sys

t = 0

class counters:
	epoch_counter = 0
	earthquake_counter = 0
	fire_counter = 0
	flood_counter = 0
	health_counter = 200

class bools:
    earthquake_bool = False
    fire_bool = False
    flood_bool = False

class chance:
	earthquake_chance = 20
	fire_chance = 30
	flood_chance = 10

class rolls:
	epoch_roll: 0
	earthquake_roll: 0
	fire_roll: 0
	flood_roll: 0

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def run():
	earthquake()
	fire()
	flood()
# ================================================
	print("\n=======================================")
	print("current century: " + str(counters.epoch_counter + 1))
	print("epoch length: " + str(rolls.epoch_roll))
	print("current health: " + str(counters.health_counter))
#	print("-----------------------\n")
#	print("earthquake roll: " + str(rolls.earthquake_roll) + "/" + str(chance.earthquake_chance))
#	print("fire roll: " + str(rolls.fire_roll) + "/" + str(chance.fire_chance))
#	print("flood roll: " + str(rolls.flood_roll) + "/" + str(chance.flood_chance))
	print("=======================================\n")
# ================================================
	if bools.earthquake_bool == True:
		print("Earthquake: Yes")
		print("-20 health\n")
		counters.health_counter -= 20
		counters.earthquake_counter += 1
		bools.earthquake_bool = False
	else:
		print("Earthquake: No\n")
# ================================================
	if bools.fire_bool == True:
		print("Fire: Yes")
		print("-15 health\n")
		counters.health_counter -= 15
		counters.fire_counter += 1
		bools.fire_bool = False
	else:
		print("Fire: No\n")
# ================================================
	if bools.flood_bool == True:
		print("Flood: Yes")
		print("-30 health\n")
		counters.health_counter -= 30
		counters.flood_counter += 1
		bools.flood_bool = False
	else:
		print("Flood: No\n")
# ================================================
	
	counters.health_counter += 25
	print("\n25 new people were born this year\n")

	t = 0
	for t in range(0,5):
		print(".")
		time.sleep(0.8)
		t += 1

def epoch():
	rolls.epoch_roll = random.randint(1,50)

def earthquake():
	rolls.earthquake_roll = random.randint(1,100)

	if rolls.earthquake_roll > chance.earthquake_chance:
		bools.earthquake_bool = True
	else:
		bools.earthquake_bool = False

def fire():
	rolls.fire_roll = random.randint(1,100)

	if rolls.fire_roll > chance.fire_chance:
		bools.fire_bool = True
	else:
		bools.fire_bool = False


def flood():
	rolls.flood_roll = random.randint(1,100)

	if rolls.flood_roll > chance.flood_chance:
		bools.flood_bool = True
	else:
		bools.flood_bool = False


def play():
	epoch()

	while rolls.epoch_roll > counters.epoch_counter:
		run()
		counters.epoch_counter += 1
		if counters.health_counter <= 0:
			break
		else:
			continue		

	if counters.health_counter <= 0:
		print("Your city did not survive {} centuries.".format(rolls.epoch_roll))
	else:
		print("Your city lasted through {} centuries.".format(rolls.epoch_roll))


clear()
play()

