import os
import pytest

import numpy as np
from astrotools.fit_line.src.models.gaussModelCreation import gaussModel
from astrotools.fit_line.src.io.ascii_load import apply_redshift_to_txt
from astrotools.fit_line.src.io.fits_load import apply_redshift_to_fits


DATA = os.path.join(os.path.dirname(__file__), 'templates')

def test_gaussCreation():
    leftX = 6.059833308266233
    leftY = 126988528488.92593

    rightX = 6.099673556854627
    rightY = 127279397737.04881
    
    sigma1X = 6.070246100510927
    sigma1Y = 130527437674.42091
   
    sigma2X = 6.079640250036031
    sigma2Y = 130414321855.70647
   
    topX = 6.072283385950106
    topY = 131755552277.6064

    wavelength, flux, z = apply_redshift_to_fits(os.path.join(DATA, 'e2e_asn_ch1-medium_extract_1d.fits'), '0.0' ,0, 1, 'um', 'erg/s/cm2/um')

    model = gaussModel()
    model.add_data_points(leftX, leftY)
    model.add_data_points(rightX, rightY)
    model.add_data_points(sigma1X, sigma1Y)
    model.add_data_points(sigma2X, sigma2Y)
    model.add_data_points(topX, topY)

    result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = model.draw_gauss_curve_fit("testFileFITS", wavelength, flux)

    assert result.params['h'].value  == pytest.approx(4651671986.159365)
    assert result.params['c'].value == pytest.approx(6.074177997174173)
    assert result.params['sigma'].value  == pytest.approx(0.006877069608042684)
    assert result.params['a'].value == pytest.approx(16411418870.348742)
    assert result.params['b'].value == pytest.approx(18182788565.592796)
    assert result.chisqr == pytest.approx(4.318055004872323e+18)

    
    leftX = 46.020320434120734
    leftY = 2200.168232716377

    rightX = 49.012102869732075
    rightY = 4561.924659979397
    
    sigma1X = 46.98871316985809
    sigma1Y = 8057.3241723286665
   
    sigma2X = 47.65792766203431
    sigma2Y = 8033.706608056036

    topX = 47.11468295662067
    topY = 10844.19675649903
    
    wavelength, flux, z = apply_redshift_to_txt(os.path.join(DATA, 'M82_ISO.txt'), '3.2', 0, 1, "um", 'erg/s/cm2/um')

    model = gaussModel()
    model.add_data_points(leftX, leftY)
    model.add_data_points(rightX, rightY)
    model.add_data_points(sigma1X, sigma1Y)
    model.add_data_points(sigma2X, sigma2Y)
    model.add_data_points(topX, topY)

    result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = model.draw_gauss_curve_fit('testFileTXT', wavelength, flux)
    
    assert result.params['h'].value  == pytest.approx(6717.776686396627)
    assert result.params['c'].value == pytest.approx(47.320760973039185)
    assert result.params['sigma'].value  == pytest.approx(0.3380262059586799)
    assert result.params['a'].value == pytest.approx(-42006.20172343335)
    assert result.params['b'].value == pytest.approx(968.5481663236021)
    assert result.chisqr == pytest.approx(2943575409.8643765)

