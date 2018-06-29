#!/usr/bin/env python3

import os
import sys
import time

class states:
    # run top row
    runTier1 = False
    # run middle row
    runTier2 = False
    # run bottom row
    runTier3 = False
    # select row
    tierSelect = ""
    # power state
    power = "off"
    # power switch
    powerSelector = ""

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def exit():
    timer()
    sys.exit()

def timer():
    t = 0
    for t in range(0,5):
        print(".")
        time.sleep(0.3)
    t += 1

def powerSwitch():
    while states.power == "off":
        clear()
        try:
            states.powerSelector = str(input("Power is Off. Turn on power? (y/N)\n> ")).lower()
        except:
            states.powerSelector = str(input("Power is Off. Turn on power? (y/N)\n> ")).lower()

        if states.powerSelector == "y":
            states.power = "on"
            clear()
            print("Power is on.")
            # insert wait here
            sprinkleStatus()
        else:
            clear()
            print("Closing Sprinkler System...")
            states.runTier1 = False
            states.runTier2 = False
            states.runTier3 = False
            exit()
    
def selector():
    try:
        states.tierSelect = str(input("Enter tier: 1, 2, or 3 to toggle individually.\nEnter 'all' to toggle all tiers.\nEnter 'q' to quit.\n> ")).lower()
    except:
        print("Error. Please try again.")
        states.tierSelect = str(input("Enter tier: 1, 2, or 3 to toggle individually.\nEnter 'all' to toggle all tiers.\nEnter 'q' to quit.\n> ")).lower()

    if states.tierSelect == "1":
        if states.runTier1 != True:
            states.runTier1 = True
            clear()
            print("Tier 1 watering.\n")
        else:
            states.runTier1 = False
    elif states.tierSelect == "2":
        if states.runTier2 != True:
            states.runTier2 = True
            clear()
            print("Tier 2 watering.\n")
        else:
            states.runTier2 = False
    elif states.tierSelect == "3":
        if states.runTier3 != True:
            states.runTier3 = True
            clear()
            print("Tier 3 watering.\n")
        else:
            states.runTier3 = False
    elif states.tierSelect == "all":
        if states.runTier1 != True and states.runTier2 != True and states.runTier3 != True:
            states.runTier1 = True
            states.runTier2 = True
            states.runTier3 = True
        else:
            states.runTier1 = False
            states.runTier2 = False
            states.runTier3 = False
    elif states.tierSelect == "status":
        sprinkleStatus()
    elif states.tierSelect == "q":
        states.power = "off"
    else:
        print("wtf? how'd i get here?!")


def sprinkleStatus():
    clear()
    print("|   Sprinkler Status   ")
    print("|______________________")
    print("| tier 1 state: " + str(states.runTier1) + "  |")
    print("| tier 2 state: " + str(states.runTier2) + "  |")
    print("| tier 3 state: " + str(states.runTier3) + "  |")
    print("|======================\n")


while True:
    powerSwitch()
    sprinkleStatus()
    selector()
