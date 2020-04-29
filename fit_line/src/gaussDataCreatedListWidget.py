"""
Create the Widget structure for the item in the gauss data list widget
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

class gaussListwidget(QtWidgets.QWidget):

    def __init__(self, parent=None, **kwargs):
        label_text =  kwargs.pop('text')
        super(gaussListwidget, self).__init__(parent, **kwargs)

        self.label = QLabel(label_text)
        plot_lay = QHBoxLayout(self)
        plot_lay.addWidget(self.label)
