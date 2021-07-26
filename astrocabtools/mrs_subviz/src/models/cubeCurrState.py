"""
Class that contains global state of the patches
"""


__all__= ['cube_curr_state']

class cube_curr_state:

    def __init__(self):
        self.__active = None

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, active):
        self.__active = active
