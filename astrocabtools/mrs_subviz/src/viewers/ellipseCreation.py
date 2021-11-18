import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui

from pubsub import pub

import astrocabtools.mrs_subviz.src.ui.ui_ellipseCreation

from ..utils.basic_transformations import sexagesimal_to_decimal, sexagesimal_to_decimal_astropy, arcsec_to_pixel

__all__=["EllipseCreation"]

class EllipseCreation(QDialog, astrocabtools.mrs_subviz.src.ui.ui_ellipseCreation.Ui_ellipseCreation):

    create_ellipse = pyqtSignal([dict, int], name= 'ellipseCreation')

    def __init__(self, parent=None):
        super(EllipseCreation, self).__init__(parent)
        self.setupUi(self)

        #self.centerXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.centerYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.aAxisLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.bAxisLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        self.createButtonPixel.clicked.connect(lambda: self.update_ellipse_pixel(0))
        self.createButtonCoord.clicked.connect(lambda: self.update_ellipse_pixel(1))

        self.pixelInfoButton.clicked.connect(self.show_pixel_info)
        self.skyCoordInfoButton.clicked.connect(self.show_skyCoord_info)

    def set_center_coordinates(self, xCenter, yCenter):
        self.centerXLineEdit.setText(str(xCenter))
        self.centerYLineEdit.setText(str(yCenter))

    def update_ellipse_pixel(self, typeOp):
        """
        Get data from center X and Y coordinates, a and b axis values and create the ellipse
        :param int typeOp: Signal that check if the coordinates are in pixel or in RA and DEC
        """

        try:
            if not typeOp:

                x_center = self.centerXLineEdit.text()
                y_center = self.centerYLineEdit.text()

                aAxis = self.aAxisLineEdit.text()
                bAxis = self.bAxisLineEdit.text()

            else:

                x_center = self.centerXLineEdit.text()
                y_center = self.centerYLineEdit.text()

                aAxis = arcsec_to_pixel(float(self.aAxisLineEdit.text()), self.model.meta.wcsinfo.cdelt2)
                bAxis = arcec_to_pixel(float(self.bAxisLineEdit.text()), self.model.meta.wcsinfo.cdelt1)

                x_center, y_center = sexagesimal_to_decimal_astropy(x_center, y_center, self.model, self.wavelengthValue)

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

                self.create_ellipse[dict, int].emit(patchesData, typeOp)
            else:
                self.missed_parameters_alert()

        except Exception as e:
            self.generic_alert("Error on parameters")

    def get_data(self, model, wavelengthValue):
        self.model = model
        self.wavelengthValue = wavelengthValue

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


    def show_pixel_info(self):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        info.setText("The pixel coordinates format are 0.00 for x, y, width and height")
        info.exec_()

    def show_skyCoord_info(self):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        info.setText("The sky coordinates format are\n 00h00m00.00s for RA, +/-00d00m00.00s for DEC")
        info.exec_()

    def missed_parameters_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Wrong or missed parameters")
        alert.exec_()
