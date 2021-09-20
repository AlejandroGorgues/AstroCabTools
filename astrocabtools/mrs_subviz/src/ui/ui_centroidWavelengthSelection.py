# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'centroidWavelengthSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_centroidWavelengthSelection(object):
    def setupUi(self, centroidWavelengthSelection):
        centroidWavelengthSelection.setObjectName("centroidWavelengthSelection")
        centroidWavelengthSelection.resize(500, 150)
        centroidWavelengthSelection.setMinimumSize(QtCore.QSize(500, 150))
        self.gridLayout_2 = QtWidgets.QGridLayout(centroidWavelengthSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.initialWavelengthLineEdit = QtWidgets.QLineEdit(centroidWavelengthSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initialWavelengthLineEdit.sizePolicy().hasHeightForWidth())
        self.initialWavelengthLineEdit.setSizePolicy(sizePolicy)
        self.initialWavelengthLineEdit.setClearButtonEnabled(False)
        self.initialWavelengthLineEdit.setObjectName("initialWavelengthLineEdit")
        self.gridLayout_2.addWidget(self.initialWavelengthLineEdit, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(centroidWavelengthSelection)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(centroidWavelengthSelection)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.customWavelengthButton = QtWidgets.QPushButton(centroidWavelengthSelection)
        self.customWavelengthButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.customWavelengthButton.setObjectName("customWavelengthButton")
        self.gridLayout_2.addWidget(self.customWavelengthButton, 3, 1, 1, 2)
        self.endWavelengthLineEdit = QtWidgets.QLineEdit(centroidWavelengthSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endWavelengthLineEdit.sizePolicy().hasHeightForWidth())
        self.endWavelengthLineEdit.setSizePolicy(sizePolicy)
        self.endWavelengthLineEdit.setObjectName("endWavelengthLineEdit")
        self.gridLayout_2.addWidget(self.endWavelengthLineEdit, 2, 3, 1, 1)
        self.allWavelengthButton = QtWidgets.QPushButton(centroidWavelengthSelection)
        self.allWavelengthButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.allWavelengthButton.setObjectName("allWavelengthButton")
        self.gridLayout_2.addWidget(self.allWavelengthButton, 1, 1, 1, 2)
        self.initialRangeLabel = QtWidgets.QLabel(centroidWavelengthSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initialRangeLabel.sizePolicy().hasHeightForWidth())
        self.initialRangeLabel.setSizePolicy(sizePolicy)
        self.initialRangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.initialRangeLabel.setObjectName("initialRangeLabel")
        self.gridLayout_2.addWidget(self.initialRangeLabel, 0, 1, 1, 1)
        self.endRangeLabel = QtWidgets.QLabel(centroidWavelengthSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endRangeLabel.sizePolicy().hasHeightForWidth())
        self.endRangeLabel.setSizePolicy(sizePolicy)
        self.endRangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endRangeLabel.setObjectName("endRangeLabel")
        self.gridLayout_2.addWidget(self.endRangeLabel, 0, 2, 1, 1)

        self.retranslateUi(centroidWavelengthSelection)
        QtCore.QMetaObject.connectSlotsByName(centroidWavelengthSelection)

    def retranslateUi(self, centroidWavelengthSelection):
        _translate = QtCore.QCoreApplication.translate
        centroidWavelengthSelection.setWindowTitle(_translate("centroidWavelengthSelection", "centroidWavelengthSelection"))
        self.label_2.setText(_translate("centroidWavelengthSelection", "End wavelength"))
        self.label.setText(_translate("centroidWavelengthSelection", "Initial wavelength"))
        self.customWavelengthButton.setText(_translate("centroidWavelengthSelection", "Select range"))
        self.allWavelengthButton.setText(_translate("centroidWavelengthSelection", "Select all wavelength range"))
        self.initialRangeLabel.setText(_translate("centroidWavelengthSelection", "Initial Range"))
        self.endRangeLabel.setText(_translate("centroidWavelengthSelection", "End Range"))
