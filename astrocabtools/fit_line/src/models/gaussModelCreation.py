"""
Class that contains the structure and operations to generate a gaussian fitted
model
"""
import numpy as np
import pandas as pd

from lmfit import Parameters

import sys
import traceback
import io

from .pointsData import pointsData
from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, curve_fitting, gauss_fitting_function

__all__ = ['gaussModel']

class gaussModel:

    def __init__(self, parent=None):
        super().__init__()
        self.__gaussFitPoints = pointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__maxCounter = 6
        self.__counter = 1
        self.__lines = []
        self.__markers = []


    @property
    def max_counter(self):
        return self.__maxCounter

    @property
    def counter(self):
        return self.__counter

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

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        if self.__counter==1:
            self.__gaussFitPoints.leftX = xdata
            self.__gaussFitPoints.leftY = ydata
            self.__counter+= 1
            return "Mark second continium"

        elif self.__counter==2:

            self.__gaussFitPoints.rightX = xdata
            self.__gaussFitPoints.rightY = ydata
            self.__counter+= 1
            return "Mark first sigma"

        elif self.__counter==3:
            self.__gaussFitPoints.sigma1X = xdata
            self.__gaussFitPoints.sigma1Y = ydata
            self.__counter+= 1
            return "Mark second sigma"

        elif self.__counter==4:
            self.__gaussFitPoints.sigma2X = xdata
            self.__gaussFitPoints.sigma2Y = ydata
            self.__counter+= 1
            return "Mark top (center and height)"

        else:

            self.__gaussFitPoints.topX = xdata
            self.__gaussFitPoints.topY = ydata
            self.__counter+= 1
            return ""

    def _generate_initial_gauss_model(self,wavelengthValues, h, c, sigma):
        y_values = []
        for x in wavelengthValues:
            y_values.append(gauss_fitting_function(x, h, c, sigma))
        return y_values




    def draw_gauss_curve_fit(self, path, wavelength, flux):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""

        #Obtain the wavelength values on given range
        wavelengthValues = wavelength[(wavelength >= self.__gaussFitPoints.leftX) & (wavelength <= self.__gaussFitPoints.rightX)]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]
        inital_y_values = self._generate_initial_gauss_model(wavelengthValues, self.__gaussFitPoints.topY - (self.__gaussFitPoints.leftY + self.__gaussFitPoints.rightY)/2.,
            self.__gaussFitPoints.topX, abs(self.__gaussFitPoints.sigma2X-self.__gaussFitPoints.sigma1X)/2.355)

        guesses = Parameters()
        guesses.add(name='a', value = calculate_intercept(calculate_slope(self.__gaussFitPoints.leftX,
            self.__gaussFitPoints.leftY,self.__gaussFitPoints.rightX,self.__gaussFitPoints.rightY), self.__gaussFitPoints.leftX, self.__gaussFitPoints.leftY))
        guesses.add(name='b', value = calculate_slope(self.__gaussFitPoints.leftX,
            self.__gaussFitPoints.leftY,self.__gaussFitPoints.rightX,self.__gaussFitPoints.rightY))
        guesses.add(name='h', value = self.__gaussFitPoints.topY - (self.__gaussFitPoints.leftY + self.__gaussFitPoints.rightY)/2.)
        guesses.add(name='c', value = self.__gaussFitPoints.topX)
        guesses.add(name='sigma', value = abs(self.__gaussFitPoints.sigma2X-self.__gaussFitPoints.sigma1X)/2.355)
        #Obtain the model
        result = curve_fitting(wavelengthValues, fluxValues, guesses)
        #Update table of results parameters
        resultText = "Path: {}".format(path)
        resultText = resultText + "\n" + \
            "Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['c'].value), str(result.params['sigma'].value))
        resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
        resultText = resultText + "\n" + "Gaussian integrated flux : "+ " = " + str(integrated_flux(result.params['h'].value, result.params['sigma'].value))

        gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

        for resultParams in gaussFitResultList:
            resultText = resultText + "\n" + resultParams
        resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)



        return result, resultText, wavelengthValues, fluxValues, inital_y_values, None
