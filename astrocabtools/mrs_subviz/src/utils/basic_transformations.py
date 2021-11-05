import math
import re
from astropy.coordinates import SkyCoord

__all__=["slice_to_wavelength", "wavelength_to_slice", "sexagesimal_to_decimal", "sexagesimal_to_decimal_astropy", "arcsec_to_pixel", "apply_redshift", "wavelength_from_redshift", "set_round_lines", "rectangle_patch_to_border_coordinates", "rectangle_border_to_patch_coordinates"]


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

def rectangle_border_to_patch_coordinates(borderData):
    width = abs(borderData["ex"] - borderData["ix"])
    height = abs(borderData["ey"] - borderData["iy"])

    return {"width" : width,
            "height" : height}

def rectangle_patch_to_border_coordinates(patchData):
    return {"centerX" : patchData["centerX"],
            "centerY" : patchData["centerY"],
            "ix" : abs(patchData["centerX"]-patchData["width"]/2.),
            "iy" : abs(patchData["centerY"]-patchData["height"]/2.),
            "ex" : abs(patchData["centerX"]+patchData["width"]/2.),
            "ey" : abs(patchData["centerY"]+patchData["height"]/2.)}

def arcsec_to_pixel(arcsec, cdelt):
    return arcsec*cdelt*3600

def apply_redshift(wValue, z):
    return wValue*(1+float(z))

def wavelength_from_redshift(wTrans, z):
    return wTrans/(1+z)

def set_round_lines(wValue, wText):
    """
    Round the wavelength value to 4 decimals if less or equal 1 micron and
    1 decimal if it is a PAH line
    """
    if wText == 'PAH':
        return round(wValue, 1)

    if len(str(wValue).split('.'))> 4 and wValue <= 1:
        return round(wValue, 4)

    if len(str(wValue).split('.'))> 3 and wValue > 1 and wText != 'PAH':
        return round(wValue, 3)

    return wValue

def set_round_value(data):
    if data %1 >= 0.5:
        return int(math.ceil(data))
    else:
        return int(round(data))
