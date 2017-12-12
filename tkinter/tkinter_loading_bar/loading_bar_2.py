#!/usr/bin/env python3

import time
import sys


def loadPercent():
    for i in range(100):
        time.sleep(.25)
        sys.stdout.write("\r%d%%" % i)
        sys.stdout.flush()

loadPercent()
print("\n")