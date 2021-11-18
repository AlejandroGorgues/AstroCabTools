"""
Allow to select the cube to be loaded
"""

import sys
import glob
import traceback
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.mrs_subviz.src.ui.ui_cubeSelection

class CubeSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_cubeSelection.Ui_cubeSelection):
    subbandSelected = pyqtSignal(int, str, str,  name="subbandSelected")

    def __init__(self, parent = None):
        super(CubeSelection, self).__init__(parent)
        self.setupUi(self)

        self.subband = 0

        self.subbandSelectionComboBox.currentIndexChanged.connect(self.subband_selection)
        self.operationButton.clicked.connect(self.send_operation)

    def subband_selection(self, index):
        self.subband = index

    def send_operation(self):
        self.subbandSelected.emit(self.subband, self.order, self.additionalOrder)

    def set_order(self, order, additionalOrder):
        ordersDetailed = {"rectangleAp":"Operation: make rectangle aperture",
                          "ellipseAp":"Operation: make ellipse aperture",
                          "interactive":"Operation: interact with the cube",
                          "rectangleCoord":"Operation: visualize rectangle coordinates",
                          "ellipseCoord":"Operation: visualize ellipse coordinates",
                          "rectangleCreate":"Operation: create rectangle from coordinates",
                          "ellipseCreate":"Operation: create ellipse from coordinates",
                          "backgSub":"Operation: generate background",
                          "collapsedSelect": "Operation: generate collapsed image",
                          "centroidSelect":"Operation: calculate centroid",
                          "centroidCoord":"Operation: show coordinates of centroid"}
        self.order = order
        self.additionalOrder = additionalOrder
        self.operationLabel.setText(ordersDetailed[order])

    def clear_data(self):
        self.subbandSelectionComboBox.setCurrentIndex(0)
        self.subband = 0
        self.close()
