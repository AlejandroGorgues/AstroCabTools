"""
Class that contains the structure and operations to generate a two gaussian fitted
model
"""
import numpy as np
import pandas as pd

from lmfit import Parameters

import sys
import traceback
import io


from .pointsData import pointsData
from  astrocabtools.fit_line.src.utils.fitting_model_creation import calculate_intercept, calculate_slope, integrated_flux, double_curve_fitting, gauss_fitting_function

__all__ = ['doubleGaussModel']

class doubleGaussModel:

    def __init__(self, parent=None):
        super().__init__()
        self.__firsGaussFitPoints = pointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__secondGaussFitPoints = pointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)
        self.__maxCounter = 9
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
            self.__firsGaussFitPoints.leftX = xdata
            self.__firsGaussFitPoints.leftY = ydata

            self.__secondGaussFitPoints.leftX = xdata
            self.__secondGaussFitPoints.leftY = ydata
            self.__counter+= 1
            return "Mark second continium"

        elif self.__counter==2:

            self.__firsGaussFitPoints.rightX = xdata
            self.__firsGaussFitPoints.rightY = ydata

            self.__secondGaussFitPoints.rightX = xdata
            self.__secondGaussFitPoints.rightY = ydata
            self.__counter+= 1
            return "Mark first sigma from first gaussian"

        elif self.__counter==3:
            self.__firsGaussFitPoints.sigma1X = xdata
            self.__firsGaussFitPoints.sigma1Y = ydata
            self.__counter+= 1
            return "Mark second sigma from first gaussian"

        elif self.__counter==4:
            self.__firsGaussFitPoints.sigma2X = xdata
            self.__firsGaussFitPoints.sigma2Y = ydata
            self.__counter+= 1
            return "Mark top (center and height) from first gaussian"

        elif self.__counter==5:

            self.__firsGaussFitPoints.topX = xdata
            self.__firsGaussFitPoints.topY = ydata
            self.__counter+= 1
            return "Mark first sigma from second gaussian"

        elif self.__counter==6:

            self.__secondGaussFitPoints.sigma1X = xdata
            self.__secondGaussFitPoints.sigma1Y = ydata
            self.__counter+= 1
            return "Mark second sigma from second gaussian"

        elif self.__counter==7:

            self.__secondGaussFitPoints.sigma2X = xdata
            self.__secondGaussFitPoints.sigma2Y = ydata
            self.__counter+= 1
            return "Mark top (center and height) from second gaussian"

        else:

            self.__secondGaussFitPoints.topX = xdata
            self.__secondGaussFitPoints.topY = ydata
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
        wavelengthValues = wavelength[(wavelength >= self.__firsGaussFitPoints.leftX) & (wavelength <= self.__firsGaussFitPoints.rightX)]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(wavelength == np.amin(wavelengthValues))
        index2 = np.where(wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = flux[index1[0][0]:(index2[0][0]+1)]

        inital_y1_values = self._generate_initial_gauss_model(wavelengthValues, self.__firsGaussFitPoints.topY - (self.__firsGaussFitPoints.leftY + self.__firsGaussFitPoints.rightY)/2.,
            self.__firsGaussFitPoints.topX, abs(self.__firsGaussFitPoints.sigma2X - self.__firsGaussFitPoints.sigma1X)/2.355)

        inital_y2_values = self._generate_initial_gauss_model(wavelengthValues, self.__secondGaussFitPoints.topY - (self.__secondGaussFitPoints.leftY + self.__secondGaussFitPoints.rightY)/2.,
            self.__secondGaussFitPoints.topX, abs(self.__secondGaussFitPoints.sigma2X - self.__secondGaussFitPoints.sigma1X)/2.355)

        guesses = Parameters()
        guesses.add(name='a', value = calculate_intercept(calculate_slope(self.__firsGaussFitPoints.leftX,
            self.__firsGaussFitPoints.leftY,self.__firsGaussFitPoints.rightX,self.__firsGaussFitPoints.rightY), self.__firsGaussFitPoints.leftX, self.__firsGaussFitPoints.leftY))
        guesses.add(name='b', value = calculate_slope(self.__firsGaussFitPoints.leftX,
            self.__firsGaussFitPoints.leftY,self.__firsGaussFitPoints.rightX,self.__firsGaussFitPoints.rightY))

        guesses.add(name='h1', value = self.__firsGaussFitPoints.topY - (self.__firsGaussFitPoints.leftY + self.__firsGaussFitPoints.rightY)/2.)
        guesses.add(name='c1', value = self.__firsGaussFitPoints.topX)
        guesses.add(name='sigma1', value = abs(self.__firsGaussFitPoints.sigma2X-self.__firsGaussFitPoints.sigma1X)/2.355)

        guesses.add(name='h2', value = self.__secondGaussFitPoints.topY - (self.__secondGaussFitPoints.leftY + self.__secondGaussFitPoints.rightY)/2.)
        guesses.add(name='c2', value = self.__secondGaussFitPoints.topX)
        guesses.add(name='sigma2', value = abs(self.__secondGaussFitPoints.sigma2X-self.__secondGaussFitPoints.sigma1X)/2.355)
        #Obtain the model
        result = double_curve_fitting(wavelengthValues, fluxValues, guesses)
        #Update table of results parameters
        resultText = "Path: {}".format(path)
        resultText = resultText + "\n" + \
            "First gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h1'].value), str(result.params['c1'].value), str(result.params['sigma1'].value))
        resultText = resultText + "\n" + \
            "Second gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h2'].value), str(result.params['c2'].value), str(result.params['sigma2'].value))
        resultText = resultText + "\n" + "Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value))
        resultText = resultText + "\n" + "First guassian integrated flux : "+ " = " + str(integrated_flux(result.params['h1'].value, result.params['sigma1'].value))


        gaussFitResultList = [key + " = " + str(result.params[key].value) for key in result.params]

        for resultParams in gaussFitResultList:
            if resultParams.startswith('h2'):
                resultText = resultText + "\n" + "Second guassian integrated flux : "+ " = " + str(integrated_flux(result.params['h2'].value, result.params['sigma2'].value))
            resultText = resultText + "\n" + resultParams
        resultText = resultText + "\n" + "Chi-square" + " = " + str(result.chisqr)
        return result, resultText, wavelengthValues, fluxValues, inital_y1_values, inital_y2_values
