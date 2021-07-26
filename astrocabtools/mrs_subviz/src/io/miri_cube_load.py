    #-*- coding: utf-8 -*-

"""
Method that read from a fits file a miri cube
"""

import numpy as np

import sys
import io

from astropy.io import fits
from jwst import datamodels

from PyQt5.QtGui import *
from PyQt5.QtCore import *

__all__ = ['get_miri_cube_data']

def get_miri_cube_data(path):
    """
    Obtain the X, Y, wavelength (slices) and flux values from a miri cube fits file
    after verified that it's a miri cube
    :
    """
    cubeModel = datamodels.CubeModel(path)
    start_index = list(cubeModel.extra_fits.HDRTAB.data[3]).index('MJy/sr')

    photmjsr = list(cubeModel.extra_fits.HDRTAB.data[3])[340]
    photujua2 = list(cubeModel.extra_fits.HDRTAB.data[3])[341]

    cubeModel.data = cubeModel.data*photujua2 / (1000*photmjsr)
    return cubeModel.meta.bunit_data != 'um' or cubeModel.meta.wcsinfo.cunit3[:3] != 'mJy', cubeModel
