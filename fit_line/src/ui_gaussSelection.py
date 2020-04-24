# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gaussSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gaussSelection(object):
    def setupUi(self, gaussSelection):
        gaussSelection.setObjectName("gaussSelection")
        gaussSelection.resize(567, 467)
        self.gridLayout_2 = QtWidgets.QGridLayout(gaussSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gaussListWidget = QtWidgets.QListWidget(gaussSelection)
        self.gaussListWidget.setObjectName("gaussListWidget")
        self.gridLayout.addWidget(self.gaussListWidget, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(gaussSelection)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(gaussSelection)
        QtCore.QMetaObject.connectSlotsByName(gaussSelection)

    def retranslateUi(self, gaussSelection):
        _translate = QtCore.QCoreApplication.translate
        gaussSelection.setWindowTitle(_translate("gaussSelection", "Data"))
        self.saveButton.setText(_translate("gaussSelection", "Save data"))
