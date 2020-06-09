"""
Set of functions that allow to creathe the fitting from the model
"""
import numpy as np
import pandas as pd
import math
from astropy.modeling import models, fitting
from lmfit import Model


__all__ = ['curve_fitting', 'double_curve_fitting', 'calculate_slope', 'integrated_flux', 'calculate_intercept', 'gauss_fitting_function','gauss_fitting_function1', 'gauss_fitting_function2', 'line_fitting_function']

def curve_fitting(wavelength, flux, guesses):
    gmodel = Model(gauss_fitting_function ) + Model(line_fitting_function)
    params = gmodel.make_params(h=guesses['h'], c=guesses['c'],sigma=guesses['sigma'], a=guesses['a'], b=guesses['b'])
    result = gmodel.fit(flux, params, x=wavelength)
    return result

def double_curve_fitting(wavelength, flux, guesses):
    gmodel = Model(gauss_fitting_function1) + Model(gauss_fitting_function2) + Model(line_fitting_function)
    params = gmodel.make_params(h1=guesses['h1'], c1=guesses['c1'],sigma1=guesses['sigma1'], h2=guesses['h2'], c2=guesses['c2'],sigma2=guesses['sigma2'],a=guesses['a'], b=guesses['b'])
    result = gmodel.fit(flux, params, x=wavelength)
    return result

def gauss_fitting_function(x, h, c, sigma):
    """
    :param ndarray x: wavelength values
    :param float h: height of the guassian
    :param float c: mean of the gaussian
    :param float sigma: FWHM of the gaussian
    :return: fitted model
    Function that create only one gaussian fitted model
    """
    return h * math.e ** ((x-c)**2/(-2*sigma**2))

def gauss_fitting_function1(x, h1, c1, sigma1):
    """
    :param ndarray x: wavelength values
    :param float h1: height of the guassian
    :param float c1: mean of the gaussian
    :param float sigma1: FWHM of the gaussian
    :return: fitted model
    Function that create the first gaussian fitted model
    from the two gaussian fitted model, which is the same as the first
    one, but it allows to differenciate the variable names that will be
    represented on the data visualization
    """
    return h1 * math.e ** ((x-c1)**2/(-2*sigma1**2))

def gauss_fitting_function2(x, h2, c2, sigma2):
    """
    :param ndarray x: wavelength values
    :param float h2: height of the guassian
    :param float c2: mean of the gaussian
    :param float sigma2: FWHM of the gaussian
    :return: fitted model
    Function that create the second gaussian fitted model
    from the two gaussian fitted model, which is the same as the first
    one, but it allows to differenciate the variable names that will be
    represented on the data visualization
    """
    return h2 * math.e ** ((x-c2)**2/(-2*sigma2**2))

def line_fitting_function(x, a, b):
    """
    :param ndarray x: wavelength values
    :param float a: slope
    :param float b: intercept
    :return: fitted model
    Function that create a line fitted model
    """
    return a + b * (x)

def integrated_flux(h, sigma):
    return h*sigma*math.sqrt(2*math.pi)

def calculate_slope(xOrigin, yOrigin, xEnd, yEnd):
    return (yEnd - yOrigin) / (xEnd - xOrigin)

def calculate_intercept(slope, x, y):
    return y - slope*x
