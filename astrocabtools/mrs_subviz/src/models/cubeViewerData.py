"""
Class that contains data to manage the properties of a cube
"""
from .cubeStats import cube_stats
from .cubePatchesData import cube_patches_data
from .centroidCoordinates import centroid_coordinates

__all__= ['cube_viewer_data']

class cube_viewer_data:

    def __init__(self, position):
        self.__path = ""
        self.__position = position
        self.__style = cube_stats('MinMax', 'Linear', 'gray')
        self.__currSlice = 0
        self.__axis = []
        self.__cubeModel = None
        self.__cubePatchesData = cube_patches_data()
        self.__centroidCoordinates = centroid_coordinates()
        self.__wavelengthRange = None
        self.__fluxAperture = None
        self.__aperture = None

    @property
    def path(self):
        return self.__path

    @property
    def position(self):
        return self.__position

    @property
    def style(self):
        return self.__style

    @property
    def currSlice(self):
        return self.__currSlice

    @property
    def axis(self):
        return self.__axis

    @property
    def cubeModel(self):
        return self.__cubeModel

    @property
    def cubePatchesData(self):
        return self.__cubePatchesData

    @property
    def centroidCoordinates(self):
        return self.__centroidCoordinates

    @property
    def aperture(self):
        return self.__aperture

    @property
    def fluxAperture(self):
        return self.__fluxAperture

    @property
    def wavelengthRange(self):
        return self.__wavelengthRange

    @path.setter
    def path(self, path):
        self.__path = path

    @position.setter
    def position(self, position):
        self.__position = position

    @style.setter
    def style(self, style):
        self.__style = style

    @currSlice.setter
    def currSlice(self, currSlice):
        self.__currSlice = currSlice

    @axis.setter
    def axis(self, axis):
        self.__axis = axis

    @cubeModel.setter
    def cubeModel(self, cubeModel):
        self.__cubeModel = cubeModel

    @cubePatchesData.setter
    def cubePatchesData(self, cubePatchesData):
        self.__cubePatchesData = cubePatchesData

    @centroidCoordinates.setter
    def centroidCoordinates(self, centroidCoordinates):
        self.__centroidCoordinates = centroidCoordinates

    @aperture.setter
    def aperture(self, aperture):
        self.__aperture = aperture

    @fluxAperture.setter
    def fluxAperture(self, fluxAperture):
        self.__fluxAperture = fluxAperture

    @wavelengthRange.setter
    def wavelengthRange(self, wavelengthRange):
        self.__wavelengthRange = wavelengthRange

    def add_axis(self, axis):
        self.__axis.insert(len(self.__axis), axis)

    def set_default_data(self):
        self.__path = ""
        self.__style = cube_stats('MinMax', 'Linear', 'gray')
        self.__currSlice = 0
        self.__cubeModel = None
        self.__cubePatchesData = cube_patches_data()
        self.__centroidCoordinates = centroid_coordinates()
        self.__wavelengthRange = None
        self.__fluxAperture = None
        self.__aperture = None

