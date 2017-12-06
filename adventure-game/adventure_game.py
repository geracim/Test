#!/usr/bin/env python3

import copy
import os
import sys
import time
import random
from engine import io, loc, animation, instance, game, calc

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
	locations = {}
	strings = {}
	
	scene_factory = {}

##########################################################################################

'''The AdventureGameApp inherits from gameBase (defined in engine/game.py) which in turn
inherits from tkinter's core (tkinter.Tk)

Under the hood, this class has support for managing the scene stack, loading in static
data, and low level ui creation / callback hooks
'''
class adventureGameApp(game.gameBase):
	
	def __init__(self):
		game.gameBase.__init__(self, staticData, io)

	def rebuildBasicUi(self, displayText, userOptions):
		self.clear()
		
		txtFrame = ttk.Frame(self, width=600, height=300).pack()
		ttk.Label(txtFrame, text=displayText).pack()
		
		btnFrame = ttk.Frame(self, width=600).pack()
		for command_key in userOptions:
			button = ttk.Button(
				btnFrame,
				text=userOptions[command_key],
				command=lambda i=command_key: self.getTopScene().onSelect(i))
			button.pack(side=tk.LEFT)

	def loadData(self, game_name):
		if not os.path.isdir(game_name):
			print('Could not find a game with the name: ' + game_name)
			exit()

		self.static_data.active_game = game_name

		self.loadDataElement('config')
		self.loadDataElement('strings', '_en')
		self.loadDataElement('locations')

		# Set up the dynamic profile with the supplied default profile in config
		dynamicData.profile = self.static_data.config['defaultProfile']

		# Load localization data
		loc.setup( self.static_data.strings, self.static_data, dynamicData )

##########################################################################################
########################################Scenes############################################
##########################################################################################

'''The Save scene plays a progress bar animation, then attempts to export the
current user's profile to a json save file

The bulk of this scene is defined in engine/animation.py, and only utilities
on scenes of this type must be implemented
'''
class sceneSave(animation.sceneAnimatingProgressBar):
	def generatePromptText(self):
	    return loc.translate('scene.save.open')

	def onFinishedAnimation(self):
	    # try saving the dynamicData.profile to a save file named for this game
	    save_file = staticData.active_game + '.sav'
	    if io.saveJsonToFile(save_file, dynamicData.profile):
	        self.game.system_response = loc.translate('scene.save.success')
	    else:
	        self.game.system_response = loc.translate('scene.save.failure')

staticData.scene_factory['save'] = lambda: sceneSave()

'''The Load scene plays a progress bar animation, then attempts to import saved
game json to replace the user's profile

The bulk of this scene is defined in engine/animation.py, and only utilities
on scenes of this type must be implemented
'''
class sceneLoad(animation.sceneAnimatingProgressBar):
	def generatePromptText(self):
	    return loc.translate('scene.load.open')

	def onFinishedAnimation(self):
		# try loading the dynamicData.profile from a save file named for this game
		# if it fails, the loadJsonFromFile function will return none
		save_file = staticData.active_game + '.sav'
		load_result = io.loadJsonFromFile( save_file )
		
		if load_result:
			dynamicData.profile = load_result
			self.game.system_response = loc.translate('scene.load.success')
		else:
			self.game.system_response = loc.translate('scene.load.failure')

staticData.scene_factory['load'] = lambda: sceneLoad()

'''An instance is a scene that walks through a set of scripted narrative choices
instances are defined on each area in the locations.py file

This type of scene is wholesale defined in engine/encounter.py
no local scene code is necessary
'''

staticData.scene_factory['instance'] = lambda: instance.sceneInstance(staticData, dynamicData, loc)

'''An encounter executes a battle between the user and an enemy configuration pulled
from the area, or another scripted source

The encounter will continue until reaching either a win or lose state, which will 
either return the user to the next highest scene on the stack, or trigger a load of the
most recent saved game
'''

