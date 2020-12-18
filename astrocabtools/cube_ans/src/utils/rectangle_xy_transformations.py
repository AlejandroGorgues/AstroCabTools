import numpy as np
from photutils import RectangularAperture, aperture_photometry
import math

__all__=["transform_xy_rectangle"]

def transform_xy_rectangle(centerX, centerY,width, height, cubeObj):
    """ Update rectangle data widgets and image object attributes
    :param float centerX: x value of the center coordinate
    :param float centerY: y value of the center coordinate
    :param float width: width value of the rectangle
    :param float height: height value of the rectangle
    :param object cubeObj: current data from the cube
    :return list fValues: flux values list for each wavelength
    :return list wValues: wavelenght list for each slice
    :return Aperture_Photometry aperture: aperture of the rectangle
    """
    fValues = []

    #Because it gets all the flux on a pixel, it needs to get the area of it rather
    #than one value.
    pixelArea = (cubeObj.cubeARValue * 3600.) * (cubeObj.cubeDValue * 3600.)
    aperture = RectangularAperture([centerX, centerY], width, height)
    for i in range(cubeObj.maxSlice):
        phot_table = aperture_photometry(cubeObj.data_cube[i], aperture, method='center')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)

    wValues = [((w+1) - cubeObj.cubeZCPix)*cubeObj.cubeWValue + cubeObj.cubeZCRVal for w in range(len(fValues))]

    return fValues, wValues, aperture
