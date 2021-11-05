"""
Class that contains data to manage the properties of a cube
"""

from .rectangleSelection import rectangle_selection
from .ellipseSelection import ellipse_selection
from .wedgesData import wedges_data
from .rectangleBackgData import rectangle_background_data

__all__= ['cube_patches_data']

class cube_patches_data:

    def __init__(self):
        self.__rectangleSelection = rectangle_selection(-1,-1, -1, -1)
        self.__ellipseSelection = ellipse_selection(-1,-1,-1,-1)
        self.__wedgesBackground = wedges_data(-1,-1,-1,-1)
        self.__rectangleBackground = rectangle_background_data(-1,-1,-1,-1, -1, -1, -1, -1)

    @property
    def rectangleSelection(self):
        return self.__rectangleSelection

    @property
    def ellipseSelection(self):
        return self.__ellipseSelection

    @property
    def wedgesBackground(self):
        return self.__wedgesBackground

    @property
    def rectangleBackground(self):
        return self.__rectangleBackground

    @rectangleSelection.setter
    def rectangleSelection(self, rectangleSelection):
        self.__rectangleSelection = rectangleSelection

    @ellipseSelection.setter
    def ellipseSelection(self, ellipseSelection):
        self.__ellipseSelection = ellipseSelection

    @wedgesBackground.setter
    def wedgesBackground(self, wedgesBackground):
        self.__wedgesBackground = wedgesBackground

    @rectangleBackground.setter
    def rectangleBackground(self, rectangleBackground):
        self.__rectangleBackground = rectangleBackground

    def reset_wedgesBackg(self):
        self.__wedgesBackground = wedges_data(-1,-1,-1,-1)

    def reset_rectangleBackg(self):
        self.__rectangleBackground = rectangle_background_data(-1,-1,-1,-1, -1, -1, -1, -1)

    def reset_coordinates(self):
        self.__rectangleSelection = rectangle_selection(-1,-1, -1, -1)
        self.__ellipseSelection = ellipse_selection(-1,-1,-1,-1)
        self.__wedgesBackground = wedges_data(-1,-1,-1,-1)
        self.__rectangleBackground = rectangle_background_data(-1,-1,-1,-1, -1, -1, -1, -1)

