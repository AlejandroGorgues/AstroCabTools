import os
import pytest

import pandas as pd
import numpy as np
import astropy.units as u
from astropy.constants import c

from astrotools.fit_line.src.utils.units_conversion import spectrumConversion


def test_um():
    sc = spectrumConversion()
    wavelength = sc.transform_wUnits(5.48, 'um')
    x = 5.48
    quantity_converted = x*u.micron
    assert wavelength.unit == quantity_converted.unit
    assert wavelength.value == pytest.approx(quantity_converted.value)

def test_aa_to_um():
    sc = spectrumConversion()
    wavelength = sc.transform_wUnits(5.48, 'angstroms')
    x = 0.000548
    quantity_converted = x*u.micron
    assert wavelength.unit == quantity_converted.unit
    assert wavelength.value == pytest.approx(quantity_converted.value)

def test_nm_to_um():
    sc = spectrumConversion()
    wavelength = sc.transform_wUnits(5.48, 'nm')
    x = 0.00548
    quantity_converted = x*u.micron
    assert wavelength.unit == quantity_converted.unit
    assert wavelength.value == pytest.approx(quantity_converted.value)

def test_Jy_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'Jy', 2.48)
    value = flux.value
    y = 2.671147e-09

    assert value == pytest.approx(y)

def test_mJy_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'mJy', 2.48)
    value = flux.value

    y = 2.6729968e-12

    assert value == pytest.approx(y)

def test_uJy_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'uJy', 2.48)
    value = flux.value

    y = 1.64286266984e-14

    assert value == pytest.approx(y)

def test_fluxWHz_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'W/m2/Hz', 2.48)
    value = flux.value
    y = 2.671147e+17 

    assert value == pytest.approx(y)

def test_fluxWAA_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'W/m2/Angstroms', 2.48)
    value = flux.value
    y = 54799999.99999999

    assert value == pytest.approx(y)

def test_fluxErgHz_to_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'erg/s/cm2/Hz', 2.48)
    value = flux.value
    y = 267114768119146.75 

    assert value == pytest.approx(y)

def test_fluxErgAAto_flam():
    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'erg/s/cm2/Angstroms', 2.48)
    value = flux.value
    y = 54799.99999999999

    assert value == y

def test_flam_to_flam():

    sc = spectrumConversion()
    flux = sc.transform_fUnits(5.48, 'erg/s/cm2/um', 2.48)
    value = flux.value
    y = 5.48

    assert value == pytest.approx(y)
