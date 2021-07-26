"""
Set of functions that allow to creathe the fitting from the model
"""
import numpy as np
import pandas as pd
import math
import cmath
from scipy.special import erfc
from scipy.special import wofz
from astropy.modeling import models, fitting
from lmfit import Model


__all__ = ['calculate_slope', 'integrated_flux', 'calculate_intercept', 'gauss_fitting_function','lorentzian_fitting_function', 'voigt_fitting_function', 'pseudoVoigt_fitting_function', 'moffat_fitting_function', 'line_fitting_function', 'quadratic_fitting_function', 'exponential_fitting_function', 'powerLaw_fitting_function']


def gauss_fitting_function(x, h, c, sigma):
    """
    :param ndarray x: wavelength values
    :param float h: height of the guassian
    :param float c: mean of the gaussian
    :param float sigma: FWHM of the gaussian
    :return: fitted model
    Function that create only one gaussian fitted model
    """
    return h * math.e ** ((x-c)**2./(-2.*sigma**2.))

def lorentzian_fitting_function(x, h, c, sigma):
    """
    :param ndarray x: wavelength values
    :param float h: height of the lorentz
    :param float c: mean of the lorentz
    :param float sigma: FWHM of the lorentz
    :return: fitted model
    Function that create the lorentzian fitted model
    using https://en.wikipedia.org/wiki/Cauchy_distribution#Characterisation
    """
    return h*(sigma**2. /((x-c)**2. + sigma**2.))

def voigt_fitting_function(x, A, c, sigma, gamma):
    """
    :param ndarray x: wavelength values
    :param float A: amplitude of the voigt model
    :param float c: mean of the voigt model
    :param float sigma: FWHM of the voigt model
    :param float gamma: variable but constrained to sigma
    :return: fitted model
    Function that create the voigt fitted model
    using https://lmfit.github.io/lmfit-py/builtin_models.html#voigtmodel
    """
    z = (x -c + 1j*gamma)/max(1.0e-15, (sigma*math.sqrt(2.0)))
    return A*wofz(z).real/max(1.0e-15, (sigma*math.sqrt(2*math.pi)))

def pseudoVoigt_fitting_function(x, A, c, sigma, fraction):
    """
    :param ndarray x: wavelength values
    :param float A: amplitude of the voigt model
    :param float c: mean of the voigt model
    :param float sigma: FWHM of the voigt model
    :param float fraction: fraction that controls the relative weight of the gauss and lorentz model
    :return: fitted model
    Function that create the pseudoVoigt fitted model
    using https://lmfit.github.io/lmfit-py/builtin_models.html#lmfit.models.PseudoVoigtModel
    """
    sigma_g = sigma/math.sqrt(2.*math.log(2))
    gaussian_dist = ((A/max(1.0e-15, math.sqrt(2*math.pi)*sigma_g))) * math.e**(-(1.0*x - c)**2/max(1.0e-15, (2*sigma_g**2)))
    lorentzian_dist = (A/(1+((1.0*x - c)/max(1.0e-15, sigma))**2)) /max(1.0e-15, (math.pi*sigma))

    return (1-fraction)*gaussian_dist + fraction*lorentzian_dist

def moffat_fitting_function(x, A, c, sigma, beta):
    """
    :param ndarray x: wavelength values
    :param float A: amplitude of the moffat model
    :param float c: mean of the moffat model
    :param float sigma: FWHM of the moffat model
    :param float beta: exponent parameter of the moffat model
    :return: fitted model
    Function that create the lorentzian fitted model
    using https://lmfit.github.io/lmfit-py/builtin_models.html#lmfit.models.MoffatModel
    """
    return A/(((x-c)/max(1.0e-15, sigma))**2. +1.)**beta


def line_fitting_function(x, a, b):
    """
    :param ndarray x: wavelength values
    :param float a: slope
    :param float b: intercept
    :return: fitted model
    Function that create a line fitted model
    """
    return a + b * (x)

def quadratic_fitting_function(x, a, b, c2):
    """
    :param ndarray x: wavelength values
    :param float a: intercept
    :param float b: coefficient of symmetry
    :param float c2: coefficient of degree of the curvature
    :return: fitted model
    Function that create a quadratic fitted model
    """
    return a + b * (x) + c2*(x**2.)

def exponential_fitting_function(x, A_exp, tau):
    """
    :param ndarray x: wavelength values
    :param float A: amplitude of the model
    :param float tau: decay of the model
    :return: fitted model
    Function that create an exponential fitted model
    """
    return A_exp*math.e**(-1.*x/tau)

def powerLaw_fitting_function(x, A_pow, k):
    """
    :param ndarray x: wavelength values
    :param float A: amplitude of the model
    :param float k: exponent of the model
    :return: fitted model
    Function that create a power law fitted model
    """
    return A_pow*x**k

def integrated_flux(h, sigma, typeInt):
    if typeInt == 'gauss':
        return h*abs(sigma)*math.sqrt(2.*math.pi)
    elif typeInt == 'lorentz':
        return h*math.pi*sigma
    elif typeInt == 'voigt':
        return h*3.6013*sigma
    elif typeInt == 'pseudoVoigt':
        return h*2.*sigma
    elif typeInt == 'moffat':
        return h*2.*sigma

def calculate_slope(xOrigin, yOrigin, xEnd, yEnd):
    return (yEnd - yOrigin) / (xEnd - xOrigin)

def calculate_intercept(slope, x, y):
    return y - slope*x
