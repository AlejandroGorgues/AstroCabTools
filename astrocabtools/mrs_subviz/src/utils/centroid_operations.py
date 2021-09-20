from photutils import EllipticalAperture, aperture_photometry
from photutils.centroids import centroid_2dg
import math

__all__=["calculate_centroid", "transform_centroid_subband"]

def calculate_centroid(data):
    x, y = centroid_2dg(data)
    return x,y

def transform_centroid_subband(from_model, to_model, patchesData, lambdaCube):
    """
    Transform the centroid coordinates from one cube to other
    :param object from_model: initial cube
    :param object to_model: cube where the data is gonna be transformed
    :param dict patchesData: coordinates of the centroid
    :param int lambdaCube: lambda value to be used in the transformation
    :return: dictionary with the new coordinates
    """
    d2w = from_model.meta.wcs.get_transform('detector', 'world')
    w2d = to_model.meta.wcs.get_transform('world', 'detector')


    ra, dec, wavelength = d2w(patchesData['xCoordinate'], patchesData['yCoordinate'], lambdaCube)
    x, y, _ = w2d(ra, dec, wavelength)
    patchesData['xCoordinate'] = x
    patchesData['yCoordinate'] = y

    return patchesData

