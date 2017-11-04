#!/usr/bin/env python3

sodas = ["Pepsi", "Cherry Coke", "Sprite"]
chips = ["Doritos", "Fritos", "Cheetohs"]
candy = ["Snickers", "Twix", "Twizzlers"]

while True:
	choice = input("Would you like Soda, Chips, or Candy?\n> ").lower()
	try:
		if choice == 'soda':
			snack = sodas.pop()
		elif choice == 'chips':
			snack = chips.pop()
		elif choice == 'candy':
			snack = candy.pop()
		else:
			print("Didn't get that... try again!")
			continue
	except IndexError:
		print("Sorry, we're all out of {}!".format(choice))
	print("Here's your {}: {}".format(choice, snack))