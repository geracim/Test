#!/usr/bin/env python3

import os

x = [1, 2, 3, 4, 5, 6]

def first_4(x):
    return x[:4:]

def first_and_last_4(x):
    return x[:4:] + x[-4::]

def odds(x):
    return x[1::2]

def reverse_evens(x):
	if len(x) % 2 == 0:
		return x[-2::-2]
	else:
		return x[::-2]


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


clear()
print(first_4())

# Want to get 9, 7, 5, 3