from maya import cmds

def createGear(teeth=10, length=0.3):

    # Teeth are every alternate face, so spans * 2
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    # this grabs the faces on the side of the cylinder that we want
    sideFaces = range(spans*2, spans*3, 2)

    for face in sideFaces:
        # the add parameter will add the new face selection to the total selection, so that way we aren't selecting just one face
        cmds.select(f"{transform}.f[{face}]", add=True)

createGear()