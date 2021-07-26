import os
import pytest

import pandas as pd
import numpy as np

from astrocabtools.mrs_subviz.src.io.miri_cube_load import get_miri_cube_data

DATA = os.path.join(os.path.dirname(__file__), 'templates')

def test_transform():
	units, cubeObj= get_miri_cube_data(os.path.join(DATA,'dither_ch2-medium_s3d.fits'))

	assert cubeObj.data_cube[0][3,39] == pytest.approx(0.0030087337)
