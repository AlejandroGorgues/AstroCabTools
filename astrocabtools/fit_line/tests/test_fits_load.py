import os
import pytest

import pandas as pd
import numpy as np

from astrotools.fit_line.src.io.fits_load import apply_redshift_to_fits

DATA = os.path.join(os.path.dirname(__file__), 'templates')

def test_transform():
	wavelength, flux, z = apply_redshift_to_fits(os.path.join(DATA, 'e2e_asn_ch1-medium_extract_1d.fits'), '3.2' ,0, 1, "um", 'erg/s/cm2/um')
	x = 23.72999982114416
	y= 32729493807.514355 
	assert wavelength[0] == pytest.approx(x)
	assert flux[0] == pytest.approx(y)
