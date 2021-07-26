import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui

from pubsub import pub

import astrocabtools.mrs_subviz.src.ui.ui_ellipseCreation

__all__=["EllipseCreation"]

class EllipseCreation(QDialog, astrocabtools.mrs_subviz.src.ui.ui_ellipseCreation.Ui_ellipseCreation):

    create_ellipse = pyqtSignal([dict], name= 'ellipseCreation')

    def __init__(self, parent=None):
        super(EllipseCreation, self).__init__(parent)
        self.setupUi(self)

        self.centerXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.centerYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.aAxisLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.bAxisLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        self.createButton.clicked.connect(self.update_ellipse)


    def update_ellipse(self):
        """Get data from center X and Y coordinates, a and b axis values and create
        the ellipse"""

        try:
            x_center = self.centerXLineEdit.text()
            y_center = self.centerYLineEdit.text()


            aAxis = self.aAxisLineEdit.text()
            bAxis = self.bAxisLineEdit.text()

            if aAxis != '' and bAxis != '' and x_center != '' and y_center != '':
                aAxis_value = float(aAxis)
                bAxis_value = float(bAxis)

                x_center_value = float(x_center)
                y_center_value = float(y_center)

                center = (x_center_value, y_center_value)
                axis = (aAxis_value, bAxis_value)

                patchesData = {}
                patchesData['centerX'] =center[0]
                patchesData['centerY'] =center[1]
                patchesData['aAxis'] =axis[0]
                patchesData['bAxis'] =axis[1]

                self.create_ellipse[dict].emit(patchesData)
            else:
                self.missed_parameters_alert()

        except Exception as e:
            self.generic_alert("Error on parameters")

    def clear_data(self):
        self.centerXLineEdit.setText('')
        self.centerYLineEdit.setText('')
        self.aAxisLineEdit.setText('')
        self.bAxisLineEdit.setText('')
        self.close()

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def missed_parameters_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Wrong or missed parameters")
        alert.exec_()
