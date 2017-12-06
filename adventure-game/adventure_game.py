#!/usr/bin/env python3

import copy
import os
import sys
import time
import random
from engine import io, loc, animation, instance, game

import tkinter as tk
from tkinter import ttk

##########################################################################################
#################################### Model & Data ########################################
##########################################################################################

class dynamicData:
	profile = {}

##########################################################################################

class staticData:
	active_game = None
	config = {}
	world_definition = {}
	strings = {}
	sceneFactory = {}

##########################################################################################

class adventureGameApp(game.gameBase):
	
	def __init__(self):
		game.gameBase.__init__(self, staticData, io)

	def rebuildBasicUi(self, displayText, userOptions):
		self.clear()
		
		txtFrame = ttk.Frame(self, width=600, height=300).pack()
		ttk.Label(txtFrame, text=displayText).pack()
		
		btnFrame = ttk.Frame(self, width=600).pack()
		for commandKey in userOptions:
			button = ttk.Button(
				btnFrame,
				text=userOptions[commandKey],
				command=lambda i=commandKey: self.getTopScene().onSelect(i))
			button.pack(side=tk.LEFT)

	def loadData(self, game_name):
		if not os.path.isdir(game_name):
			print("Could not find a game with the name: " + game_name)
			exit()

		self.static_data.active_game = game_name

		self.loadDataElement('config')
		self.loadDataElement('strings', '_en')
		self.loadDataElement('world_definition')

		# Set up the dynamic profile with the supplied default profile in config
		dynamicData.profile = self.static_data.config["defaultProfile"]

		# Load localization data
		loc.setup( self.static_data.strings, self.static_data, dynamicData )

##########################################################################################
########################################Scenes############################################
##########################################################################################

class sceneSave(animation.sceneAnimatingProgressBar):
	def generatePromptText(self):
	    return loc.translate("scene.save.open")

	def onFinishedAnimation(self):
	    # try saving the dynamicData.profile to a save file named for this game
	    save_file = staticData.active_game + ".sav"
	    if io.saveJsonToFile(save_file, dynamicData.profile):
	        self.game.system_response = loc.translate("scene.save.success")
	    else:
	        self.game.system_response = loc.translate("scene.save.failure")

staticData.sceneFactory['save'] = lambda: sceneSave()

##########################################################################################
class sceneLoad(animation.sceneAnimatingProgressBar):
	def generatePromptText(self):
	    return loc.translate("scene.load.open")

	def onFinishedAnimation(self):
		# try loading the dynamicData.profile from a save file named for this game
		# if it fails, the loadJsonFromFile function will return none
		save_file = staticData.active_game + ".sav"
		load_result = io.loadJsonFromFile( save_file )
		
		if load_result:
			dynamicData.profile = load_result
			self.game.system_response = loc.translate("scene.load.success")
		else:
			self.game.system_response = loc.translate("scene.load.failure")

staticData.sceneFactory['load'] = lambda: sceneLoad()

##########################################################################################
class sceneEncounter:
	def onOpen(self, game):
		self.game = game
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		enemyTypeIndex = random.randint(0, len(area["enemy_types"])-1)
		enemyType = area["enemy_types"][enemyTypeIndex]
		self.current_enemy_type = enemyType["id"]
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		display_text = "You are being attacked by a " + self.current_enemy_type
		user_options = { 'w': 'Win', 'l': 'Lose' }
		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		if selection == 'w':
			self.game.system_response = "You survived."
			self.game.popScene()
		elif selection == 'l':
			self.game.system_response = "You died."
			self.game.resetSceneStack()
			self.game.pushScene('load')

staticData.sceneFactory['encounter'] = lambda: sceneEncounter()

##########################################################################################

staticData.sceneFactory['instance'] = lambda: instance.sceneInstance(staticData, dynamicData, loc)

##########################################################################################
class sceneLocation:
	def onOpen(self, game):
		self.game = game
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		
		# always display the "general" section of the explore info
		translated_area_text = loc.translate("scene.explore.info.general", area)
		display_text = self.game.flushSystemResponseAndAppend(translated_area_text)

		user_options = {"q": "Quit", "l": "Load", "s": "Save"}
		if "options" in area:
			for command in area["options"]:
				user_options[command] = loc.translate(command)
		if "instances" in area:
			for command in area["instances"]:
				instance_data = area["instances"][command]
				if "completionFlag" not in instance_data or instance_data["completionFlag"] not in dynamicData.profile["game_flags"]:
					if instance_data["mode"] == "selectable":
						user_options[command] = loc.translate(command)
		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		if selection == 'l':
			self.game.pushScene('load')
		elif selection == 's':
			self.game.pushScene('save')
		elif selection == 'q':
			self.game.destroy()
		elif "options" in area and selection in area["options"]:
			dynamicData.profile["current_state"] = selection
			area = staticData.world_definition[selection]
			if random.randint(1, 100) < area["encounter_rate"]:
				self.game.pushScene('encounter')
			else:
				self.ui()
		elif "instances" in area and selection in area["instances"]:
			dynamicData.profile["current_instance"] = selection
			self.game.pushScene('instance')

staticData.sceneFactory['location'] = lambda: sceneLocation()

##########################################################################################        
#######################################Core loop##########################################
##########################################################################################

if __name__ == "__main__":
	app = adventureGameApp()
	
	# if the script was run with a command line argument, load that game
	if len(sys.argv) > 1:
		app.loadData(sys.argv[1])
	# if no arguments are supplied, default to gary data
	else:
		app.loadData('gary')

	# load the default scene as specified in the game config
	app.resetSceneStack()

	# start game core
	app.mainloop()
