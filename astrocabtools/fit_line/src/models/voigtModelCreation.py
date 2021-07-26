"""
Class that contains the structure and operations to generate a voigtian fitted
model
"""
import numpy as np
import pandas as pd

from lmfit import Parameters, Model

import sys
import traceback
import io

from collections import deque

from .voigtPointsData import voigtPointsData
from .linePointsData import linePointsData
from .quadraticPointsData import quadraticPointsData
from .exponentialPointsData import exponentialPointsData
from .powerLawPointsData import powerLawPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, voigt_fitting_function, line_fitting_function, quadratic_fitting_function, exponential_fitting_function, powerLaw_fitting_function

__all__ = ['voigtModel']

class voigtModel:

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

        self.__voigtFitPoints = voigtPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0, gamma=0.0)
        self.__voigtDict = {}
        self.__voigtDeque = deque()
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
        voigtFitDict = self.__voigtFitPoints.asdict()

        """
        Merge two dicts to simplify the use in the iterative process and
        in case of duplicate parameters on both
        """
        self.__voigtDict = voigtFitDict.update(continuumFitDict) or voigtFitDict

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """
        self.__voigtDeque.append((xdata, ydata))

        return self.__textLines


    def _generate_initial_voigt_model(self,wavelengthValues, A, c, sigma, gamma):
        y_values = []
        for x in wavelengthValues:
            y_values.append(voigt_fitting_function(x, A, c, sigma, gamma))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the voigt model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        if self.__typeCont == 'quadratic':
            self.__voigtDeque.append(1)

        self.__voigtDeque.append(1.)

        for i, key in enumerate(self.__voigtDict.keys()):
            self.__voigtDict[key] = self.__voigtDeque[i]
        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__voigtDict['left'][0]) & (wavelength <= self.__voigtDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]
        voigt = Model(voigt_fitting_function, name= 'model1')

        c = self.__voigtDict['top'][0]
        sigma=abs(self.__voigtDict['sigma2'][1]-self.__voigtDict['sigma1'][1])/3.6013
        A = (self.__voigtDict['top'][1] - (self.__voigtDict['left'][1] + self.__voigtDict['right'][1])/2.) *3.6013* sigma
        gamma = sigma
        initial_y_values = self._generate_initial_voigt_model(wavelengthValues, A, c, sigma, gamma)

        if self.__typeCont == 'line':
            b = calculate_slope(self.__voigtDict['left'][0], self.__voigtDict['left'][1],self.__voigtDict['right'][0], self.__voigtDict['right'][1])
            a=calculate_intercept(b, self.__voigtDict['left'][0], self.__voigtDict['left'][1])

            line = Model(line_fitting_function, name='continuum_fitting_function')

            voigt_model = voigt + line
            params = voigt_model.make_params(A = A,
                                             c = c,
                                             sigma= sigma,
                                             gamma = gamma,
                                             a= a,
                                             b= b)
            init = voigt_model.eval(params, x=wavelengthValues)
            result = voigt_model.fit(fluxValues, params, x=wavelengthValues, nan_policy='omit')

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "z: (x - {} + i*{})/(sigma * sqrt(2)".format(str(result.params['c'].value), str(result.params['gamma'].value))
            resultText = resultText + "\n" + \
                "Voigt model: ({} * Re[e**(-z**2)*erfc(-i*z)])/({} * sqrt(2*pi))".format(str(result.params['A'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
            resultText = resultText + "\n" + "Voigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'voigt'))

            voigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in voigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'quadratic':

            b = calculate_slope(self.__voigtDict['left'][0], self.__voigtDict['left'][1],self.__voigtDict['right'][0], self.__voigtDict['right'][1])
            a=calculate_intercept(b, self.__voigtDict['left'][0], self.__voigtDict['left'][1])
            c2 = 1.

            quadratic = Model(quadratic_fitting_function, name= 'continuum_fitting_function')

            voigt_model = voigt + quadratic

            params = voigt_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             gamma = gamma,
                                             a=a,
                                             b=b,
                                             c2= c2)

            init = voigt_model.eval(params, x=wavelengthValues)
            result = voigt_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "z: (x - {} + i*{})/(sigma * sqrt(2)".format(str(result.params['c'].value), str(result.params['gamma'].value))
            resultText = resultText + "\n" + \
                "Voigt model: ({} * Re[e**(-z**2)*erfc(-i*z)])/({} * sqrt(2*pi))".format(str(result.params['A'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Quadratic model: {} + {} * x + {}*x**2".format(str(result.params['a'].value), str(result.params['b'].value), str(result.params['c2'].value))
            resultText = resultText + "\n" + "Voigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'voigt'))

            voigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in voigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'exponential':

            tau = (self.__voigtDict['right'][0] - self.__voigtDict['left'][0])/np.log(self.__voigtDict['left'][1]/self.__voigtDict['right'][1])
            A_exp = self.__voigtDict['left'][1]/math.e**(-self.__voigtDict['left'][0]/tau)

            exponential = Model(exponential_fitting_function, name= 'continuum_fitting_function')

            voigt_model = voigt + exponential

            params = voigt_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             gamma=gamma,
                                             A_exp = A_exp,
                                             tau=tau)

            init = voigt_model.eval(params, x=wavelengthValues)
            result = voigt_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "z: (x - {} + i*{})/(sigma * sqrt(2)".format(str(result.params['c'].value), str(result.params['gamma'].value))
            resultText = resultText + "\n" + \
                "Voigt model: ({} * Re[e**(-z**2)*erfc(-i*z)])/({} * sqrt(2*pi))".format(str(result.params['A'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Exponential model: {} * e**(-x    /{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))
            resultText = resultText + "\n" + "Voigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'voigt'))

            voigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in voigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'powerLaw':

            k = math.log10(self.__voigtDict['left'][1]/self.__voigtDict['right'][1])/math.log10(self.__voigtDict['left'][0]/self.__voigtDict['right'][0])
            A_pow = self.__voigtDict['left'][1]/(self.__voigtDict['left'][0]**k)

            powerLaw = Model(powerLaw_fitting_function, name= 'continuum_fitting_function')

            voigt_model = voigt + powerLaw

            params = voigt_model.make_params(A = A,
                                             c = c,
                                             sigma=sigma,
                                             gamma = gamma,
                                             A_pow=A_pow,
                                             k=k)

            init = voigt_model.eval(params, x=wavelengthValues)
            result = voigt_model.fit(fluxValues, params, x=wavelengthValues)
            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "z: (x - {} + i*{})/(sigma * sqrt(2)".format(str(result.params['c'].value), str(result.params['gamma'].value))
            resultText = resultText + "\n" + \
                "Voigt model: ({} * Re[e**(-z**2)*erfc(-i*z)])/({} * sqrt(2*pi))".format(str(result.params['A'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + "Power law model: {} * x**{}".format(str(result.params['A_pow'].value), str(result.params['k'].value))
            resultText = resultText + "\n" + "Voigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'voigt'))

            voigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in voigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)

            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None
