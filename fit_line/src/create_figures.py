import numpy as np
import pandas as pd
import math
from astropy.modeling import models, fitting
from lmfit import Model

def curve_fitting(wavelength, flux, guesses):
    #gmodel = Model(gauss_curve_fitting_function)
    gmodel = Model(gauss_fitting_function ) + Model(line_fitting_function)
    params = gmodel.make_params(a=guesses['a'], b=guesses['b'], h=guesses['h'], meanL=guesses['c'], meanG=guesses['c'],sigma=guesses['sigma'])
    #params = gmodel.make_params(a=guesses['a'], b=guesses['b'], h=guesses['h'], c=guesses['c'],sigma=guesses['sigma'])
    result = gmodel.fit(flux, params, x=wavelength)

    return result

def gauss_fitting_function(x, h, meanG, sigma):
    return h * math.e ** ((x-meanG)**2/(-2*sigma**2))

def line_fitting_function(x, a, b, meanL):
    return a + b * (x)

def gauss_curve_fitting_function(x, a, b, h, c, sigma):

    return a + b * (x-c) + h * math.e ** ((x-c)**2/(-2*sigma**2))

def calculate_slope(xOrigin, yOrigin, xEnd, yEnd):
    return (yEnd - yOrigin) / (xEnd - xOrigin)

def calculate_intercept(slope, x, y):
    return y - slope*x
