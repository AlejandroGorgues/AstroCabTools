"""
Class that contains coordinates for each model
"""
__all__ = ['pointsData']

class pointsData:

    def __init__(self, leftX, rightX, topX, sigma1X, sigma2X, leftY, rightY, topY, sigma1Y,sigma2Y):
        self.__leftX = leftX
        self.__rightX = rightX
        self.__topX = topX
        self.__sigma1X = sigma1X
        self.__sigma2X = sigma2X
        self.__leftY = leftY
        self.__rightY = rightY
        self.__topY = topY
        self.__sigma1Y = sigma1Y
        self.__sigma2Y = sigma2Y

    @property
    def leftX(self):
        return self.__leftX

    @property
    def rightX(self):
        return self.__rightX

    @property
    def topX(self):
        return self.__topX

    @property
    def sigma1X(self):
        return self.__sigma1X

    @property
    def sigma2X(self):
        return self.__sigma2X

    @property
    def leftY(self):
        return self.__leftY

    @property
    def rightY(self):
        return self.__rightY

    @property
    def topY(self):
        return self.__topY

    @property
    def sigma1Y(self):
        return self.__sigma1Y

    @property
    def sigma2Y(self):
        return self.__sigma2Y

    @leftX.setter
    def leftX(self, leftX):
        self.__leftX = leftX

    @rightX.setter
    def rightX(self, rightX):
        self.__rightX = rightX

    @topX.setter
    def topX(self, topX):
        self.__topX = topX

    @sigma1X.setter
    def sigma1X(self, sigma1X):
        self.__sigma1X = sigma1X

    @sigma2X.setter
    def sigma2X(self, sigma2X):
        self.__sigma2X = sigma2X

    @leftY.setter
    def leftY(self, leftY):
        self.__leftY = leftY

    @rightY.setter
    def rightY(self, rightY):
        self.__rightY = rightY

    @topY.setter
    def topY(self, topY):
        self.__topY = topY

    @sigma1Y.setter
    def sigma1Y(self, sigma1Y):
        self.__sigma1Y = sigma1Y

    @sigma2Y.setter
    def sigma2Y(self, sigma2Y):
        self.__sigma2Y = sigma2Y
