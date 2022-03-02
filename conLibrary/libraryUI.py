from fileinput import close
from conLibrary.controllerLibrary import ControllerLibrary
from PySide2 import QtWidgets, QtGui, QtCore

class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle("Controller Library UI")
        self.library = ControllerLibrary()
        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton("Save")
        saveLayout.addWidget(saveBtn)

        self.listWidget = QtWidgets.QListWidget()
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton("Import")
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton("Refresh")
        btnLayout.addWidget(refreshBtn)
        
        closeBtn = QtWidgets.QPushButton("Close")
        btnLayout.addWidget(closeBtn)

    def populate(self):
        pass

def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui
