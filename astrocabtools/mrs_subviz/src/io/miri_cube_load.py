    #-*- coding: utf-8 -*-

"""
Method that read from a fits file a miri cube
"""

import numpy as np

import sys
import io

from astropy.io import fits
from jwst import datamodels

from ..utils.subband_position import subband_position

__all__ = ['get_miri_cube_data']

def get_miri_cube_data(path, ignoreHeaderSubband = False):
    """
    Obtain the X, Y, wavelength (slices) and flux values from a miri cube fits file
    after verified that it's a miri cube
    :
    """
    subband = None
    cubeModel = datamodels.CubeModel(path)
    start_index = list(cubeModel.extra_fits.HDRTAB.data[3]).index('MJy/sr')

    photmjsr = list(cubeModel.extra_fits.HDRTAB.data[3])[start_index+1]
    photujua2 = list(cubeModel.extra_fits.HDRTAB.data[3])[start_index+2]

    cubeModel.data = cubeModel.data*photujua2 / (1000*photmjsr)

    #If the subband of the cube is gonna be calculated from the header, enter
    if not ignoreHeaderSubband:
        hdul = fits.open(path)


        if hdul[0].header['BAND'] == "MULTIPLE":
            subband = subband_position(int(hdul[1].header["NAXIS3"]), float(hdul[1].header["CRPIX3"]), float(hdul[1].header["CDELT3"]),float(hdul[1].header["CRVAL3"]))
        elif hdul[0].header['BAND'] == "SHORT":
            subband = hdul[0].header['CHANNEL'] + 'S'
        elif hdul[0].header['BAND'] == "MEDIUM":
            subband = hdul[0].header['CHANNEL'] + 'M'
        elif hdul[0].header['BAND'] == "LONG":
            subband = hdul[0].header['CHANNEL'] + 'L'
        hdul.close()

        return subband, cubeModel
    #Otherwise, use the selected manually
    else:
        return cubeModel
