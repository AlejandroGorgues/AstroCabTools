"""
Class that contains the structure and operations to generate a voigtian fitted
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

from .moffatPointsData import moffatPointsData
from .linePointsData import linePointsData
from .quadraticPointsData import quadraticPointsData
from .exponentialPointsData import exponentialPointsData
from .powerLawPointsData import powerLawPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, moffat_fitting_function, line_fitting_function, quadratic_fitting_function, exponential_fitting_function, powerLaw_fitting_function

__all__ = ['moffatModel']

class moffatModel:

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

        self.__moffatFitPoints = moffatPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0, beta=1.)
        self.__moffatDict = {}
        self.__moffatDeque = deque()
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
        moffatFitDict = self.__moffatFitPoints.asdict()

        """
        Merge two dicts to simplify the use in the iterative process and
        in case of duplicate parameters on both
        """
        self.__moffatDict = moffatFitDict.update(continuumFitDict) or moffatFitDict

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        self.__moffatDeque.append((xdata, ydata))

        return self.__textLines


    def _generate_initial_moffat_model(self,wavelengthValues, h, c, sigma, beta):
        y_values = []
        for x in wavelengthValues:
            y_values.append(moffat_fitting_function(x, h, c, sigma, beta))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the voigt model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        if self.__typeCont == 'quadratic':
            self.__moffatDeque.append(1)
        self.__moffatDeque.append(1)
        for i, key in enumerate(self.__moffatDict.keys()):
            self.__moffatDict[key] = self.__moffatDeque[i]

        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__moffatDict['left'][0]) & (wavelength <= self.__moffatDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]
        moffat = Model(moffat_fitting_function, name= 'model1')

        c = self.__moffatDict['top'][0]
        beta=self.__moffatDict['beta']
        sigma=abs(self.__moffatDict['sigma2'][0]-self.__moffatDict['sigma1'][0])*math.sqrt(2**(1/beta)-1)/2.
        A = (self.__moffatDict['top'][1] - (self.__moffatDict['left'][1] + self.__moffatDict['right'][1])/2.)*2*sigma

        initial_y_values = self._generate_initial_moffat_model(wavelengthValues, A, c, sigma, beta)

        if self.__typeCont == 'line':

            b = calculate_slope(self.__moffatDict['left'][0], self.__moffatDict['left'][1],self.__moffatDict['right'][0], self.__moffatDict['right'][1])
            a=calculate_intercept(b, self.__moffatDict['left'][0], self.__moffatDict['left'][1])

            line = Model(line_fitting_function, name='continuum_fitting_function')

            moffat_model = moffat + line

            params = moffat_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             beta=beta,
                                             a=a,
                                             b=b)

            init = moffat_model.eval(params, x=wavelengthValues)
            result = moffat_model.fit(fluxValues, params, x=wavelengthValues, nan_policy='omit')

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Moffat model: {} * (((x - {})/{}) **2 + 1) ** -{}".format(str(result.params['A'].value), str(result.params['c'].value), str(result.params['sigma'].value), str(result.params['beta'].value))
            resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
            resultText = resultText + "\n" + "Moffat integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'moffat'))

            moffatFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in moffatFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'quadratic':

            b = calculate_slope(self.__moffatDict['left'][0], self.__moffatDict['left'][1],self.__moffatDict['right'][0], self.__moffatDict['right'][1])
            a=calculate_intercept(b, self.__moffatDict['left'][0], self.__moffatDict['left'][1])
            c2 = 1.

            quadratic = Model(quadratic_fitting_function, name= 'continuum_fitting_function')

            moffat_model = moffat + quadratic

            params = moffat_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             beta=beta,
                                             a=a,
                                             b=b,
                                             c2=c2)

            init = moffat_model.eval(params, x=wavelengthValues)
            result = moffat_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Moffat model: {} * (((x - {})/{}) **2 + 1) ** -{}".format(str(result.params['A'].value), str(result.params['c'].value), str(result.params['sigma'].value), str(result.params['beta'].value))
            resultText = resultText + "\n" + "Quadratic model: {} + {} * x + {}*x**2".format(str(result.params['a'].value), str(result.params['b'].value), str(result.params['c2'].value))
            resultText = resultText + "\n" + "Moffat integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'moffat'))

            moffatFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in moffatFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'exponential':
            tau = (self.__moffatDict['right'][0] - self.__moffatDict['left'][0])/np.log(self.__moffatDict['left'][1]/self.__moffatDict['right'][1])
            A_exp = self.__moffatDict['left'][1]/math.e**(-self.__moffatDict['left'][0]/tau)

            exponential = Model(exponential_fitting_function, name='continuum_fitting_function')

            moffat_model = moffat + exponential

            params = moffat_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             beta=beta,
                                             A_exp=A_exp,
                                             tau=tau)

            init = moffat_model.eval(params, x=wavelengthValues)
            result = moffat_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Moffat model: {} * (((x - {})/{}) **2 + 1) ** -{}".format(str(result.params['A'].value), str(result.params['c'].value), str(result.params['sigma'].value), str(result.params['beta'].value))
            resultText = resultText + "\n" + "Exponential model: {} * e**(-x/{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))
            resultText = resultText + "\n" + "Moffat integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'moffat'))

            moffatFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in moffatFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'powerLaw':

            k = math.log10(self.__moffatDict['left'][1]/self.__moffatDict['right'][1])/math.log10(self.__moffatDict['left'][0]/self.__moffatDict['right'][0])
            A_pow = self.__moffatDict['left'][1]/(self.__moffatDict['left'][0]**k)

            powerLaw = Model(powerLaw_fitting_function, name='continuum_fitting_function')

            moffat_model = moffat + powerLaw

            params = moffat_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             beta=beta,
                                             A_pow=A_pow,
                                             k=k)

            init = moffat_model.eval(params, x=wavelengthValues)
            result = moffat_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Moffat model: {} * (((x - {})/{}) **2 + 1) ** -{}".format(str(result.params['A'].value), str(result.params['c'].value), str(result.params['sigma'].value), str(result.params['beta'].value))
            resultText = resultText + "\n" + "Power law model: {} * x**{}".format(str(result.params['A_pow'].value), str(result.params['k'].value))
            resultText = resultText + "\n" + "Moffat integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'moffat'))

            moffatFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in moffatFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

