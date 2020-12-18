from photutils import EllipticalAperture, aperture_photometry

__all__=["transform_xy_ellipse"]

def transform_xy_ellipse(centerX, centerY, aAxis, bAxis, cubeObj):
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
    fValues = []
    #Because it gets all the flux on a pixel, it needs to get the area of it rather
    #the sum of it
    pixelArea = (cubeObj.cubeARValue * 3600.) * (cubeObj.cubeDValue * 3600.)

    position = [(centerX, centerY)]
    aperture = EllipticalAperture(position,aAxis/2, bAxis/2)
    for i in range(cubeObj.maxSlice):
        phot_table = aperture_photometry(cubeObj.data_cube[i], aperture, method= 'exact')
        fValues.append(phot_table['aperture_sum'][0]*pixelArea)

    wValues = [((w+1) - cubeObj.cubeZCPix)*cubeObj.cubeWValue + cubeObj.cubeZCRVal for w in range(len(fValues))]

    return fValues, wValues, aperture
