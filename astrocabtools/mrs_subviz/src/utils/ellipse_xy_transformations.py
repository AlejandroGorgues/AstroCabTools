from photutils import EllipticalAperture, aperture_photometry
import math

__all__=["transform_xy_ellipse", "transform_ellipse_subband", "transform_ellipse_subband_from_coord"]

def transform_xy_ellipse(centerX, centerY, aAxis, bAxis, cubeModel):
    """ Update rectangle data widgets and image object attributes
    :param float centerX: center x coordinate
    :param float centerY: center y coordinate
    :param float a: long axis value
    :param float b: short axis value
    :param object cubeModel: current data with standarized structure of the cube
    :return: flux, wavelength and aperture values
    """
    fValues = []
    wValues = []
    #Because it gets all the flux on a pixel, it needs to get the area of it rather
    #the sum of it
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)

    position = [(centerX-1, centerY-1)]
    aperture = EllipticalAperture(position,aAxis/2, bAxis/2)
    d2w = cubeModel.meta.wcs.get_transform('detector', 'world')
    for i in range(cubeModel.weightmap.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], aperture, method= 'exact')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)

        ra, dec, wavelength = d2w(1,1,i)
        wValues.append(wavelength)

    return fValues, wValues, aperture

def transform_ellipse_subband(from_model, to_model, patchesData, lambdaCube):
    """
    Transform the figure coordinates from one cube to other
    :param object from_model: initial cube
    :param object to_model: cube where the data is gonna be transformed
    :param dict patchesData: coordinates of the figure
    :param int lambdaCube: lambda value to be used in the transformation
    :return: dictionary with the new coordinates
    """
    d2w = from_model.meta.wcs.get_transform('detector', 'world')
    w2d = to_model.meta.wcs.get_transform('world', 'detector')

    leftAAxis = (abs(patchesData['aAxis']/2. - patchesData['centerX']), patchesData['centerY'])
    rightAAxis = (patchesData['aAxis']/2. + patchesData['centerX'], patchesData['centerY'])

    topBAxis = (patchesData['centerX'], patchesData['bAxis']/2. + patchesData['centerY'])
    bottomBAxis = (patchesData['centerX'],abs(patchesData['bAxis']/2. - patchesData['centerY']))

    ra, dec, wavelength = d2w(patchesData['centerX'], patchesData['centerY'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    patchesData['centerX'] = x
    patchesData['centerY'] = y

    ra, dec, wavelength = d2w(leftAAxis[0], leftAAxis[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    leftAAxis = (x, y)

    ra, dec, wavelength = d2w(rightAAxis[0], rightAAxis[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    rightAAxis = (x,y)

    ra, dec, wavelength = d2w(topBAxis[0], topBAxis[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    topBAxis = (x,y)

    ra, dec, wavelength = d2w(bottomBAxis[0], bottomBAxis[1], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    bottomBAxis = (x,y)

    patchesData['aAxis'] = abs(rightAAxis[0] - leftAAxis[0])
    patchesData['bAxis'] = abs(topBAxis[1] - bottomBAxis[1])

    return patchesData

def transform_ellipse_subband_from_coord(from_model, patchesData, wavelengthValue):
    """
    Transform the figure coordinates from RA and DEC to pixel of the same cube
    :param object from_model: cube where the data is gonna be transformed
    :param dict patchesData: coordinates of the figure
    :param float wavelenghtValue: wavelength value to be used in the transformation
    :return: dictionary with pixel coordinates
    """
    w2d = from_model.meta.wcs.get_transform('world', 'detector')

    leftAAxis = (abs(patchesData['aAxis']/2. - patchesData['centerX']), patchesData['centerY'])
    rightAAxis = (patchesData['aAxis']/2. + patchesData['centerX'], patchesData['centerY'])

    topBAxis = (patchesData['centerX'], patchesData['bAxis']/2. + patchesData['centerY'])
    bottomBAxis = (patchesData['centerX'],abs(patchesData['bAxis']/2. - patchesData['centerY']))

    x, y, _ = w2d(patchesData['centerX'], patchesData['centerY'], wavelengthValue)
    patchesData['centerX'] = x
    patchesData['centerY'] = y

    x, y, _ = w2d(leftAAxis[0], leftAAxis[1], wavelengthValue)
    leftAAxis = (x, y)

    x, y, _= w2d(rightAAxis[0], rightAAxis[1], wavelengthValue)
    rightAAxis = (x,y)

    x, y, _ = w2d(topBAxis[0], topBAxis[1], wavelengthValue)
    topBAxis = (x,y)

    x, y, _= w2d(bottomBAxis[0], bottomBAxis[1], wavelengthValue)
    bottomBAxis = (x,y)

    patchesData['aAxis'] = abs(rightAAxis[0] - leftAAxis[0])
    patchesData['bAxis'] = abs(topBAxis[1] - bottomBAxis[1])

    return patchesData
