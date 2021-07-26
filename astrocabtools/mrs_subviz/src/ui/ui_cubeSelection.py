# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cubeSelection.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cubeSelection(object):
    def setupUi(self, cubeSelection):
        cubeSelection.setObjectName("cubeSelection")
        cubeSelection.resize(336, 88)
        self.gridLayout_2 = QtWidgets.QGridLayout(cubeSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.operationButton = QtWidgets.QPushButton(cubeSelection)
        self.operationButton.setObjectName("operationButton")
        self.gridLayout.addWidget(self.operationButton, 5, 1, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(cubeSelection)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 5, 0, 1, 1)
        self.subbandSelectionComboBox = QtWidgets.QComboBox(cubeSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subbandSelectionComboBox.sizePolicy().hasHeightForWidth())
        self.subbandSelectionComboBox.setSizePolicy(sizePolicy)
        self.subbandSelectionComboBox.setDuplicatesEnabled(False)
        self.subbandSelectionComboBox.setObjectName("subbandSelectionComboBox")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.gridLayout.addWidget(self.subbandSelectionComboBox, 0, 1, 1, 1)
        self.operationLabel = QtWidgets.QLabel(cubeSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operationLabel.sizePolicy().hasHeightForWidth())
        self.operationLabel.setSizePolicy(sizePolicy)
        self.operationLabel.setObjectName("operationLabel")
        self.gridLayout.addWidget(self.operationLabel, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(cubeSelection)
        self.cancelButton.clicked.connect(cubeSelection.close)
        QtCore.QMetaObject.connectSlotsByName(cubeSelection)

    def retranslateUi(self, cubeSelection):
        _translate = QtCore.QCoreApplication.translate
        cubeSelection.setWindowTitle(_translate("cubeSelection", "cubeSelection"))
        self.operationButton.setText(_translate("cubeSelection", "Make operation"))
        self.cancelButton.setText(_translate("cubeSelection", "Cancel"))
        self.subbandSelectionComboBox.setItemText(0, _translate("cubeSelection", "1A"))
        self.subbandSelectionComboBox.setItemText(1, _translate("cubeSelection", "1B"))
        self.subbandSelectionComboBox.setItemText(2, _translate("cubeSelection", "1C"))
        self.subbandSelectionComboBox.setItemText(3, _translate("cubeSelection", "2A"))
        self.subbandSelectionComboBox.setItemText(4, _translate("cubeSelection", "2B"))
        self.subbandSelectionComboBox.setItemText(5, _translate("cubeSelection", "2C"))
        self.subbandSelectionComboBox.setItemText(6, _translate("cubeSelection", "3A"))
        self.subbandSelectionComboBox.setItemText(7, _translate("cubeSelection", "3B"))
        self.subbandSelectionComboBox.setItemText(8, _translate("cubeSelection", "3C"))
        self.subbandSelectionComboBox.setItemText(9, _translate("cubeSelection", "4A"))
        self.subbandSelectionComboBox.setItemText(10, _translate("cubeSelection", "4B"))
        self.subbandSelectionComboBox.setItemText(11, _translate("cubeSelection", "4C"))
        self.operationLabel.setText(_translate("cubeSelection", "Select cube to make operation"))

