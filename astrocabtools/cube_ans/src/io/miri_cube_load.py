    #-*- coding: utf-8 -*.items()-

"""
Method that read from a fits file a miri cube
"""

import numpy as np

import sys
import io

from astropy.io import fits
from jwst import datamodels

__all__ = ['get_miri_cube_data']

def get_miri_cube_data(path):
    """
    Obtain the X, Y, wavelength (slices) and flux values from a miri cube fits file
    after verified that it's a miri cube
    str path: path where the cube is located
    """
    cubeModel = datamodels.CubeModel(path)
    start_index = list(cubeModel.extra_fits.HDRTAB.data[3]).index('MJy/sr')

    photmjsr = list(cubeModel.extra_fits.HDRTAB.data[3])[start_index+1]
    photujua2 = list(cubeModel.extra_fits.HDRTAB.data[3])[start_index+2]

    #photmjsr = 1.0
    #photujua2 = 1.0
    cubeModel.data = cubeModel.data*photujua2 / (1000*photmjsr)

    return cubeModel
