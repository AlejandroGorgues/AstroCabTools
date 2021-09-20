import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.mrs_subviz.src.ui.ui_centroidCoordinates

__all__=["CentroidCoordinates"]

class CentroidCoordinates(QDialog, astrocabtools.mrs_subviz.src.ui.ui_centroidCoordinates.Ui_centroidCoordinates):

    def __init__(self, parent=None):
        super(CentroidCoordinates, self).__init__(parent)
        self.setupUi(self)

    def set_coordinates(self, cx, cy):

        self.xCoordLineEdit.setText(str(float('{:.3f}'.format(cx))))
        self.yCoordLineEdit.setText(str(float('{:.3f}'.format(cy))))

    def clear_data(self):
        self.xCoordLineEdit.setText('')
        self.yCoordLineEdit.setText('')
        self.close()
