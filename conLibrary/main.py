from conLibrary import controllerLibrary as cl
reload(controllerLibrary)

lib = cl.ControllerLibrary()
# lib.save("test")
lib.find()
# the lib object is a dictionary b/c it's class inherits from dictionary
# the key is the file name, the value is the path
print(lib)