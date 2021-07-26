import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui

import astrocabtools.mrs_subviz.src.ui.ui_backgroundSubtraction

__all__=["BackgroundSubstraction"]

class BackgroundSubtraction(QDialog, astrocabtools.mrs_subviz.src.ui.ui_backgroundSubtraction.Ui_backgroundSubtraction):

    wedgesSelected = pyqtSignal(object, bool, name='wedgesEmit')

    def __init__(self, parent=None):
        super(BackgroundSubtraction, self).__init__(parent)
        self.setupUi(self)

        self.innerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())
        self.outerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())

        self.applyButton.clicked.connect(self.apply_background_subs)

    @pyqtSlot()
    def apply_background_subs(self, updateWedgesCenter= True):
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

                    self.wedgesSelected.emit(data, updateWedgesCenter)

                except Exception as e:
                    self.generic_alert("Error")
        else:
            self.radius_alert("Error: the inner and outer must have a value")

    def update_center_data(self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY

        self.xCenterLineEdit.setText(str(round(centerX)))
        self.yCenterLineEdit.setText(str(round(centerY)))

    def clear_data(self):
        self.xCenterLineEdit.setText('')
        self.yCenterLineEdit.setText('')
        self.innerRadiusLineEdit.setText('')
        self.outerRadiusLineEdit.setText('')
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
