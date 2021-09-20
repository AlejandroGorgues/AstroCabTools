"""
Class that contains the basic coordinates of the centroid to be drawed along all slice
"""

__all__= ['centroid_coordinates']

class centroid_coordinates:

    def __init__(self):
        self.__xCoordinate = -1
        self.__yCoordinate = -1

    @property
    def xCoordinate(self):
        return self.__xCoordinate

    @property
    def yCoordinate(self):
        return self.__yCoordinate

    @xCoordinate.setter
    def xCoordinate(self, xCoordinate):
        self.__xCoordinate = xCoordinate

    @yCoordinate.setter
    def yCoordinate(self, yCoordinate):
        self.__yCoordinate = yCoordinate

    def asdict(self):
        return {'xCoordinate': self.__xCoordinate, 'yCoordinate': self.__yCoordinate}
