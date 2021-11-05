# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sliceManager.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sliceManager(object):
    def setupUi(self, sliceManager):
        sliceManager.setObjectName("sliceManager")
        sliceManager.resize(891, 107)
        self.gridLayout = QtWidgets.QGridLayout(sliceManager)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.wavelengthLineEdit = QtWidgets.QLineEdit(sliceManager)
        self.wavelengthLineEdit.setEnabled(False)
        self.wavelengthLineEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.wavelengthLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.wavelengthLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.wavelengthLineEdit.setObjectName("wavelengthLineEdit")
        self.gridLayout_3.addWidget(self.wavelengthLineEdit, 1, 1, 1, 1)
        self.sliceSlider = QtWidgets.QSlider(sliceManager)
        self.sliceSlider.setEnabled(False)
        self.sliceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sliceSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliceSlider.setTickInterval(50)
        self.sliceSlider.setObjectName("sliceSlider")
        self.gridLayout_3.addWidget(self.sliceSlider, 1, 2, 2, 2)
        self.sliceSpinBox = QtWidgets.QSpinBox(sliceManager)
        self.sliceSpinBox.setEnabled(False)
        self.sliceSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.sliceSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.sliceSpinBox.setWrapping(False)
        self.sliceSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sliceSpinBox.setMinimum(0)
        self.sliceSpinBox.setProperty("value", 0)
        self.sliceSpinBox.setObjectName("sliceSpinBox")
        self.gridLayout_3.addWidget(self.sliceSpinBox, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 2, 1, 2)
        self.subbandSelectionComboBox = QtWidgets.QComboBox(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subbandSelectionComboBox.sizePolicy().hasHeightForWidth())
        self.subbandSelectionComboBox.setSizePolicy(sizePolicy)
        self.subbandSelectionComboBox.setObjectName("subbandSelectionComboBox")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.subbandSelectionComboBox.addItem("")
        self.gridLayout_3.addWidget(self.subbandSelectionComboBox, 3, 1, 2, 1)
        self.label = QtWidgets.QLabel(sliceManager)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 2, 1)
        self.sliceMinimumValue = QtWidgets.QLabel(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliceMinimumValue.sizePolicy().hasHeightForWidth())
        self.sliceMinimumValue.setSizePolicy(sizePolicy)
        self.sliceMinimumValue.setText("")
        self.sliceMinimumValue.setObjectName("sliceMinimumValue")
        self.gridLayout_3.addWidget(self.sliceMinimumValue, 3, 2, 2, 1)
        self.sliceMaximumValue = QtWidgets.QLabel(sliceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliceMaximumValue.sizePolicy().hasHeightForWidth())
        self.sliceMaximumValue.setSizePolicy(sizePolicy)
        self.sliceMaximumValue.setText("")
        self.sliceMaximumValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sliceMaximumValue.setObjectName("sliceMaximumValue")
        self.gridLayout_3.addWidget(self.sliceMaximumValue, 3, 3, 2, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(sliceManager)
        QtCore.QMetaObject.connectSlotsByName(sliceManager)

    def retranslateUi(self, sliceManager):
        _translate = QtCore.QCoreApplication.translate
        sliceManager.setWindowTitle(_translate("sliceManager", "sliceManager"))
        self.label_3.setText(_translate("sliceManager", "Wavelengt Value"))
        self.label_2.setText(_translate("sliceManager", "Slice Value"))
        self.label_4.setText(_translate("sliceManager", "Slice"))
        self.subbandSelectionComboBox.setItemText(0, _translate("sliceManager", "Select subband"))
        self.subbandSelectionComboBox.setItemText(1, _translate("sliceManager", "1 Short"))
        self.subbandSelectionComboBox.setItemText(2, _translate("sliceManager", "1 Medium"))
        self.subbandSelectionComboBox.setItemText(3, _translate("sliceManager", "1 Long"))
        self.subbandSelectionComboBox.setItemText(4, _translate("sliceManager", "2 Short"))
        self.subbandSelectionComboBox.setItemText(5, _translate("sliceManager", "2 Medium"))
        self.subbandSelectionComboBox.setItemText(6, _translate("sliceManager", "2 Long"))
        self.subbandSelectionComboBox.setItemText(7, _translate("sliceManager", "3 Short"))
        self.subbandSelectionComboBox.setItemText(8, _translate("sliceManager", "3 Medium"))
        self.subbandSelectionComboBox.setItemText(9, _translate("sliceManager", "3 Long"))
        self.subbandSelectionComboBox.setItemText(10, _translate("sliceManager", "4 Short"))
        self.subbandSelectionComboBox.setItemText(11, _translate("sliceManager", "4 Medium"))
        self.subbandSelectionComboBox.setItemText(12, _translate("sliceManager", "4 Long"))
        self.label.setText(_translate("sliceManager", "Current subband"))
