# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrumVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(778, 581)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.spectrumLayout_vbox = QtWidgets.QVBoxLayout()
        self.spectrumLayout_vbox.setObjectName("spectrumLayout_vbox")
        self.verticalLayout_2.addLayout(self.spectrumLayout_vbox)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.loadButton = QtWidgets.QPushButton(Dialog)
        self.loadButton.setEnabled(False)
        self.loadButton.setObjectName("loadButton")
        self.gridLayout.addWidget(self.loadButton, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "spectrumVisualization"))
        self.saveButton.setText(_translate("Dialog", "Save"))
        self.loadButton.setText(_translate("Dialog", "Load spectrum on fitLine"))

