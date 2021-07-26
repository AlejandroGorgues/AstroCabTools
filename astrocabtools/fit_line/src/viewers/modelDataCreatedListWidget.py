"""
Create the Widget structure for the item in the model data list widget
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

class modelListwidget(QtWidgets.QWidget):

    def __init__(self, parent=None, **kwargs):
        label_text =  kwargs.pop('text')
        super(modelListwidget, self).__init__(parent, **kwargs)

        self.label = QLabel(label_text)
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        plot_lay = QHBoxLayout(self)
        plot_lay.addWidget(self.label)
