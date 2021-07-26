import math

__all__=["slice_to_wavelength", "wavelength_to_slice"]


def slice_to_wavelength(cube_slice, cPix, cWValue, cCRVal):

    #print(round(((cube_slice+1) - cPix)*cWValue + cCRVal, 5))
    return round(((cube_slice+1) - cPix)*cWValue + cCRVal, 5)

def wavelength_to_slice(wavelength, cPix, cWValue, cCRVal):

    return set_round_value(((wavelength -cCRVal)/cWValue) + cPix)

def set_round_value(data):
    if data %1 >= 0.5:
        return int(math.ceil(data))
    else:
        return int(round(data))