class sceneEncounter:
	def onOpen(self, game):
		self.game = game
		area = staticData.locations[dynamicData.profile['current_state']]
		self.current_enemy_type = calc.pick_random_with_weights(area['encounter_types'])
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		display_text = 'You have started a ' + self.current_enemy_type + ' encounter'
		user_options = { 'w': 'Win', 'l': 'Lose' }
		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		if selection == 'w':
			self.game.system_response = 'You survived.'
			self.game.popScene()
		elif selection == 'l':
			self.game.system_response = 'You died.'
			self.game.resetSceneStack()
			self.game.pushScene('load')

staticData.scene_factory['encounter'] = lambda: sceneEncounter()

'''The Menu scene expose the system level actions to the user

(Saving the game, loading the saved game, and quitting)
'''
class sceneMenu:
	def onOpen(self, game):
		self.game = game
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		user_options = {'b': '<-', 's': 'Save', 'l': 'Load', 'q': 'Quit'}
		self.game.rebuildBasicUi("", user_options)

	def onSelect(self, selection):
		area = staticData.locations[dynamicData.profile['current_state']]
		if selection == 'b':
			self.game.popScene()
		elif selection == 's':
			self.game.popScene()
			self.game.pushScene('save')
		elif selection == 'l':
			self.game.popScene()
			self.game.pushScene('load')
		elif selection == 'q':
			self.game.destroy()

staticData.scene_factory['menu'] = lambda: sceneMenu()

'''The Travel scene shows other areas the user can travel to, allowing the
user to move around the 'map'
'''
class sceneTravel:
	def onOpen(self, game):
		self.game = game
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		user_options = {'b': '<-'}
		area = staticData.locations[dynamicData.profile['current_state']]

		for command in area['travel']:
			user_options[command] = loc.translate(command)

		self.game.rebuildBasicUi('', user_options)

	def onSelect(self, selection):
		area = staticData.locations[dynamicData.profile['current_state']]
		if selection == 'b':
			self.game.popScene()
		elif selection in area['travel']:
			dynamicData.profile['current_state'] = selection
			area = staticData.locations[selection]
			self.game.popScene()
			if 'encounter_rate' in area and random.randint(1, 100) < area['encounter_rate']:
				self.game.pushScene('encounter')

staticData.scene_factory['travel'] = lambda: sceneTravel()

'''The Location scene is the bottom level interaction scene, which all other
scenes are intended to build upon.  This scene should mostly serve as a first
menu, which mostly just opens other menus for the player to navigate
'''
class sceneLocation:
	def onOpen(self, game):
		self.game = game
		self.ui()

	def onClose(self):
		pass

	def ui(self):
		
		area = staticData.locations[dynamicData.profile['current_state']]
		
		# always display the "general" section of the explore info
		translated_area_text = loc.translate('scene.explore.info.general', area)
		display_text = self.game.flushSystemResponseAndAppend(translated_area_text)

		user_options = {'m': 'Menu'}
		explore_weights = {}
		if 'travel' in area and len(area['travel']) > 0:
			user_options['t'] = 'Travel'
		if 'instances' in area:
			for command in area['instances']:
				instance_data = area['instances'][command]
				if 'completionFlag' not in instance_data or instance_data['completionFlag'] not in dynamicData.profile['game_flags']:
					if 'canSelectDirectly' in instance_data and instance_data['canSelectDirectly']:
						user_options[command] = loc.translate(command)
					if 'exploreWeight' in instance_data and instance_data['exploreWeight'] > 0:
						explore_weights[command] = instance_data['exploreWeight']

		if len(explore_weights) > 0:
			explore_action = calc.pick_random_with_weights(explore_weights)
			user_options[explore_action] = 'Explore'

		self.game.rebuildBasicUi(display_text, user_options)

	def onSelect(self, selection):
		area = staticData.locations[dynamicData.profile['current_state']]
		if selection == 'm':
			self.game.pushScene('menu')
		elif selection == 't':
			self.game.pushScene('travel')
		elif 'instances' in area and selection in area['instances']:
			dynamicData.profile['current_instance'] = selection
			self.game.pushScene('instance')

staticData.scene_factory['location'] = lambda: sceneLocation()

##########################################################################################        
#######################################Core loop##########################################
##########################################################################################

if __name__ == '__main__':
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
