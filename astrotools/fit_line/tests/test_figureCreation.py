import os
import pytest

import pandas as pd
import numpy as np

from astrotools.fit_line.src.utils.fitting_model_creation import calculate_slope, calculate_intercept


def test_slope():
    slope = 1.0512820512821
    slope2 = calculate_slope(2.2,4.6,6.1,8.7)

    assert slope == pytest.approx(slope2)

def test_intercept():
    intersect = 4.6- 3*3.5

    intercept2 = calculate_intercept(3, 3.5, 4.6)
