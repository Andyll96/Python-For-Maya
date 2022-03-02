# from conLibrary import controllerLibrary as cl
# from importlib import reload

# reload(cl)

# lib = cl.ControllerLibrary()
# lib.save("trinity")
# lib.find()
# lib.load("trinity")
# # the lib object is a dictionary b/c it's class inherits from dictionary
# # the key is the file name, the value is the path
# # print(lib)
# #lib.load('test')

from conLibrary import libraryUI
from importlib import reload
reload(libraryUI)

libraryUI.showUI()