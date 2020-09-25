import numpy as np

import math

__all__=["transform_xy_rectangle"]

def transform_xy_rectangle(ix, iy, ex, ey, cubeObj):
    """ Update rectangle data widgets and image object attributes
    :param float ix: initial x coordinate
    :param float iy: initial y coordinate
    :param float ex: final x coordinate
    :param float ey: final y coordinate
    :param object cubeObj: current data from the cube
    """
    #Instead of beeing a coord (x,y) it's (y,x)
    ixRound = set_round_value(ix)
    iyRound = set_round_value(iy)
    exRound = set_round_value(ex)
    eyRound = set_round_value(ey)
    fValues = None

    #Because it gets all the flux on a pixel, it needs to get the area of it rather
    #than one value.
    pixelArea = (cubeObj.cubeARValue * 3600.) * (cubeObj.cubeDValue * 3600.)

    #Same pixel
    if ixRound == exRound and iyRound == eyRound:
        fValues = get_fValues(ixRound, iyRound, fValues, cubeObj)

    #Start Top left rectangle
    elif ixRound < exRound and iyRound > eyRound:
        for i in range(ixRound, exRound + 1):
            for j in range(eyRound, iyRound +1):

                fValues = get_fValues(i, j, fValues, cubeObj, pixelArea)

    #Start Bottom left rectangle
    elif ixRound < exRound and iyRound < eyRound:
        for i in range(ixRound, exRound + 1):
            for j in range(iyRound, eyRound+1):

                fValues = get_fValues(i, j, fValues, cubeObj, pixelArea)
    #Start Top right rectangle
    elif ixRound > exRound and iyRound > eyRound:
        for i in range(exRound, ixRound + 1):
            for j in range(eyRound, iyRound+1):

                fValues = get_fValues(i, j, fValues, cubeObj, pixelArea)

    #Start Bottom right rectangle
    elif ixRound > exRound and iyRound < eyRound:
        for i in range(exRound, ixRound +1):
            for j in range(iyRound, eyRound+1):

                fValues = get_fValues(i, j, fValues, cubeObj, pixelArea)

    #Rectangle along y axis down
    elif ixRound == exRound and iyRound > eyRound:
        for j in range(eyRound, iyRound +1):

            fValues = get_fValues(ixRound, j, fValues, cubeObj, pixelArea)

    #Rectangle along y axis up
    elif ixRound == exRound and iyRound < eyRound:
        for j in range(iyRound, eyRound+1):

            fValues = get_fValues(ixRound, j, fValues, cubeObj, pixelArea)

    #Rectangle along x axis to right
    elif ixRound < exRound and iyRound == eyRound:
        for i in range(ixRound, exRound +1):

            fValues = get_fValues(i, iyRound, fValues, cubeObj, pixelArea)

    #Rectangle along x axis to left
    elif ixRound > exRound and iyRound == eyRound:
        for i in range(exRound, ixRound +1):

            fValues = get_fValues(i, iyRound, fValues, cubeObj, pixelArea)

    #for w in range(len(fValues) + 1)
    wValues = [((w+1) - cubeObj.cubeZCPix)*cubeObj.cubeWValue + cubeObj.cubeZCRVal for w in range(len(fValues))]

    return fValues, wValues

def set_round_value(data):
    if data %1 >= 0.5:
        return int(math.ceil(data))
    else:
        return int(round(data))

def get_fValues(i, j, fValue, cubeObj, pixelArea):
    if fValue is None:
        fValue = cubeObj.data_cube[:, j, i]
    else:
        fValue = cubeObj.data_cube[:, j, i] + fValue
    return fValue * pixelArea
