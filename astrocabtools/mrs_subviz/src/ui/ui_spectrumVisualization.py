# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrumVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_spectrumVisualization(object):
    def setupUi(self, spectrumVisualization):
        spectrumVisualization.setObjectName("spectrumVisualization")
        spectrumVisualization.resize(788, 581)
        self.gridLayout_2 = QtWidgets.QGridLayout(spectrumVisualization)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(spectrumVisualization)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.spectrumLayout_vbox = QtWidgets.QVBoxLayout()
        self.spectrumLayout_vbox.setObjectName("spectrumLayout_vbox")
        self.verticalLayout_2.addLayout(self.spectrumLayout_vbox)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.saveButton = QtWidgets.QPushButton(spectrumVisualization)
        self.saveButton.setEnabled(False)
        self.saveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 0, 1, 2)
        self.zoomResetButton = QtWidgets.QPushButton(spectrumVisualization)
        self.zoomResetButton.setEnabled(False)
        self.zoomResetButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.gridLayout.addWidget(self.zoomResetButton, 1, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(spectrumVisualization)
        QtCore.QMetaObject.connectSlotsByName(spectrumVisualization)

    def retranslateUi(self, spectrumVisualization):
        _translate = QtCore.QCoreApplication.translate
        spectrumVisualization.setWindowTitle(_translate("spectrumVisualization", "spectrumVisualization"))
        self.saveButton.setText(_translate("spectrumVisualization", "Save spectra in txt"))
        self.zoomResetButton.setText(_translate("spectrumVisualization", "Zoom reset"))

