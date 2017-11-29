#!/usr/bin/env python3

import os
import random
import sys
import time

from engine import io, loc

##########################################################################################
#################################### Model & Data ########################################
##########################################################################################

class dynamicData:
    profile = {}
    has_seen_menu = False
    system_response = None
    current_scene = None
    play = True


##########################################################################################

class staticData:
    active_game = None
    config = {}
    world_definition = {}
    strings = {}
    sceneFactory = {}

##########################################################################################
######################################Utility Functions###################################
##########################################################################################

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def loadDataElement( element, file_extra_tag="" ):
    config_file_path = os.path.join(staticData.active_game, element + file_extra_tag + '.json')
    data = io.loadJsonFromFile(config_file_path)
    if not data:
        print("The \"" + staticData.active_game + "\" game has broken " + element + " data")
        exit()
    setattr(staticData, element, data)


def loadData( game_name ):
    if not os.path.isdir(game_name):
        print("Could not find a game with the name: " + game_name)
        exit()

    staticData.active_game = game_name

    loadDataElement('config')
    loadDataElement('strings', '_en')
    loadDataElement('world_definition')

    # Set up the dynamic profile with the supplied default profile in config
    dynamicData.profile = staticData.config["defaultProfile"]

def changeScene( new_scene_id ):
    # get the scene factory for the specified id, and call it to create a new scene
    newScene = staticData.sceneFactory[new_scene_id]()

    if dynamicData.current_scene != None:
        dynamicData.current_scene.onClose()
    dynamicData.current_scene = newScene
    dynamicData.current_scene.onOpen()

##########################################################################################
########################################Scenes############################################
##########################################################################################

class sceneSave:
    t = 0

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def displayState(self):
        if self.t == 0:
            print( loc.translate("scene.save.open") )
        else:
            print(".")        

    def requestInput(self):
        framerate = 3.0
        time.sleep(1 / framerate)
        return None

    def respondToInput(self,command):
        self.t += 1
        if self.t > 5:
            # try saving the dynamicData.profile to a save file named for this game
            save_file = staticData.active_game + ".sav"
            if io.saveJsonToFile(save_file, dynamicData.profile):
                dynamicData.system_response = loc.translate("scene.save.success")
            else:
                dynamicData.system_response = loc.translate("scene.save.failure")

            return staticData.config["defaultScene"]
        else:
            return None

staticData.sceneFactory['save'] = lambda: sceneSave()

##########################################################################################
class sceneLoad:
    t = 0

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def displayState(self):
        if self.t == 0:
            print( loc.translate("scene.load.open") )
        else:
            print(".")

    def requestInput(self):
        framerate = 3.0
        time.sleep(1 / framerate)
        return None

    def respondToInput(self,command):
        self.t += 1
        if self.t > 5:
            # try loading the dynamicData.profile from a save file named for this game
            # if it fails, the loadJsonFromFile function will return none
            save_file = staticData.active_game + ".sav"
            load_result = io.loadJsonFromFile( save_file )
            
            if load_result:
                dynamicData.profile = load_result
                dynamicData.system_response = loc.translate("scene.load.success")
            else:
                dynamicData.system_response = loc.translate("scene.load.failure")
            return staticData.config["defaultScene"]

        else:
            return None

staticData.sceneFactory['load'] = lambda: sceneLoad()

##########################################################################################
class sceneEncounter:
    actions = [ "win", "lose" ]

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def displayState(self):
        print("You are being attacked by a " + dynamicData.profile["current_enemy_type"])
        print("your choices: " + str(self.actions) )

    def requestInput(self):
        return input("What would you like to do?\n> ")

    def respondToInput(self,command):
        if command == 'win':
            dynamicData.system_response = "You survived."
            return 'explore'
        elif command == "lose":
            dynamicData.system_response = "You died."
            return 'load'

        return None

staticData.sceneFactory['encounter'] = lambda: sceneEncounter()

##########################################################################################
class sceneExplore:

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def displayState(self):
        clear()
        if dynamicData.system_response:
            print(dynamicData.system_response)
        
        area = staticData.world_definition[dynamicData.profile["current_state"]]

        # optionally display the "help" section of the explore info
        if dynamicData.has_seen_menu == False:
            print(loc.translate("scene.explore.info.help", area))

        # always display the "general" section of the explore info
        print(loc.translate("scene.explore.info.general", area))


    def requestInput(self):
        return input(loc.translate("scene.explore.prompt")).lower()

    def respondToInput(self,command):
        dynamicData.has_seen_menu = True
        dynamicData.system_response = None
        area = staticData.world_definition[dynamicData.profile["current_state"]]

        if command == 'l':
            return 'load'
        elif command == 's':
            return 'save'
        elif command == 'q':
            dynamicData.play = False
        elif command == 'm':
            dynamicData.has_seen_menu = False
        elif command in area["options"]:
            dynamicData.profile["current_state"] = command
            destination = staticData.world_definition[command]
            if random.randint(1, 100) < destination["encounter_rate"]:
                enemyTypeIndex = random.randint(0, len(destination["enemy_types"])-1)
                enemyType = destination["enemy_types"][enemyTypeIndex]
                dynamicData.profile["current_enemy_type"] = enemyType["id"]
                dynamicData.profile["current_enemy_level"] = random.randint(enemyType["levelRange"][0], enemyType["levelRange"][1])
                return 'encounter'

        return None

staticData.sceneFactory['explore'] = lambda: sceneExplore()

##########################################################################################        
#######################################Core loop##########################################
##########################################################################################

# if the script was run with a command line argument, load that game
if len(sys.argv) > 1:
    loadData(sys.argv[1])
# if no arguments are supplied, default to gary data
else:
    loadData('gary')

loc.setup( staticData.strings, staticData, dynamicData )

# load the default scene as specified in the game config
changeScene( staticData.config["defaultScene"] )

# main loop
while dynamicData.play == True:
    dynamicData.current_scene.displayState()
    command = dynamicData.current_scene.requestInput()
    newScene = dynamicData.current_scene.respondToInput(command)
    if newScene:
        changeScene( newScene )




