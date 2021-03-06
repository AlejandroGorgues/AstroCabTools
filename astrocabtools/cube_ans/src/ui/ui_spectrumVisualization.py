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
        self.rangeImageButton = QtWidgets.QPushButton(spectrumVisualization)
        self.rangeImageButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeImageButton.sizePolicy().hasHeightForWidth())
        self.rangeImageButton.setSizePolicy(sizePolicy)
        self.rangeImageButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rangeImageButton.setObjectName("rangeImageButton")
        self.gridLayout.addWidget(self.rangeImageButton, 6, 0, 1, 3)
        self.moveRangeButton = QtWidgets.QToolButton(spectrumVisualization)
        self.moveRangeButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moveRangeButton.sizePolicy().hasHeightForWidth())
        self.moveRangeButton.setSizePolicy(sizePolicy)
        self.moveRangeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.moveRangeButton.setCheckable(True)
        self.moveRangeButton.setObjectName("moveRangeButton")
        self.gridLayout.addWidget(self.moveRangeButton, 1, 1, 1, 1)
        self.createRangeButton = QtWidgets.QToolButton(spectrumVisualization)
        self.createRangeButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createRangeButton.sizePolicy().hasHeightForWidth())
        self.createRangeButton.setSizePolicy(sizePolicy)
        self.createRangeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.createRangeButton.setCheckable(True)
        self.createRangeButton.setObjectName("createRangeButton")
        self.gridLayout.addWidget(self.createRangeButton, 1, 0, 1, 1)
        self.zoomResetButton = QtWidgets.QPushButton(spectrumVisualization)
        self.zoomResetButton.setEnabled(False)
        self.zoomResetButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.gridLayout.addWidget(self.zoomResetButton, 1, 2, 1, 1)
        self.saveButton = QtWidgets.QPushButton(spectrumVisualization)
        self.saveButton.setEnabled(False)
        self.saveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(spectrumVisualization)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.spectrumLayout_vbox = QtWidgets.QVBoxLayout()
        self.spectrumLayout_vbox.setObjectName("spectrumLayout_vbox")
        self.verticalLayout_2.addLayout(self.spectrumLayout_vbox)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.loadButton = QtWidgets.QPushButton(spectrumVisualization)
        self.loadButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        self.loadButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loadButton.setObjectName("loadButton")
        self.gridLayout.addWidget(self.loadButton, 5, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(spectrumVisualization)
        QtCore.QMetaObject.connectSlotsByName(spectrumVisualization)

    def retranslateUi(self, spectrumVisualization):
        _translate = QtCore.QCoreApplication.translate
        spectrumVisualization.setWindowTitle(_translate("spectrumVisualization", "spectrumVisualization"))
        self.rangeImageButton.setText(_translate("spectrumVisualization", "Show image from wavelength range"))
        self.moveRangeButton.setText(_translate("spectrumVisualization", "Move range"))
        self.createRangeButton.setText(_translate("spectrumVisualization", "Select area"))
        self.zoomResetButton.setText(_translate("spectrumVisualization", "Zoom reset"))
        self.saveButton.setText(_translate("spectrumVisualization", "Save"))
        self.loadButton.setText(_translate("spectrumVisualization", "Load spectrum on fitLine"))

