from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
# print(userAppDir)
#uses the os to create this new path appropriatley
DIRECTORY = os.path.join(USERAPPDIR, "controllerLibrary")

def createDirectory(directory=DIRECTORY):
    """Creates the given directory if it doesn't exist already

    Args:
        directory (str, optional): The directory to create. Defaults to DIRECTORY.
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class ControllerLibrary(dict):
    
    def save(self, name, directory=DIRECTORY):
        createDirectory()
        path = os.path.join(directory, f"{name}.ma")
        cmds.file(rename=path)
        if cmds.ls(selection=True):
            cmds.file(force=True, type="mayaAscii", exportSelected=True)
        else:
            cmds.file(save=True, type="mayaAscii", force=True)

    def find(self, directory=DIRECTORY):
        if not os.path.exists(directory):
            return
        
        files = os.listdir(directory) 
        mayaFiles = [f for f in files if f.endswith(".ma")]
        print(mayaFiles)

        for ma in mayaFiles:
            name, ext = os.path.splittext(ma)
            path = os.path.join(directory, ma)

            # remember that this class is a dictionary 
            self[name] = path

        pprint.pprint(self)