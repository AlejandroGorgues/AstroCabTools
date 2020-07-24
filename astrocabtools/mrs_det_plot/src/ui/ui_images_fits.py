# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagesFits.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsImagesFits(object):
    def setupUi(self, MrsImagesFits):
        MrsImagesFits.setObjectName("MrsImagesFits")
        MrsImagesFits.resize(856, 548)
        self.gridLayout_2 = QtWidgets.QGridLayout(MrsImagesFits)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.gridLayout_2.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(MrsImagesFits)
        QtCore.QMetaObject.connectSlotsByName(MrsImagesFits)

    def retranslateUi(self, MrsImagesFits):
        _translate = QtCore.QCoreApplication.translate
        MrsImagesFits.setWindowTitle(_translate("MrsImagesFits", "images - Beta version"))
