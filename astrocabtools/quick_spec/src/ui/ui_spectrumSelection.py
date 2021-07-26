# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrumSelection.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_spectrumSelection(object):
    def setupUi(self, spectrumSelection):
        spectrumSelection.setObjectName("spectrumSelection")
        spectrumSelection.setWindowModality(QtCore.Qt.NonModal)
        spectrumSelection.resize(500, 91)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(spectrumSelection.sizePolicy().hasHeightForWidth())
        spectrumSelection.setSizePolicy(sizePolicy)
        spectrumSelection.setMinimumSize(QtCore.QSize(500, 0))
        spectrumSelection.setAutoFillBackground(False)
        spectrumSelection.setSizeGripEnabled(False)
        spectrumSelection.setModal(False)
        self.gridLayout_2 = QtWidgets.QGridLayout(spectrumSelection)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.pathLabel = QtWidgets.QLabel(spectrumSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathLabel.sizePolicy().hasHeightForWidth())
        self.pathLabel.setSizePolicy(sizePolicy)
        self.pathLabel.setObjectName("pathLabel")
        self.gridLayout.addWidget(self.pathLabel, 4, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(spectrumSelection)
        self.cancelButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 6, 0, 1, 2)
        self.pathInputLabel = QtWidgets.QLabel(spectrumSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathInputLabel.sizePolicy().hasHeightForWidth())
        self.pathInputLabel.setSizePolicy(sizePolicy)
        self.pathInputLabel.setText("")
        self.pathInputLabel.setObjectName("pathInputLabel")
        self.gridLayout.addWidget(self.pathInputLabel, 4, 1, 1, 3)
        self.acceptButton = QtWidgets.QPushButton(spectrumSelection)
        self.acceptButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy)
        self.acceptButton.setMinimumSize(QtCore.QSize(0, 0))
        self.acceptButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 6, 2, 1, 2)
        self.fileButton = QtWidgets.QPushButton(spectrumSelection)
        self.fileButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileButton.sizePolicy().hasHeightForWidth())
        self.fileButton.setSizePolicy(sizePolicy)
        self.fileButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fileButton.setObjectName("fileButton")
        self.gridLayout.addWidget(self.fileButton, 0, 0, 1, 4)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(spectrumSelection)
        self.cancelButton.clicked.connect(spectrumSelection.reject)
        self.acceptButton.clicked.connect(spectrumSelection.accept)
        QtCore.QMetaObject.connectSlotsByName(spectrumSelection)

    def retranslateUi(self, spectrumSelection):
        _translate = QtCore.QCoreApplication.translate
        spectrumSelection.setWindowTitle(_translate("spectrumSelection", "spectrumSelection"))
        self.pathLabel.setText(_translate("spectrumSelection", "Path: "))
        self.cancelButton.setText(_translate("spectrumSelection", "Cancel"))
        self.acceptButton.setText(_translate("spectrumSelection", "Accept"))
        self.fileButton.setText(_translate("spectrumSelection", "Select File"))

