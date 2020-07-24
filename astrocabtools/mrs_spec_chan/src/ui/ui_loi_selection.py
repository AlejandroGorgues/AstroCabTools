# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loiSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MrsLoiList(object):
    def setupUi(self, MrsLoiList):
        MrsLoiList.setObjectName("MrsLoiList")
        MrsLoiList.resize(472, 762)
        self.gridLayout_2 = QtWidgets.QGridLayout(MrsLoiList)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(MrsLoiList)
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
        self.loiW = QtWidgets.QListWidget(self.groupBox)
        self.loiW.setObjectName("loiW")
        self.verticalLayout.addWidget(self.loiW)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(MrsLoiList)
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

        self.retranslateUi(MrsLoiList)
        self.acceptButton.clicked.connect(MrsLoiList.accept)
        self.cancelButton.clicked.connect(MrsLoiList.reject)
        QtCore.QMetaObject.connectSlotsByName(MrsLoiList)

    def retranslateUi(self, MrsLoiList):
        _translate = QtCore.QCoreApplication.translate
        MrsLoiList.setWindowTitle(_translate("MrsLoiList", "Line of interest selection  - Beta version"))
        self.groupBox.setTitle(_translate("MrsLoiList", "Lines of Interest"))
        self.groupBox_2.setTitle(_translate("MrsLoiList", "Options"))
        self.acceptButton.setText(_translate("MrsLoiList", "Accept"))
        self.cancelButton.setText(_translate("MrsLoiList", "Cancel"))
