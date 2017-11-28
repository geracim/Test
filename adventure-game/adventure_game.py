#!/usr/bin/env python3

import json
import os
import time
import random

play = True
##########################################################################################
#################################### Model & Data ########################################
##########################################################################################

class stateVars:
    current_state = "Cambria"
    has_seen_menu = False
    system_response = None
    current_scene = None
    current_enemy_type = None
    current_enemy_level = None
    enemy_types = None


##########################################################################################

class staticData:
    world_definitions = {}
    save_file_name = "adventure_game_save.txt"

##########################################################################################
######################################Utility Functions###################################
##########################################################################################

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def saveState():
    try:
        with open (staticData.save_file_name,"w") as out_file:
            out_file.write(stateVars.current_state)
        result = True
    except:
        result = False
    return result

def loadState():
    try: 
        with open (staticData.save_file_name,"r") as in_file:
            stateVars.current_state = in_file.readline()
        result = True  
    except:
        result = False
    return result

def loadData():
    with open ('adventure_game_states.txt', 'r') as in_file:
        rawStringContents = in_file.read()
        staticData.world_definitions = json.loads(rawStringContents)

def changeScene( newScene ):
    if newScene != stateVars.current_scene:
        if stateVars.current_scene != None:
            stateVars.current_scene.onClose()
        stateVars.current_scene = newScene
        stateVars.current_scene.onOpen()

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
            print("Trying to remember our meeting place for next time.")
        else:
            print(".")        

    def requestInput(self):
        framerate = 3.0
        time.sleep(1 / framerate)
        return None

    def respondToInput(self,command):
        self.t += 1
        if self.t > 5:
            if saveState():
                stateVars.system_response = "I'll remember this as the last place we met!"
            else:
                stateVars.system_response = "I couldn't find you, adventurer."

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
            print("Let's see... where did we last meet?")
        else:
            print(".")

    def requestInput(self):
        framerate = 3.0
        time.sleep(1 / framerate)
        return None

    def respondToInput(self,command):
        self.t += 1
        if self.t > 5:
            if loadState():
                stateVars.system_response = "Ah, I found you, adventurer.\nWe left off at the {}.".format(stateVars.current_state)
            else:
                stateVars.system_response = "Hmm... Have we met before, adventurer?\nIf this is the first time, please enter 's' to have me remember this meeting spot."
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
        print("You are being attacked by a " + stateVars.current_enemy_type)
        print("your choices: " + str(self.actions) )

    def requestInput(self):
        return input("What would you like to do?\n> ")

    def respondToInput(self,command):
        if command == 'win':
            stateVars.system_response = "You survived."
            return sceneExplore()
        elif command == "lose":
            stateVars.system_response = "You died."
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
        if stateVars.system_response:
            print(stateVars.system_response)
        
        if stateVars.has_seen_menu == False:
            print("""~~~~~~~~~~~~ MENU ~~~~~~~~~~~~
|Hit Enter/Return to play.
|Enter 'l' to load a past game.
|Enter 's' to save your current game.
|Enter 'm' to show this menu again.
|Enter 'q' to quit without saving.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

        # This describes where the Hero is currently (the current state)
        print(staticData.world_definitions[stateVars.current_state]["description"])
        # This describes the Hero's options (possible state transitions)
        print("""~~~~~~~~~~~~ MAP ~~~~~~~~~~~~
From here you can travel to: {}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""".format(str(staticData.world_definitions[stateVars.current_state]["options"])))


    def requestInput(self):
        return input("What would you like to do?\n> ").lower()

    def respondToInput(self,command):
        stateVars.has_seen_menu = True
        stateVars.system_response = None
        area = staticData.world_definitions[stateVars.current_state]

        if command == 'l':
            return sceneLoad()
        elif command == 's':
            return sceneSave()
        elif command == 'q':
            global play
            play = False
        elif command == 'm':
            stateVars.has_seen_menu = False
        elif command in area["options"]:
            stateVars.current_state = command
            destination = staticData.world_definitions[command]
            if random.randint(1, 100) < destination["encounter_rate"]:
                enemyTypeIndex = random.randint(0, len(destination["enemy_types"])-1)
                enemyType = destination["enemy_types"][enemyTypeIndex]
                stateVars.current_enemy_type = enemyType["id"]
                stateVars.current_enemy_level = random.randint(enemyType["levelRange"][0], enemyType["levelRange"][1])
                return sceneEncounter()

        return self

##########################################################################################        
#######################################Core loop##########################################
##########################################################################################

loadData()
changeScene( sceneExplore() )

while play == True:
    stateVars.current_scene.displayState()
    command = stateVars.current_scene.requestInput()
    changeScene( stateVars.current_scene.respondToInput(command) )




