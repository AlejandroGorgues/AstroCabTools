import math
import re
from astropy.coordinates import SkyCoord

__all__=["slice_to_wavelength", "wavelength_to_slice", "sexagesimal_to_decimal", "sexagesimal_to_decimal_astropy", "arcsec_to_pixel"]


def slice_to_wavelength(cube_slice, cPix, cWValue, cCRVal):

    return round(((cube_slice+1) - cPix)*cWValue + cCRVal, 5)

def wavelength_to_slice(wavelength, cPix, cWValue, cCRVal):

    return set_round_value(((wavelength -cCRVal)/cWValue) + cPix)

def sexagesimal_to_decimal(coordinate):
    strList = re.split(':', coordinate)

    intSplit = [int(numStr) for numStr in strList]
    return intSplit[0] + intSplit[1]/60 + intSplit[2]/3600

def sexagesimal_to_decimal_astropy(ra, dec, model, wavelengthValue):
    w2d = model.meta.wcs.get_transform('world', 'detector')
    c = SkyCoord(ra, dec)
    x, y, _ = w2d(c.ra.degree, c.dec.degree, wavelengthValue)
    return x, y

def arcsec_to_pixel(arcsec, cdelt):
    return arcsec*cdelt*3600

def set_round_value(data):
    if data %1 >= 0.5:
        return int(math.ceil(data))
    else:
        return int(round(data))
