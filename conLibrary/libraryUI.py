from fileinput import close
from maya import cmds
# if something is added or deleted, the libraryUI will hold onto the instance so it must be reloaded. Investigate the use of reload function with python 3, this solution doesn't work right now and is a bug that must be fixed
from importlib import reload
import conLibrary.controllerLibrary 
reload(conLibrary.controllerLibrary)
from PySide2 import QtWidgets, QtGui, QtCore
import pprint

class ControllerLibraryUI(QtWidgets.QDialog):
    """The ControllerLibrary is a dialog that lets us save and import controllers

    Args:
        QtWidgets (_type_): _description_
    """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle("Controller Library UI")
        # The library variable points to an instance of our conroller library
        self.library = ControllerLibrary()
        # Every time we create a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds the UI
        """
        # This is the master Layout
        layout = QtWidgets.QVBoxLayout(self)
        # This is the child horizontal widget
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton("Save")
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)
        # parameters for thumbnail size
        size = 150
        buffer = 12
        # This will create a grid list widget to display our controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)
        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton("Import")
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton("Refresh")
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)
        
        closeBtn = QtWidgets.QPushButton("Close")
        # self.close is defined in qtWidget
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """This clears the listWidget and then repopulates it with the contents of our library
        """
        self.listWidget.clear()
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

            item.setToolTip(pprint.pformat(info))

    def load(self):
        """This loads the currently selected controller
        """
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return
        
        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """This saves the controller with the given file name
        """
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return
        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

def showUI():
    """This shows and returns a hgandle to the ui

    Returns:
        _type_: _description_
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui
