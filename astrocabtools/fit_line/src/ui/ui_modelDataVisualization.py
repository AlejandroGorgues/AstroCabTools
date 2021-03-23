# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modelDataVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_modelDataVisualization(object):
    def setupUi(self, modelDataVisualization):
        modelDataVisualization.setObjectName("modelDataVisualization")
        modelDataVisualization.resize(567, 467)
        self.gridLayout_2 = QtWidgets.QGridLayout(modelDataVisualization)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.saveButton = QtWidgets.QPushButton(modelDataVisualization)
        self.saveButton.setEnabled(False)
        self.saveButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.modelListWidget = QtWidgets.QListWidget(modelDataVisualization)
        self.modelListWidget.setObjectName("modelListWidget")
        self.gridLayout.addWidget(self.modelListWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(modelDataVisualization)
        QtCore.QMetaObject.connectSlotsByName(modelDataVisualization)

    def retranslateUi(self, modelDataVisualization):
        _translate = QtCore.QCoreApplication.translate
        modelDataVisualization.setWindowTitle(_translate("modelDataVisualization", "Data"))
        self.saveButton.setText(_translate("modelDataVisualization", "Save data"))

