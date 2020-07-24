# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templateSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsTmpltList(object):
    def setupUi(self, MrsTmpltList):
        MrsTmpltList.setObjectName("MrsTmpltList")
        MrsTmpltList.resize(620, 740)
        self.gridLayout_2 = QtWidgets.QGridLayout(MrsTmpltList)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(MrsTmpltList)
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
        self.templateListWidget = QtWidgets.QListWidget(self.groupBox)
        self.templateListWidget.setObjectName("templateListWidget")
        self.verticalLayout.addWidget(self.templateListWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(MrsTmpltList)
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
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(MrsTmpltList)
        self.acceptButton.clicked.connect(MrsTmpltList.accept)
        self.cancelButton.clicked.connect(MrsTmpltList.reject)
        QtCore.QMetaObject.connectSlotsByName(MrsTmpltList)

    def retranslateUi(self, MrsTmpltList):
        _translate = QtCore.QCoreApplication.translate
        MrsTmpltList.setWindowTitle(_translate("MrsTmpltList", "Template selection  - Beta version"))
        self.groupBox.setTitle(_translate("MrsTmpltList", "Spectra"))
        self.groupBox_2.setTitle(_translate("MrsTmpltList", "Options"))
        self.acceptButton.setText(_translate("MrsTmpltList", "Accept"))
        self.cancelButton.setText(_translate("MrsTmpltList", "Cancel"))
