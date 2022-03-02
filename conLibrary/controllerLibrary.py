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
    
    # *info will pass in a tuple, **info will pass in a dictionary
    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        createDirectory()

        path = os.path.join(directory, f"{name}.ma")
        infoFile = os.path.join(directory,f"{name}.json")

        info['name'] = name
        info['path'] = path

        # rename the file to what we want it to be saved as
        cmds.file(rename=path)

        # If something is selected, we only export the selection, otherwise we save the whole file
        if cmds.ls(selection=True):
            cmds.file(force=True, type="mayaAscii", exportSelected=True)
        else:
            cmds.file(save=True, type="mayaAscii", force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)  

        self[name] = info
        
        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)


    def find(self, directory=DIRECTORY):
        if not os.path.exists(directory):
            return
        
        files = os.listdir(directory) 
        mayaFiles = [f for f in files if f.endswith(".ma")]
        #print(mayaFiles)

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            # path = os.path.join(directory, ma)

            infoFile = f"{name}.json"
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)
        
                with open(infoFile, 'r') as f:
                    data = json.load(f)
                    # pprint.pprint(info)
            else:
                # print("no info found")
                data = {}

            screenshot = f"{name}.jpg"        
            if screenshot in files:
                data['screenshot'] = os.path.join(directory, screenshot)

            data['name'] = name
            data['path'] = os.path.join(directory, ma)

            # remember that this class is a dictionary 
            self[name] = data

        pprint.pprint(self)

    def load(self, name):
        path = self[name]['path']
        # i is for import
        cmds.file(path,i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, f"{name}.jpg")
        cmds.viewFit()
        # you can figure this out through the MEL commands when you go to the Maya render settings and set the File Output, Image Format to JPEG
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        # showOrnaments is maya overlays 
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200, showOrnaments=False, startTime=1, endTime=1, viewer=False)
        return path