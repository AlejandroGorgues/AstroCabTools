# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backgroundSubtraction.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_backgroundSubtraction(object):
    def setupUi(self, backgroundSubtraction):
        backgroundSubtraction.setObjectName("backgroundSubtraction")
        backgroundSubtraction.resize(656, 293)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backgroundSubtraction.sizePolicy().hasHeightForWidth())
        backgroundSubtraction.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(backgroundSubtraction)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.innerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.innerRadiusLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.innerRadiusLineEdit.setObjectName("innerRadiusLineEdit")
        self.gridLayout.addWidget(self.innerRadiusLineEdit, 2, 1, 1, 1)
        self.outerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.outerRadiusLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.outerRadiusLineEdit.setObjectName("outerRadiusLineEdit")
        self.gridLayout.addWidget(self.outerRadiusLineEdit, 3, 1, 1, 1)
        self.applyButton = QtWidgets.QPushButton(backgroundSubtraction)
        self.applyButton.setEnabled(True)
        self.applyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 4, 0, 1, 3)
        self.label = QtWidgets.QLabel(backgroundSubtraction)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.xCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.xCenterLineEdit.setEnabled(False)
        self.xCenterLineEdit.setAutoFillBackground(False)
        self.xCenterLineEdit.setReadOnly(True)
        self.xCenterLineEdit.setClearButtonEnabled(False)
        self.xCenterLineEdit.setObjectName("xCenterLineEdit")
        self.horizontalLayout.addWidget(self.xCenterLineEdit)
        self.label_4 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.yCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.yCenterLineEdit.setEnabled(False)
        self.yCenterLineEdit.setObjectName("yCenterLineEdit")
        self.horizontalLayout.addWidget(self.yCenterLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(backgroundSubtraction)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(backgroundSubtraction)
        QtCore.QMetaObject.connectSlotsByName(backgroundSubtraction)

    def retranslateUi(self, backgroundSubtraction):
        _translate = QtCore.QCoreApplication.translate
        backgroundSubtraction.setWindowTitle(_translate("backgroundSubtraction", "backgroundSubtraction"))
        self.innerRadiusLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.outerRadiusLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.applyButton.setText(_translate("backgroundSubtraction", "Apply background subtraction"))
        self.label.setText(_translate("backgroundSubtraction", "Radius of inner circle"))
        self.label_3.setText(_translate("backgroundSubtraction", "X Center"))
        self.label_4.setText(_translate("backgroundSubtraction", "Y Center"))
        self.label_2.setText(_translate("backgroundSubtraction", "Radius of outer circle"))

