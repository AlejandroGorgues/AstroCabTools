import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_ellipseCoordinates

__all__=["EllipseCoordinates"]

class EllipseCoordinates(QDialog, astrocabtools.cube_ans.src.ui.ui_ellipseCoordinates.Ui_ellipseCoordinates):

    def __init__(self, parent=None):
        super(EllipseCoordinates, self).__init__(parent)
        self.setupUi(self)
        pub.subscribe(self.set_coordinates, 'ellipseUpdateCoordinates')

    def set_coordinates(self, cx, cy, aAxis, bAxis):
        cxRound = self.set_round_value(cx)
        cyRound = self.set_round_value(cy)
        aAxisRound = self.set_round_value(aAxis)
        bAxisRound = self.set_round_value(bAxis)

        centerX = cxRound
        centerY = cyRound

        aAxis = aAxisRound
        bAxis = bAxisRound


        self.centerXLineEdit.setText(str(centerX))
        self.centerYLineEdit.setText(str(centerY))
        self.aAxisLineEdit.setText(str(aAxis))
        self.bAxisLineEdit.setText(str(bAxis))

    def set_round_value(self, data):
        if data %1 >= 0.5:
            return int(math.ceil(data))
        else:
            return int(round(data))

    def clear_data(self):
        self.centerXLineEdit.setText('')
        self.centerYLineEdit.setText('')
        self.aAxisLineEdit.setText('')
        self.bAxisLineEdit.setText('')
