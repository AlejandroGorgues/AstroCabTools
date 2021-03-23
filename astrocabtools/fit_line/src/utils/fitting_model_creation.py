"""
Set of functions that allow to creathe the fitting from the model
"""
import numpy as np
import pandas as pd
import math
from astropy.modeling import models, fitting
from lmfit import Model


__all__ = ['calculate_slope', 'integrated_flux', 'calculate_intercept', 'gauss_fitting_function','lorentzian_fitting_function', 'line_fitting_function', 'quadratic_fitting_function']


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

#This functionality is not implemented yet
def lorentzian_fitting_function(x, h, c, sigma):
    """
    :param ndarray x: wavelength values
    :param float h: height of the lorentz
    :param float c: mean of the lorentz
    :param float sigma: FWHM of the lorentz
    :return: fitted model
    Function that create the lorentzian fitted model
    """
    return (h/math.pi)*(sigma/((x-c)**2 + sigma**2))

def line_fitting_function(x, a, b):
    """
    :param ndarray x: wavelength values
    :param float a: slope
    :param float b: intercept
    :return: fitted model
    Function that create a line fitted model
    """
    return a + b * (x)
#This functionality is not implemented yet
def quadratic_fitting_function(x, a, b, c2):
    """
    :param ndarray x: wavelength values
    :param float a: intercept
    :param float b: coefficient of symmetry
    :param float c2: coefficient of degree of the curvature
    :return: fitted model
    Function that create a quadratic fitted model
    """
    return a + b * (x) + c2*(x**2)


def integrated_flux(h, sigma, typeInt):
    if typeInt == 'gauss':
        return h*abs(sigma)*math.sqrt(2*math.pi)
    elif typeInt == 'lorentz':
        return h*math.pi*sigma

def calculate_slope(xOrigin, yOrigin, xEnd, yEnd):
    return (yEnd - yOrigin) / (xEnd - xOrigin)

def calculate_intercept(slope, x, y):
    return y - slope*x
