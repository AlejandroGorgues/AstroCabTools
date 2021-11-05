# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'styleManagerCubeViewer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_styleManagerCubeViewer(object):
    def setupUi(self, styleManagerCubeViewer):
        styleManagerCubeViewer.setObjectName("styleManagerCubeViewer")
        styleManagerCubeViewer.resize(388, 82)
        styleManagerCubeViewer.setMinimumSize(QtCore.QSize(250, 80))
        self.gridLayout_2 = QtWidgets.QGridLayout(styleManagerCubeViewer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout_3.setObjectName("formLayout_3")
        self.stretchLabel = QtWidgets.QLabel(styleManagerCubeViewer)
        self.stretchLabel.setObjectName("stretchLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.stretchLabel)
        self.stretchComboBox = QtWidgets.QComboBox(styleManagerCubeViewer)
        self.stretchComboBox.setObjectName("stretchComboBox")
        self.stretchComboBox.addItem("")
        self.stretchComboBox.addItem("")
        self.stretchComboBox.addItem("")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stretchComboBox)
        self.gridLayout.addLayout(self.formLayout_3, 0, 2, 1, 1)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout_4.setObjectName("formLayout_4")
        self.scaleLabel = QtWidgets.QLabel(styleManagerCubeViewer)
        self.scaleLabel.setObjectName("scaleLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.scaleLabel)
        self.scaleComboBox = QtWidgets.QComboBox(styleManagerCubeViewer)
        self.scaleComboBox.setObjectName("scaleComboBox")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.scaleComboBox)
        self.gridLayout.addLayout(self.formLayout_4, 0, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout.setObjectName("formLayout")
        self.colorLabel = QtWidgets.QLabel(styleManagerCubeViewer)
        self.colorLabel.setObjectName("colorLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.colorLabel)
        self.colorComboBox = QtWidgets.QComboBox(styleManagerCubeViewer)
        self.colorComboBox.setObjectName("colorComboBox")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.colorComboBox)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(styleManagerCubeViewer)
        QtCore.QMetaObject.connectSlotsByName(styleManagerCubeViewer)

    def retranslateUi(self, styleManagerCubeViewer):
        _translate = QtCore.QCoreApplication.translate
        styleManagerCubeViewer.setWindowTitle(_translate("styleManagerCubeViewer", "styleManagerCubeViewer"))
        self.stretchLabel.setText(_translate("styleManagerCubeViewer", "Stretch"))
        self.stretchComboBox.setItemText(0, _translate("styleManagerCubeViewer", "Linear"))
        self.stretchComboBox.setItemText(1, _translate("styleManagerCubeViewer", "Sqrt"))
        self.stretchComboBox.setItemText(2, _translate("styleManagerCubeViewer", "Log"))
        self.scaleLabel.setText(_translate("styleManagerCubeViewer", "Scale"))
        self.scaleComboBox.setItemText(0, _translate("styleManagerCubeViewer", "MinMax"))
        self.scaleComboBox.setItemText(1, _translate("styleManagerCubeViewer", "ZScale"))
        self.colorLabel.setText(_translate("styleManagerCubeViewer", "Color"))
        self.colorComboBox.setItemText(0, _translate("styleManagerCubeViewer", "Gray"))
        self.colorComboBox.setItemText(1, _translate("styleManagerCubeViewer", "Accent"))
        self.colorComboBox.setItemText(2, _translate("styleManagerCubeViewer", "Heat"))
        self.colorComboBox.setItemText(3, _translate("styleManagerCubeViewer", "Rainbow"))
        self.colorComboBox.setItemText(4, _translate("styleManagerCubeViewer", "CoolWarm"))

