import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_rectangleCreation

__all__=["RectangleCreation"]

class RectangleCreation(QDialog, astrocabtools.cube_ans.src.ui.ui_rectangleCreation.Ui_rectangleCreation):

    def __init__(self, parent=None):
        super(RectangleCreation, self).__init__(parent)
        self.setupUi(self)

        self.createButton.clicked.connect(self.update_rectangle)

    @pyqtSlot()
    def update_rectangle(self):
        """Get data from the active line edit coordinates and create the rectangle on the plot"""

        try:
            x_value = int(self.bottomLeftXLineEdit.text())
            y_value = int(self.bottomLeftYLineEdit.text())

            width = int(self.widthLineEdit.text())
            height = int(self.heightLineEdit.text())

            coord1 = (x_value, y_value)
            coord2 = (x_value + (width-1), y_value + (height-1))

            pub.sendMessage('rectangleCoordinates', coord1 = coord1, coord2 = coord2)

        except Exception as e:
            self.generic_alert("Error on parameters")

    def set_round_value(self, data):
        if data %1 >= 0.5:
            return int(math.ceil(data))
        else:
            return int(round(data))

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
