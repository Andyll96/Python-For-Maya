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
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    # this grabs the faces on the side of the cylinder that we want
    sideFaces = range(spans*2, spans*3, 2)

    # clears any selection already made
    cmds.select(clear=True)

    for face in sideFaces:
        # the add parameter will add the new face selection to the total selection, so that way we aren't selecting just one face
        cmds.select(f"{transform}.f[{face}]", add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return transform, constructor, extrude

createGear()