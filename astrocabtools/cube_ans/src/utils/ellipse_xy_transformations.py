from photutils import EllipticalAperture, aperture_photometry

__all__=["transform_xy_ellipse"]

def transform_xy_ellipse(centerX, centerY, aAxis, bAxis, cubeModel):
    """ Update rectangle data widgets and image object attributes
    :param float centerX: center x coordinate
    :param float centerY: center y coordinate
    :param float a: long axis value
    :param float b: short axis value
    :param object cubeObj: current data from the cube
    :return list fValues: flux values list for each wavelength
    :return list wValues: wavelenght list for each slice
    :return Aperture_Photometry aperture: aperture of the ellipse
    """
    wValues = []
    fValues = []
    #Because it gets all the flux on a pixel, it needs to get the area of it rather
    #the sum of it
    pixelArea = (cubeModel.meta.wcsinfo.cdelt1 * 3600.) * (cubeModel.meta.wcsinfo.cdelt2 * 3600.)

    #To correct the additional extend applied to the figure, the center cooridnates must
    #be 1 pixel unit less
    position = [(centerX-1, centerY-1)]
    aperture = EllipticalAperture(position,aAxis/2, bAxis/2)
    d2w = cubeModel.meta.wcs.get_transform('detector', 'world')
    for i in range(cubeModel.data.shape[0]):
        phot_table = aperture_photometry(cubeModel.data[i], aperture, method= 'exact')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)
        ra, dec, wavelength = d2w(1,1,i)
        wValues.append(wavelength)
    #wValues = [((w+1) - cubeModel.meta.wcsinfo.crpix3)*cubeModel.meta.wcsinfo.cdelt3 + cubeModel.meta.wcsinfo.crval3 for w in range(len(fValues))]

    return fValues, wValues, aperture
