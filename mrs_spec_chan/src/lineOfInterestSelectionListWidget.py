"""
Create the Widget structure for the item in the line of interest list widget
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

class loiListwidget(QtWidgets.QWidget):
    checked = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        label_text =  kwargs.pop('title')
        super(loiListwidget, self).__init__(parent, **kwargs)

        self.checkbox_button = QCheckBox()
        self.label = QLabel(label_text)
        plot_lay = QHBoxLayout(self)
        plot_lay.addWidget(self.checkbox_button)
        plot_lay.addWidget(self.label)
        self.checkbox_button.setChecked(False)
        self.checkbox_button.clicked.connect(self.checked)

    def loi_text(self):
        return self.label.text()

    def checkbox_state(self):
        return self.checkbox_button.isChecked()


    def set_checkbox_state(self, state):
        self.checkbox_button.setChecked(state)
