"""
Class that contains the structure and operations to generate a two gaussian fitted
model
"""
import numpy as np
import pandas as pd

from lmfit import Parameters, Model

import sys
import traceback
import io

from collections import deque

from .pseudoVoigtPointsData import pseudoVoigtPointsData
from .linePointsData import linePointsData
from .quadraticPointsData import quadraticPointsData
from .exponentialPointsData import exponentialPointsData
from .powerLawPointsData import powerLawPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, pseudoVoigt_fitting_function, line_fitting_function, quadratic_fitting_function, exponential_fitting_function, powerLaw_fitting_function

__all__ = ['pseudoVoigtModel']

class pseudoVoigtModel:

    def __init__(self,textLines, typeCont,  parent=None):
        super().__init__()
        if typeCont == 'line':
            self.__continuumFitPoints = linePointsData(leftX=0.0,rightX=0.0,leftY=0.0,rightY=0.0)
        elif typeCont == 'quadratic':
            self.__continuumFitPoints = quadraticPointsData(leftX=0.0,rightX=0.0,leftY=0.0,rightY=0.0, c2=0.0)
        elif typeCont == 'exponential':
            self.__continuumFitPoints = exponentialPointsData(leftX=0.0,rightX=0.0,leftY=0.0,rightY=0.0)
        elif typeCont == 'powerLaw':
            self.__continuumFitPoints = powerLawPointsData(leftX=0.0,rightX=0.0,leftY=0.0,rightY=0.0)

        self.__pseudoVoigtFitPoints = pseudoVoigtPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0,leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0, fraction=0.5)
        self.__pseudoVoigtDict = {}
        self.__pseudoVoigtDeque = deque()
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
        pseudoVoigtFitDict = self.__pseudoVoigtFitPoints.asdict()

        self.__pseudoVoigtDict = pseudoVoigtFitDict.update(continuumFitDict) or pseudoVoigtFitDict

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        self.__pseudoVoigtDeque.append((xdata, ydata))

        return self.__textLines

    def _generate_initial_pseudoVoigt_model(self,wavelengthValues, A, c, sigma, fraction):
        y_values = []
        for x in wavelengthValues:
            y_values.append(pseudoVoigt_fitting_function(x, A, c, sigma, fraction))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        if self.__typeCont == 'quadratic':
             self.__pseudoVoigtDeque.append(1)
        self.__pseudoVoigtDeque.append(0.5)
        for i, key in enumerate(self.__pseudoVoigtDict.keys()):
            self.__pseudoVoigtDict[key] = self.__pseudoVoigtDeque[i]
        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__pseudoVoigtDict['left'][0]) & (wavelength <= self.__pseudoVoigtDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]

        pseudoVoigt = Model(pseudoVoigt_fitting_function, name = 'model1', nan_policy='omit')


        c = self.__pseudoVoigtDict['top'][0]
        sigma=abs(self.__pseudoVoigtDict['sigma2'][0]-self.__pseudoVoigtDict['sigma1'][0])/2.
        A = (self.__pseudoVoigtDict['top'][1] - (self.__pseudoVoigtDict['left'][1] + self.__pseudoVoigtDict['right'][1])/2.)*2.*sigma
        fraction=self.__pseudoVoigtDict['fraction']

        #Obtain the initial values of the gaussian model to be drawn
        initial_y_values = self._generate_initial_pseudoVoigt_model(wavelengthValues, A, c, sigma, fraction)

        #Check type of continuum used
        if self.__typeCont == 'line':

            b = calculate_slope(self.__pseudoVoigtDict['left'][0], self.__pseudoVoigtDict['left'][1],self.__pseudoVoigtDict['right'][0], self.__pseudoVoigtDict['right'][1])
            a=calculate_intercept(b, self.__pseudoVoigtDict['left'][0], self.__pseudoVoigtDict['left'][1])

            line = Model(line_fitting_function, name = 'continuum_fitting_function')

            pseudoVoigt_model = pseudoVoigt + line

            params = pseudoVoigt_model.make_params(A = A,
                                             c = c,
                                             sigma= sigma,
                                             fraction = fraction,
                                             a=a,
                                             b=b)


            init = pseudoVoigt_model.eval(params, x=wavelengthValues)
            result = pseudoVoigt_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Sigma subg: {}/sqrt(2* ln(2))".format(str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "Gaussian model: (((1 - {})*{})/(sigma_g * sqrt(2*pi))) * e **(-(x - {})**2 /(2*sigma_g)**2)".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['c'].value))
            resultText = resultText + "\n" + \
                    "Lorentzian model: (({} * {})/pi)*(sigma/((x - {})**2 + {}**2))".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['sigma'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "PseudoVoigt model: Gaussian model + Lorentzian model"
            resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
            resultText = resultText + "\n" + "PseudoVoigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'pseudoVoigt'))

            pseudoVoigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in pseudoVoigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'quadratic':

            b = calculate_slope(self.__pseudoVoigtDict['left'][0], self.__pseudoVoigtDict['left'][1],self.__pseudoVoigtDict['right'][0], self.__pseudoVoigtDict['right'][1])
            a=calculate_intercept(b, self.__pseudoVoigtDict['left'][0], self.__pseudoVoigtDict['left'][1])
            c2 = 1.

            quadratic = Model(quadratic_fitting_function, name= 'continuum_fitting_function')

            pseudoVoigt_model = pseudoVoigt + quadratic

            params = pseudoVoigt_model.make_params(A = A,
                                             c = c,
                                             sigma= sigma,
                                             fraction = fraction,
                                             a=a,
                                             b=b,
                                             c2 = c2)

            init = pseudoVoigt_model.eval(params, x=wavelengthValues)
            result = pseudoVoigt_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Sigma subg: {}/sqrt(2* ln(2))".format(str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "Gaussian model: (((1 - {})*{})/(sigma_g * sqrt(2*pi))) * e **(-(x - {})**2 /(2*sigma_g)**2)".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['c'].value))
            resultText = resultText + "\n" + \
                    "Lorentzian model: (({} * {})/pi)*(sigma/((x - {})**2 + {}**2))".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['sigma'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "PseudoVoigt model: Gaussian model + Lorentzian model"
            resultText = resultText + "\n" + "Quadratic model: {} + {} * x + {}*x**2".format(str(result.params['a'].value), str(result.params['b'].value), str(result.params['c2'].value))
            resultText = resultText + "\n" + "PseudoVoigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'pseudoVoigt'))


            pseudoVoigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in pseudoVoigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'exponential':

            tau = (self.__pseudoVoigtDict['right'][0] - self.__pseudoVoigtDict['left'][0])/np.log(self.__pseudoVoigtDict['left'][1]/self.__pseudoVoigtDict['right'][1])
            A_exp = self.__pseudoVoigtDict['left'][1]/math.e**(-self.__pseudoVoigtDict['left'][0]/tau)

            exponential = Model(exponential_fitting_function, name = 'continuum_fitting_function')

            pseudoVoigt_model = pseudoVoigt + exponential

            params = pseudoVoigt_model.make_params(A = A,
                                             c = c,
                                             sigma= sigma,
                                             fraction=fraction,
                                             A_exp=A_exp,
                                             tau=tau)


            init = pseudoVoigt_model.eval(params, x=wavelengthValues)
            result = pseudoVoigt_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Sigma subg: {}/sqrt(2* ln(2))".format(str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "Gaussian model: (((1 - {})*{})/(sigma_g * sqrt(2*pi))) * e **(-(x - {})**2 /(2*sigma_g)**2)".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['c'].value))
            resultText = resultText + "\n" + \
                    "Lorentzian model: (({} * {})/pi)*(sigma/((x - {})**2 + {}**2))".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['sigma'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "PseudoVoigt model: Gaussian model + Lorentzian model"
            resultText = resultText + "\n" + "Exponential model: {} * e**(-x    /{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))
            resultText = resultText + "\n" + "PseudoVoigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'pseudoVoigt'))

            pseudoVoigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in pseudoVoigtFitResultList:
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

        elif self.__typeCont == 'powerLaw':

            k = math.log10(self.__pseudoVoigtDict['left'][1]/self.__pseudoVoigtDict['right'][1])/math.log10(self.__pseudoVoigtDict['left'][0]/self.__pseudoVoigtDict['right'][0])
            A_pow = self.__pseudoVoigtDict['left'][1]/(self.__pseudoVoigtDict['left'][0]**k)

            powerLaw = Model(powerLaw_fitting_function, name = 'continuum_fitting_function')

            pseudoVoigt_model = pseudoVoigt + powerLaw

            params = pseudoVoigt_model.make_params(A = A,
                                             c = c,
                                             sigma= sigma,
                                             fraction = fraction,
                                             A_pow=A_pow,
                                             k=k)


            init = pseudoVoigt_model.eval(params, x=wavelengthValues)
            result = pseudoVoigt_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Sigma subg: {}/sqrt(2* ln(2))".format(str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "Gaussian model: (((1 - {})*{})/(sigma_g * sqrt(2*pi))) * e **(-(x - {})**2 /(2*sigma_g)**2)".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['c'].value))
            resultText = resultText + "\n" + \
                    "Lorentzian model: (({} * {})/pi)*(sigma/((x - {})**2 + {}**2))".format(str(result.params['fraction'].value), str(result.params['A'].value), str(result.params['sigma'].value), str(result.params['c'].value), str(result.params['sigma'].value))
            resultText = resultText + "\n" + \
                    "PseudoVoigt model: Gaussian model + Lorentzian model"
        resultText = resultText + "\n" + "Power law model: {} * x**{}".format(str(result.params['A_pow'].value), str(result.params['k'].value))
        resultText = resultText + "\n" + "PseudoVoigt integrated flux : "+ " = " + str(integrated_flux(result.params['A'].value, result.params['sigma'].value, 'pseudoVoigt'))

        pseudoVoigtFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

        for resultParams in pseudoVoigtFitResultList:
            resultText = resultText + "\n" + resultParams
        resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
        return result, resultText, wavelengthValues, fluxValues, initial_y_values, None

