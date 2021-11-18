"""
Allow to select the cube to be loaded
"""

import sys
import glob
import traceback

import numpy as np

from os.path import expanduser

from ..utils.basic_transformations import wavelength_to_slice

from PyQt5.QtWidgets import QDialog, QMessageBox, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.mrs_subviz.src.ui.ui_collapsedWavelengthSelection

class CollapsedWavelengthSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_collapsedWavelengthSelection.Ui_collapsedWavelengthSelection):
    rangeData = pyqtSignal(int, int, name='getRangeData')

    def __init__(self, parent = None):
        super(CollapsedWavelengthSelection, self).__init__(parent)
        self.setupUi(self)

        self.subband = 0

        self.allWavelengthButton.clicked.connect(lambda: self.send_range(True))
        self.customWavelengthButton.clicked.connect(lambda: self.send_range(False))

        self.initialWavelengthLineEdit.setValidator(QtGui.QDoubleValidator())
        self.endWavelengthLineEdit.setValidator(QtGui.QDoubleValidator())

    def send_range(self, allRange):
        """
        Get the sum of the data from the range selected
        :param bool allRange: If True, get the sum of all values of the cube, else, get the sum values of the range
        """
        if allRange:
            initialWaveTrans = wavelength_to_slice(float(self.initialWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)
            endWaveTrans = wavelength_to_slice(float(self.endWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)

            self.rangeData.emit(initialWaveTrans,endWaveTrans)
        else:

            if float(self.initialRangeWavelengthLineEdit.text()) < float(self.initialWavelengthLineEdit.text()) or \
                float(self.endRangeWavelengthLineEdit.text()) > float(self.endWavelengthLineEdit.text()):
                    self.range_warning()
            else:
                initialWaveTrans = wavelength_to_slice(float(self.initialRangeWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)
                endWaveTrans = wavelength_to_slice(float(self.endRangeWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)

                self.rangeData.emit(initialWaveTrans, endWaveTrans)

    def get_data_from_sub_viz(self, initRange, endRange, cubeParams):
        """
        Get data from the main window to initialize the values
        :param float initRange: initial wavelength value
        :param float endRange: end wavelength value
        :param int subband: subband value
        :param object cubeParams: cube data structured
        """
        self.initialWavelengthLineEdit.setText(str(initRange))
        self.endWavelengthLineEdit.setText(str(endRange))
        self.cubeParams = cubeParams

    def range_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Range values out of the limits of the cube values")
        warning.exec_()

    def clear_data(self):
        self.initialWavelengthLineEdit.setText('')
        self.endWavelengthLineEdit.setText('')
        self.initialRangeWavelengthLineEdit.setText('')
        self.endRangeWavelengthLineEdit.setText('')
        self.close()
