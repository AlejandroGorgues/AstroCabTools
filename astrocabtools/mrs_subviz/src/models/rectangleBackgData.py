"""
Class that contains the coordinates of the rectangle to be drawed along all slices
"""

__all__= ['rectangle_background_data']

class rectangle_background_data:

    def __init__(self, centerX, centerY, width, height, ix, iy, ex, ey):
        self.__centerX = centerX
        self.__centerY = centerY
        self.__width = width
        self.__height = height
        self.__ix = ix
        self.__iy = iy
        self.__ex = ex
        self.__ey = ey

    @property
    def centerX(self):
        return self.__centerX

    @property
    def centerY(self):
        return self.__centerY

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def ix(self):
        return self.__ix

    @property
    def iy(self):
        return self.__iy

    @property
    def ex(self):
        return self.__ex

    @property
    def ey(self):
        return self.__ey

    @centerX.setter
    def centerX(self, centerX):
        self.__centerX = centerX

    @centerY.setter
    def centerY(self, centerY):
        self.__centerY = centerY

    @width.setter
    def width(self, width):
        self.__width = width

    @height.setter
    def height(self, height):
        self.__height = height

    @ix.setter
    def ix(self, ix):
        self.__ix = ix

    @iy.setter
    def iy(self, iy):
        self.__iy = iy

    @ex.setter
    def ex(self, ex):
        self.__ex = ex

    @ey.setter
    def ey(self, ey):
        self.__ey = ey

    def asdict(self):
        #width = abs(self.__ex - self.__ix)
        #height = abs(self.__ey - self.__iy)

        #centerX = self.__ix + width/2.
        #centerY = self.__iy + height/2.
        return {'centerX': self.__centerX, 'centerY': self.__centerY, 'ix': self.__ix, 'iy': self.__iy, 'ex': self.__ex, 'ey': self.__ey}
