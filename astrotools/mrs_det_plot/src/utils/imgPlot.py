"""
Class that contains data only to the image, not to the fits file
"""
__all__=['imgPlot']

class imgPlot:

    def __init__(self, xValues, yValues, zValues, maxFValue, minFValue):
        self.__xValues  = xValues
        self.__yValues  = yValues
        self.__zValues = zValues
        self.__maxFValue = maxFValue
        self.__minFValue = minFValue

    @property
    def xValues(self):
        return self.__xValues

    @property
    def yValues(self):
        return self.__yValues

    @property
    def zValues(self):
        return self.__zValues

    @property
    def maxFValue(self):
        return self.__maxFValue

    @property
    def minFValue(self):
        return self.__minFValue

    @xValues.setter
    def xValues(self, xValues):
        self.__xValues = xValues

    @yValues.setter
    def yValues(self, yValues):
        self.__yValues = yValues

    @zValues.setter
    def zValues(self, zValues):
        self.__zValues = zValues

    @maxFValue.setter
    def maxFValue(self, maxFValue):
        self.__maxFValue = maxFValue

    @minFValue.setter
    def minFValue(self, minFValue):
        self.__minFValue = minFValue
