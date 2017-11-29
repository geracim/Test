#!/usr/bin/env python3

import json
import os
import random
import re
import sys
import time

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

# takes an input string and runs it through the staticData strings for replacing
def localize(input_string, localData=None):
    if input_string in staticData.strings:
        result = staticData.strings[input_string]

        # if result is not a string, assume its a list of strings and join them into a newline delimited string
        if not isinstance( result, str ):
            result = '\n'.join(result)

        # Um, regular expressions are a whole mess of bullshit, but this means:
        # "find all things inside {} and give me a list of them"
        substitutions = re.findall('\{([^}]+)\}', result)
        if substitutions:
            for matchKey in substitutions:
                # split the contained string within the braces into an array of keys
                replaceKeyComponents = matchKey.split('.')
                node = None
                # check if the first key is an attribute of either the staticData or dynamicData classes
                firstKey = replaceKeyComponents[0]
                if firstKey in localData:
                    node = localData[firstKey]
                elif hasattr(dynamicData, firstKey):
                    node = getattr(dynamicData, firstKey)
                elif hasattr(staticData, firstKey):
                    node = getattr(staticData, firstKey)

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

def loadData( game_name ):
    if not os.path.isdir(game_name):
        print("Could not find a game with the name: " + game_name)
        exit()

    staticData.active_game = game_name

    # Load the config for the active game into staticData
    config_file_path = os.path.join(staticData.active_game, 'config.json')
    staticData.config = loadJsonFromFile(config_file_path)
    if not staticData.config:
        print("The \"" + game_name + "\" game has broken config data")
        exit()

    # Load the strings for the active game into staticData
    strings_file_path = os.path.join(staticData.active_game, 'strings_en.json')
    staticData.strings = loadJsonFromFile(strings_file_path)
    if not staticData.strings:
        print("The \"" + game_name + "\" game has broken strings data")
        exit()

    # Load the world definition for the active game into staticData
    world_definition_file_path = os.path.join(staticData.active_game, 'world_definition.json')
    staticData.world_definition = loadJsonFromFile(world_definition_file_path)
    if not staticData.world_definition:
        print("The \"" + game_name + "\" game has broken world_definition data")
        exit()

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
            print(localize("scene.explore.info.help", area))

        # always display the "general" section of the explore info
        print(localize("scene.explore.info.general", area))


    def requestInput(self):
        return input(localize("scene.explore.prompt")).lower()

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

# load the default scene as specified in the game config
changeScene( staticData.config["defaultScene"] )

# main loop
while dynamicData.play == True:
    dynamicData.current_scene.displayState()
    command = dynamicData.current_scene.requestInput()
    newScene = dynamicData.current_scene.respondToInput(command)
    if newScene:
        changeScene( newScene )




