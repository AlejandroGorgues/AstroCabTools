import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_rectangleCoordinates

__all__=["RectangleCoordinates"]

class RectangleCoordinates(QDialog, astrocabtools.cube_ans.src.ui.ui_rectangleCoordinates.Ui_rectangleCoordinates):

    def __init__(self, parent=None):
        super(RectangleCoordinates, self).__init__(parent)
        self.setupUi(self)
        pub.subscribe(self.set_coordinates, 'rectangleUpdateCoordinates')

    def set_coordinates(self, ix, iy, ex, ey):
        ixRound = self.set_round_value(ix)
        iyRound = self.set_round_value(iy)
        exRound = self.set_round_value(ex)
        eyRound = self.set_round_value(ey)

        leftX = 0
        topY = 0

        rightX = 0
        bottomY = 0

        #Same pixel
        if ixRound == exRound and iyRound == eyRound:
            leftX = ixRound
            rightX = ixRound

            topY = iyRound
            bottomY = iyRound

        #Start Top left rectangle
        elif ixRound < exRound and iyRound > eyRound:

            leftX = ixRound
            rightX = exRound

            topY = iyRound
            bottomY = iyRound

        #Start Bottom left rectangle
        elif ixRound < exRound and iyRound < eyRound:
            leftX = ixRound
            rightX = exRound

            topY = eyRound
            bottomY = iyRound

        #Start Top right rectangle
        elif ixRound > exRound and iyRound > eyRound:

            leftX = exRound
            rightX = ixRound

            topY = iyRound
            bottomY = eyRound

        #Start Bottom right rectangle
        elif ixRound > exRound and iyRound < eyRound:

            leftX = exRound
            rightX = ixRound

            topY = eyRound
            bottomY = iyRound

        #Same X and goes from left to right Y
        elif ixRound == exRound and iyRound > eyRound:

            leftX = ixRound
            rightX = ixRound

            topY = iyRound
            bottomY = iyRound

        #Same X and goes from right to left Y
        elif ixRound == exRound and iyRound < eyRound:

            leftX = exRound
            rightX = ixRound

            topY = eyRound
            bottomY = eyRound

        #Same Y and goes from top to bottom X
        elif ixRound < exRound and iyRound == eyRound:

            leftX = ixRound
            rightX = exRound

            topY = iyRound
            bottomY = iyRound

        #Same Y and goes from bottom to top X
        elif ixRound > exRound and iyRound == eyRound:

            leftX = exRound
            rightX = ixRound

            topY = iyRound
            bottomY = iyRound

        self.topYLineEdit.setText(str(topY))
        self.rightXLineEdit.setText(str(rightX))
        self.leftXLineEdit.setText(str(leftX))
        self.bottomYLineEdit.setText(str(bottomY))

    def set_round_value(self, data):
        if data %1 >= 0.5:
            return int(math.ceil(data))
        else:
            return int(round(data))

    def clear_data(self):
        self.topYLineEdit.setText('')
        self.rightXLineEdit.setText('')
        self.leftXLineEdit.setText('')
        self.bottomYLineEdit.setText('')
