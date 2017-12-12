#!/usr/bin/env python3

import tkinter as tk
from tkinter import *

root = tk.Tk()
image = tk.PhotoImage(file="mygif.gif")
label = tk.Label(image=image)
label.pack()
root.mainloop()
