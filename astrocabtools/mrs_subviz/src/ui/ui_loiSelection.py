# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loiSelection.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_loiSelection(object):
    def setupUi(self, loiSelection):
        loiSelection.setObjectName("loiSelection")
        loiSelection.resize(472, 762)
        self.gridLayout_2 = QtWidgets.QGridLayout(loiSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(loiSelection)
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
        self.groupBox_2 = QtWidgets.QGroupBox(loiSelection)
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
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")
        self.redshiftLabel = QtWidgets.QLabel(loiSelection)
        self.redshiftLabel.setObjectName("redshiftLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.redshiftLabel)
        self.redshiftLineEdit = QtWidgets.QLineEdit(loiSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redshiftLineEdit.sizePolicy().hasHeightForWidth())
        self.redshiftLineEdit.setSizePolicy(sizePolicy)
        self.redshiftLineEdit.setAutoFillBackground(False)
        self.redshiftLineEdit.setObjectName("redshiftLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.redshiftLineEdit)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(loiSelection)
        self.acceptButton.clicked.connect(loiSelection.accept)
        self.cancelButton.clicked.connect(loiSelection.reject)
        QtCore.QMetaObject.connectSlotsByName(loiSelection)

    def retranslateUi(self, loiSelection):
        _translate = QtCore.QCoreApplication.translate
        loiSelection.setWindowTitle(_translate("loiSelection", "Line of interest selection"))
        self.groupBox.setTitle(_translate("loiSelection", "Lines of Interest"))
        self.groupBox_2.setTitle(_translate("loiSelection", "Options"))
        self.acceptButton.setText(_translate("loiSelection", "Accept"))
        self.cancelButton.setText(_translate("loiSelection", "Cancel"))
        self.redshiftLabel.setText(_translate("loiSelection", "Redshift"))
        self.redshiftLineEdit.setPlaceholderText(_translate("loiSelection", "0"))

