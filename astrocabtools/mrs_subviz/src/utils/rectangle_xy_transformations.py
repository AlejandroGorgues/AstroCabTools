import numpy as np
from photutils import RectangularAperture, aperture_photometry
import math

__all__=["transform_xy_rectangle", "transform_rectangle_subband"]

def transform_xy_rectangle(centerX, centerY,width, height, cubeModel):
    """ Update rectangle data widgets and image object attributes
    :param float centerX: x value of the center coordinate
    :param float centerY: y value of the center coordinate
    :param float width: width value of the rectangle
    :param float height: height value of the rectangle
    :param object cubeModel: current data with standarized structure of the cube
    :param object cubeObj: current data from the cube
    :return list fValues: flux values list for each wavelength
    :return list wValues: wavelenght list for each slice
    :return Aperture_Photometry aperture: aperture of the rectangle
    """
    fValues = []
    wValues = []
    #Because it gets all the flux on a pixel, it needs to get the area of it rather than one value.
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)
    aperture = RectangularAperture([centerX-1, centerY-1], width, height)
    d2w = cubeModel.meta.wcs.get_transform('detector', 'world')
    for i in range(cubeModel.weightmap.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], aperture, method='subpixel')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)

        ra, dec, wavelength = d2w(1,1, i)
        wValues.append(wavelength)
    #wValues = [((w+1) - cubeObj.cubeZCPix)*cubeObj.cubeWValue + cubeObj.cubeZCRVal for w in range(len(fValues))]
    #print("*********************")
    #print(wValues)
    #print("---------------------")
    #print([((w+1) - cubeObj.cubeZCPix)*cubeObj.cubeWValue + cubeObj.cubeZCRVal for w in range(len(fValues))])
    #print("*********************")

    return fValues, wValues, aperture

def transform_rectangle_subband(from_model, to_model, patchesData, lambdaCube):
    d2w = from_model.meta.wcs.get_transform('detector', 'world')
    w2d = to_model.meta.wcs.get_transform('world', 'detector')

    ra, dec, wavelength = d2w(patchesData['ix'], patchesData['iy'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    patchesData['ix'] = x
    patchesData['iy'] = y

    ra, dec, wavelength = d2w(patchesData['ex'], patchesData['ey'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    patchesData['ex'] = x
    patchesData['ey'] = y

    ra, dec, wavelength = d2w(patchesData['centerX'], patchesData['centerY'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    patchesData['centerX'] = x
    patchesData['centerY'] = y

    #print(patchesData)
    return patchesData
