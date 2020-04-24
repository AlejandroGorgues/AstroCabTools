#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import sys
import io

def apply_redshift_to_txt(path, z):
	z = float(z)

	if z < 0:
		raise Exception('Redshift value {} must not be negative'.format(z))
	data = pd.read_csv(path, sep=' ', comment='#', header=None)

	#Obtain the values of the emmited wavelength

	wavelength= (data.iloc[:, 0]*(1.+z)).to_numpy()
	flux = (data.iloc[:, 1]*(1.+z)).to_numpy()

	wavelengthTuple, fluxTuple = zip(*sorted(zip(wavelength, flux)))

	wavelength = np.asarray(wavelengthTuple)
	flux = np.asarray(fluxTuple)

	return wavelength, flux, z
