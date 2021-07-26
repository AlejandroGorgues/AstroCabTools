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
        cubeSelection.resize(650, 120)
        cubeSelection.setMinimumSize(QtCore.QSize(650, 120))
        cubeSelection.setMaximumSize(QtCore.QSize(650, 120))
        self.gridLayout_2 = QtWidgets.QGridLayout(cubeSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cubeSelectionButton = QtWidgets.QPushButton(cubeSelection)
        self.cubeSelectionButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cubeSelectionButton.setObjectName("cubeSelectionButton")
        self.gridLayout.addWidget(self.cubeSelectionButton, 0, 2, 1, 2)
        self.cubeComboBox = QtWidgets.QComboBox(cubeSelection)
        self.cubeComboBox.setObjectName("cubeComboBox")
        self.cubeComboBox.addItem("")
        self.cubeComboBox.addItem("")
        self.cubeComboBox.addItem("")
        self.cubeComboBox.addItem("")
        self.gridLayout.addWidget(self.cubeComboBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(cubeSelection)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.filePathLabel = QtWidgets.QLabel(cubeSelection)
        self.filePathLabel.setText("")
        self.filePathLabel.setObjectName("filePathLabel")
        self.gridLayout.addWidget(self.filePathLabel, 1, 1, 1, 3)
        self.label_2 = QtWidgets.QLabel(cubeSelection)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(cubeSelection)
        self.cancelButton.setEnabled(True)
        self.cancelButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 2, 0, 1, 2)
        self.acceptButton = QtWidgets.QPushButton(cubeSelection)
        self.acceptButton.setEnabled(False)
        self.acceptButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 2, 2, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(cubeSelection)
        self.acceptButton.clicked.connect(cubeSelection.accept)
        self.cancelButton.clicked.connect(cubeSelection.reject)
        QtCore.QMetaObject.connectSlotsByName(cubeSelection)

    def retranslateUi(self, cubeSelection):
        _translate = QtCore.QCoreApplication.translate
        cubeSelection.setWindowTitle(_translate("cubeSelection", "cubeSelection"))
        self.cubeSelectionButton.setText(_translate("cubeSelection", "Select File Path"))
        self.cubeComboBox.setItemText(0, _translate("cubeSelection", "Select cube model"))
        self.cubeComboBox.setItemText(1, _translate("cubeSelection", "MIRI"))
        self.cubeComboBox.setItemText(2, _translate("cubeSelection", "MUSE"))
        self.cubeComboBox.setItemText(3, _translate("cubeSelection", "MEGARA"))
        self.label.setText(_translate("cubeSelection", "Type of cube"))
        self.label_2.setText(_translate("cubeSelection", "File Path: "))
        self.cancelButton.setText(_translate("cubeSelection", "Cancel"))
        self.acceptButton.setText(_translate("cubeSelection", "Accept"))

