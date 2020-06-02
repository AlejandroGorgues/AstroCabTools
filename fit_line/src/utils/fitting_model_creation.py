"""
Set of functions that allow to creathe the fitting from the model
"""
import numpy as np
import pandas as pd
import math
from astropy.modeling import models, fitting
from lmfit import Model


__all__ = ['curve_fitting', 'double_curve_fitting', 'calculate_slope', 'integrated_flux', 'calculate_intercept', 'gauss_fitting_function', 'gauss_fitting_function2', 'line_fitting_function']

def curve_fitting(wavelength, flux, guesses):
    gmodel = Model(gauss_fitting_function ) + Model(line_fitting_function)
    params = gmodel.make_params(a=guesses['a'], b=guesses['b'], h=guesses['h'], c=guesses['c'],sigma=guesses['sigma'])
    result = gmodel.fit(flux, params, x=wavelength)
    return result

def double_curve_fitting(wavelength, flux, guesses):
    gmodel = Model(line_fitting_function) + Model(gauss_fitting_function) + Model(gauss_fitting_function2)
    params = gmodel.make_params(a=guesses['a'], b=guesses['b'], h=guesses['h'], c=guesses['c'],sigma=guesses['sigma'], h2=guesses['h2'], c2=guesses['c2'],sigma2=guesses['sigma2'])
    result = gmodel.fit(flux, params, x=wavelength)
    return result

def gauss_fitting_function(x, h, c, sigma):
    return h * math.e ** ((x-c)**2/(-2*sigma**2))

def gauss_fitting_function2(x, h2, c2, sigma2):
    return h2 * math.e ** ((x-c2)**2/(-2*sigma2**2))

def line_fitting_function(x, a, b):
    return a + b * (x)

def integrated_flux(h, sigma):
    return h*sigma*math.sqrt(2*math.pi)

def calculate_slope(xOrigin, yOrigin, xEnd, yEnd):
    return (yEnd - yOrigin) / (xEnd - xOrigin)

def calculate_intercept(slope, x, y):
    return y - slope*x
