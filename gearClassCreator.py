from maya import cmds

class Gear(object):
    """This is a Gear object that lets us create and modify a gear

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.transform = None
        self.extrude = None
        self.constructor = None

    def createGear(self, teeth=10, length=0.3):
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)
        sideFaces = range(spans*2, spans*3, 2)

        cmds.select(clear=True)
        # selects the required faces
        for face in sideFaces:
            # the add parameter will add the new face selection to the total selection, so that way we aren't selecting just one face
            cmds.select(f"{self.transform}.f[{face}]", add=True)

        # extrudes faces
        extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
        # the transform node gives transform/positional data
        # the constructor node gives attributes such as subdivisions
        # the extrude node gives extrude settings
        return self.transform, self.constructor, extrude

    def changeTeeth(self, teeth=10, length=0.3):
        spans = teeth * 2

        # edits the existing cylinder by passing it the constructor of the existing cylinder
        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        # gets every other side face on the new cylinder
        sideFaces = range(spans*2, spans*3, 2)
        print(f"sideFaces: {sideFaces}")
        faceNames = []

        for face in sideFaces:
            faceName = f"f[{face}]"
            faceNames.append(faceName)

        print(f"faceNames: {faceNames}")
        
        cmds.setAttr(f"{self.extrude}.inputComponents", len(faceNames), *faceNames, type="componentList")

        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)