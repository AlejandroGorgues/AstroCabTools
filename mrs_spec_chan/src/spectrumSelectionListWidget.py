"""
Create the Widget structure for the item in the spectrum selection list widget
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

class spectrumListWidget(QtWidgets.QWidget):
    checked = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        label_text =  kwargs.pop('title')
        super(spectrumListWidget, self).__init__(parent, **kwargs)

        self.checkbox_button = QCheckBox()
        self.line_edit = QLineEdit()
        self.label = QLabel(label_text)

        self.line_edit.setMaximumWidth(100)

        self.line_edit.setSizePolicy(QSizePolicy.Preferred,
                                             QSizePolicy.Preferred)
        self.label.setSizePolicy(QSizePolicy.Preferred,
                                             QSizePolicy.Preferred)

        self.line_edit.setPlaceholderText("Redshift value")
        self.line_edit.setValidator(QtGui.QDoubleValidator())

        plot_lay = QHBoxLayout(self)
        plot_lay.addWidget(self.checkbox_button)
        plot_lay.addWidget(self.line_edit)
        plot_lay.addWidget(self.label)
        plot_lay.setAlignment(Qt.AlignLeft)
        self.checkbox_button.setChecked(False)
        self.checkbox_button.clicked.connect(self.checked)
        self.line_edit.textChanged.connect(self.changed)

        self.checkbox_button.setEnabled(False)

    def path_text(self):
        return self.label.text()

    def redshift_value(self):
        return self.line_edit.text()

    def checkbox_state(self):
        return self.checkbox_button.isChecked()

    def set_redshift_value(self, text):
        self.line_edit.setText(text)

    def set_checkbox_state(self, state):
        self.checkbox_button.setEnabled(state)

    def set_checkbox_checked(self, state):
        self.checkbox_button.setChecked(state)
