import tkinter as tk
from tkinter import ttk

class sceneAnimatingProgressBar:
    def onOpen(self, game):
        self.game = game

        self.game.clear()
        ttk.Label(text=self.generatePromptText()).pack()
        self.progressBar = ttk.Progressbar(
            self.game, orient="horizontal",
            length=400, mode="determinate")
        self.progressBar.pack()
        self.progressBar["value"] = 0
        self.progressBar["maximum"] = 100
        
        self.updateProgressBar()

    def onClose(self):
        pass

    def updateProgressBar(self):
        if self.progressBar["value"] < self.progressBar["maximum"]:
            self.progressBar["value"] += 5
            self.game.after(50, self.updateProgressBar)
        else:
            self.onFinishedAnimation()