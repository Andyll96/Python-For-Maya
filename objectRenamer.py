from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"

def rename(selection=False):
    """This function will rename any objects to have the correct suffix

    Args:
        selection (bool, optional): Whether or not we use the current selection. Defaults to False.

    Raises:
        RuntimeError: Checks to see if there's an object that is selected

    Returns:
        list: A list of all the objects we operated on
    """

    # this will also print DAG objects
    # print(cmds.ls())

    # this will list the current objects
    # print(cmds.ls(objects=True))

    objects = cmds.ls(objects=selection, dag=True, long=True)

    # error check, if you set selection to True but don't actually select something
    if selection and not objects:
        raise RuntimeError("You don't have anything selected!")

    # if len(objects) == 0:
    #     # dag parameter will list only objects in the outliner that's not hidden
    #     # long parameter will give full path of object to avoid duplicate errors
    #     objects = cmds.ls(dag=True, long=True)
        
    # we need to sort the objects list by length with the children objects first, b/c if parent name is changed then path to children will change    
    objects.sort(key=len, reverse=True)

    # gives the short name for each object in the objects list derived from it's path
    for obj in objects:
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
        
        # if objType == "mesh":
        #     suffix = "geo"
        # elif objType == "joint":
        #     suffix = "jnt"
        # elif objType == "camera":
        #     print("Skipping camera")
        #     continue
        # else:
        #     suffix = "grp"

        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        # in case None is returned for a camera
        if not suffix:
            continue
            
        #skips objects that have suffix already applied
        if obj.endswith("_"+suffix):
            print("Skipping " + shortName)
            continue

        # newName = shortName + "_" + suffix
        newName = f"{shortName}_{suffix}"
        # print(newName)
        cmds.rename(obj, newName)

        # updates the list with the new name in order to return an updated list
        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects