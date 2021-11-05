import numpy as np
import math

from photutils import aperture_photometry, CircularAnnulus, RectangularAperture

__all__=["annulus_background_subtraction","rectangle_background_subtraction", "transform_wedges_subband"]

def rectangle_background_subtraction(centerX, centerY, width, height, aperture, cubeModel, spectrumValues):
    """Get the total flux values subtracting the aperture position of the rectangle
    :param float centerX: center x coordinate
    :param float centerY: center y coordinate
    :param float width: value of the width
    :param float height: value of the height
    :param Aperture Photometry aperture: aperture object
    :param Spectrum Values spectrumValues: object that contains reference to current wavelength and flux values transformed
    :return: list fValues_sub
    :return: list bkg_sum
    """

    fValues_sub = []
    bkg_sum = []
    rectangular_aperture = RectangularAperture([centerX, centerY], width, height)
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)
    for i in range(cubeModel.weightmap.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], rectangular_aperture)
        bkg_mean = (phot_table['aperture_sum'][0]/rectangular_aperture.area)*pixelArea
        bkg_sum.append(bkg_mean*aperture.area)
        fValues_sub.append(spectrumValues[i] - bkg_sum[i])
    return fValues_sub, bkg_sum

def annulus_background_subtraction(centerX, centerY, r_in, r_out, aperture, cubeModel, spectrumValues):
    """Get the total flux values subtracting the aperture position of the rings
    :param float centerX: center x coordinate
    :param float centerY: center y coordinate
    :param float r_in: value of the inner circle radius
    :param float r_out: value of the outer circle radius
    :param Aperture Photometry aperture: aperture object
    :param Spectrum Values spectrumValues: object that contains reference to current wavelength and flux values transformed
    :return: list fValues_sub
    :return: list bkg_sum
    """

    fValues_sub = []
    bkg_sum = []
    annulus_aperture = CircularAnnulus([centerX, centerY], r_in=r_in,r_out=r_out)
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)
    for i in range(cubeModel.weightmap.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], annulus_aperture)
        bkg_mean = (phot_table['aperture_sum'][0]/annulus_aperture.area)*pixelArea
        bkg_sum.append(bkg_mean*aperture.area)
        fValues_sub.append(spectrumValues[i] - bkg_sum[i])
    return fValues_sub, bkg_sum

def transform_wedges_subband(from_model, to_model, wedgesData, lambdaCube):
    """
    Transform the wedges coordinates from one cube to other
    :param object from_model: initial cube
    :param object to_model: cube where the data is gonna be transformed
    :param dict patchesData: coordinates of the figure
    :param int lambdaCube: lambda value to be used in the transformation
    :return: dictionary with the new coordinates
    """
    d2w = from_model.meta.wcs.get_transform('detector', 'world')
    w2d = to_model.meta.wcs.get_transform('world', 'detector')

    innerLeftPixel = (abs(wedgesData['innerRadius'] - wedgesData['centerX']), wedgesData['centerY'])
    innerRightPixel = (wedgesData['innerRadius'] + wedgesData['centerX'], wedgesData['centerY'])

    outerLeftPixel = (abs(wedgesData['outerRadius'] - wedgesData['centerX']), wedgesData['centerY'])
    outerRightPixel = (wedgesData['outerRadius'] + wedgesData['centerX'], wedgesData['centerY'])

    ra, dec, wavelength = d2w(wedgesData['centerX'], wedgesData['centerY'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    wedgesData['centerX'] = x
    wedgesData['centerY'] = y

    ra, dec, wavelength = d2w(innerLeftPixel[0], innerLeftPixel[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    innerLeftPixel = (x,y)

    ra, dec, wavelength = d2w(innerRightPixel[0], innerRightPixel[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    innerRightPixel = (x,y)

    ra, dec, wavelength = d2w(outerLeftPixel[0], outerLeftPixel[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    outerLeftPixel = (x,y)

    ra, dec, wavelength = d2w(outerRightPixel[0], outerRightPixel[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    outerRightPixel = (x,y)

    wedgesData['innerRadius'] = abs((innerLeftPixel[0] - innerRightPixel[0])/2.)
    wedgesData['outerRadius'] = abs((outerLeftPixel[0] - outerRightPixel[0])/2.)
    return wedgesData
