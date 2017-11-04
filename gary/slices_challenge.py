#!/usr/bin/env python3

# Create a new variable named slice1 that has the  
# second, third, and fourth items from favorite_things.

# given:

def challenge1():

	favorite_things = ['raindrops on roses', 'whiskers on kittens', 'bright copper kettles',
	                   'warm woolen mittens', 'bright paper packages tied up with string',
	                   'cream colored ponies', 'crisp apple strudels']

	slice1 = favorite_things[1:4]
	print("slice 1: {}\n".format(slice1))

	# OK, let's do another test. 
	# Get the last two items from favorite_things and put them into slice2.

	slice2 = favorite_things[5:7]
	print("slice 2: {}\n".format(slice2))

	# Make a copy of favorite_things and name it sorted_things.
	# Then use .sort() to sort sorted_things.

	sorted_things = favorite_things[:]
	sorted_things.sort()
	print("sorted copy of favorite things: {}\n".format(sorted_things))

def challenge2():
	



challenge2()