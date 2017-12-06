class sceneInstance:
    def __init__(self, static_data, dynamic_data, loc_hook, *args, **kwargs):
        self.static_data = static_data
        self.dynamic_data = dynamic_data
        self.loc_hook = loc_hook

    def onOpen(self, game):
        self.game = game
        self.node_id = 0
        self.display_text = ""
        self.temp_flags = {}
        self.traverseNodes()

    def onClose(self):
        pass

    def currentInstanceData(self):
        host_state = self.static_data.world_definition[self.dynamic_data.profile["current_state"]]
        return host_state["instances"][self.dynamic_data.profile["current_instance"]]

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
        self.dynamic_data.profile["game_flags"][flag_id] = True
        return 1

    def doDisplay(self, node_data):
        if "text" in node_data:
            if self.display_text:           
                self.display_text += "\n"
            self.display_text += self.loc_hook.translate(node_data["text"])
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
                options[key] = self.loc_hook.translate(key)

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
