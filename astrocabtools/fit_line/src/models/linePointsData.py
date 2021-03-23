"""
Class that contains coordinates for each model
"""
__all__ = ['linePointsData']

class linePointsData:

    def __init__(self, leftX, rightX, leftY, rightY):
        self.__leftX = leftX
        self.__rightX = rightX
        self.__leftY = leftY
        self.__rightY = rightY

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

    def asdict(self):
        return {'left': (self.__leftX, self.__leftY), 'right':(self.__rightX, self.__rightY)}
