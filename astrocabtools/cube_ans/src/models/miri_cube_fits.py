"""
Class that containts data_cube related to the miri cube in the fits file"""

__all__=['miriCubeClass']

class miriCubeClass:

    def __init__(self, currSlice, maxSlice, cubeARValue,
                 cubeDValue, cubeWValue,cubeXCRVal, cubeYCRVal, cubeZCRVal, cubeWavelengthUnit, cubeFluxUnit, maxXAxis, maxYAxis, cubeXCPix, cubeYCPix, cubeZCPix, data_cube, filename):

        self.__currSlice = currSlice
        self.__maxSlice = maxSlice
        self.__cubeARValue = cubeARValue
        self.__cubeDValue = cubeDValue
        self.__cubeWValue = cubeWValue
        self.__cubeXCRVal = cubeXCRVal
        self.__cubeYCRVal = cubeYCRVal
        self.__cubeZCRVal = cubeZCRVal
        self.__cubeWavelengthUnit = cubeWavelengthUnit
        self.__cubeFluxUnit = cubeFluxUnit
        self.__maxXAxis = maxXAxis
        self.__maxYAxis = maxYAxis
        self.__cubeXCPix = cubeXCPix
        self.__cubeYCPix = cubeYCPix
        self.__cubeZCPix = cubeZCPix
        self.__data_cube = data_cube
        self.__filename = filename


        @property
        def currSlice(self):
            return self.__currSlice

        @property
        def maxSlice(self):
            return self.__maxSlice

        @property
        def cubeARValue(self):
            return self.__cubeARValue

        @property
        def cubeDValue(self):
            return self.__cubeDValue

        @property
        def cubeWValue(self):
            return self.__cubeWValue

        @property
        def cubeXCRVal(self):
            return self.__cubeXCRVal

        @property
        def cubeYCRVal(self):
            return self.__cubeYCRVal

        @property
        def cubeZCRVal(self):
            return self.__cubeZCRVal

        @property
        def cubeWavelengthUnit(self):
            return self.__cubeWavelengthUnit

        @property
        def cubeFluxUnit(self):
            return self.__cubeFluxUnit

        @property
        def maxXAxis(self):
            return self.__maxXAxis

        @property
        def maxYAxis(self):
            return self.__maxYAxis

        @property
        def cubeXCPix(self):
            return self.__cubeXCPix

        @property
        def cubeYCPix(self):
            return self.__cubeYCPix

        @property
        def cubeZCPix(self):
            return self.__cubeZCPix

        @property
        def data_cube(self):
            return self.__data_cube

        @property
        def filename(self):
            return self.__filename

        @currSlice.setter
        def currSlice(self, currSlice):
            self.__currSlice = currSlice

        @maxSlice.setter
        def maxSlice(self, maxSlice):
            self.__maxSlice = maxSlice

        @cubeARValue.setter
        def cubeARValue(self, cubeARValue):
            self.__cubeARValue = cubeARValue

        @cubeDValue.setter
        def cubeDValue(self, cubeDValue):
            self.__cubeDValue = cubeDValue

        @cubeWValue.setter
        def cubeWValue(self, cubeWValue):
            self.__cubeWValue = cubeWValue

        @cubeXCRVal.setter
        def cubeXCRVal(self, cubeXCRVal):
            self.__cubeXCRVal = cubeXCRVal

        @cubeYCRVal.setter
        def cubeYCRVal(self, cubeYCRVal):
            self.__cubeYCRVal = cubeYCRVal

        @cubeZCRVal.setter
        def cubeZCRVal(self, cubeZCRVal):
            self.__cubeZCRVal = cubeZCRVal

        @cubeWavelengthUnit.setter
        def cubeWavelengthUnit(self, cubeWavelenghtUnit):
            self.__cubeWavelengthUnit = cubeWavelengthUnit

        @cubeFluxUnit.setter
        def cubeFluxUnit(self, cubeFluxUnit):
            self.__cubeFluxUnit = cubeFluxUnit

        @maxXAxis.setter
        def maxXAxis(self, maxXAxis):
            self.__maxXAxis = maxXAxis

        @maxYAxis.setter
        def maxYAxis(self, maxYAxis):
            self.__maxYAxis = maxYAxis

        @cubeXCPix.setter
        def cubeXCPix(self, cubeXCPix):
            self.__cubeXCPix = cubeXCPix

        @cubeYCPix.setter
        def cubeYCPix(self, cubeYCPix):
            self.__cubeYCPix = cubeYCPix

        @cubeZCPix.setter
        def cubeZCPix(self, cubeZCPix):
            self.__cubeZCPix = cubeZCPix

        @data_cube.setter
        def data_cube(self, data_cube):
            self.__data_cube = data_cube

        @filename.setter
        def filename(self, filename):
            self.__filename = filename
