"""
Class that containts data related to the fits image
"""

__all__=['fitsClass']

class fitsClass:

    def __init__(self, currFrame, currIntegration, maxFrame, maxIntegration, shiftedXValue,shiftedYValue,
     fitsXCenter, fitsYCenter, fitsZUnit, maxXAxis, maxYAxis, filename ):
        self.__currFrame = currFrame
        self.__currIntegration = currIntegration
        self.__maxFrame = maxFrame
        self.__maxIntegration = maxIntegration
        self.__shiftedXValue = shiftedXValue
        self.__shiftedYValue = shiftedYValue
        self.__fitsXCenter = fitsXCenter
        self.__fitsYCenter = fitsYCenter
        self.__fitsZUnit = fitsZUnit
        self.__maxXAxis = maxXAxis
        self.__maxYAxis = maxYAxis
        self.__filename = filename

    @property
    def currFrame(self):
        return self.__currFrame

    @property
    def currIntegration(self):
        return self.__currIntegration

    @property
    def maxFrame(self):
        return self.__maxFrame

    @property
    def maxIntegration(self):
        return self.__maxIntegration

    @property
    def shiftedXValue(self):
        return self.__shiftedXValue

    @property
    def shiftedYValue(self):
        return self.__shiftedYValue

    @property
    def fitsXCenter(self):
        return self.__fitsXCenter

    @property
    def fitsYCenter(self):
        return self.__fitsYCenter

    @property
    def fitsZUnit(self):
        return self.__fitsZUnit

    @property
    def maxXAxis(self):
        return self.__maxXAxis

    @property
    def maxYAxis(self):
        return self.__maxYAxis

    @property
    def filename(self):
        return self.__filename

    @currFrame.setter
    def currFrame(self, currFrame):
        self.__currFrame = currFrame

    @currIntegration.setter
    def currIntegration(self, currIntegration):
        self.__currIntegration = currIntegration

    @maxFrame.setter
    def maxFrame(self, maxFrame):
        self.__maxFrame = maxFrame

    @maxIntegration.setter
    def maxIntegration(self, maxIntegration):
        self.__maxIntegration = maxIntegration

    @shiftedXValue.setter
    def shiftedXValue(self, shiftedXValue):
        self.__shiftedXValue = shiftedXValue

    @shiftedYValue.setter
    def shiftedYValue(self, shiftedYValue):
        self.__shiftedYValue = shiftedYValue

    @fitsXCenter.setter
    def fitsXCenter(self, fitsXCenter):
        self.__fitsXCenter = fitsXCenter

    @fitsYCenter.setter
    def fitsYCenter(self, fitsYCenter):
        self.__fitsYCenter = fitsYCenter

    @fitsZUnit.setter
    def fitsZUnit(self, fitsZUnit):
        self.__fitsZUnit = fitsZUnit

    @maxXAxis.setter
    def maxXAxis(self, maxXAxis):
        self.__maxXAxis = maxXAxis

    @maxYAxis.setter
    def maxYAxis(self, maxYAxis):
        self.__maxYAxis = maxYAxis

    @filename.setter
    def filename(self, filename):
        self.__filename = filename
