#!/usr/bin/env python3

import random
import time

class bools:
    earthquake_bool = False
    fire_bool = False
    flood_bool = False

class chance:
	earthquake_chance = 1
	fire_chance = 5
	flood_chance = 2

class roll:
	earthquake_roll: 0
	fire_roll: 0
	flood_roll: 0

def play():
	earthquake()
	fire()
	flood()

	if bools.earthquake_bool == True:
		print("There was an earthquake!")
	elif bools.fire_bool == True:
		print("There was a fire!")
	elif bools.flood_bool == True:
		print("There was a flood!")
	else:
		print("Nothing happened.")

def earthquake():
	# "earthquake" is the roll for liklihood that the earthquakeearthquake weighted event will occur.
	roll.earthquake_roll = random.randint(1,100)

	if roll.earthquake_roll > chance.earthquake_chance:
		bools.earthquake_bool = True
	else:
		bools.earthquake_bool = False

#	print("earthquake roll: " + str(roll.earthquake_roll))
#	print("earthquake chance: " + str(chance.earthquake_chance))
#	print("earthquake bool: " + str(bools.earthquake_bool))

def fire():
	roll.fire_roll = random.randint(1,100)

	if roll.fire_roll > chance.fire_chance:
		bools.fire_bool = True
	else:
		bools.fire_bool = False

#	print("fire roll: " + str(roll.fire_roll))
#	print("fire chance: " + str(chance.fire_chance))
#	print("fire bool: " + str(bools.fire_bool))

def flood():
	roll.flood_roll = random.randint(1,100)

	if roll.flood_roll > chance.flood_chance:
		bools.flood_bool = True
	else:
		bools.flood_bool = False

#	print("flood roll: " + str(roll.flood_roll))
#	print("flood chance: " + str(chance.flood_chance))
#	print("flood bool: " + str(bools.flood_bool))

while True:   
	play()
	t = 0
	for t in range(0,3):
		print(".")
		time.sleep(0.3)
		t += 1 

