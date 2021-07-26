"""
Class that contains the basic coordinates of the wedges to be drawed along all slices
"""

__all__= ['wedges_data']

class wedges_data:

    def __init__(self, centerX, centerY, innerRadius, outerRadius):
        self.__centerX = centerX
        self.__centerY = centerY
        self.__innerRadius = innerRadius
        self.__outerRadius = outerRadius

    @property
    def centerX(self):
        return self.__centerX

    @property
    def centerY(self):
        return self.__centerY

    @property
    def innerRadius(self):
        return self.__innerRadius

    @property
    def outerRadius(self):
        return self.__outerRadius

    @centerX.setter
    def centerX(self, centerX):
        self.__centerX = centerX

    @centerY.setter
    def centerY(self, centerY):
        self.__centerY = centerY

    @innerRadius.setter
    def innerRadius(self, innerRadius):
        self.__innerRadius = innerRadius

    @outerRadius.setter
    def outerRadius(self, outerRadius):
        self.__outerRadius = outerRadius

    def asdict(self):
        return {'centerX': self.__centerX, 'centerY': self.__centerY, 'innerRadius': self.__innerRadius, 'outerRadius': self.__outerRadius}
