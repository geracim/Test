#!/usr/bin/env python3

import json
import re
import os
import time
import random

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
    active_game = "gary"
    config = {}
    world_definition = {}
    strings = {}

##########################################################################################
######################################Utility Functions###################################
##########################################################################################

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# takes an input string and runs it through the staticData strings for replacing
def localize(input_string):
    if input_string in staticData.strings:
        result = staticData.strings[input_string]
        # Um, regular expressions are a whole mess of bullshit, but this means:
        # "find all things inside {} and give me a list of them"
        substitutions = re.findall('\{([^}]+)\}', result)
        if substitutions:
            for matchKey in substitutions:
                # split the contained string within the braces into an array of keys
                replaceKeyComponents = matchKey.split('.')
                node = None
                # check if the first key is an attribute of either the staticData or dynamicData classes
                if hasattr(dynamicData, replaceKeyComponents[0]):
                    node = getattr(dynamicData, replaceKeyComponents[0])
                if hasattr(staticData, replaceKeyComponents[0]):
                    node = getattr(staticData, replaceKeyComponents[0])

                if node:
                    # remove the first item from the list
                    replaceKeyComponents.pop(0)
                    # walk the json object using the keys
                    for key in replaceKeyComponents:
                        if key in node:
                            node = node[key]
                        else:
                            node = None
                            break
                if node:
                    # replace the string
                    result = result.replace( "{" + matchKey + "}", str(node) )
        return result
    else:
        return "[" + input_string + "]"



# reads a file at a specified path and exports its contents to json
# returns json object if successful, None otherwise
def loadJsonFromFile(file_path):
    try:
        with open (file_path, 'r') as in_file:
            rawStringContents = in_file.read()
            return json.loads(rawStringContents)
    except:
        return None

# writes a file at a specified path filled with supplied json
# returns true if successful, false otherwise
def saveJsonToFile(file_path, json_object):
    try:
        with open (file_path, 'w') as out_file:
            # when using json."dump to string", indent=4 specifies tab spacing
            # this will result in a nicely formatted human readible file
            rawStringContents = json.dumps(json_object, indent=4)
            out_file.write(rawStringContents)
        result = True
    except:
        result = False
    return result

def loadData():
    # Load the config for the active game into staticData
    config_file_path = os.path.join(staticData.active_game, 'config.json')
    staticData.config = loadJsonFromFile(config_file_path)

    # Load the strings for the active game into staticData
    strings_file_path = os.path.join(staticData.active_game, 'strings_en.json')
    staticData.strings = loadJsonFromFile(strings_file_path)

    # Load the world definition for the active game into staticData
    world_definition_file_path = os.path.join(staticData.active_game, 'world_definition.json')
    staticData.world_definition = loadJsonFromFile(world_definition_file_path)

    # Set up the dynamic profile with the supplied default profile in config
    dynamicData.profile = staticData.config["defaultProfile"]

def changeScene( newScene ):
    if newScene != dynamicData.current_scene:
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
            print( localize("scene.save.open") )
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
            if saveJsonToFile(save_file, dynamicData.profile):
                dynamicData.system_response = localize("scene.save.success")
            else:
                dynamicData.system_response = localize("scene.save.failure")

            return sceneExplore()
        else:
            return self

##########################################################################################
class sceneLoad:
    t = 0

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def displayState(self):
        if self.t == 0:
            print( localize("scene.load.open") )
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
            load_result = loadJsonFromFile( save_file )
            
            if load_result:
                dynamicData.profile = load_result
                dynamicData.system_response = localize("scene.load.success")
            else:
                dynamicData.system_response = localize("scene.load.failure")
            return sceneExplore()

        else:
            return self

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
            return sceneExplore()
        elif command == "lose":
            dynamicData.system_response = "You died."
            return sceneLoad()

        return self

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
        
        if dynamicData.has_seen_menu == False:
            print("""~~~~~~~~~~~~ MENU ~~~~~~~~~~~~
|Hit Enter/Return to play.
|Enter 'l' to load a past game.
|Enter 's' to save your current game.
|Enter 'm' to show this menu again.
|Enter 'q' to quit without saving.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

        area = staticData.world_definition[dynamicData.profile["current_state"]]
        # This describes where the Hero is currently (the current state)
        print(area["description"])
        # This describes the Hero's options (possible state transitions)
        print("""~~~~~~~~~~~~ MAP ~~~~~~~~~~~~
From here you can travel to: {}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""".format(str(area["options"])))


    def requestInput(self):
        return input("What would you like to do?\n> ").lower()

    def respondToInput(self,command):
        dynamicData.has_seen_menu = True
        dynamicData.system_response = None
        area = staticData.world_definition[dynamicData.profile["current_state"]]

        if command == 'l':
            return sceneLoad()
        elif command == 's':
            return sceneSave()
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
                return sceneEncounter()

        return self

##########################################################################################        
#######################################Core loop##########################################
##########################################################################################

loadData()
changeScene( sceneExplore() )

while dynamicData.play == True:
    dynamicData.current_scene.displayState()
    command = dynamicData.current_scene.requestInput()
    changeScene( dynamicData.current_scene.respondToInput(command) )




