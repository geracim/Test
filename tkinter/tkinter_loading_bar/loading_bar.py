#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # When you click start, the loading start(self) function runs
        self.button = ttk.Button(text="Load", command=self.start)
        self.button.pack()
        # When you click reset, the reset(self) function runs
        self.button = ttk.Button(text="Reset", command=self.reset)
        self.button.pack()
        # This draws the progress bar & determines the size & orientation
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack()

        self.bytes = 0
        self.maxbytes = 0

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 100
        self.progress["maximum"] = 100
        self.read_bytes()

    def reset(self):
        self.progress["value"] = 0
        self.maxbytes = 100
        self.bytes = 0

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 5
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(8, self.read_bytes)

app = SampleApp()
app.mainloop()