import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui

from pubsub import pub

from ..utils.aperture_operations import background_subtraction, rect_background_subtraction

import astrocabtools.cube_ans.src.ui.ui_backgroundSubtraction

__all__=["BackgroundSubstraction"]

class BackgroundSubtraction(QDialog, astrocabtools.cube_ans.src.ui.ui_backgroundSubtraction.Ui_backgroundSubtraction):

    innerWedgeSelected = pyqtSignal(float, float, float, name='innerEmit')
    outerWedgeSelected = pyqtSignal(float, float, float, name='outerEmit')
    valuesSubstracted = pyqtSignal(list, list, name='backgroundParameters')


    rectSelected = pyqtSignal(float, float, float, float, name='rectEmit')



    def __init__(self, parent=None):
        super(BackgroundSubtraction, self).__init__(parent)
        self.setupUi(self)

        self.innerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())
        self.outerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())

        self.applyButton.clicked.connect(self.apply_background_subs)

        self.hRect.setValidator(QtGui.QDoubleValidator())
        self.hRect.setValidator(QtGui.QDoubleValidator())

        self.rectXCenter.setValidator(QtGui.QDoubleValidator())
        self.rectYCenter.setValidator(QtGui.QDoubleValidator())

        self.recPushButton.clicked.connect(self.apply_rectAux_background_subs)


    @pyqtSlot()
    def apply_rectAux_background_subs(self):
        widthValue = self.wRect.text()
        heightValue = self.hRect.text()

        xCenter = self.rectXCenter.text()
        yCenter = self.rectYCenter.text()

        self.rectSelected.emit(abs(float(xCenter) - float(widthValue)/2),
                                       abs(float(yCenter) - float(heightValue)/2),
                                            float(heightValue),float(widthValue))

        self.fValues_sub, self.bkg_sum = rect_background_subtraction(xCenter, yCenter, float(heightValue), float(widthValue), self.aperture, self.cubeObj, self.spectrumValues)
        self.valuesSubstracted.emit(self.fValues_sub, self.bkg_sum)

    @pyqtSlot()
    def apply_background_subs(self):
        innerValue = self.innerRadiusLineEdit.text()
        outerValue = self.outerRadiusLineEdit.text()

        if innerValue != '' and outerValue != '':

            if float(innerValue) == 0 or float(outerValue == 0):
                self.radius_alert("Error: the inner or outer radius must not be 0")

            elif float(innerValue) >= float(outerValue):
                self.radius_alert("Error: the inner radius must be less than the outer")

            elif float(innerValue) != 0 and float(outerValue) != 0:
                try:
                    self.innerWedgeSelected.emit(self.xCenter, self.yCenter,float(innerValue))
                    self.outerWedgeSelected.emit(self.xCenter, self.yCenter,float(outerValue))

                    self.fValues_sub, self.bkg_sum = background_subtraction(self.xCenter, self.yCenter, float(innerValue),
                                                float(outerValue), self.aperture, self.cubeObj, self.spectrumValues)
                    self.valuesSubstracted.emit(self.fValues_sub, self.bkg_sum)

                except Exception as e:
                    self.generic_alert("Error")
        else:
            self.radius_alert("Error: the inner and outer must have a value")

    def update_center_data(self, center_point, cubeObj, aperture, spectrumValues):

        self.xCenter = center_point[1][0]
        self.yCenter = center_point[1][1]

        self.aAxis = center_point[0][2]
        self.bAxis = center_point[0][3]
        self.xCenterLineEdit.setText(str(round(center_point[1][0],4)))
        self.yCenterLineEdit.setText(str(round(center_point[1][1],4)))
        self.cubeObj = cubeObj
        self.aperture = aperture
        self.spectrumValues = spectrumValues

    def return_valuesSubs(self):
        return self.fValues_sub, self.bkg_sum

    def clear_data(self):
        self.xCenterLineEdit.setText('')
        self.yCenterLineEdit.setText('')
        self.innerRadiusLineEdit.setText('')
        self.outerRadiusLineEdit.setText('')

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def radius_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
