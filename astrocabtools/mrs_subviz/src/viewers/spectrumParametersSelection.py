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

import astrocabtools.mrs_subviz.src.ui.ui_spectrumParameterSelection

from ..utils.subband_contiguous import subband_contiguous


class SpectrumParametersSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_spectrumParameterSelection.Ui_spectrumParametersSelection):

    def __init__(self, parent=None):
        super(SpectrumParametersSelection, self).__init__(parent)
        self.setupUi(self)
        self.extension = "*.txt"
        self.wUnits = "um"
        self.fUnits = "erg/s/cm2/micron"
        self.spectrumType = "Aperture spectrum"
        self.subbands = ["1S","1M","1SL","2S","2M","2L","3S","3M","3L","4S","4M","4L",]
        self.subbandToggledSelected = "All subbands"

        self.wUnitsComboBox.currentIndexChanged.connect(self.set_left_units)
        self.fUnitsComboBox.currentIndexChanged.connect(self.set_right_units)
        self.spectrumComboBox.currentIndexChanged.connect(self.set_spectrum)

        self.allRadioButton.toggled.connect(self.subbandToggled)
        self.contiguousRadioButton.toggled.connect(self.subbandToggled)


    def set_left_units(self, index):
        self.wUnits = self.wUnitsComboBox.itemText(index)

    def set_right_units(self, index):
        self.fUnits =self.fUnitsComboBox.itemText(index)

    def set_spectrum(self, index):
        self.spectrumType = self.spectrumComboBox.itemText(index)

    def subbandToggled(self):
        if self.sender().text() == "All subbands" and self.sender().isChecked():
            self.subbandToggledSelected = self.sender().text()
            self.set_checked_state_subbands(False)
            self.subbandGroupBox.setEnabled(False)

        elif self.sender().text() != "All subbands" and self.sender().isChecked():
            self.subbandToggledSelected = self.sender().text()
            self.set_checked_state_subbands(False)
            self.subbandGroupBox.setEnabled(True)

    def get_data(self):
        if self.subbandToggledSelected == "All subbands":
            self.subbands =["1S", "1M", "1L", "2S", "2M", "2L", "3S", "3M", "3L", "4S", "4M", "4L"]
        else:
            self.subbands.clear()
            self.get_subbands_checked()

        if (subband_contiguous(self.subbands) or len(self.subbands) == 1) and len(self.subbands) != 0:
            return self.wUnits, self.fUnits, self.spectrumType, self.subbands
        else:
            self.wrong_subband_warning()

    def get_subbands_checked(self):
        widgets = (self.gridLayout_3.itemAt(i).widget() for i in range(self.gridLayout_3.count()-1,-1, -1))
        for widget in widgets:
            if widget.isChecked():
                self.subbands.append(widget.text())

    def set_checked_state_subbands(self, state):
        widgets = (self.gridLayout_3.itemAt(i).widget() for i in range(self.gridLayout_3.count()))
        for widget in widgets:
            if widget.isChecked():
                widget.setChecked(state)

    def wrong_subband_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Subbands selected must be contiguous")
        warning.exec_()

    def clear_data(self):
        self.spectrumComboBox.setCurrentIndex(0)
        self.wUnitsComboBox.setCurrentIndex(0)
        self.fUnitsComboBox.setCurrentIndex(0)


