
#-*- coding: utf-8 -*-

"""
Method that read from a fits file
"""

import numpy as np

import sys
import io

from astropy.io import fits

from ..models.fits import fitsClass

__all__ = ['get_fits_image_data']

def get_fits_image_data(path):

    hdul = fits.open(path)
    fitsObj = fitsClass(0, 0, -1, -1, 0, 0, 0, 0, '', 0, 0, '')
    #Frames and integration could change positions, because of that
    #I look into the first position to check the order
    if hdul[1].header["CUNIT3"] == "groups":
        fitsObj.maxFrame = int(hdul[1].header["NAXIS3"])
        fitsObj.maxIntegration = int(hdul[1].header["NAXIS1"])
    else:
        fitsObj.maxFrame = int(hdul[1].header["NAXIS3"])
        fitsObj.maxIntegration = int(hdul[1].header["NAXIS"])
        fitsObj.maxXAxis = int(hdul[1].header["NAXIS1"]) - 1
        fitsObj.maxYAxis = int(hdul[1].header["NAXIS2"]) - 1

        #Because the value of the x and y axis could not be 1,
    #Which would correspond with the values from the image axis,
    #The values are obtained to use it
    fitsObj.shidXValue = float(hdul[1].header["CDELT1"])
    fitsObj.shidYValue = float(hdul[1].header["CDELT2"])

    #The value of the center could also not be the same, so it's also obtained
    fitsObj.fitsXCenter = int(hdul[1].header["CRVAL1"])
    fitsObj.fitsYCenter = int(hdul[1].header["CRVAL2"])
    fitsObj.fitsZUnit = hdul[1].header["BUNIT"]

    fitsObj.filename = path

    return hdul, fitsObj
