"""
Class that containt global parameters related to all the slices
"""

__all__= ['global_stats']
class global_stats:

    def __init__(self, scale, stretch, color, currSlice):
        self.__scale = scale
        self.__stretch = stretch
        self.__color = color
        self.__currSlice = currSlice
        self.__path = ""

    @property
    def scale(self):
        return self.__scale

    @property
    def stretch(self):
        return self.__stretch

    @property
    def color(self):
        return self.__color

    @property
    def currSlice(self):
        return self.__currSlice

    @property
    def path(self):
        return self.__path

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    @stretch.setter
    def stretch(self, stretch):
        self.__stretch = stretch

    @color.setter
    def color(self, color):
        self.__color = color

    @currSlice.setter
    def currSlice(self, currSlice):
        self.__currSlice = currSlice

    @path.setter
    def path(self, path):
        self.__path = path
