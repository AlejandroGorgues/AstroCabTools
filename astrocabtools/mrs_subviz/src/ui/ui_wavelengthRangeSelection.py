# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wavelengthRangeSelection.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wavelengthRangeSelection(object):
    def setupUi(self, wavelengthRangeSelection):
        wavelengthRangeSelection.setObjectName("wavelengthRangeSelection")
        wavelengthRangeSelection.setWindowModality(QtCore.Qt.NonModal)
        wavelengthRangeSelection.resize(600, 600)
        wavelengthRangeSelection.setMinimumSize(QtCore.QSize(600, 600))
        self.gridLayout_2 = QtWidgets.QGridLayout(wavelengthRangeSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(wavelengthRangeSelection)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.waveSelect_vbox = QtWidgets.QVBoxLayout()
        self.waveSelect_vbox.setObjectName("waveSelect_vbox")
        self.verticalLayout_3.addLayout(self.waveSelect_vbox)
        self.zoomResetButton = QtWidgets.QPushButton(self.groupBox)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.verticalLayout_3.addWidget(self.zoomResetButton)
        self.saveFITSButton = QtWidgets.QPushButton(self.groupBox)
        self.saveFITSButton.setObjectName("saveFITSButton")
        self.verticalLayout_3.addWidget(self.saveFITSButton)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.rangeLabel = QtWidgets.QLabel(wavelengthRangeSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeLabel.sizePolicy().hasHeightForWidth())
        self.rangeLabel.setSizePolicy(sizePolicy)
        self.rangeLabel.setText("")
        self.rangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rangeLabel.setObjectName("rangeLabel")
        self.gridLayout.addWidget(self.rangeLabel, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(wavelengthRangeSelection)
        QtCore.QMetaObject.connectSlotsByName(wavelengthRangeSelection)

    def retranslateUi(self, wavelengthRangeSelection):
        _translate = QtCore.QCoreApplication.translate
        wavelengthRangeSelection.setWindowTitle(_translate("wavelengthRangeSelection", "wavelegthRangeSelection"))
        self.zoomResetButton.setText(_translate("wavelengthRangeSelection", "Zoom Reset"))
        self.saveFITSButton.setText(_translate("wavelengthRangeSelection", "Save image as .fits"))

