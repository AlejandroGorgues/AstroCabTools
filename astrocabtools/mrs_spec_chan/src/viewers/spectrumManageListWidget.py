"""
Create the Widget structure for the item in the spectrum manage list widget
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtWidgets import *

class listWidget(QtWidgets.QWidget):
    clicked = pyqtSignal()
    checked = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        label_text =  kwargs.pop('title')
        redshift_text = kwargs.pop('redshift')
        super(listWidget, self).__init__(parent, **kwargs)

        self.checkbox_button = QCheckBox()
        self.labelRedshift = QLabel("z: "+str(redshift_text))
        self.labelPath = QLabel("Path: "+label_text)
        delete_button = QPushButton("D")

        delete_button.setFixedWidth(20)
        plot_lay = QHBoxLayout(self)
        plot_lay.addWidget(self.checkbox_button)
        plot_lay.addWidget(self.labelRedshift)
        plot_lay.addWidget(self.labelPath)
        plot_lay.addWidget(delete_button)
        delete_button.clicked.connect(self.clicked)
        self.checkbox_button.setChecked(True)
        self.checkbox_button.clicked.connect(self.checked)


    def path_text(self):
        return self.labelPath.text()

    def redshift_text(self):
        return self.labelRedshift.text()

    def checkbox_state(self):
        return self.checkbox_button.isChecked()
