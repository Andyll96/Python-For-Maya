from copyreg import constructor
from msilib.schema import Component
from maya import cmds

def createGear(teeth=10, length=0.3):
    """This function will create a gear with the given parameters

    Args:
        teeth (int, optional): The number of teeth to create. Defaults to 10.
        length (float, optional): The length of the teeth. Defaults to 0.3.

    Returns:
        _type_: A tuple of the transform, constructor and extrude node
    """

    # Teeth are every alternate face, so spans * 2
    # spans are the number of faces on the side of the cylinder
    spans = teeth * 2

    # creates cylinder with that many faces
    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    # this grabs the faces on the side of the cylinder that we want
    sideFaces = range(spans*2, spans*3, 2)

    # clears any selection already made
    cmds.select(clear=True)

    # selects the required faces
    for face in sideFaces:
        # the add parameter will add the new face selection to the total selection, so that way we aren't selecting just one face
        cmds.select(f"{transform}.f[{face}]", add=True)

    # extrudes faces
    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    # the transform node gives transform/positional data
    # the constructor node gives attributes such as subdivisions
    # the extrude node gives extrude settings
    return transform, constructor, extrude

def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth * 2

    # edits the existing cylinder by passing it the constructor of the existing cylinder
    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    # gets every other side face on the new cylinder
    sideFaces = range(spans*2, spans*3, 2)
    print(f"sideFaces: {sideFaces}")
    faceNames = []

    for face in sideFaces:
        faceName = f"f[{face}]"
        faceNames.append(faceName)

    print(f"faceNames: {faceNames}")
    
    cmds.setAttr(f"{extrude}.inputComponents", len(faceNames), *faceNames, type="componentList")

    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length)


transform, constructor, extrude = createGear()
# you can't just change the subdivisions in the constructor node, the extrude node won't know how to react. Therefore you have to change both 
changeTeeth(constructor, extrude, teeth=40)