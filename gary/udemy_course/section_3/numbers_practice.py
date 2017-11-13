#!/usr/bin/env python3

x = "Hello World"
#  ["A","b","c","d","e","F","g","h","I","j","k","l","m","n","o","p","q","r","s","t","U","v","w","x","y","z"]


for y in x:
	print(x)
	if y.lower() == "a":
		x.remove(y)
	elif y.lower() == "e":
		x.remove(y)
	elif y.lower() == "i":
		x.remove(y)
	elif y.lower() == "o":
		x.remove(y)
	elif y.lower() == "u":
		x.remove(y)
	else:
		print(x)