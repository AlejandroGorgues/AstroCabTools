# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'residualsVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_residualsVisualization(object):
    def setupUi(self, residualsVisualization):
        residualsVisualization.setObjectName("residualsVisualization")
        residualsVisualization.resize(833, 747)
        self.residualsLayout = QtWidgets.QGridLayout(residualsVisualization)
        self.residualsLayout.setObjectName("residualsLayout")
        self.residualGroupbox = QtWidgets.QGroupBox(residualsVisualization)
        self.residualGroupbox.setTitle("")
        self.residualGroupbox.setObjectName("residualGroupbox")
        self.residualsLayout.addWidget(self.residualGroupbox, 0, 0, 1, 1)

        self.retranslateUi(residualsVisualization)
        QtCore.QMetaObject.connectSlotsByName(residualsVisualization)

    def retranslateUi(self, residualsVisualization):
        _translate = QtCore.QCoreApplication.translate
        residualsVisualization.setWindowTitle(_translate("residualsVisualization", "Residuals"))
