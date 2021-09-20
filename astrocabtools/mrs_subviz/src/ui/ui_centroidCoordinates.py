# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'centroidCoordinates.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_centroidCoordinates(object):
    def setupUi(self, centroidCoordinates):
        centroidCoordinates.setObjectName("centroidCoordinates")
        centroidCoordinates.resize(250, 100)
        centroidCoordinates.setMinimumSize(QtCore.QSize(250, 100))
        self.gridLayout_2 = QtWidgets.QGridLayout(centroidCoordinates)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(centroidCoordinates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(centroidCoordinates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.xCoordLineEdit = QtWidgets.QLineEdit(centroidCoordinates)
        self.xCoordLineEdit.setReadOnly(True)
        self.xCoordLineEdit.setObjectName("xCoordLineEdit")
        self.gridLayout.addWidget(self.xCoordLineEdit, 1, 0, 1, 1)
        self.yCoordLineEdit = QtWidgets.QLineEdit(centroidCoordinates)
        self.yCoordLineEdit.setReadOnly(True)
        self.yCoordLineEdit.setObjectName("yCoordLineEdit")
        self.gridLayout.addWidget(self.yCoordLineEdit, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(centroidCoordinates)
        QtCore.QMetaObject.connectSlotsByName(centroidCoordinates)

    def retranslateUi(self, centroidCoordinates):
        _translate = QtCore.QCoreApplication.translate
        centroidCoordinates.setWindowTitle(_translate("centroidCoordinates", "centroidCoordinates"))
        self.label.setText(_translate("centroidCoordinates", "X Coordinate"))
        self.label_2.setText(_translate("centroidCoordinates", "Y Coordinate"))
