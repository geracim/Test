#!/usr/bin/env python3

import random
import sys
import json
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load(source_file):
    result = []
    try:
        with open (source_file, 'r') as in_file:
            rawStringContents = in_file.read()
            result = json.loads(rawStringContents)
    except:
        print("error loading source json")
    return result

def pick_random_with_weights(option_list):
    # tally up the total roll by summing all the weight values
    total = sum( item["weight"] for item in option_list )
    roll = random.randint(0, total-1)

    result = ""
    # loop through each id/weight item
    for item in option_list:
        # deduct this weighting from the roll
        roll -= item["weight"]
        # if this deduction drops us to zero, then this is our result
        if roll < 0:
            result = item["id"]
            break

    return result


def main():
    clear()

    if len(sys.argv) > 1:
        roll_count = int(sys.argv[1])
    else:
        roll_count = 1000

    # load in the json data
    option_list = load('probs.json')

    # throw the dice a fuckton of times, and tally the results
    counts = {}
    for t in range(roll_count):

    	random_choice = pick_random_with_weights(option_list)
    	if not random_choice in counts:
    		counts[random_choice] = 1
    	else:
    		counts[random_choice] += 1

    # display the result of rolls
    for item in counts:
        percent = 100 * (counts[item] / roll_count)
        formatted_percent = '%.2f' % percent + "%"
        print(item + ": " + formatted_percent)

if __name__ == "__main__":
    main()

