# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gaussDataVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_gaussDataVisualization(object):
    def setupUi(self, gaussDataVisualization):
        gaussDataVisualization.setObjectName("gaussDataVisualization")
        gaussDataVisualization.resize(567, 467)
        self.gridLayout_2 = QtWidgets.QGridLayout(gaussDataVisualization)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtWidgets.QPushButton(gaussDataVisualization)
        self.saveButton.setEnabled(False)
        self.saveButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.gaussListWidget = QtWidgets.QListWidget(gaussDataVisualization)
        self.gaussListWidget.setObjectName("gaussListWidget")
        self.gridLayout.addWidget(self.gaussListWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(gaussDataVisualization)
        QtCore.QMetaObject.connectSlotsByName(gaussDataVisualization)

    def retranslateUi(self, gaussDataVisualization):
        _translate = QtCore.QCoreApplication.translate
        gaussDataVisualization.setWindowTitle(_translate("gaussDataVisualization", "Data"))
        self.saveButton.setText(_translate("gaussDataVisualization", "Save data"))

