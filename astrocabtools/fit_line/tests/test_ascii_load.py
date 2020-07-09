import os
import pytest

import pandas as pd
import numpy as np

from astrotools.fit_line.src.io.ascii_load import apply_redshift_to_txt

DATA = os.path.join(os.path.dirname(__file__), 'templates')

def test_transform():
	wavelength, flux, z = apply_redshift_to_txt(os.path.join(DATA, 'M82_ISO.txt'), '3.2', 0, 1, "um", 'erg/s/cm2/um')
	x = 9.909899711608887
	y= 1421.4285214742024 
	assert wavelength[0] == pytest.approx(x)
	assert flux[0] == pytest.approx(y)
