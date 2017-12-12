#!/usr/bin/env python3

import tkinter as tk
import random

root = tk.Tk()
# width x height + x_offset + y_offset:
root.geometry("1920x1080+50+50") 
     
languages = ['Choice 1','Choice 2','Choice 3','Choice 4','Choice 5']
labels = range(5)
for i in range(5):
   ct = [random.randrange(256) for x in range(3)]
   brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
   ct_hex = "%02x%02x%02x" % tuple(ct)
   bg_colour = '#' + "".join(ct_hex)
   l = tk.Label(root, 
                text=languages[i], 
                fg='White' if brightness < 120 else 'Black', 
                bg=bg_colour)
   l.place(x = 80, y = 80 + i*30, width=120, height=25)
root.lift ()
          
root.mainloop()