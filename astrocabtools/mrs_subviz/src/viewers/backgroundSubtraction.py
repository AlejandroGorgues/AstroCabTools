import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui

import astrocabtools.mrs_subviz.src.ui.ui_backgroundSubtraction

from ..utils.basic_transformations import rectangle_patch_to_border_coordinates

__all__=["BackgroundSubstraction"]

class BackgroundSubtraction(QDialog, astrocabtools.mrs_subviz.src.ui.ui_backgroundSubtraction.Ui_backgroundSubtraction):

    wedgesSelected = pyqtSignal(object, str, bool, name='wedgesEmit')
    rectangleSelected = pyqtSignal(object, str, name='rectangleEmit')

    def __init__(self, parent=None):
        super(BackgroundSubtraction, self).__init__(parent)
        self.setupUi(self)

        self.innerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())
        self.outerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())

        self.rectangleXCenterLineEdit.setValidator(QtGui.QDoubleValidator())
        self.rectangleYCenterLineEdit.setValidator(QtGui.QDoubleValidator())
        self.widthLineEdit.setValidator(QtGui.QDoubleValidator())
        self.heightLineEdit.setValidator(QtGui.QDoubleValidator())

        self.wedgesApplyButton.clicked.connect(self.wedges_apply_background_subs)
        self.rectangleApplyButton.clicked.connect(self.rectangle_apply_background_subs)

    @pyqtSlot()
    def wedges_apply_background_subs(self, updateWedgesCenter= True):
        innerValue = self.innerRadiusLineEdit.text()
        outerValue = self.outerRadiusLineEdit.text()

        if innerValue != '' and outerValue != '':

            if float(innerValue) == 0 or float(outerValue == 0):
                self.radius_alert("Error: the inner or outer radius must not be 0")

            elif float(innerValue) >= float(outerValue):
                self.radius_alert("Error: the inner radius must be less than the outer")

            elif float(innerValue) != 0 and float(outerValue) != 0:
                try:

                    data = {}
                    data['innerRadius'] = float(innerValue)
                    data['outerRadius'] = float(outerValue)
                    data['centerX'] = self.centerX
                    data['centerY'] = self.centerY

                    self.wedgesSelected.emit(data, "wedges",  updateWedgesCenter)

                except Exception as e:
                    self.generic_alert("Error")
        else:
            self.radius_alert("Error: the inner and outer must have a value")

    def update_center_data(self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY

        self.wedgesXCenterLineEdit.setText(str(round(centerX)))
        self.wedgesYCenterLineEdit.setText(str(round(centerY)))

    def rectangle_apply_background_subs(self):
        centerXValue = self.rectangleXCenterLineEdit.text()
        centerYValue = self.rectangleYCenterLineEdit.text()

        widthValue = self.widthLineEdit.text()
        heightValue = self.heightLineEdit.text()

        if centerXValue != '' and centerYValue != '' and widthValue != '' and heightValue != '':

            if float(centerXValue) == 0 or float(centerYValue) == 0 or float(widthValue)== 0 or float(heightValue) == 0:
                self.generic_alert("Error: all of the rectangle parameters must not be 0")

            else:
                try:
                    data = {}
                    data['width'] = float(widthValue)
                    data['height'] = float(heightValue)
                    data['centerX'] = float(centerXValue)
                    data['centerY'] = float(centerYValue)
                    borderCoord = rectangle_patch_to_border_coordinates(data)
                    borderCoord.update(data)

                    self.rectangleSelected.emit(borderCoord, "rectangle")

                except Exception as e:
                    self.generic_alert("Error")
        else:
            self.generic_alert("Error: all rectangle parameters must have a value")

    def clear_data(self):
        self.wedgesXCenterLineEdit.setText('')
        self.wedgesYCenterLineEdit.setText('')
        self.rectangleXCenterLineEdit.setText('')
        self.rectangleYCenterLineEdit.setText('')
        self.innerRadiusLineEdit.setText('')
        self.outerRadiusLineEdit.setText('')
        self.widthLineEdit.setText('')
        self.heightLineEdit.setText('')
        self.close()

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def radius_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
