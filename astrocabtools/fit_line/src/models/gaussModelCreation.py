"""
Class that contains the structure and operations to generate a gaussian fitted
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

from .gaussPointsData import gaussPointsData
from .linePointsData import linePointsData
from .exponentialPointsData import exponentialPointsData
from .powerLawPointsData import powerLawPointsData
from .quadraticPointsData import quadraticPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, gauss_fitting_function, line_fitting_function, quadratic_fitting_function, exponential_fitting_function, powerLaw_fitting_function

__all__ = ['gaussModel']

class gaussModel:

    def __init__(self, textLines, typeCont, parent=None):
        super().__init__()

        if typeCont == 'line':
            self.__continuumFitPoints = linePointsData(leftX=0.0, rightX=0.0, leftY=0.0, rightY=0.0)
        elif typeCont == 'quadratic':
            self.__continuumFitPoints = quadraticPointsData(leftX=0.0, rightX=0.0, leftY=0.0, rightY=0.0, c2=0.0)
        elif typeCont == 'exponential':
            self.__continuumFitPoints = exponentialPointsData(leftX=0.0, rightX=0.0, leftY=0.0, rightY=0.0)
        elif typeCont == 'powerLaw':
            self.__continuumFitPoints = powerLawPointsData(leftX=0.0, rightX=0.0, leftY=0.0, rightY=0.0)

        self.__gaussFitPoints = gaussPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__gaussDict = {}
        self.__gaussDeque = deque()
        self.__lines = []
        self.__markers = []
        self.__textLines = textLines
        self.__typeCont = typeCont

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
        continuumFitDict = self.__continuumFitPoints.asdict()
        gaussFitDict = self.__gaussFitPoints.asdict()

        """
        Merge two dicts to simplify the use in the iterative process and
        in case of duplicate parameters on both
        """
        self.__gaussDict = gaussFitDict.update(continuumFitDict) or gaussFitDict

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        self.__gaussDeque.append((xdata, ydata))

        return self.__textLines


    def _generate_initial_gauss_model(self,wavelengthValues, h, c, sigma):
        y_values = []
        for x in wavelengthValues:
            y_values.append(gauss_fitting_function(x, h, c, sigma))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        if self.__typeCont == 'quadratic':
            self.__gaussDeque.append(1)
        for i, key in enumerate(self.__gaussDict.keys()):
            self.__gaussDict[key] = self.__gaussDeque[i]

        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__gaussDict['left'][0]) & (wavelength <= self.__gaussDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]
        gauss = Model(gauss_fitting_function, name= 'model1')

        h = self.__gaussDict['top'][1] - (self.__gaussDict['left'][1] + self.__gaussDict['right'][1])/2.
        c = self.__gaussDict['top'][0]
        sigma = abs(self.__gaussDict['sigma2'][0]-self.__gaussDict['sigma1'][0])/2.355

        initial_y_values = self._generate_initial_gauss_model(wavelengthValues, h,c,sigma)

        if self.__typeCont == 'line':

            b = calculate_slope(self.__gaussDict['left'][0], self.__gaussDict['left'][1],self.__gaussDict['right'][0], self.__gaussDict['right'][1])
            a = calculate_intercept(b, self.__gaussDict['left'][0], self.__gaussDict['left'][1])

            line = Model(line_fitting_function, name='continuum_fitting_function')

            gauss_model = gauss + line

            params = gauss_model.make_params(h = h,
                                             c = c,
                                             sigma=sigma,
                                             a=a,
                                             b=b)

            init = gauss_model.eval(params, x=wavelengthValues)
            result = gauss_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
            resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['h'].value, result.params['sigma'].value, 'gauss'))

            gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in gaussFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)


            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'quadratic':

            b = calculate_slope(self.__gaussDict['left'][0], self.__gaussDict['left'][1],self.__gaussDict['right'][0], self.__gaussDict['right'][1])
            a = calculate_intercept(b, self.__gaussDict['left'][0], self.__gaussDict['left'][1])
            c2 = 1.

            quadratic = Model(quadratic_fitting_function, name= 'continuum_fitting_function')

            gauss_model = gauss + quadratic

            params = gauss_model.make_params(h = h,
                                             c = c,
                                             sigma=sigma,
                                             a=a,
                                             b=b,
                                             c2=c2)

            init = gauss_model.eval(params, x=wavelengthValues)
            result = gauss_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Quadratic model: {} + {} * x + {}*x**2".format(str(result.params['a'].value), str(result.params['b'].value), str(result.params['c2'].value))
            resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['h'].value, result.params['sigma'].value, 'gauss'))

            gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in gaussFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None
        elif self.__typeCont == 'exponential':

            tau = (self.__gaussDict['right'][0] - self.__gaussDict['left'][0])/np.log(self.__gaussDict['left'][1]/self.__gaussDict['right'][1])
            A = self.__gaussDict['left'][1]/math.e**(-self.__gaussDict['left'][0]/tau)

            exponential = Model(exponential_fitting_function, name= 'continuum_fitting_function')

            gauss_model = gauss + exponential

            params = gauss_model.make_params(h = h,
                                             c = c,
                                             sigma=sigma,
                                             tau=tau,
                                             A_exp=A)

            init = gauss_model.eval(params, x=wavelengthValues)
            result = gauss_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Exponential model: {} * e**(-x/{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))
            resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['h'].value, result.params['sigma'].value, 'gauss'))

            gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in gaussFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'powerLaw':

            k = math.log10(self.__gaussDict['left'][1]/self.__gaussDict['right'][1])/math.log10(self.__gaussDict['left'][0]/self.__gaussDict['right'][0])
            A = self.__gaussDict['left'][1]/(self.__gaussDict['left'][0]**k)

            powerLaw = Model(powerLaw_fitting_function, name= 'continuum_fitting_function')

            gauss_model = gauss + powerLaw

            params = gauss_model.make_params(h = h,
                                             c = c,
                                             sigma=sigma,
                                             k=k,
                                             A_pow=A)

            init = gauss_model.eval(params, x=wavelengthValues)
            result = gauss_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Power law model: {} * x**{}".format(str(result.params['A_pow'].value), str(result.params['k'].value))
            resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['h'].value, result.params['sigma'].value, 'gauss'))

            gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in gaussFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None
