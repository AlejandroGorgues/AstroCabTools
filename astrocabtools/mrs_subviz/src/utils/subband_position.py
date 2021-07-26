import math

__all__=["subband_position"]


def subband_position(cube_slice, cPix, cWValue, cCRVal):
    """ Calculate the channel and the lambda transformed
    :param string emit: lambda emitted
     :param string z: redshift value
    """

    maxSubband = ((cube_slice+1) - cPix)*cWValue + cCRVal
    minSubband = (1 - cPix)*cWValue + cCRVal
    subband = (maxSubband + minSubband)/2
    if 4.87 <= subband <= 7.45:
        if 4.87 <= subband  <= 5.62:
            return '1A'
        elif 5.62 < subband <= 6.49:
            return '1B'
        elif 6.49 < subband <= 7.45:
            return '1C'

    elif 7.76 < subband <= 11.47:
        if 7.45 <= subband <= 8.61:
            return '2A'
        elif 8.90 < subband <= 9.91:
            return '2B'
        elif 9.91 < subband <=  11.47:
            return '2C'

    elif 11.47 < subband <= 17.54:
        if 11.47 <= subband <= 13.25:
            return '3A'
        elif 13.35 < subband <= 15.30:
            return '3B'
        elif 15.30 < subband <= 17.54:
            return '3C'

    elif 17.54 <= subband <= 28.82:
        if subband >= 23.84:
            return '4C'
        elif subband >= 20.44:
            return '4B'
        elif subband >=17.54:
            return '4A'
