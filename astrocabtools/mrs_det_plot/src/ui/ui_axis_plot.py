# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'axisPlot.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsAxisPlot(object):
    def setupUi(self, MrsAxisPlot):
        MrsAxisPlot.setObjectName("MrsAxisPlot")
        MrsAxisPlot.resize(679, 458)
        self.gridLayout_2 = QtWidgets.QGridLayout(MrsAxisPlot)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.axisPlot = QtWidgets.QGroupBox(MrsAxisPlot)
        self.axisPlot.setTitle("")
        self.axisPlot.setObjectName("axisPlot")
        self.gridLayout = QtWidgets.QGridLayout(self.axisPlot)
        self.gridLayout.setObjectName("gridLayout")
        self.axis_vbox = QtWidgets.QVBoxLayout()
        self.axis_vbox.setObjectName("axis_vbox")
        self.gridLayout.addLayout(self.axis_vbox, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.axisPlot, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(MrsAxisPlot)
        self.saveButton.setObjectName("saveButton")
        self.mainLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(MrsAxisPlot)
        QtCore.QMetaObject.connectSlotsByName(MrsAxisPlot)

    def retranslateUi(self, MrsAxisPlot):
        _translate = QtCore.QCoreApplication.translate
        MrsAxisPlot.setWindowTitle(_translate("MrsAxisPlot", "axisPlot - Beta version"))
        self.saveButton.setText(_translate("MrsAxisPlot", "Save as png"))
