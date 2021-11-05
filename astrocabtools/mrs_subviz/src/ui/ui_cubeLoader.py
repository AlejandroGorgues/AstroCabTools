# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cubeLoader.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cubeLoader(object):
    def setupUi(self, cubeLoader):
        cubeLoader.setObjectName("cubeLoader")
        cubeLoader.resize(650, 150)
        cubeLoader.setMinimumSize(QtCore.QSize(650, 150))
        cubeLoader.setMaximumSize(QtCore.QSize(650, 169))
        self.gridLayout_2 = QtWidgets.QGridLayout(cubeLoader)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(cubeLoader)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(cubeLoader)
        self.cancelButton.setEnabled(True)
        self.cancelButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 4, 0, 1, 2)
        self.cubeComboBox = QtWidgets.QComboBox(cubeLoader)
        self.cubeComboBox.setObjectName("cubeComboBox")
        self.cubeComboBox.addItem("")
        self.gridLayout.addWidget(self.cubeComboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(cubeLoader)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.subbandComboBox = QtWidgets.QComboBox(cubeLoader)
        self.subbandComboBox.setEnabled(True)
        self.subbandComboBox.setObjectName("subbandComboBox")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.subbandComboBox.addItem("")
        self.gridLayout.addWidget(self.subbandComboBox, 1, 1, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(cubeLoader)
        self.acceptButton.setEnabled(False)
        self.acceptButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 4, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(cubeLoader)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.selectFileButton = QtWidgets.QPushButton(cubeLoader)
        self.selectFileButton.setObjectName("selectFileButton")
        self.gridLayout.addWidget(self.selectFileButton, 0, 2, 1, 1)
        self.selectDirectoryButton = QtWidgets.QPushButton(cubeLoader)
        self.selectDirectoryButton.setObjectName("selectDirectoryButton")
        self.gridLayout.addWidget(self.selectDirectoryButton, 0, 3, 1, 1)
        self.filePathLabel = QtWidgets.QLabel(cubeLoader)
        self.filePathLabel.setText("")
        self.filePathLabel.setObjectName("filePathLabel")
        self.gridLayout.addWidget(self.filePathLabel, 2, 1, 1, 3)
        self.filterLineEdit = QtWidgets.QLineEdit(cubeLoader)
        self.filterLineEdit.setEnabled(False)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.gridLayout.addWidget(self.filterLineEdit, 3, 1, 1, 1)
        self.filterLabel = QtWidgets.QLabel(cubeLoader)
        self.filterLabel.setEnabled(False)
        self.filterLabel.setObjectName("filterLabel")
        self.gridLayout.addWidget(self.filterLabel, 3, 0, 1, 1)
        self.customSubbandCheckBox = QtWidgets.QCheckBox(cubeLoader)
        self.customSubbandCheckBox.setEnabled(False)
        self.customSubbandCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.customSubbandCheckBox.setObjectName("customSubbandCheckBox")
        self.gridLayout.addWidget(self.customSubbandCheckBox, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(cubeLoader)
        self.acceptButton.clicked.connect(cubeLoader.accept)
        self.cancelButton.clicked.connect(cubeLoader.reject)
        QtCore.QMetaObject.connectSlotsByName(cubeLoader)

    def retranslateUi(self, cubeLoader):
        _translate = QtCore.QCoreApplication.translate
        cubeLoader.setWindowTitle(_translate("cubeLoader", "cubeLoader"))
        self.label.setText(_translate("cubeLoader", "Type of cube"))
        self.cancelButton.setText(_translate("cubeLoader", "Cancel"))
        self.cubeComboBox.setItemText(0, _translate("cubeLoader", "MIRI"))
        self.label_2.setText(_translate("cubeLoader", "File Path: "))
        self.subbandComboBox.setItemText(0, _translate("cubeLoader", "1 Short"))
        self.subbandComboBox.setItemText(1, _translate("cubeLoader", "1 Medium"))
        self.subbandComboBox.setItemText(2, _translate("cubeLoader", "1 Long"))
        self.subbandComboBox.setItemText(3, _translate("cubeLoader", "2 Short"))
        self.subbandComboBox.setItemText(4, _translate("cubeLoader", "2 Medium"))
        self.subbandComboBox.setItemText(5, _translate("cubeLoader", "2 Long"))
        self.subbandComboBox.setItemText(6, _translate("cubeLoader", "3 Short"))
        self.subbandComboBox.setItemText(7, _translate("cubeLoader", "3 Medium"))
        self.subbandComboBox.setItemText(8, _translate("cubeLoader", "3 Long"))
        self.subbandComboBox.setItemText(9, _translate("cubeLoader", "4 Short"))
        self.subbandComboBox.setItemText(10, _translate("cubeLoader", "4 Medium"))
        self.subbandComboBox.setItemText(11, _translate("cubeLoader", "4 Long"))
        self.acceptButton.setText(_translate("cubeLoader", "Accept"))
        self.label_3.setText(_translate("cubeLoader", "Subband associate with"))
        self.selectFileButton.setText(_translate("cubeLoader", "Select .fits file"))
        self.selectDirectoryButton.setText(_translate("cubeLoader", "Select directory"))
        self.filterLineEdit.setPlaceholderText(_translate("cubeLoader", "*.fits"))
        self.filterLabel.setText(_translate("cubeLoader", "Filter text"))
        self.customSubbandCheckBox.setText(_translate("cubeLoader", "Use custom subband instead of default"))
