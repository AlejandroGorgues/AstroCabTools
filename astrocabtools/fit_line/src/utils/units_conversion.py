
"""
Class that change the values of the wavelength and the flux to
micron and u.erg/(u.s*u.cm**2*u.micron) respectively, to make it possible,
it use astropy units module

"""
import numpy as np
import math

from astropy import units as u
from astropy.constants import c

__all__=['spectrumConversion']

class spectrumConversion():

    def transform_wUnits(self, wValues_without_units, wUnits):
        """
        Transform the values with it's corresponding units to microns
        :param nparray wValues_without_units: array of wavelength values
        :param str wUnits: initial units of the wavelength values
        """
        wValues_with_units = 0
        nano = u.micron/1000

        if wUnits == 'nm':
            wValues = wValues_without_units*nano
            wValues_with_units = wValues.to(u.micron)

        elif wUnits == 'angstroms':
            wValues = wValues_without_units*u.Angstrom
            wValues_with_units = wValues.to(u.micron)

        else:
            wValues_with_units = wValues_without_units*u.micron

        return wValues_with_units

    def transform_fUnits(self, fValues_without_units, fUnits, wValues_with_units):
        """
        Transform the values with it's corresponding units to u.erg/(u.s*u.cm**2*u.micron)
        :param nparray fValues_without_units: array of flux values
        :param str fUnits: initial units of the flux values
        :param nparray wValues_with_units: array of wavelength values converted previously
        """
        fValues_with_units = 0
        fluxNormalized = u.erg/(u.s*u.cm**2*u.micron)
        FnuHertz = u.erg/(u.s*u.cm**2*u.Hz)

        c_transformed = 299792458000000.0*u.micron/u.s

        if fUnits == 'Jy':

            fValues = fValues_without_units*u.Jy

            fValues_with_units=(fValues).to(FnuHertz, equivalencies=u.spectral_density(wValues_with_units))
            fValues_with_units = (fValues_with_units*c_transformed)/(wValues_with_units**2)

        elif fUnits == 'mJy':
            mJy = u.Jy/1000
            fValues = fValues_without_units*mJy
            fValues_with_units=(fValues).to(FnuHertz, equivalencies=u.spectral_density(wValues_with_units))
            fValues_with_units = (fValues_with_units*c_transformed)/(wValues_with_units**2)

        elif fUnits == 'uJy':
            uJy = u.Jy/1000000
            fValues = fValues_without_units*uJy
            fValues_with_units=(fValues).to(FnuHertz, equivalencies=u.spectral_density(wValues_with_units))
            fValues_with_units = (fValues_with_units*c_transformed)/(wValues_with_units**2)

        elif fUnits == 'W/m2/Hz':
            fUnitsDensity = u.W/(u.m**2*u.Hz)
            fValues = fValues_without_units*fUnitsDensity
            fValues_with_units=(fValues).to(FnuHertz, equivalencies=u.spectral_density(wValues_with_units))
            fValues_with_units = (fValues_with_units*c_transformed)/(wValues_with_units**2)

        elif fUnits == 'W/m2/Angstroms':
            fUnitsAngstrom = u.W/(u.m**2*u.Angstrom)
            fValues = fValues_without_units*fUnitsAngstrom
            fValues_with_units=(fValues).to(fluxNormalized, equivalencies=u.spectral_density(wValues_with_units))

        elif fUnits == 'erg/s/cm2/Hz':
            fUnitsAstro = u.erg/(u.s*u.cm**2*u.Hz)
            fValues = fValues_without_units*fUnitsAstro
            fValues_with_units = (fValues*c_transformed)/(wValues_with_units**2)

        elif fUnits == 'erg/s/cm2/Angstroms':
            fUnitsAstro = u.erg/(u.s*u.cm**2*u.Angstrom)
            fValues = fValues_without_units*fUnitsAstro
            fValues_with_units=(fValues).to(fluxNormalized, equivalencies=u.spectral_density(wValues_with_units))

        else:
            fUnitsAstro = u.erg/(u.s*u.cm**2*u.micron)
            fValues_with_units = fValues_without_units*fUnitsAstro

        return fValues_with_units
