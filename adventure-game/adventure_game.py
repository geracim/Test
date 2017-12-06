#!/usr/bin/env python3

import copy
import os
import random
import sys
import time

from engine import io, loc, animation, instance

import tkinter as tk
from tkinter import ttk

##########################################################################################
#################################### Model & Data ########################################
##########################################################################################

class dynamicData:
	profile = {}
	system_response = None
	play = True

##########################################################################################

class staticData:
	active_game = None
	config = {}
	world_definition = {}
	strings = {}
	sceneFactory = {}

##########################################################################################

class adventureGameApp(tk.Tk):
	scene_stack = []
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

	def getTopScene(self):
		if len(self.scene_stack) > 0:
			return self.scene_stack[-1]
		else:
			return None

	def pushScene(self, scene_type_id):
		new_scene = staticData.sceneFactory[scene_type_id]()
		self.scene_stack.append(new_scene)
		new_scene.onOpen(self)

	def popScene(self):
		if len(self.scene_stack) > 0:
			self.getTopScene().onClose()
			self.scene_stack = self.scene_stack[:-1]
			if len(self.scene_stack) > 0:
				ui_update_call = getattr(self.getTopScene(), "ui", None)
				if ui_update_call is not None:
					self.getTopScene().ui()
		else:
			raise "ERROR: Attempt to pop with no scenes"

	def clearSceneStack(self):
		while len(self.scene_stack):
			self.popScene()

	def resetSceneStack(self):
		self.clearSceneStack()
		self.pushScene(staticData.config["defaultScene"])

	def clear(self):
		for widget in self.pack_slaves():
			widget.destroy()
	
	def flushSystemResponseAndAppend(self, text):
		result = ""
		if dynamicData.system_response:
			result += dynamicData.system_response + "\n"
			dynamicData.system_response = ""

		result += text
		return result

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

	def loadDataElement(self, element, file_extra_tag=""):
		config_file_path = os.path.join(staticData.active_game, element + file_extra_tag + '.json')
		data = io.loadJsonFromFile(config_file_path)
		if not data:
			print("The \"" + staticData.active_game + "\" game has broken " + element + " data")
			exit()
		setattr(staticData, element, data)

	def loadData(self, game_name):
		if not os.path.isdir(game_name):
			print("Could not find a game with the name: " + game_name)
			exit()

		staticData.active_game = game_name

		self.loadDataElement('config')
		self.loadDataElement('strings', '_en')
		self.loadDataElement('world_definition')

		# Set up the dynamic profile with the supplied default profile in config
		dynamicData.profile = staticData.config["defaultProfile"]

		# Load localization data
		loc.setup( staticData.strings, staticData, dynamicData )

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
	        dynamicData.system_response = loc.translate("scene.save.success")
	    else:
	        dynamicData.system_response = loc.translate("scene.save.failure")

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
			dynamicData.system_response = loc.translate("scene.load.success")
		else:
			dynamicData.system_response = loc.translate("scene.load.failure")

staticData.sceneFactory['load'] = lambda: sceneLoad()

##########################################################################################
class sceneEncounter:
	def onOpen(self, game):
		self.game = game
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		enemyTypeIndex = random.randint(0, len(area["enemy_types"])-1)
		enemyType = area["enemy_types"][enemyTypeIndex]
		dynamicData.profile["current_enemy_type"] = enemyType["id"]
		dynamicData.profile["current_enemy_level"] = random.randint(enemyType["levelRange"][0], enemyType["levelRange"][1])
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		display_text = "You are being attacked by a " + dynamicData.profile["current_enemy_type"]
		user_options = { 'w': 'Win', 'l': 'Lose' }
		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		if selection == 'w':
			dynamicData.system_response = "You survived."
			self.game.popScene()
		elif selection == 'l':
			dynamicData.system_response = "You died."
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
