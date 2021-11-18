    #-*- coding: utf-8 -*-

"""
Method that read from a fits file a miri cube
"""

import numpy as np

import sys
import io

from astropy.io import fits
from jwst import datamodels

__all__ = ['get_muse_cube_data']

def get_muse_cube_data(path):
    """
    Obtain the X, Y, wavelength (slices) and flux values from a muse cube fits file
    after verified that it's a miri cube
    :
    """
    cubeModel = datamodels.CubeModel(path)
    cubeModel.meta.wcsinfo.cdelt1 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CD1_1"][0]
    cubeModel.meta.wcsinfo.cdelt2 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CD2_2"][0]
    cubeModel.meta.wcsinfo.cdelt3 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CD3_3"][0]
    cubeModel.meta.wcsinfo.crpix1 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRPIX1"][0]
    cubeModel.meta.wcsinfo.crpix2 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRPIX2"][0]
    cubeModel.meta.wcsinfo.crpix3 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRPIX3"][0]
    cubeModel.meta.wcsinfo.crval1 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRVAL1"][0]
    cubeModel.meta.wcsinfo.crval2 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRVAL2"][0]
    cubeModel.meta.wcsinfo.crval3 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CRVAL3"][0]
    cubeModel.meta.bunit_unit = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "BUNIT"][0]
    cubeModel.meta.wcsinfo.cunit3 = [item[1] for item in cubeModel.extra_fits.DATA.header if item[0] == "CUNIT3"][0]

    cubeModel.data = cubeModel.extra_fits.DATA.data
    return cubeModel

