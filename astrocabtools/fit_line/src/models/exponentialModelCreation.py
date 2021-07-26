"""
Class that contains the structure and operations to generate a line fitted
model
"""
import numpy as np
import pandas as pd
import math

from lmfit import Parameters, Model

import sys
import traceback
import io

from collections import deque

from .exponentialPointsData import exponentialPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, exponential_fitting_function

__all__ = ['exponentialModel']

class exponentialModel:

    def __init__(self, textLines, typeCont, parent=None):
        super().__init__()

        self.__exponentialFitPoints = exponentialPointsData(leftX=0.0, rightX=0.0, leftY=0.0, rightY=0.0)

        self.__exponentialDict = {}
        self.__exponentialDeque = deque()
        self.__lines = []
        self.__markers = []
        self.__textLines = textLines

    @property
    def lines(self):
        return self.__lines

    @property
    def markers(self):
        return self.__markers

    @lines.setter
    def lines(self, figure):
        self.__lines.append(figure)

    @markers.setter
    def markers(self, marker):
        self.__markers.append(marker)

    def del_marker(self, marker):
        self.__markers.remove(marker)

    def del_line(self, line):
        self.__lines.remove(line)

    def init_data_points(self):
        self.__exponentialDict = self.__exponentialFitPoints.asdict()

        """
        Merge two dicts to simplify the use in the iterative process and
        in case of duplicate parameters on both
        """

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        self.__exponentialDeque.append((xdata, ydata))

        return self.__textLines


    def _generate_initial_exponential_model(self,wavelengthValues, a, b):
        y_values = []
        for x in wavelengthValues:
            y_values.append(exponential_fitting_function(x, a, b))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        for i, key in enumerate(self.__exponentialDict.keys()):
            self.__exponentialDict[key] = self.__exponentialDeque[i]

        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__exponentialDict['left'][0]) & (wavelength <= self.__exponentialDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]
        exponential_model = Model(exponential_fitting_function, name= 'model1')

        tau = (self.__exponentialDict['right'][0] - self.__exponentialDict['left'][0])/np.log(self.__exponentialDict['left'][1]/self.__exponentialDict['right'][1])

        A = self.__exponentialDict['left'][1]/math.e**(-1*self.__exponentialDict['left'][0]/tau)

        inital_y_values = self._generate_initial_exponential_model(wavelengthValues, tau, A)

        params = exponential_model.make_params(A_exp=A, tau=tau)

        init = exponential_model.eval(params, x=wavelengthValues)
        result = exponential_model.fit(fluxValues, params, x=wavelengthValues, nan_policy='omit')

        #Update table of results parameters
        resultText = "Path: {}".format(path)
        resultText = resultText + "\n" + \
            "Exponential model: {} * e**(-x/{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))

        exponentialFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

        for resultParams in exponentialFitResultList:
            resultText = resultText + "\n" + resultParams
        resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

        return result, resultText, wavelengthValues, fluxValues, inital_y_values, None
