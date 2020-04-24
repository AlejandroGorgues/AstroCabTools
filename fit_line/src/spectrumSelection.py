import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QIdentityProxyModel
from PyQt5 import QtGui
from PyQt5 import uic

import fit_line.src.ui_spectrumSelection

class MrsPltList(QDialog, fit_line.src.ui_spectrumSelection.Ui_spectrumSelection):

    def __init__(self, parent=None ):
        super(MrsPltList, self).__init__(parent)
        self.setupUi(self)

        self.setModal(False)

        self.fileButton.clicked.connect(self.load_directory)

        self.redshiftLineEdit.setValidator(QtGui.QDoubleValidator())
        self.redshiftLineEdit.textChanged.connect(self.update_redshift)

    @pyqtSlot()
    def load_directory(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("txt files (*.txt)")

        if fileSearch.exec_():
            self.spectrumPath = fileSearch.selectedFiles()[0]

            self.pathInputLabel.setText(self.spectrumPath)
            self.redshiftLineEdit.setEnabled(True)
            self.acceptButton.setEnabled(True)
            self.redshift = 0.0

    @pyqtSlot()
    def update_redshift(self):

        if self.redshiftLineEdit.text() != '':

            self.redshift=float(self.redshiftLineEdit.text())

        if self.redshiftLineEdit.text() == '':

            self.redshift= 0.0
            self.redshiftLineEdit.setPlaceholderText('0.0')

    def get_data(self):
        return self.spectrumPath, self.redshift
