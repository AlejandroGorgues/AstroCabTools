"""
Allow to modify the scale, stretch and color of the current slice
"""

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.mrs_subviz.src.ui.ui_styleManagerCubeViewer

__all__=["StyleManagerCubeViewer"]

class StyleManagerCubeViewer(QDialog, astrocabtools.mrs_subviz.src.ui.ui_styleManagerCubeViewer.Ui_styleManagerCubeViewer):
    update_color = pyqtSignal(str, name ='cubeColorChanged')
    update_scale = pyqtSignal(str, name ='cubeScaleChanged')
    update_stretch = pyqtSignal(str, name ='cubeStretchChanged')

    def __init__(self, parent = None):
        super(StyleManagerCubeViewer, self).__init__(parent)
        self.setupUi(self)

        self.colorComboBox.currentIndexChanged.connect(self.set_color)
        self.scaleComboBox.currentIndexChanged.connect(self.set_scale)
        self.stretchComboBox.currentIndexChanged.connect(self.set_stretch)

    def set_color(self):
        self.update_color.emit(self.colorComboBox.currentText())

    def set_scale(self):

        self.update_scale.emit(self.scaleComboBox.currentText())

    def set_stretch(self):
        self.update_stretch.emit(self.stretchComboBox.currentText())

    def get_data(self):
        return self.colorComboBox.currentText(), self.scaleComboBox.currentText(), self.stretchComboBox.currentText()

    def clear_data(self):
        self.colorComboBox.setCurrentIndex(0)
        self.scaleComboBox.setCurrentIndex(0)
        self.stretchComboBox.setCurrentIndex(0)
        self.close()
