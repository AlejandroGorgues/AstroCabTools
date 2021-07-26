import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtGui

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_rectangleCreation

__all__=["RectangleCreation"]

class RectangleCreation(QDialog, astrocabtools.cube_ans.src.ui.ui_rectangleCreation.Ui_rectangleCreation):

    def __init__(self, parent=None):
        super(RectangleCreation, self).__init__(parent)
        self.setupUi(self)

        self.centerXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.centerYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.bottomLeftXLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.bottomLeftYLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        self.widthLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))
        self.heightLineEdit.setValidator(QtGui.QDoubleValidator(bottom=0.0))

        self.createCenterButton.clicked.connect(self.update_rectangle_center)
        self.createBottomButton.clicked.connect(self.update_rectangle_bottom)


    @pyqtSlot()
    def update_rectangle_center(self):
        """Get data from the center coordinates, width and height values and create
        the rectangle"""

        try:

            x_center = self.centerXLineEdit.text()
            y_center = self.centerYLineEdit.text()

            width = self.widthLineEdit.text()
            height = self.heightLineEdit.text()

            if width != '' and height != '' and x_center != '' and y_center != '':
                width_value = float(width)
                height_value = float(height)

                x_center_value = float(x_center)
                y_center_value = float(y_center)

                #left_bottom = (x_center_value - (width_value-1)/2, y_center_value - (height_value-1)/2)
                #right_top = (x_center_value + (width_value-1)/2, y_center_value + (height_value-1)/2)
                left_bottom = (x_center_value - width_value/2, y_center_value - height_value/2)
                right_top = (x_center_value + width_value/2, y_center_value + height_value/2)
                pub.sendMessage('rectangleCreation', left_bottom = left_bottom, right_top = right_top)

            else:
                self.missed_parameters_alert()

        except Exception as e:
            self.generic_alert("Error on parameters")

    @pyqtSlot()
    def update_rectangle_bottom(self):
        """Get data from bottom X and Y coordinates, width and height values and create
        the rectangle"""

        try:
            x_bottom = self.bottomLeftXLineEdit.text()
            y_bottom = self.bottomLeftYLineEdit.text()


            width = self.widthLineEdit.text()
            height = self.heightLineEdit.text()

            if width != '' and height != '' and x_bottom != '' and y_bottom != '':
                width_value = float(width)
                height_value = float(height)

                x_bottom_value = float(x_bottom)
                y_bottom_value = float(y_bottom)

                left_bottom = (x_bottom_value, y_bottom_value)
                #right_top = (x_bottom_value + (width_value-1), y_bottom_value + (height_value-1))
                right_top = (x_bottom_value + width_value, y_bottom_value + height_value)

                pub.sendMessage('rectangleCreation', left_bottom = left_bottom, right_top = right_top)

            else:
                self.missed_parameters_alert()

        except Exception as e:
            self.generic_alert("Error on parameters")

    def clear_data(self):
        self.centerXLineEdit.setText('')
        self.centerYLineEdit.setText('')
        self.bottomLeftXLineEdit.setText('')
        self.bottomLeftYLineEdit.setText('')
        self.widthLineEdit.setText('')
        self.heightLineEdit.setText('')


    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def missed_parameters_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Wrong or missing parameters (maybe width or height")
        alert.exec_()
