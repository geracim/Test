#!/usr/bin/env python3

import copy
import os
import random
import sys
import time

from engine import io, loc, animation

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
	current_scene = None
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

	def changeScene(self, new_scene_id):
		if self.current_scene != None:
			self.current_scene.onClose()
		# get the scene factory for the specified id, and call it to create a new scene
		self.current_scene = staticData.sceneFactory[new_scene_id]()
		self.current_scene.onOpen(self)

	def clear(self):
		for widget in self.pack_slaves():
			widget.destroy()
	
	def rebuildBasicUi(self, displayText, userOptions):
		self.clear()
		
		txtFrame = ttk.Frame(self, width=600, height=300).pack()
		ttk.Label(txtFrame, text=displayText).pack()
		
		btnFrame = ttk.Frame(self, width=600).pack()
		for commandKey in userOptions:
			button = ttk.Button(
				btnFrame,
				text=userOptions[commandKey],
				command=lambda i=commandKey: self.current_scene.onSelect(i))
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
	    self.game.changeScene(staticData.config["defaultScene"])

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
		self.game.changeScene(staticData.config["defaultScene"])

staticData.sceneFactory['load'] = lambda: sceneLoad()

##########################################################################################
class sceneEncounter:
	def onOpen(self, game):
		self.game = game
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
			self.game.changeScene('explore')
		elif selection == 'l':
			dynamicData.system_response = "You died."
			self.game.changeScene('load')

staticData.sceneFactory['encounter'] = lambda: sceneEncounter()

##########################################################################################
class sceneInstance:
	def __init__(self, dynamic_data, *args, **kwargs):
		self.dynamic_data = dynamic_data

	def onOpen(self, game):
		self.game = game
		self.node_id = 0
		self.display_text = ""
		self.temp_flags = {}
		self.traverseNodes()

	def onClose(self):
		pass

	def currentInstanceData(self):
		host_state = staticData.world_definition[dynamicData.profile["current_state"]]
		return host_state["instances"][dynamicData.profile["current_instance"]]

	def currentNodeData(self):
		instance_data = self.currentInstanceData()
		if self.node_id >= len(instance_data["nodes"]):
			return None
		else:
			return instance_data["nodes"][self.node_id]

	def getTemp(self, id):
		if id in self.temp_flags:
			return self.temp_flags[id]
		else:
			return False
	def setTemp(self, id, value):
		self.temp_flags[id] = bool(value)

	def getFlag(self, id): 
		dy_d = self.dynamic_data.profile["game_flags"]
		if id in dy_d:
			return dy_d[id]
		else:
			return False
	def setFlag(self, id, value): 
		dy_d = self.dynamic_data.profile["game_flags"]
		dy_d[id] = bool(value)

	def getNumber(self, id): 
		dy_d = self.dynamic_data.profile["game_numbers"]
		if id in dy_d:
			return dy_d[id]
		else:
			return 0
	def setNumber(self, id, value): 
		dy_d = self.dynamic_data.profile["game_numbers"]
		dy_d[id] = int(value)

	def getString(self, id): 
		dy_d = self.dynamic_data.profile["game_strings"]
		if id in dy_d:
			return dy_d[id]
		else:
			return ""
	def setString(self, id, value): 
		dy_d = self.dynamic_data.profile["game_strings"]
		dy_d[id] = str(value)

	def skip(self, amount):
		self.node_id += amount

	def traverseNodes(self):
		node_data = self.currentNodeData()
		if not node_data:
			self.dynamic_data.system_response = self.display_text
			self.game.changeScene('explore')
		else:
			try:
				function = getattr(self, "do" + node_data["type"])
			except:
				print("ERROR: could not execute node of this type: " + str(node_data))
				self.game.destroy()
				return
			finally:
				result = function(node_data)
				if result > 0:
					self.node_id += result
					self.traverseNodes()

	def doMarkCompleted(self, node_data):
		instance_data = self.currentInstanceData()
		if "completionFlag" not in instance_data:
			print("ERROR: instance wants to MarkCompleted, but has no completion flag: " + str(instance_data))
			self.game.destroy()
			return 0
		flag_id = instance_data["completionFlag"]
		dynamicData.profile["game_flags"][flag_id] = True
		return 1

	def doDisplay(self, node_data):
		if "text" in node_data:
			if self.display_text:			
				self.display_text += "\n"
			self.display_text += loc.translate(node_data["text"])
		return 1

	def doChoice(self, node_data):
		options = {}
		if "options" not in node_data:
			print("ERROR: instance has choice node with no choices: " + str(node_data))
			self.game.destroy()
			return 0

		for key in node_data["options"]:
			option_data = node_data["options"][key]
			# if a key has a condition, only add it when condition is met
			if "condition" not in option_data or eval(option_data["condition"]):
				options[key] = loc.translate(key)

		self.game.rebuildBasicUi(self.display_text, options)
		self.display_text = ""
		return 0

	def onSelect(self, selection):
		node = self.currentNodeData()
		option_data = node["options"][selection]

		if "action" in option_data:
			exec(option_data["action"])

		self.node_id += 1
		self.traverseNodes()

staticData.sceneFactory['instance'] = lambda: sceneInstance(dynamicData)

##########################################################################################
class sceneExplore:
	def onOpen(self, game):
		self.game = game
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		display_text = ""
		if dynamicData.system_response:
			display_text += dynamicData.system_response + "\n"
		
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		
		# always display the "general" section of the explore info
		display_text += loc.translate("scene.explore.info.general", area)

		user_options = {"q": "Quit", "l": "Load", "s": "Save"}
		for command in area["options"]:
			user_options[command] = loc.translate(command)
		for command in area["instances"]:
			instance_data = area["instances"][command]
			if "completionFlag" not in instance_data or instance_data["completionFlag"] not in dynamicData.profile["game_flags"]:
				if instance_data["mode"] == "selectable":
					user_options[command] = loc.translate(command)
		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		area = staticData.world_definition[dynamicData.profile["current_state"]]
		if selection == 'l':
			self.game.changeScene('load')
		elif selection == 's':
			self.game.changeScene('save')
		elif selection == 'q':
			self.game.destroy()
		elif selection in area["options"]:
			dynamicData.profile["current_state"] = selection
			area = staticData.world_definition[selection]
			if random.randint(1, 100) < area["encounter_rate"]:
				enemyTypeIndex = random.randint(0, len(area["enemy_types"])-1)
				enemyType = area["enemy_types"][enemyTypeIndex]
				dynamicData.profile["current_enemy_type"] = enemyType["id"]
				dynamicData.profile["current_enemy_level"] = random.randint(enemyType["levelRange"][0], enemyType["levelRange"][1])
				self.game.changeScene('encounter')
			else:
				self.ui()
		elif selection in area["instances"]:
			dynamicData.profile["current_instance"] = selection
			self.game.changeScene('instance')

staticData.sceneFactory['explore'] = lambda: sceneExplore()

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
	app.changeScene( staticData.config["defaultScene"] )

	# start game core
	app.mainloop()
