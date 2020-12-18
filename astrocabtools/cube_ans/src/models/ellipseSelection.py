"""
Class that contains the basic coordinates of the ellipse to be drawed along all slices
"""

__all__= ['ellipse_selection']

class ellipse_selection:

    def __init__(self, centerX, centerY, aAxis, bAxis):
        self.__centerX = centerX
        self.__centerY = centerY
        self.__aAxis = aAxis
        self.__bAxis = bAxis

    @property
    def centerX(self):
        return self.__centerX

    @property
    def centerY(self):
        return self.__centerY

    @property
    def aAxis(self):
        return self.__aAxis

    @property
    def bAxis(self):
        return self.__bAxis

    @centerX.setter
    def centerX(self, centerX):
        self.__centerX = centerX

    @centerY.setter
    def centerY(self, centerY):
        self.__centerY = centerY

    @aAxis.setter
    def aAxis(self, aAxis):
        self.__aAxis = aAxis

    @bAxis.setter
    def bAxis(self, bAxis):
        self.__bAxis = bAxis
