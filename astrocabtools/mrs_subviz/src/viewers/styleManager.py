"""
Allow to modify the slice of the current subband selected
"""

import sys
import glob
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.mrs_subviz.src.ui.ui_styleManager

__all__=["StyleManager"]

class StyleManager(QDialog, astrocabtools.mrs_subviz.src.ui.ui_styleManager.Ui_styleManager):
    update_color = pyqtSignal(str, int, name ='colorChanged')
    update_scale = pyqtSignal(str, int, name ='scaleChanged')
    update_stretch = pyqtSignal(str, int, name ='stretchChanged')

    def __init__(self, parent = None):
        super(StyleManager, self).__init__(parent)
        self.setupUi(self)

        self.index = 0

        self.subbandComboBox.currentIndexChanged.connect(self.set_subband)
        self.colorComboBox.currentIndexChanged.connect(self.set_color)
        self.scaleComboBox.currentIndexChanged.connect(self.set_scale)
        self.stretchComboBox.currentIndexChanged.connect(self.set_stretch)
        self.allSubbandsCheckBox.stateChanged.connect(self.update_subbands)


    def set_subband(self, index):
        self.index = index
        if index > 0:
            self.update_color.emit(self.colorComboBox.currentText(), index-1)
            self.update_scale.emit(self.scaleComboBox.currentText(), index-1)
            self.update_stretch.emit(self.stretchComboBox.currentText(), index-1)

    def set_color(self, index):
        if self.index > 0:
            self.update_color.emit(self.colorComboBox.currentText(), self.index-1)

    def set_scale(self, index):

        if self.index > 0:
            self.update_scale.emit(self.scaleComboBox.currentText(), self.index-1)

    def set_stretch(self, index):
        if self.index > 0:
            self.update_stretch.emit(self.stretchComboBox.currentText(), self.index-1)

    def update_subbands(self, state):
        if(Qt.Checked == state):
            self.subbandComboBox.setEnabled(False)
            #Number 13 means that each style modification
            #is applied to all subbands
            self.index = 14
        else:
            self.subbandComboBox.setEnabled(True)
            self.index = self.subbandComboBox.currentIndex()

    def clear_data(self):
        self.colorComboBox.setCurrentIndex(0)
        self.scaleComboBox.setCurrentIndex(0)
        self.stretchComboBox.setCurrentIndex(0)
        self.close()
