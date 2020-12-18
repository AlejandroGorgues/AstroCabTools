"""
Object that allow to select the spectrum to be loaded
and the redshift to be applied
"""
import numpy as np

import sys
import glob
import traceback
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QRegExp
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.cube_ans.src.ui.ui_spectrumParametersSelection

class SpectrumParametersSelection(QDialog, astrocabtools.cube_ans.src.ui.ui_spectrumParametersSelection.Ui_spectrumParametersSelection):

    def __init__(self, parent=None):
        super(SpectrumParametersSelection, self).__init__(parent)
        self.setupUi(self)
        self.extension = "*.txt"
        self.wUnits = "um"
        self.fUnits = "erg/s/cm2/micron"
        self.spectrumPath = ''
        self.redshift = 0.0
        self.spectrumType = "Aperture spectrum"

        self.redshiftLineEdit.setValidator(QtGui.QDoubleValidator())
        self.redshiftLineEdit.textChanged.connect(self.update_redshift)

        self.wUnitsComboBox.currentIndexChanged.connect(self.set_left_units)
        self.fUnitsComboBox.currentIndexChanged.connect(self.set_right_units)
        self.spectrumComboBox.currentIndexChanged.connect(self.set_spectrum)

    def update_path(self, path):
        self.pathLabel.setText(path)

    @pyqtSlot()
    def update_redshift(self):
        """Modified redshift value wen line edit update"""
        if self.redshiftLineEdit.text() != '':
            self.redshift = self.redshiftLineEdit.text()
        if self.redshiftLineEdit.text() == '':
            self.redshift= 0.0

    def set_left_units(self, index):
        self.wUnits = self.wUnitsComboBox.itemText(index)

    def set_right_units(self, index):
        self.fUnits =self.fUnitsComboBox.itemText(index)

    def set_spectrum(self, index):
        self.spectrumType = self.spectrumComboBox.itemText(index)

    def get_data(self):
        return self.redshift, self.wUnits, self.fUnits, self.spectrumType

    def clear_data(self):
        self.pathLabel.setText('')
        self.redshiftLineEdit.setText('')
        self.spectrumComboBox.setCurrentIndex(0)
        self.wUnitsComboBox.setCurrentIndex(0)
        self.fUnitsComboBox.setCurrentIndex(0)

    def redhisft_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Wrong redshift value")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
