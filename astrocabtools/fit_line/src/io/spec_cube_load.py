#-*- coding: utf-8 -*-
"""
Method that applied redshift to flux and wavelength
"""
import numpy as np

import sys
import io

from ..utils.units_conversion import spectrumConversion

__all__ = ['apply_redshift_to_cube']

def apply_redshift_to_cube(z, wValues, fValues, wUnits, fUnits):
	"""
	Apply the redshift to wavelength and flux values from the cube_ans tool to
	convert them to the established units
	:param float z: redshift value
	:param int wColumn: wavelength values
	:param int fColumn: flux values
	:param str wUnits: string that indicates the units of the wavelength in the file
	:param str fUnits: string that indicates the units of the flux in the file
	"""
	z = float(z)

	if z < 0:
		raise Exception('Redshift value {} must not be negative'.format(z))

	#wavelengthTuple, fluxTuple = zip(*sorted(zip(wavelength, flux)))

	#wavelength = np.asarray(wavelengthTuple)
	#flux = np.asarray(fluxTuple)

	sc = spectrumConversion()

	wavelength = sc.transform_wUnits(wValues, wUnits)
	flux = sc.transform_fUnits(fValues, fUnits, wValues)

	wavelenthNorm =wavelength.value*(1.+z)
	fluxNorm = flux.value/(1.+z)

	return wavelenthNorm, fluxNorm, z
