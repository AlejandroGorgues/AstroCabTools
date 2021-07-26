import numpy as np
from photutils import RectangularAperture, aperture_photometry
import math

__all__=["transform_xy_rectangle"]

def transform_xy_rectangle(centerX, centerY,width, height, cubeModel):
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
    wValues = []
    fValues = []

    #Because it gets all the flux on a pixel, it needs to get the area of it rather than one value.
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)

    #To correct the additional extend applied to the figure, the center cooridnates must
    #be 1 pixel unit less
    aperture = RectangularAperture([centerX-1, centerY-1], width, height)
    d2w = cubeModel.meta.wcs.get_transform('detector', 'world')
    for i in range(cubeModel.data.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], aperture, method='subpixel')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)
        ra, dec, wavelength = d2w(1,1,i)
        wValues.append(wavelength)
    #wValues = [((w+1) - cubeModel.meta.wcsinfo.crpix3)*cubeModel.meta.wcsinfo.cdelt3 + cubeModel.meta.wcsinfo.crval3 for w in range(len(fValues))]

    return fValues, wValues, aperture
