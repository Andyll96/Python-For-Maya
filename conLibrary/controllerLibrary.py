from maya import cmds
import os
import json
#import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
# print(userAppDir)
#uses the os to create this new path appropriatley
DIRECTORY = os.path.join(USERAPPDIR, "controllerLibrary")

def createDirectory(directory=DIRECTORY):
    """Creates the given directory if it doesn't exist already

    Args:
        directory (str, optional): The directory to create. Defaults to DIRECTORY.
    """
    if not os.path.exists(directory)
        os.mkdir(directory)