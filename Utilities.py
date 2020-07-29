def rbiqCalc(direction, opt):
    # direction: direction of run in degrees\n",
    # opt: optimal path direction in degrees\n",
    dirRad = direction * np.pi / 180
    optRad = opt * np.pi / 180
    diff = optRad - dirRad
    RBIQ = (50 * np.cos(diff)) + 50

    return RBIQ

def listRun(dirList, optList):
    i = 0
    sum = 0
    
    listlength = len(dirList);
    if listlength != len(optList):
        return
    
    while i < listlength-1:
        sum = sum + rbiqCalc(dirList[i+1], optList[i])
        i = i + 1

    RBIQ = sum / (listlength-1)
    return RBIQ