#-*- coding: utf-8 -*-
"""
Method that read from a fits file and normalize its values
"""
import pandas as pd
import numpy as np

import sys
import io
from astropy.io import fits

from ..utils.units_conversion import spectrumConversion

__all__ = ['apply_redshift_to_fits']

def apply_redshift_to_fits(path, z, wColumn, fColumn, wUnits, fUnits):
	"""
	Obtain the wavelenth and flux values from a fits file, apply the redshift to them, and
	convert the values to the established units
	:param str path: path of the sprectrum file
	:param float z: redshift value
	:param int wColumn: colum where the wavelength values are in the file
	:param int fColumn: colum where the flux values are in the file
	:param str wUnits: string that indicates the units of the wavelength in the file
	:param str fUnits: string that indicates the units of the flux in the file
	"""
	z = float(z)

	if z < 0:	raise Exception('Redshift value {} must not be negative'.format(z))
	hdul = fits.open(path)
	wavelength = hdul[1].data[wColumn]
	flux = hdul[1].data[fColumn]

	wavelength = [hdul[1].data[i][wColumn] for i in range(len(hdul[1].data))]
	flux = [hdul[1].data[i][fColumn] for i in range(len(hdul[1].data))]
	hdul.close()

	wavelength = np.asarray(wavelength)
	flux = np.asarray(flux)

	sc = spectrumConversion()

	wavelength = sc.transform_wUnits(wavelength, wUnits)
	flux = sc.transform_fUnits(flux, fUnits, wavelength)
	
	wavelenthNorm =wavelength.value*(1.+z)
	fluxNorm = flux.value/(1.+z)

	return wavelenthNorm, fluxNorm, z
