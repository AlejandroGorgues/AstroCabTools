import numpy as np
import math

from photutils import aperture_photometry, CircularAnnulus

__all__=["background_subtraction"]

def background_subtraction(centerX, centerY, r_in, r_out, aperture, cubeObj, spectrumValues):
    """Get the total flux values subtracting the aperture position of the rings
    :param float centerX: center x coordinate
    :param float centerY: center y coordinate
    :param float r_in: value of the inner circle radius
    :param float r_out: value of the outer circle radius
    :param Fits Obj cubeObj: object that contains reference to basic data of the current cube
    :param Aperture Photometry aperture: aperture object
    :param Spectrum Values spectrumValues: object that contains reference to current wavelength and flux values transformed
    :return: list fValues_sub
    :return: list bkg_sum
    """

    fValues_sub = []
    bkg_sum = []
    annulus_aperture = CircularAnnulus([centerX, centerY], r_in=r_in,r_out=r_out)
    pixelArea = (cubeObj.cubeARValue * 3600.) * (cubeObj.cubeDValue * 3600.)

    for i in range(cubeObj.maxSlice):
        phot_table = aperture_photometry(cubeObj.data_cube[i], annulus_aperture)
        bkg_mean = (phot_table['aperture_sum'][0]/annulus_aperture.area)*pixelArea
        bkg_sum.append(bkg_mean*aperture.area)
        fValues_sub.append(spectrumValues[i] - bkg_sum[i])
    return fValues_sub, bkg_sum
