# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rectangleCoordinates.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_rectangleCoordinates(object):
    def setupUi(self, rectangleCoordinates):
        rectangleCoordinates.setObjectName("rectangleCoordinates")
        rectangleCoordinates.resize(525, 106)
        rectangleCoordinates.setMinimumSize(QtCore.QSize(525, 100))
        rectangleCoordinates.setMaximumSize(QtCore.QSize(16777215, 106))
        self.gridLayout_2 = QtWidgets.QGridLayout(rectangleCoordinates)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(rectangleCoordinates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3, QtCore.Qt.AlignHCenter)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.leftXLabel = QtWidgets.QLabel(rectangleCoordinates)
        self.leftXLabel.setObjectName("leftXLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.leftXLabel)
        self.leftXLineEdit = QtWidgets.QLineEdit(rectangleCoordinates)
        self.leftXLineEdit.setEnabled(True)
        self.leftXLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.leftXLineEdit.setReadOnly(True)
        self.leftXLineEdit.setObjectName("leftXLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.leftXLineEdit)
        self.rightXLabel = QtWidgets.QLabel(rectangleCoordinates)
        self.rightXLabel.setObjectName("rightXLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rightXLabel)
        self.rightXLineEdit = QtWidgets.QLineEdit(rectangleCoordinates)
        self.rightXLineEdit.setEnabled(True)
        self.rightXLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.rightXLineEdit.setReadOnly(True)
        self.rightXLineEdit.setObjectName("rightXLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rightXLineEdit)
        self.gridLayout.addLayout(self.formLayout, 7, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout_2.setObjectName("formLayout_2")
        self.topYLabel = QtWidgets.QLabel(rectangleCoordinates)
        self.topYLabel.setObjectName("topYLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.topYLabel)
        self.topYLineEdit = QtWidgets.QLineEdit(rectangleCoordinates)
        self.topYLineEdit.setEnabled(True)
        self.topYLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.topYLineEdit.setReadOnly(True)
        self.topYLineEdit.setObjectName("topYLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.topYLineEdit)
        self.bottomYLabel = QtWidgets.QLabel(rectangleCoordinates)
        self.bottomYLabel.setObjectName("bottomYLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.bottomYLabel)
        self.bottomYLineEdit = QtWidgets.QLineEdit(rectangleCoordinates)
        self.bottomYLineEdit.setEnabled(True)
        self.bottomYLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.bottomYLineEdit.setReadOnly(True)
        self.bottomYLineEdit.setObjectName("bottomYLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.bottomYLineEdit)
        self.gridLayout.addLayout(self.formLayout_2, 7, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)

        self.retranslateUi(rectangleCoordinates)
        QtCore.QMetaObject.connectSlotsByName(rectangleCoordinates)

    def retranslateUi(self, rectangleCoordinates):
        _translate = QtCore.QCoreApplication.translate
        rectangleCoordinates.setWindowTitle(_translate("rectangleCoordinates", "rectangleCoordinates"))
        self.label.setText(_translate("rectangleCoordinates", "Rectangle selection coordinates"))
        self.leftXLabel.setText(_translate("rectangleCoordinates", "Left X"))
        self.rightXLabel.setText(_translate("rectangleCoordinates", "Right X"))
        self.topYLabel.setText(_translate("rectangleCoordinates", "Top Y"))
        self.bottomYLabel.setText(_translate("rectangleCoordinates", "Bottom Y"))
