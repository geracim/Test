#!/usr/bin/env python3

import sys
import time


def search_replace():
    t = 0
    for t in range(0,5):
        print(".")
        time.sleep(0.3)
        t += 1    

    file = open("file.txt", "r")
    
    print(file)
    file.close()

search_replace()