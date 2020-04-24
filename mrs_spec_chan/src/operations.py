import numpy as np
import pandas as pd

def transform_spectrum(data, z):
    """ Obtain wavelength and flux values. Transform and limit the range of values
    :param HDUList data: content of Fits file
    :param str z: redshift value
    :return : data transformed and limited
    """
    waveLengthL = []
    fluxL = []

    z = float(z)

    if z < 0:
        raise Exception('Redshift value {} must not be negative'.format(z))

    #Obtain the values of the emmited wavelength that are between 4.87 and 28.82
    wavelength = (data.iloc[:, 0]*(1.+z)).to_numpy()
    flux = (data.iloc[:, 1]*(1.+z)).to_numpy()
    flux = normalize_spectrum(waveLengthL, flux)

    wavelenghtValues,flux = zip(*sorted(zip(wavelength, flux)))

    wavelength = np.asarray(wavelength)
    flux = np.asarray(flux)

    wavelenghtValues = wavelength[(wavelength >= 0.) & (wavelength <= 30.)]

    #Obtain de indexes from the initial wavelength array
    #based on the min a max values of the slice made previously
    index1 = np.where(wavelength == np.amin(wavelenghtValues))
    index2 = np.where(wavelength == np.amax(wavelenghtValues))
    #Obtain the flux values between the indexes obtained previously
    fluxValues = flux[index1[0][0]:(index2[0][0]+1)]

    return wavelenghtValues, fluxValues, z

def divide_op_wavelength(opWave, z):
    """ Obtain optional wavelength values and make
    apply the redshift values
    :param str opWave: Optional wavelengths
    :param str z: Redshift value
    :return: list of wavelengths transformed
    """
    emWaveL = [float(e) for e in opWave.split(',')] if len(opWave) > 0 else []

    opWaveL = [self.transform_wavelength(emWaveL[n], z) for n in range(len(emWaveL))]
    return opWaveL

def normalize_spectrum(waveL, fluxL):
    """ Normalize the flux values based on the 10th element of the
    wavelength values
    :param list waveL: wavelength list
    :param list fluxL: flux list
    :return: flux list normalized
    """
    absDistArr = np.abs(waveL - 10)
    smallDiffIndex = absDistArr.argmin()

    return fluxL/fluxL[smallDiffIndex]
