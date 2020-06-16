# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_tools.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_all_tools(object):
    def setupUi(self, all_tools):
        all_tools.setObjectName("all_tools")
        all_tools.resize(450, 100)
        all_tools.setMinimumSize(QtCore.QSize(450, 100))
        self.centralwidget = QtWidgets.QWidget(all_tools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.fitLineButton = QtWidgets.QPushButton(self.centralwidget)
        self.fitLineButton.setObjectName("fitLineButton")
        self.gridLayout.addWidget(self.fitLineButton, 2, 1, 1, 1)
        self.mrsDetPlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.mrsDetPlotButton.setObjectName("mrsDetPlotButton")
        self.gridLayout.addWidget(self.mrsDetPlotButton, 2, 0, 1, 1)
        self.mrsChanButton = QtWidgets.QPushButton(self.centralwidget)
        self.mrsChanButton.setObjectName("mrsChanButton")
        self.gridLayout.addWidget(self.mrsChanButton, 1, 0, 1, 1)
        self.mrsSpecChanButton = QtWidgets.QPushButton(self.centralwidget)
        self.mrsSpecChanButton.setObjectName("mrsSpecChanButton")
        self.gridLayout.addWidget(self.mrsSpecChanButton, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        all_tools.setCentralWidget(self.centralwidget)

        self.retranslateUi(all_tools)
        QtCore.QMetaObject.connectSlotsByName(all_tools)

    def retranslateUi(self, all_tools):
        _translate = QtCore.QCoreApplication.translate
        all_tools.setWindowTitle(_translate("all_tools", "AllTools"))
        self.fitLineButton.setText(_translate("all_tools", "fit_line"))
        self.mrsDetPlotButton.setText(_translate("all_tools", "mrs_det_plot"))
        self.mrsChanButton.setText(_translate("all_tools", "mrs_chan"))
        self.mrsSpecChanButton.setText(_translate("all_tools", "mrs_spec_chan"))
        self.label.setText(_translate("all_tools", "Select tool to show"))

