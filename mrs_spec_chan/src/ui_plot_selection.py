# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsPltList(object):
    def setupUi(self, MrsPltList):
        MrsPltList.setObjectName("MrsPltList")
        MrsPltList.resize(641, 709)
        self.gridlayout = QtWidgets.QGridLayout(MrsPltList)
        self.gridlayout.setObjectName("gridlayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(MrsPltList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileButton = QtWidgets.QPushButton(self.groupBox)
        self.fileButton.setObjectName("fileButton")
        self.verticalLayout.addWidget(self.fileButton)
        self.spectraListWidget = QtWidgets.QListWidget(self.groupBox)
        self.spectraListWidget.setObjectName("spectraListWidget")
        self.verticalLayout.addWidget(self.spectraListWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(MrsPltList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.acceptButton = QtWidgets.QPushButton(self.groupBox_2)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout.addWidget(self.acceptButton)
        self.cancelButton = QtWidgets.QPushButton(self.groupBox_2)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridlayout.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(MrsPltList)
        QtCore.QMetaObject.connectSlotsByName(MrsPltList)

    def retranslateUi(self, MrsPltList):
        _translate = QtCore.QCoreApplication.translate
        MrsPltList.setWindowTitle(_translate("MrsPltList", "Spectra selection"))
        self.groupBox.setTitle(_translate("MrsPltList", "Spectra"))
        self.fileButton.setText(_translate("MrsPltList", "Select Directory"))
        self.groupBox_2.setTitle(_translate("MrsPltList", "Options"))
        self.acceptButton.setText(_translate("MrsPltList", "Accept"))
        self.cancelButton.setText(_translate("MrsPltList", "Cancel"))
