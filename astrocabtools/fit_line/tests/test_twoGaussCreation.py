import os
import pytest

import numpy as np
from astrotools.fit_line.src.models.doubleGaussModelCreation import doubleGaussModel
from astrotools.fit_line.src.io.ascii_load import apply_redshift_to_txt
from astrotools.fit_line.src.io.fits_load import apply_redshift_to_fits


DATA = os.path.join(os.path.dirname(__file__), 'templates')

def test_gaussCreation():
    leftX = 6.228197775163386
    leftY = 124611208255.74753

    rightX = 6.350721843125295
    rightY = 123310959411.76181
    
    firstSigma1X = 6.273821491336555
    firstSigma1Y = 131855451815.09648
   
    firstSigma2X = 6.3076806014524935
    firstSigma2Y = 132226951484.80669
   
    firstTopX = 6.289029396727612
    firstTopY = 134976049040.66219
    
    secondSigma1X = 6.247422863110571
    secondSigma1Y = 128957754391.3569
   
    secondSigma2X = 6.270091250391579
    secondSigma2Y = 129366404028.03812
   
    secondTopX = 6.255744169833979
    secondTopY = 129737903697.74832

    wavelength, flux, z = apply_redshift_to_fits(os.path.join(DATA, 'e2e_asn_ch1-medium_extract_1d.fits'), '0.0' ,0, 1, 'um', 'erg/s/cm2/um')

    model = doubleGaussModel()
    model.add_data_points(leftX, leftY)
    model.add_data_points(rightX, rightY)
    model.add_data_points(firstSigma1X, firstSigma1Y)
    model.add_data_points(firstSigma2X, firstSigma2Y)
    model.add_data_points(firstTopX, firstTopY)
    model.add_data_points(secondSigma1X, secondSigma1Y)
    model.add_data_points(secondSigma2X, secondSigma2Y)
    model.add_data_points(secondTopX, secondTopY)

    result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = model.draw_gauss_curve_fit("testFileFITS", wavelength, flux)

    assert result.params['h1'].value  == pytest.approx(10251037227.49869)
    assert result.params['c1'].value == pytest.approx(6.292282556169206)
    assert result.params['sigma1'].value  == pytest.approx(0.02370939937504167)
    assert result.params['h2'].value  == pytest.approx(2672357311.6241426)
    assert result.params['c2'].value == pytest.approx(6.248327155292726)
    assert result.params['sigma2'].value  == pytest.approx(0.007456597002866558)
    assert result.params['a'].value == pytest.approx(189542227461.62698)
    assert result.params['b'].value == pytest.approx(-10444049034.724892)
    assert result.chisqr == pytest.approx(3.66407563374124e+19)

    
    leftX = 95.39918218043015
    leftY = 29978.79744034294

    rightX = 96.86304414847658
    rightY = 30775.89023454421
    
    firstSigma1X = 96.29779051725073
    firstSigma1Y = 32752.68036416336
   
    firstSigma2X = 96.48620839432601
    firstSigma2Y = 32688.91294062726
   
    firstTopX = 96.37025893151045
    firstTopY = 35526.56328798378
    
    secondSigma1X = 95.50063796039376
    secondSigma1Y = 30425.16940509565
   
    secondSigma2X = 96.00791686021182
    secondSigma2Y = 30393.2856933276
   
    secondTopX = 95.76152425172876
    secondTopY = 30680.23909924006
    
    wavelength, flux, z = apply_redshift_to_txt(os.path.join(DATA, 'M82_ISO.txt'), '3.2', 0, 1, "um", 'erg/s/cm2/um')

    model = doubleGaussModel()
    model.add_data_points(leftX, leftY)
    model.add_data_points(rightX, rightY)
    model.add_data_points(firstSigma1X, firstSigma1Y)
    model.add_data_points(firstSigma2X, firstSigma2Y)
    model.add_data_points(firstTopX, firstTopY)
    model.add_data_points(secondSigma1X, secondSigma1Y)
    model.add_data_points(secondSigma2X, secondSigma2Y)
    model.add_data_points(secondTopX, secondTopY)

    result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = model.draw_gauss_curve_fit('testFileTXT', wavelength, flux)
    
    assert result.params['h1'].value  == pytest.approx(4936.849461706795)
    assert result.params['c1'].value == pytest.approx(96.35800032776956)
    assert result.params['sigma1'].value  == pytest.approx(0.06467727189983155)
    assert result.params['h2'].value  == pytest.approx(-365.32281165883194)
    assert result.params['c2'].value == pytest.approx(95.38483882260569)
    assert result.params['sigma2'].value  == pytest.approx(0.09573765461229826)
    assert result.params['a'].value == pytest.approx(20907.860015655362)
    assert result.params['b'].value == pytest.approx(99.87703541031998)
    assert result.chisqr == pytest.approx(63472329.04707792)

