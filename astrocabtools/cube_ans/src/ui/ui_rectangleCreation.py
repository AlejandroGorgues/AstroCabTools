# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rectangleCreation.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_rectangleCreation(object):
    def setupUi(self, rectangleCreation):
        rectangleCreation.setObjectName("rectangleCreation")
        rectangleCreation.resize(450, 175)
        rectangleCreation.setMinimumSize(QtCore.QSize(450, 175))
        self.gridLayout_2 = QtWidgets.QGridLayout(rectangleCreation)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.widthLineEdit = QtWidgets.QLineEdit(rectangleCreation)
        self.widthLineEdit.setMinimumSize(QtCore.QSize(70, 0))
        self.widthLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.widthLineEdit.setObjectName("widthLineEdit")
        self.gridLayout.addWidget(self.widthLineEdit, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(rectangleCreation)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(rectangleCreation)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(rectangleCreation)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(rectangleCreation)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.bottomLeftXLineEdit = QtWidgets.QLineEdit(rectangleCreation)
        self.bottomLeftXLineEdit.setMinimumSize(QtCore.QSize(60, 0))
        self.bottomLeftXLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.bottomLeftXLineEdit.setObjectName("bottomLeftXLineEdit")
        self.gridLayout.addWidget(self.bottomLeftXLineEdit, 1, 1, 1, 1)
        self.bottomLeftYLineEdit = QtWidgets.QLineEdit(rectangleCreation)
        self.bottomLeftYLineEdit.setMinimumSize(QtCore.QSize(60, 0))
        self.bottomLeftYLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.bottomLeftYLineEdit.setObjectName("bottomLeftYLineEdit")
        self.gridLayout.addWidget(self.bottomLeftYLineEdit, 1, 3, 1, 1)
        self.heightLineEdit = QtWidgets.QLineEdit(rectangleCreation)
        self.heightLineEdit.setMinimumSize(QtCore.QSize(70, 0))
        self.heightLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.gridLayout.addWidget(self.heightLineEdit, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(rectangleCreation)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.createButton = QtWidgets.QPushButton(rectangleCreation)
        self.createButton.setObjectName("createButton")
        self.gridLayout_2.addWidget(self.createButton, 1, 0, 1, 1)

        self.retranslateUi(rectangleCreation)
        QtCore.QMetaObject.connectSlotsByName(rectangleCreation)

    def retranslateUi(self, rectangleCreation):
        _translate = QtCore.QCoreApplication.translate
        rectangleCreation.setWindowTitle(_translate("rectangleCreation", "rectangleCreation"))
        self.label_5.setText(_translate("rectangleCreation", "Height"))
        self.label_3.setText(_translate("rectangleCreation", "Width"))
        self.label_2.setText(_translate("rectangleCreation", "Bottom Left X"))
        self.label_4.setText(_translate("rectangleCreation", "Bottom Left Y"))
        self.label.setText(_translate("rectangleCreation", "Write the parameters to create the rectangle"))
        self.createButton.setText(_translate("rectangleCreation", "Create or update rectangle"))

