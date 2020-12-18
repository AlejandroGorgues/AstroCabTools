    #-*- coding: utf-8 -*-

"""
Method that read from a fits file a miri cube
"""

import numpy as np

import sys
import io

from astropy.io import fits

from ..models.miri_cube_fits import miriCubeClass

from PyQt5.QtGui import *
from PyQt5.QtCore import *

__all__ = ['get_miri_cube_data']

def get_miri_cube_data(path):
    """
    Obtain the X, Y, wavelength (slices) and flux values from a miri cube fits file
    after verified that it's a miri cube
    :
    """
    hdul = fits.open(path)
    fitsObj = miriCubeClass(0, 0, -1, -1, 0, 0, 0, 0, '', '', 0, 0, 0 , 0, 0, None, '')

    fitsObj.currSlice = 0
    fitsObj.maxSlice = int(hdul[1].header["NAXIS3"])
    fitsObj.maxXAxis = int(hdul[1].header["NAXIS1"]) - 1
    fitsObj.maxYAxis = int(hdul[1].header["NAXIS2"]) - 1

    #Because the value of the x and y axis could not be exactly 1,
    #which would correspond with the values from the image axis,
    #the values that are going to increment each axis
    #are obtained from the next two parameters
    fitsObj.cubeARValue = float(hdul[1].header["CDELT1"])
    fitsObj.cubeDValue = float(hdul[1].header["CDELT2"])
    fitsObj.cubeWValue = float(hdul[1].header["CDELT3"])

    #The value of the center could also not be the same, so it's also obtained
    fitsObj.cubeXCRVal = int(hdul[1].header["CRVAL1"])
    fitsObj.cubeYCRVal = int(hdul[1].header["CRVAL2"])
    fitsObj.cubeZCRVal = int(hdul[1].header["CRVAL3"])

    fitsObj.cubeWavelengthUnit = hdul[1].header["CUNIT3"]
    fitsObj.cubeFluxUnit = hdul[1].header["BUNIT"]

    fitsObj.cubeXCPix = float(hdul[1].header["CRPIX1"])
    fitsObj.cubeYCPix = float(hdul[1].header["CRPIX2"])
    fitsObj.cubeZCPix = float(hdul[1].header["CRPIX3"])

    fitsObj.data_cube = hdul[1].data
    fitsObj.filename = path

    hdul.close()
    return fitsObj.cubeWavelengthUnit != 'um' or fitsObj.cubeFluxUnit[:3] != 'mJy',fitsObj
