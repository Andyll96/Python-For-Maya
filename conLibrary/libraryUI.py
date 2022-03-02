from conLibrary.controllerLibrary import ControllerLibrary
from PySide2 import QtWidgets, QtGui, QtCore

class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui