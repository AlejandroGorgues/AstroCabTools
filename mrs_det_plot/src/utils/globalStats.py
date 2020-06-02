"""
Class that containt global parameters related to all the images
"""

__all__= ['globalStats']
class globalStats:

    def __init__(self, scale, stretch, color):
        self.__scale = scale
        self.__stretch = stretch
        self.__color = color

    @property
    def scale(self):
        return self.__scale

    @property
    def stretch(self):
        return self.__stretch

    @property
    def color(self):
        return self.__color

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    @stretch.setter
    def stretch(self, stretch):
        self.__stretch = stretch

    @color.setter
    def color(self, color):
        self.__color = color
