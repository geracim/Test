#!/usr/bin/env python3

import tkinter as tk
from tkinter import *

root = tk.Tk()
root.geometry("640x360+20+200") 

colours = ['1','2','3','4','5','6']

r = 0
for c in colours:
    Label(text=c, bg="#ffffff", relief=RIDGE, width=15).grid(row=r,column=0)
    Entry(bg="#ffffff", relief=SUNKEN, width=20).grid(row=r,column=1)
    r = r + 1

mainloop()