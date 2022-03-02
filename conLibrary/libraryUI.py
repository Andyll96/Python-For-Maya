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

        size = 150
        buffer = 12
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
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
        self.library.find()

        # self.library is a dictionary
        for name, info in self.library.items():
            # print(name, info)
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get("screenshot")
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui
