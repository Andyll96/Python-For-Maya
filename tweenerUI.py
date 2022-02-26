from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):

    # If obj isn't give and selection is set to False, error early
    if not obj and not selection:
        raise ValueError("No object given to tween")
    # If no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]
    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)
    #print(f"{obj},{attrs}")

    currentTime = cmds.currentTime(query=True)

    for attr in attrs:

        #construct the full name of the attribute with its object
        attrFull = f"{obj}.{attr}"
        # Get the keyframes of the attribute on this object
        keyframes = cmds.keyframe(attrFull, query=True)
        # If there are no keyframes, then continue
        if not keyframes:
            continue

        previousKeyframes = []
        for frame in keyframes:
            if frame < currentTime:
                previousKeyframes.append(frame)

        # list comprehension version of the previouse statements
        # read: for frame in keyframes, if frame > currentTime add frame into the list
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
            previousFrame = max(previousKeyframes)
        else:
            previousFrame = None
        
        # "List" comprehension
        nextFrame = min(laterKeyframes) if laterKeyframes else None

        # print(f"previousFrame: {previousFrame}")
        # print(f"nextFrame: {nextFrame}")
        
        if not previousFrame or not nextFrame:
            continue

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        difference = nextValue - previousValue
        weightedDifference = (difference * percentage / 100.0)
        currentValue = previousValue + weightedDifference

        cmds.setKeyfram(attrFull, time=currentTime, value=currentValue)

class TweenWindow(object):
    windowName = "TweenerWindow"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        self.buildUI()
        cmds.window(self.windowName)
        cmds.showWindow()

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

    def close(self, *args):
        cmds.deleteUI(self.windowName)

# tween(12, selection=False)
tweenerUi = TweenWindow()
tweenerUi.show()