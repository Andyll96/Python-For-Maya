from maya import cmds

# this will also print DAG objects
# print(cmds.ls())

# this will list the current selection
# print(cmds.ls(selection=True))

selection = cmds.ls(selection=True)

if len(selection) == 0:
    # dag parameter will list only objects in the outliner that's not hidden
    # long parameter will give full path of object to avoid duplicate errors
    selection = cmds.ls(dag=True, long=True)
    
# we need to sort the selection list by length with the children objects first, b/c if parent name is changed then path to children will change    
selection.sort(key=len, reverse=True)

# gives the short name for each object in the selection list derived from it's path
for obj in selection:
    shortName = obj.split("|")[-1]
    
    # maya represents shapes as a transform, right click in outliner to show shape
    # print(cmds.objectType(obj))
    
    # we do this in order to get the children of the transform which is the object
    children = cmds.listRelatives(obj, children=True, fullPath=True) or []
    # print(children)
    
    if len(children) == 1:
        child = children[0]
        objType = cmds.objectType(child) 
    else:
        objType = cmds.objectType(obj)
    # print(objType)
    
    if objType == "mesh":
        suffix = "geo"
    elif objType == "joint":
        suffix = "jnt"
    elif objType == "camera":
        print("Skipping camera")
        continue
    else:
        suffix = "grp"
        
    newName = shortName + "_" + suffix
    # print(newName)
    
    cmds.rename(obj, newName)