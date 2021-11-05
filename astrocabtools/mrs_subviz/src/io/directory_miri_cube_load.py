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

__all__ = ['get_miri_cube_subband']

def get_miri_cube_subband(path):
    """
    Obtain the list of X, Y, wavelength (slices) and flux values from each miri cube fits file in a directory selected previously
    :param dict pathCubes: list of paths of each cube
    """
    subband = ""
    cubeModel = datamodels.CubeModel(path)
    start_index = list(cubeModel.extra_fits.HDRTAB.data[3]).index('MJy/sr')

    photmjsr = list(cubeModel.extra_fits.HDRTAB.data[3])[340]
    photujua2 = list(cubeModel.extra_fits.HDRTAB.data[3])[341]

    cubeModel.data = cubeModel.data*photujua2 / (1000*photmjsr)

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