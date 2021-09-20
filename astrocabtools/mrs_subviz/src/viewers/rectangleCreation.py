import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui

from pubsub import pub

from ..utils.basic_transformations import sexagesimal_to_decimal, sexagesimal_to_decimal_astropy, arcsec_to_pixel

import astrocabtools.mrs_subviz.src.ui.ui_rectangleCreation

__all__=["RectangleCreation"]

class RectangleCreation(QDialog, astrocabtools.mrs_subviz.src.ui.ui_rectangleCreation.Ui_rectangleCreation):

    create_rectangle = pyqtSignal([dict, int], name= 'rectangleCreation')

    def __init__(self, parent=None):
        super(RectangleCreation, self).__init__(parent)
        self.setupUi(self)


        #self.centerXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.centerYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.bottomLeftXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.bottomLeftYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        #self.widthLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        #self.heightLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        self.createCenterButtonPixel.clicked.connect(lambda: self.update_rectangle_center(0))
        self.createBottomButtonPixel.clicked.connect(lambda: self.update_rectangle_bottom(0))

        self.createCenterButtonCoord.clicked.connect(lambda: self.update_rectangle_center(1))
        self.createBottomButtonCoord.clicked.connect(lambda: self.update_rectangle_bottom(1))


        self.pixelInfoButton.clicked.connect(self.show_pixel_info)
        self.skyCoordInfoButton.clicked.connect(self.show_skyCoord_info)

    def set_center_coordinates(self, xCenter, yCenter):
        self.centerXLineEdit.setText(str(xCenter))
        self.centerYLineEdit.setText(str(yCenter))

    def update_rectangle_center(self, typeOp):
        """
        Get data from the center coordinates, width and height values and create
        the rectangle
        :param int typeOp: Signal that check if the coordinates are in pixel or in RA and DEC
        """

        try:
            x_center = ''
            y_center = ''

            width = ''
            height = ''


            if not typeOp:
                x_center = self.centerXLineEdit.text()
                y_center = self.centerYLineEdit.text()

                width = self.widthLineEdit.text()
                height = self.heightLineEdit.text()

            else:
                x_center = self.centerXLineEdit.text()
                y_center = self.centerYLineEdit.text()

                width = arcsec_to_pixel(float(self.widthLineEdit.text()), self.model.meta.wcsinfo.cdelt2)
                height = arcsec_to_pixel(float(self.heightLineEdit.text()), self.model.meta.wcsinfo.cdelt1)

                x_center, y_center = sexagesimal_to_decimal_astropy(x_center, y_center, self.model, self.wavelengthValue)

            if width != '' and height != '' and x_center != '' and y_center != '':
                width_value = float(width)
                height_value = float(height)

                x_center_value = float(x_center)
                y_center_value = float(y_center)

                left_bottom = (x_center_value - width_value/2, y_center_value - height_value/2)
                right_top = (x_center_value + width_value/2, y_center_value + height_value/2)

                patchesData = {}
                patchesData['ix'] = left_bottom[0]
                patchesData['iy'] = left_bottom[1]
                patchesData['ex'] = right_top[0]
                patchesData['ey'] = right_top[1]
                patchesData['centerX'] = float(x_center)
                patchesData['centerY'] = float(y_center)

                self.create_rectangle[dict, int].emit(patchesData, typeOp)

            else:
                self.missed_parameters_alert()

        except Exception as e:
            self.generic_alert("Error on parameters")

    def update_rectangle_bottom(self, typeOp):
        """
        Get data from bottom X and Y coordinates, width and height values and create
        the rectangle
        :param int typeOp: Signal that check if the coordinates are in pixel or in RA and DEC
        """

        try:
            x_bottom = ''
            y_bottom = ''

            width = ''
            height = ''

            if typeOp:

                x_bottom = self.bottomLeftXLineEdit.text()
                y_bottom = self.bottomLeftYLineEdit.text()

                width = self.widthLineEdit.text()
                height = self.heightLineEdit.text()

            else:

                x_bottom = self.bottomLeftXLineEdit.text()
                y_bottom = self.bottomLeftYLineEdit.text()

                x_bottom, y_bottom = sexagesimal_to_decimal_astropy(x_bottom, y_bottom, self.model, self.wavelengthValue)

                width = arcsec_to_pixel(self.widthLineEdit.text(), self.model.meta.wcsinfo.cdelt2)
                height = arcsec_to_pixel(self.heightLineEdit.text(), self.model.meta.wcsinfo.cdelt1)

            if width != '' and height != '' and x_bottom != '' and y_bottom != '':
                width_value = float(width)
                height_value = float(height)

                x_bottom_value = float(x_bottom)
                y_bottom_value = float(y_bottom)

                left_bottom = (x_bottom_value, y_bottom_value)
                right_top = (x_bottom_value + width_value, y_bottom_value + height_value)

                patchesData = {}
                patchesData['ix'] = left_bottom[0]
                patchesData['iy'] = left_bottom[1]
                patchesData['ex'] = right_top[0]
                patchesData['ey'] = right_top[1]
                patchesData['centerX'] = left_bottom[0] + width_value/2.
                patchesData['centerY'] = right_top[1] + height_value/2.

                self.create_rectangle[dict, int].emit(patchesData, typeOp)

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
        self.bottomLeftXLineEdit.setText('')
        self.bottomLeftYLineEdit.setText('')
        self.widthLineEdit.setText('')
        self.heightLineEdit.setText('')
        self.close()

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_pixel_info(self):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        info.setText("The pixel coordinates format are 0.00 for x, y and both axes")
        info.exec_()

    def show_skyCoord_info(self):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        info.setText("The sky coordinates format are\n 00h00m00.00s for RA, +/-00d00m00.00s for DEC")
        info.exec_()

    def missed_parameters_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Wrong or missing parameters (maybe width or height")
        alert.exec_()
