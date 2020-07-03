"""
Object that allow to select the spectrum to be loaded
and the redshift to be applied
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QIdentityProxyModel, QRegExp
from PyQt5 import QtGui
from PyQt5 import uic

import astrotools.fit_line.src.ui.ui_spectrumSelection

class MrsPltList(QDialog, astrotools.fit_line.src.ui.ui_spectrumSelection.Ui_spectrumSelection):

    def __init__(self, parent=None ):
        super(MrsPltList, self).__init__(parent)
        self.setupUi(self)
        self.extension = "*.txt"
        self.wUnits = "um"
        self.fUnits = "erg/s/cm2/micron"
        self.spectrumPath = ''

        regex = QRegExp('^(0|[1-9][0-9]?|100)$')
        validator = QtGui.QRegExpValidator(regex, self)
        self.waveColumnLineEdit.setValidator(validator)
        self.fluxColumnLineEdit.setValidator(validator)


        self.fileButton.clicked.connect(self.load_directory)

        self.redshiftLineEdit.setValidator(QtGui.QDoubleValidator())
        self.redshiftLineEdit.textChanged.connect(self.update_redshift)

        self.extensionSelectCombobox.currentIndexChanged.connect(self.set_extension)

        self.wUnitsCombobox.currentIndexChanged.connect(self.set_left_units)
        self.fUnitsCombobox.currentIndexChanged.connect(self.set_right_units)

    @pyqtSlot()
    def load_directory(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("files ({})".format(self.extension))

        if fileSearch.exec_():
            self.spectrumPath = fileSearch.selectedFiles()[0]

            self.pathInputLabel.setText(self.spectrumPath)
            self.redshiftLineEdit.setEnabled(True)
            self.acceptButton.setEnabled(True)
            self.redshift = 0.0

    @pyqtSlot()
    def update_redshift(self):
        """Modified redshift value wen line edit update"""
        if self.redshiftLineEdit.text() != '':

            self.redshift=float(self.redshiftLineEdit.text())

        if self.redshiftLineEdit.text() == '':

            self.redshift= 0.0
            self.redshiftLineEdit.setPlaceholderText('0.0')

    def set_extension(self, index):
        if index == 0:
            self.extension = "*.txt"
            self.pathInputLabel.setText('')
        else:
            self.extension = "*.fits"
            self.pathInputLabel.setText('')

    def set_left_units(self, index):
        self.wUnits = self.wUnitsCombobox.itemText(index)

    def set_right_units(self, index):
        self.fUnits =self.fUnitsCombobox.itemText(index)


    def get_data(self):
        wColumn = self.waveColumnLineEdit.text()
        fColumn = self.fluxColumnLineEdit.text()
        if wColumn == '':
            wColumn = self.waveColumnLineEdit.placeholderText()
        if fColumn == '':
            fColumn = self.fluxColumnLineEdit.placeholderText()
        return self.spectrumPath, self.redshift, int(wColumn), int(fColumn), self.wUnits, self.fUnits, self.extension