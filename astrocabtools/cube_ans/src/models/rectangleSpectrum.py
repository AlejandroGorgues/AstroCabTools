"""
Class that contains the coordinates of the rectangle to be drawed along the spectrum
"""

__all__= ['rectangle_spectrum']

class rectangle_spectrum:

    def __init__(self, direction):
        self.__direction = direction

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction
