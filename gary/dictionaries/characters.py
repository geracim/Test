#!/usr/bin/env python3

import os
import sys
import time

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

##############
# DICTIONARY #
##############

Samurai = {	
			"health": {"20", "35"},
			"armor": {"medium", "heavy"}, 
			"weapon": {"1h_sword", "2h_sword", "spear", "bow"}
			}


print("Samurai: " + Samurai)