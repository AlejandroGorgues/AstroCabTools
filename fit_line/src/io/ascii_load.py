#-*- coding: utf-8 -*-
"""
Method that applied redshift to flux and wavelength
"""
import pandas as pd
import numpy as np

import sys
import io

from ..utils.units_conversion import spectrumConversion

__all__ = ['apply_redshift_to_txt']

def apply_redshift_to_txt(path, z, wColumn, fColumn, wUnits, fUnits):
	"""
	Obtain the wavelenth and flux values from an ascii file, apply the redshift to them, and
	convert the values to the established units
	:param str path: path of the sprectrum file
	:param float z: redshift value
	:param int wColumn: colum where the wavelength values are in the file
	:param int fColumn: colum where the flux values are in the file
	:param str wUnits: string that indicates the units of the wavelength in the file
	:param str fUnits: string that indicates the units of the flux in the file
	"""
	z = float(z)

	if z < 0:
		raise Exception('Redshift value {} must not be negative'.format(z))
	data = pd.read_csv(path, sep=' ', comment='#', header=None, usecols = [wColumn, fColumn])
	#Obtain the values of the emmited wavelength

	wavelength= (data.iloc[:, 0]*(1.+z)).to_numpy()
	flux = (data.iloc[:, 1]*(1.+z)).to_numpy()

	wavelengthTuple, fluxTuple = zip(*sorted(zip(wavelength, flux)))

	wavelength = np.asarray(wavelengthTuple)
	flux = np.asarray(fluxTuple)

	sc = spectrumConversion()

	wavelength = sc.transform_wUnits(wavelength, wUnits)
	flux = sc.transform_fUnits(flux, fUnits, wavelength)

	return wavelength.value, flux.value, z
