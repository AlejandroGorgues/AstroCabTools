"""
Class that contains the structure and operations to generate a two gaussian fitted
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
from .lorentzPointsData import lorentzPointsData
from .linePointsData import linePointsData
from .quadraticPointsData import quadraticPointsData
from .exponentialPointsData import exponentialPointsData
from .powerLawPointsData import powerLawPointsData

from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, gauss_fitting_function, lorentzian_fitting_function, line_fitting_function, quadratic_fitting_function, exponential_fitting_function, powerLaw_fitting_function

__all__ = ['lorentzGaussModel']

class lorentzGaussModel:

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

        self.__gaussFitPoints = gaussPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0,leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__lorentzFitPoints = lorentzPointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0,leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__modelDict = {}
        self.__modelDeque = deque()
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
        gaussFitDict = self.__gaussFitPoints.asdict(prefix='p1_')
        lorentzFitDict = self.__lorentzFitPoints.asdict('p2_')


        gaussFitDict.update(lorentzFitDict)
        self.__modelDict = gaussFitDict.update(continuumFitDict) or gaussFitDict

        self.__textLines = iter(self.__textLines)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        self.__modelDeque.append((xdata, ydata))

        return self.__textLines

    def _generate_initial_gauss_model(self,wavelengthValues, h, c, sigma):
        y_values = []
        for x in wavelengthValues:
            y_values.append(gauss_fitting_function(x, h, c, sigma))
        return y_values

    def _generate_initial_lorentz_model(self,wavelengthValues, h, c, sigma):
        y_values = []
        for x in wavelengthValues:
            y_values.append(lorentzian_fitting_function(x, h, c, sigma))
        return y_values

    def draw_model_fit(self, path, wavelength, flux):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""
        if self.__typeCont == 'quadratic':
             self.__modelDeque.append(1)
        for i, key in enumerate(self.__modelDict.keys()):
            self.__modelDict[key] = self.__modelDeque[i]
        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__modelDict['left'][0]) & (wavelength <= self.__modelDict['right'][0])]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]

        gauss = Model(gauss_fitting_function, prefix='p1_', name = 'model2')
        lorentz = Model(lorentzian_fitting_function, prefix='p2_', name = 'model1')


        p1_h = self.__modelDict['p1_top'][1] - (self.__modelDict['left'][1] + self.__modelDict['right'][1])/2.
        p1_c = self.__modelDict['p1_top'][0]
        p1_sigma=abs(self.__modelDict['p1_sigma2'][0]-self.__modelDict['p1_sigma1'][0])/2.355
        p2_h=self.__modelDict['p2_top'][1] - (self.__modelDict['left'][1] + self.__modelDict['right'][1])/2.
        p2_c=self.__modelDict['p2_top'][0]
        p2_sigma=abs(self.__modelDict['p2_sigma2'][0]-self.__modelDict['p2_sigma1'][0])/2.

        #Obtain the initial values of the gaussian model to be drawn
        initial_y1_values = self._generate_initial_lorentz_model(wavelengthValues, p1_h, p1_c, p1_sigma)
        initial_y2_values = self._generate_initial_gauss_model(wavelengthValues, p2_h, p2_c, p2_sigma)

        #Check type of continuum used
        if self.__typeCont == 'line':

            b = calculate_slope(self.__modelDict['left'][0], self.__modelDict['left'][1],self.__modelDict['right'][0], self.__modelDict['right'][1])
            a=calculate_intercept(b, self.__modelDict['left'][0], self.__modelDict['left'][1])

            line = Model(line_fitting_function, name = 'continuum_fitting_function')


            lorentzGauss_model = lorentz + gauss + line


            params = lorentzGauss_model.make_params(p1_h = p1_h,
                                             p1_c = p1_c,
                                             p1_sigma= p1_sigma,
                                             p2_h= p2_h,
                                             p2_c= p2_c,
                                             p2_sigma= p2_sigma,
                                             a= a,
                                             b= b)


            init = lorentzGauss_model.eval(params, x=wavelengthValues)
            result = lorentzGauss_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Lorentz model: (2*{}*{}/pi)*({}/(x-{})**2 + {}**2)".format(str(result.params['p1_sigma'].    value), str(result.params['p1_h'].value), str(result.params['p1_sigma'].value), str(result.params['p1_c'].value)    , str(result.params['p1_sigma'].value))
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['p2_h'].value), str(result.params['p2_c'].value), str(result.params['p2_sigma'].value))

            resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
            resultText = resultText + "\n" + "Lorentz integrated flux : "+ " = " + str(integrated_flux(result.params['p1_h'].value, result.params['p1_sigma'].value, 'lorentz'))

            lorentzGaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in lorentzGaussFitResultList:
                if resultParams.startswith('p2_h'):
                    resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['p2_h'].value, result.params['p2_sigma'].value, 'gauss'))
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values

        elif self.__typeCont == 'quadratic':
            b = calculate_slope(self.__modelDict['left'][0], self.__modelDict['left'][1],self.__modelDict['right'][0], self.__modelDict['right'][1])
            a=calculate_intercept(b, self.__modelDict['left'][0], self.__modelDict['left'][1])
            c2 = 1.

            quadratic = Model(quadratic_fitting_function, name= 'continuum_fitting_function')

            lorentzGauss_model = lorentz + gauss + quadratic

            params = lorentzGauss_model.make_params(p1_h = p1_h,
                                             p1_c = p1_c,
                                             p1_sigma= p1_sigma,
                                             p2_h= p2_h,
                                             p2_c= p2_c,
                                             p2_sigma= p2_sigma,
                                             a= a,
                                             b= b,
                                             c2= c2)


            init = lorentzGauss_model.eval(params, x=wavelengthValues)
            result = lorentzGauss_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                "Lorentz model: (2*{}*{}/pi)*({}/(x-{})**2 + {}**2)".format(str(result.params['p1_sigma'].    value), str(result.params['p1_h'].value), str(result.params['p1_sigma'].value), str(result.params['p1_c'].value)    , str(result.params['p1_sigma'].value))
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['p2_h'].value), str(result.params['p2_c'].value), str(result.params['p2_sigma'].value))

            resultText = resultText + "\n" + "Quadratic model: {} + {} * x + {}*x**2".format(str(result.params['a'].value), str(result.params['b'].value), str(result.params['c2'].value))
            resultText = resultText + "\n" + "Lorentz integrated flux : "+ " = " + str(integrated_flux(result.params['p1_h'].value, result.params['p1_sigma'].value, 'lorentz'))


            lorentzGaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in lorentzGaussFitResultList:
                if resultParams.startswith('p2_h'):
                    resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['p2_h'].value, result.params['p2_sigma'].value, 'gauss'))
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values

        elif self.__typeCont == 'exponential':

            tau = (self.__modelDict['right'][0] - self.__modelDict['left'][0])/np.log(self.__modelDict['left'][1]/self.__modelDict['right'][1])
            A = self.__modelDict['left'][1]/math.e**(-self.__modelDict['left'][0]/tau)

            exponential = Model(exponential_fitting_function, name = 'continuum_fitting_function')


            lorentzGauss_model = lorentz + gauss + line


            params = lorentzGauss_model.make_params(p1_h = p1_h,
                                             p1_c = p1_c,
                                             p1_sigma= p1_sigma,
                                             p2_h= p2_h,
                                             p2_c= p2_c,
                                             p2_sigma= p2_sigma,
                                             A_exp=A,
                                             tau=tau)


            init = lorentzGauss_model.eval(params, x=wavelengthValues)
            result = lorentzGauss_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Lorentz model: (2*{}*{}/pi)*({}/(x-{})**2 + {}**2)".format(str(result.params['p1_sigma'].    value), str(result.params['p1_h'].value), str(result.params['p1_sigma'].value), str(result.params['p1_c'].value)    , str(result.params['p1_sigma'].value))
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['p2_h'].value), str(result.params['p2_c'].value), str(result.params['p2_sigma'].value))
            resultText = resultText + "\n" + "Exponential model: {} * e**(-x    /{})".format(str(result.params['A_exp'].value), str(result.params['tau'].value))
            resultText = resultText + "\n" + "Lorentz integrated flux : "+ " = " + str(integrated_flux(result.params['p1_h'].value, result.params['p1_sigma'].value, 'lorentz'))

            lorentzGaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in lorentzGaussFitResultList:
                if resultParams.startswith('p2_h'):
                    resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['p2_h'].value, result.params['p2_sigma'].value, 'gauss'))
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values

        elif self.__typeCont == 'powerLaw':

            k = math.log10(self.__modelDict['left'][1]/self.__modelDict['right'][1])/math.log10(self.__modelDict['left'][0]/self.__modelDict['right'][0])
            A = self.__modelDict['left'][1]/(self.__modelDict['left'][0]**k)

            powerLaw = Model(powerLaw_fitting_function, name = 'continuum_fitting_function')


            lorentzGauss_model = lorentz + gauss + powerLaw


            params = lorentzGauss_model.make_params(p1_h = p1_h,
                                             p1_c = p1_c,
                                             p1_sigma= p1_sigma,
                                             p2_h= p2_h,
                                             p2_c= p2_c,
                                             p2_sigma= p2_sigma,
                                             A_pow=A,
                                             k=k)


            init = lorentzGauss_model.eval(params, x=wavelengthValues)
            result = lorentzGauss_model.fit(fluxValues, params, x=wavelengthValues)

            #Update table of results parameters
            resultText = "Path: {}".format(path)
            resultText = resultText + "\n" + \
                    "Lorentz model: (2*{}*{}/pi)*({}/(x-{})**2 + {}**2)".format(str(result.params['p1_sigma'].    value), str(result.params['p1_h'].value), str(result.params['p1_sigma'].value), str(result.params['p1_c'].value)    , str(result.params['p1_sigma'].value))
            resultText = resultText + "\n" + \
                "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['p2_h'].value), str(result.params['p2_c'].value), str(result.params['p2_sigma'].value))
            resultText = resultText + "\n" + "Power law model: {} * x**{}".format(str(result.params['A_pow'].value), str(result.params['k'].value))
            resultText = resultText + "\n" + "Lorentz integrated flux : "+ " = " + str(integrated_flux(result.params['p1_h'].value, result.params['p1_sigma'].value, 'lorentz'))

            lorentzGaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

            for resultParams in lorentzGaussFitResultList:
                if resultParams.startswith('p2_h'):
                    resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['p2_h'].value, result.params['p2_sigma'].value, 'gauss'))
                resultText = resultText + "\n" + resultParams
            resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
            return result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values
