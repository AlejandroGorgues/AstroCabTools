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

import astrocabtools.mrs_subviz.src.viewers.centroidAreaSelection as centSelect

import astrocabtools.mrs_subviz.src.ui.ui_centroidWavelengthSelection

class CentroidWavelengthSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_centroidWavelengthSelection.Ui_centroidWavelengthSelection):

    def __init__(self, parent = None):
        super(CentroidWavelengthSelection, self).__init__(parent)
        self.setupUi(self)

        self.subband = 0

        self.allWavelengthButton.clicked.connect(lambda: self.send_range(True))
        self.customWavelengthButton.clicked.connect(lambda: self.send_range(False))

        self.initialWavelengthLineEdit.setValidator(QtGui.QDoubleValidator())
        self.endWavelengthLineEdit.setValidator(QtGui.QDoubleValidator())

        self.centSelect = centSelect.CentroidAreaSelection()

    def send_range(self, allRange):
        """
        Get the sum of the data from the range selected
        :param bool allRange: If True, get the sum of all values of the cube, else, get the sum values of the range
        """
        if allRange:

            self.centSelect.get_data_from_centroid_wave(self.order, self.cubeParams, self.subband, np.mean(self.cubeParams.cubeModel.data[:], axis=0), self.additionalOrder)

            self.centSelect.show()
            self.centSelect.open()
        else:

            if float(self.initialWavelengthLineEdit.text()) < self.initRange or \
                float(self.endWavelengthLineEdit.text()) > self.endRange:
                    self.range_warning()
            else:
                initialWaveTrans = wavelength_to_slice(float(self.initialWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)
                endWaveTrans = wavelength_to_slice(float(self.endWavelengthLineEdit.text()), self.cubeParams.cubeModel.meta.wcsinfo.crpix3, self.cubeParams.cubeModel.meta.wcsinfo.cdelt3, self.cubeParams.cubeModel.meta.wcsinfo.crval3)

                self.centSelect.get_data_from_centroid_wave(self.order, self.cubeParams, self.subband, np.mean(self.cubeParams.cubeModel.data[initialWaveTrans:endWaveTrans], axis=0), self.additionalOrder)

                self.centSelect.show()
                self.centSelect.open()


    def get_data_from_sub_viz(self, initRange, endRange, subband, cubeParams, order=None, additionalOrder = None):
        """
        Get data from the main window to initialize the values
        :param float initRange: initial wavelength value
        :param float endRange: end wavelength value
        :param int subband: subband value
        :param object cubeParams: cube data structured
        :param str order: type of action to be done
        :param str additionalOrder: extra action to be done after the centroid had been calculated
        """
        self.initRange = initRange
        self.endRange = endRange
        self.initialWavelengthLineEdit.setText(str(initRange))
        self.endWavelengthLineEdit.setText(str(endRange))
        self.subband = 0
        self.cubeParams = cubeParams
        self.order = order
        self.additionalOrder = additionalOrder

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
        self.initRange = -1
        self.endRange = -1
        self.subband = 0
        self.centSelect.clear_data()
        self.close()

    def closeEvent(self, event):
        self.centSelect.close()
