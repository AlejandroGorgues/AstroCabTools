import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.mrs_subviz.src.ui.ui_ellipseCoordinates

__all__=["EllipseCoordinates"]

class EllipseCoordinates(QDialog, astrocabtools.mrs_subviz.src.ui.ui_ellipseCoordinates.Ui_ellipseCoordinates):

    def __init__(self, parent=None):
        super(EllipseCoordinates, self).__init__(parent)
        self.setupUi(self)

    def set_coordinates(self, centerX, centerY, aAxis, bAxis):
        centerXRound = self.set_round_value(centerX)
        centerYRound = self.set_round_value(centerY)
        bAxisRound = self.set_round_value(aAxis)
        aAxisRound = self.set_round_value(bAxis)


        self.centerXLineEdit.setText(str(centerXRound))
        self.centerYLineEdit.setText(str(centerYRound))
        self.aAxisLineEdit.setText(str(aAxisRound))
        self.bAxisLineEdit.setText(str(bAxisRound))

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
        self.close()
