from lib2to3.pytree import Base
from maya import cmds
from tweenerUI import tween
from gearClassCreator import Gear

class BaseWindow(object):
    windowName = "BaseWindow"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        self.buildUI()
        cmds.window(self.windowName)
        cmds.showWindow()

    def buildUI(self):
        pass

    # maya buttons send an extra argument to the command functions, we don't care about theses extra arguments therefore we just use *args to capture it
    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)

class TweenerUI(BaseWindow):
    windowName = "Tweener Window"

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    # maya buttons send an extra argument to the command functions, we don't care about theses extra arguments therefore we just use *args to capture it
    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)

class GearUI(BaseWindow):
    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        row = cmds.rowLayout(numberOfColumns=4)
        self.label = cmds.text(label="10")
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)
        self.gear = Gear()
        self.gear.createGear(teeth=teeth)



    def modifyGear(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)