# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ellipseCoordinates.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ellipseCoordinates(object):
    def setupUi(self, ellipseCoordinates):
        ellipseCoordinates.setObjectName("ellipseCoordinates")
        ellipseCoordinates.resize(525, 100)
        ellipseCoordinates.setMinimumSize(QtCore.QSize(525, 100))
        self.gridLayout_2 = QtWidgets.QGridLayout(ellipseCoordinates)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ellipseCoordinates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3, QtCore.Qt.AlignHCenter)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.centerXLabel = QtWidgets.QLabel(ellipseCoordinates)
        self.centerXLabel.setObjectName("centerXLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.centerXLabel)
        self.centerXLineEdit = QtWidgets.QLineEdit(ellipseCoordinates)
        self.centerXLineEdit.setEnabled(True)
        self.centerXLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.centerXLineEdit.setReadOnly(True)
        self.centerXLineEdit.setObjectName("centerXLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.centerXLineEdit)
        self.aAxisLabel = QtWidgets.QLabel(ellipseCoordinates)
        self.aAxisLabel.setObjectName("aAxisLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.aAxisLabel)
        self.aAxisLineEdit = QtWidgets.QLineEdit(ellipseCoordinates)
        self.aAxisLineEdit.setEnabled(True)
        self.aAxisLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.aAxisLineEdit.setReadOnly(True)
        self.aAxisLineEdit.setObjectName("aAxisLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.aAxisLineEdit)
        self.gridLayout.addLayout(self.formLayout, 7, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout_2.setObjectName("formLayout_2")
        self.centerYLabel = QtWidgets.QLabel(ellipseCoordinates)
        self.centerYLabel.setObjectName("centerYLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.centerYLabel)
        self.centerYLineEdit = QtWidgets.QLineEdit(ellipseCoordinates)
        self.centerYLineEdit.setEnabled(True)
        self.centerYLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.centerYLineEdit.setReadOnly(True)
        self.centerYLineEdit.setObjectName("centerYLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.centerYLineEdit)
        self.bAxisLabel = QtWidgets.QLabel(ellipseCoordinates)
        self.bAxisLabel.setObjectName("bAxisLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.bAxisLabel)
        self.bAxisLineEdit = QtWidgets.QLineEdit(ellipseCoordinates)
        self.bAxisLineEdit.setEnabled(True)
        self.bAxisLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.bAxisLineEdit.setReadOnly(True)
        self.bAxisLineEdit.setObjectName("bAxisLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.bAxisLineEdit)
        self.gridLayout.addLayout(self.formLayout_2, 7, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)

        self.retranslateUi(ellipseCoordinates)
        QtCore.QMetaObject.connectSlotsByName(ellipseCoordinates)

    def retranslateUi(self, ellipseCoordinates):
        _translate = QtCore.QCoreApplication.translate
        ellipseCoordinates.setWindowTitle(_translate("ellipseCoordinates", "ellipseCoordinates"))
        self.label.setText(_translate("ellipseCoordinates", "Ellipse selection coordinates"))
        self.centerXLabel.setText(_translate("ellipseCoordinates", "Center X"))
        self.aAxisLabel.setText(_translate("ellipseCoordinates", "Axis a (Major axis)"))
        self.centerYLabel.setText(_translate("ellipseCoordinates", "Center Y"))
        self.bAxisLabel.setText(_translate("ellipseCoordinates", "Axis b (Minor Axis)"))

