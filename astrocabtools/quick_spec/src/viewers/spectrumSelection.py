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

import astrocabtools.quick_spec.src.ui.ui_spectrumSelection

class SpectrumSelection(QDialog, astrocabtools.quick_spec.src.ui.ui_spectrumSelection.Ui_spectrumSelection):

    def __init__(self, parent=None ):
        super(SpectrumSelection, self).__init__(parent)
        self.setupUi(self)
        self.spectrumPath = ''

        self.fileButton.clicked.connect(self.load_directory)

    @pyqtSlot()
    def load_directory(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("files ({})".format('*.txt'))

        if fileSearch.exec_():
            self.spectrumPath = fileSearch.selectedFiles()[0]

            self.pathInputLabel.setText(self.spectrumPath)
            self.acceptButton.setEnabled(True)

    def get_data(self):

        return self.spectrumPath
