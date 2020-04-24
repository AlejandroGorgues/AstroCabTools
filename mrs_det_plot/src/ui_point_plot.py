# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pointPlot.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsPointPlot(object):
    def setupUi(self, MrsPointPlot):
        MrsPointPlot.setObjectName("MrsPointPlot")
        MrsPointPlot.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(MrsPointPlot)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.pointPlot = QtWidgets.QGroupBox(MrsPointPlot)
        self.pointPlot.setTitle("")
        self.pointPlot.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.pointPlot)
        self.gridLayout.setObjectName("gridLayout")
        self.axis_vbox = QtWidgets.QVBoxLayout()
        self.axis_vbox.setObjectName("axis_vbox")
        self.gridLayout.addLayout(self.axis_vbox, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.pointPlot, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(MrsPointPlot)
        self.saveButton.setObjectName("saveButton")
        self.mainLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(MrsPointPlot)
        QtCore.QMetaObject.connectSlotsByName(MrsPointPlot)

    def retranslateUi(self, MrsPointPlot):
        _translate = QtCore.QCoreApplication.translate
        MrsPointPlot.setWindowTitle(_translate("MrsPointPlot", "PointPlot"))
        self.saveButton.setText(_translate("MrsPointPlot", "Save as png"))
