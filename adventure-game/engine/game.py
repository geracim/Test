import os

import tkinter as tk

class gameBase(tk.Tk):
    scene_stack = []
    static_data = None
    io_hook = None
    system_response = ""

    def __init__(self, static_data, io_hook, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.io_hook = io_hook
        self.static_data = static_data

    def loadDataElement(self, element, file_extra_tag=""):
        config_file_path = os.path.join(self.static_data.active_game, element + file_extra_tag + '.json')
        data = self.io_hook.loadJsonFromFile(config_file_path)
        if not data:
            print("The \"" + self.static_data.active_game + "\" game has broken " + element + " data")
            exit()
        setattr(self.static_data, element, data)

    def getTopScene(self):
        if len(self.scene_stack) > 0:
            return self.scene_stack[-1]
        else:
            return None

    def pushScene(self, scene_type_id):
        new_scene = self.static_data.sceneFactory[scene_type_id]()
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
        self.pushScene(self.static_data.config["defaultScene"])

    def clear(self):
        for widget in self.pack_slaves():
            widget.destroy()
    
    def flushSystemResponseAndAppend(self, text):
        result = ""
        if self.system_response:
            result += self.system_response + "\n"
            self.system_response = ""

        result += text
        return result
