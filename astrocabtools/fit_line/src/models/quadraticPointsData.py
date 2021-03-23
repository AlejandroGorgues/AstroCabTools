"""
Class that contains coordinates for each model
"""
__all__ = ['quadraticPointsData']

class quadraticPointsData:

    def __init__(self, leftX, rightX, leftY, rightY, c2):
        self.__leftX = leftX
        self.__rightX = rightX
        self.__leftY = leftY
        self.__rightY = rightY
        self.__c2 = c2

    @property
    def leftX(self):
        return self.__leftX

    @property
    def rightX(self):
        return self.__rightX

    @property
    def leftY(self):
        return self.__leftY

    @property
    def rightY(self):
        return self.__rightY

    @property
    def c2(self):
        return self.__c2

    @leftX.setter
    def leftX(self, leftX):
        self.__leftX = leftX

    @rightX.setter
    def rightX(self, rightX):
        self.__rightX = rightX

    @leftY.setter
    def leftY(self, leftY):
        self.__leftY = leftY

    @rightY.setter
    def rightY(self, rightY):
        self.__rightY = rightY

    @c2.setter
    def c2(self, c2):
        self.__c2 = c2

    def asdict(self):
        return {'left': (self.__leftX, self.__leftY), 'right':(self.__rightX, self.__rightY), 'c2': self.__c2}
