# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrumParametersSelection.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_spectrumParametersSelection(object):
    def setupUi(self, spectrumParametersSelection):
        spectrumParametersSelection.setObjectName("spectrumParametersSelection")
        spectrumParametersSelection.resize(526, 233)
        self.gridLayout_2 = QtWidgets.QGridLayout(spectrumParametersSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.subbandGroupBox = QtWidgets.QGroupBox(spectrumParametersSelection)
        self.subbandGroupBox.setEnabled(False)
        self.subbandGroupBox.setObjectName("subbandGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.subbandGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_3.addWidget(self.checkBox_4, 0, 3, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout_3.addWidget(self.checkBox_8, 2, 0, 1, 1)
        self.checkBox_7 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout_3.addWidget(self.checkBox_7, 1, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_3.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_3.addWidget(self.checkBox_2, 0, 1, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_3.addWidget(self.checkBox_6, 1, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_3.addWidget(self.checkBox_3, 0, 2, 1, 1)
        self.checkBox_16 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_16.setObjectName("checkBox_16")
        self.gridLayout_3.addWidget(self.checkBox_16, 1, 2, 1, 1)
        self.checkBox_14 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_14.setObjectName("checkBox_14")
        self.gridLayout_3.addWidget(self.checkBox_14, 2, 3, 1, 1)
        self.checkBox_10 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_10.setObjectName("checkBox_10")
        self.gridLayout_3.addWidget(self.checkBox_10, 2, 1, 1, 1)
        self.checkBox_12 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout_3.addWidget(self.checkBox_12, 2, 2, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.subbandGroupBox)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_3.addWidget(self.checkBox_5, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.subbandGroupBox, 4, 0, 1, 4)
        self.spectrumComboBox = QtWidgets.QComboBox(spectrumParametersSelection)
        self.spectrumComboBox.setObjectName("spectrumComboBox")
        self.spectrumComboBox.addItem("")
        self.spectrumComboBox.addItem("")
        self.spectrumComboBox.addItem("")
        self.gridLayout.addWidget(self.spectrumComboBox, 1, 1, 1, 3)
        self.label_2 = QtWidgets.QLabel(spectrumParametersSelection)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.fUnitsComboBox = QtWidgets.QComboBox(spectrumParametersSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fUnitsComboBox.sizePolicy().hasHeightForWidth())
        self.fUnitsComboBox.setSizePolicy(sizePolicy)
        self.fUnitsComboBox.setObjectName("fUnitsComboBox")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.fUnitsComboBox.addItem("")
        self.gridLayout.addWidget(self.fUnitsComboBox, 0, 3, 1, 1)
        self.wUnitsComboBox = QtWidgets.QComboBox(spectrumParametersSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wUnitsComboBox.sizePolicy().hasHeightForWidth())
        self.wUnitsComboBox.setSizePolicy(sizePolicy)
        self.wUnitsComboBox.setObjectName("wUnitsComboBox")
        self.wUnitsComboBox.addItem("")
        self.wUnitsComboBox.addItem("")
        self.wUnitsComboBox.addItem("")
        self.gridLayout.addWidget(self.wUnitsComboBox, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(spectrumParametersSelection)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(spectrumParametersSelection)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(spectrumParametersSelection)
        self.acceptButton.setEnabled(True)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 5, 2, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(spectrumParametersSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 5, 0, 1, 2)
        self.label = QtWidgets.QLabel(spectrumParametersSelection)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.allRadioButton = QtWidgets.QRadioButton(spectrumParametersSelection)
        self.allRadioButton.setChecked(True)
        self.allRadioButton.setObjectName("allRadioButton")
        self.gridLayout.addWidget(self.allRadioButton, 2, 1, 1, 1)
        self.contiguousRadioButton = QtWidgets.QRadioButton(spectrumParametersSelection)
        self.contiguousRadioButton.setObjectName("contiguousRadioButton")
        self.gridLayout.addWidget(self.contiguousRadioButton, 2, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(spectrumParametersSelection)
        self.acceptButton.clicked.connect(spectrumParametersSelection.accept)
        self.cancelButton.clicked.connect(spectrumParametersSelection.close)
        QtCore.QMetaObject.connectSlotsByName(spectrumParametersSelection)

    def retranslateUi(self, spectrumParametersSelection):
        _translate = QtCore.QCoreApplication.translate
        spectrumParametersSelection.setWindowTitle(_translate("spectrumParametersSelection", "spectrumParametersSelection"))
        self.subbandGroupBox.setTitle(_translate("spectrumParametersSelection", "Subbands"))
        self.checkBox_4.setText(_translate("spectrumParametersSelection", "4S"))
        self.checkBox_8.setText(_translate("spectrumParametersSelection", "1L"))
        self.checkBox_7.setText(_translate("spectrumParametersSelection", "4M"))
        self.checkBox.setText(_translate("spectrumParametersSelection", "1S"))
        self.checkBox_2.setText(_translate("spectrumParametersSelection", "2S"))
        self.checkBox_6.setText(_translate("spectrumParametersSelection", "2M"))
        self.checkBox_3.setText(_translate("spectrumParametersSelection", "3S"))
        self.checkBox_16.setText(_translate("spectrumParametersSelection", "3M"))
        self.checkBox_14.setText(_translate("spectrumParametersSelection", "4L"))
        self.checkBox_10.setText(_translate("spectrumParametersSelection", "2L"))
        self.checkBox_12.setText(_translate("spectrumParametersSelection", "3L"))
        self.checkBox_5.setText(_translate("spectrumParametersSelection", "1M"))
        self.spectrumComboBox.setItemText(0, _translate("spectrumParametersSelection", "Aperture spectrum"))
        self.spectrumComboBox.setItemText(1, _translate("spectrumParametersSelection", "Background spectrum"))
        self.spectrumComboBox.setItemText(2, _translate("spectrumParametersSelection", "Background subtracted spectrum"))
        self.label_2.setText(_translate("spectrumParametersSelection", "Spectrum type"))
        self.fUnitsComboBox.setItemText(0, _translate("spectrumParametersSelection", "erg/s/cm2/um"))
        self.fUnitsComboBox.setItemText(1, _translate("spectrumParametersSelection", "Jy"))
        self.fUnitsComboBox.setItemText(2, _translate("spectrumParametersSelection", "mJy"))
        self.fUnitsComboBox.setItemText(3, _translate("spectrumParametersSelection", "uJy"))
        self.fUnitsComboBox.setItemText(4, _translate("spectrumParametersSelection", "W/m2/Hz"))
        self.fUnitsComboBox.setItemText(5, _translate("spectrumParametersSelection", "erg/s/cm2/Hz"))
        self.fUnitsComboBox.setItemText(6, _translate("spectrumParametersSelection", "W/m2/Angstroms"))
        self.fUnitsComboBox.setItemText(7, _translate("spectrumParametersSelection", "erg/s/cm2/Angstroms"))
        self.wUnitsComboBox.setItemText(0, _translate("spectrumParametersSelection", "um"))
        self.wUnitsComboBox.setItemText(1, _translate("spectrumParametersSelection", "angstroms"))
        self.wUnitsComboBox.setItemText(2, _translate("spectrumParametersSelection", "nm"))
        self.label_4.setText(_translate("spectrumParametersSelection", "Wavelength units"))
        self.label_5.setText(_translate("spectrumParametersSelection", "Flux units"))
        self.acceptButton.setText(_translate("spectrumParametersSelection", "Accept"))
        self.cancelButton.setText(_translate("spectrumParametersSelection", "Cancel"))
        self.label.setText(_translate("spectrumParametersSelection", "Subband"))
        self.allRadioButton.setText(_translate("spectrumParametersSelection", "All subbands"))
        self.contiguousRadioButton.setText(_translate("spectrumParametersSelection", "Contiguous subbands"))
