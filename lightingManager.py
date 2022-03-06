from logging.config import valid_ident
from msilib.schema import Directory
from PySide2 import QtWidgets, QtGui, QtCore
import pymel.core as pm
from functools import partial
import json
import os
import time
# from maya import OpenMayaUI as omui

# from PyQt5 import Qt
# import logging

# logging.basicConfig()
# logger = logging.getLogger('LightingManager')
# logger.setLevel(logging.DEBUG)

# if Qt.__binding__ == 'Pyside':
#     logger.debug('Using PySide with Shiboken')
#     from shiboken import wrapInstance
#     from Qt.QtCore import Signal
# elif Qt.__binding__.startswith('PyQt'):
#     logger.debug('Using PyQt with sip')
#     from sip import wrapinstance as wrapInstance
#     from Qt.QtCore import pyqtSignal as Signal
# else:
#     logger.debug('Using PySide2 with Shiboken')
#     from shiboken2 import wrapInstance
#     from Qt.QtCore import Signal


class LightManager(QtWidgets.QDialog):

    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True)
    }

    def __init__(self):
        super(LightManager, self).__init__()
        self.setWindowTitle('Lighting Manager')
        self.buildUI()
        self.populate()

    def populate(self):
        lightWidgets = self.findChildren(LightWidget)
        print(lightWidgets)
        for widgets in lightWidgets:
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()

        for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight","volumeLight"]):
            self.addLight(light)


        # while self.scrollLayout.count():
        #     widget = self.scrollLayout.takeAt(0).widget()
        #     if widget:
        #         widget.setVisible(False)
        #         widget.deleteLater()

        #     for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight","volumeLight"]):
        #         self.addLight(light)

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)

        layout.addWidget(self.lightTypeCB, 0, 0, 1, 2)

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 2)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 3)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.saveLights)
        layout.addWidget(saveBtn, 2, 0)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.importLights)
        layout.addWidget(importBtn, 2, 1)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        layout.addWidget(refreshBtn, 2, 2)

    def saveLights(self):
        properties = {}
        for lightWidget in self.findChildren(LightWidget):
            light = lightWidget.light
            transform = light.getTransform()

            properties[str(transform)] = {
                'translate': list(transform.translate.get()),
                'rotation': list(transform.rotate.get()),
                'intensity': light.intensity.get(),
                'color': light.color.get(),
            }

        directory = self.getDirectory()

        lightFile = os.path.join(directory, f"lightFile_{time.strftime('%m%d')}.json")
        with open(lightFile, 'w') as f:
            json.dump(properties, f, indent=4)


    def getDirectory(self):
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory


    def importLights(self):
        directory = self.getDirectory()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Light Browser', directory)
        with open(fileName[0], 'r') as f:
            properties = json.load(f)
        
        for light, info in properties.items():
            lightType = info.get('lightType')
            for lt in self.lightTypes:
                if f"{lt.split()[0].lower()}Light" == lightType:
                    break
            else:
                print(f'Cannot find a corresponding light type for {light} ({lightType})')
                continue
            light = self.createLight(lightType=lt)
            light.intensity.set(info.get('intensity'))
            light.color.set(info.get('color'))
            transform = light.getTransform()
            transform.translate.set(info.get('translate'))
            transform.rotate.set(info.get('rotation'))
        self.populate()

    def createLight(self, lightType=None, add=True):
        if not lightType:
            lightType = self.lightTypeCB.currentText()
        lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]
        light = func()
        if add:
            self.addLight(light)

        return light

    def addLight(self, light):
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        lightWidgets = self.findChildren(LightWidget)
        # print(LightWidget)
        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)


class LightWidget(QtWidgets.QWidget):

    # if using PyQt, it'll be called pyqtSignal()
    onSolo = QtCore.Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()
        light = pm.PyNode(light)
        if isinstance(light, pm.nodetypes.Transform):
            light = light.getShape()

        self.light = light
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        # lambda is the same as writing
        # def setLightVisibility(val):
        #   self.light.visibility.set(val)
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        layout.addWidget(self.name, 0, 0)

        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        # Qt allows you to define your own signals
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0, 1)

        deleteBtn = QtWidgets.QPushButton(" X ")
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)

        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1)
        intensity.setMaximum(1000)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)

        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

    def setButtonColor(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(color) == 3, "You must provide a list of 3 colors"

        r,g,b = [c*255 for c in color]
        self.colorBtn.setStyleSheet(f'background-color: rgba({r},{g},{b}, 1.0)')

    def setColor(self):
        lightColor = self.light.color.get()
        color = pm.colorEditor(rgbValue=lightColor)
        r,g,b,a = [float(c) for c in color.split()]
        color = (r,g,b)
        self.light.color.set(color)
        self.setButtonColor(color)
        
    def disableLight(self, value):
        self.name.setChecked(not value)

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.light.getTransform())

def showUI():
    ui = LightManager()
    ui.show()
    return ui