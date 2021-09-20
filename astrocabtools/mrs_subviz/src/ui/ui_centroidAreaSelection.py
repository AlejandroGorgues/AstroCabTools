# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'centroidAreaSelection.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_centroidAreaSelection(object):
    def setupUi(self, centroidAreaSelection):
        centroidAreaSelection.setObjectName("centroidAreaSelection")
        centroidAreaSelection.setWindowModality(QtCore.Qt.NonModal)
        centroidAreaSelection.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(centroidAreaSelection.sizePolicy().hasHeightForWidth())
        centroidAreaSelection.setSizePolicy(sizePolicy)
        centroidAreaSelection.setMinimumSize(QtCore.QSize(600, 600))
        self.gridLayout_2 = QtWidgets.QGridLayout(centroidAreaSelection)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cubeGroupBox = QtWidgets.QGroupBox(centroidAreaSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cubeGroupBox.sizePolicy().hasHeightForWidth())
        self.cubeGroupBox.setSizePolicy(sizePolicy)
        self.cubeGroupBox.setTitle("")
        self.cubeGroupBox.setObjectName("cubeGroupBox")
        self.gridLayout.addWidget(self.cubeGroupBox, 2, 0, 1, 2)
        self.infoLabel = QtWidgets.QLabel(centroidAreaSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout.addWidget(self.infoLabel, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.centroidButton = QtWidgets.QToolButton(centroidAreaSelection)
        self.centroidButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centroidButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.centroidButton.setObjectName("centroidButton")
        self.horizontalLayout.addWidget(self.centroidButton)
        self.zoomButton = QtWidgets.QToolButton(centroidAreaSelection)
        self.zoomButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.zoomButton.setObjectName("zoomButton")
        self.horizontalLayout.addWidget(self.zoomButton)
        self.panButton = QtWidgets.QToolButton(centroidAreaSelection)
        self.panButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.panButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.panButton.setObjectName("panButton")
        self.horizontalLayout.addWidget(self.panButton)
        self.zoomResetButton = QtWidgets.QToolButton(centroidAreaSelection)
        self.zoomResetButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomResetButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.horizontalLayout.addWidget(self.zoomResetButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(centroidAreaSelection)
        QtCore.QMetaObject.connectSlotsByName(centroidAreaSelection)

    def retranslateUi(self, centroidAreaSelection):
        _translate = QtCore.QCoreApplication.translate
        centroidAreaSelection.setWindowTitle(_translate("centroidAreaSelection", "centroidAreaSelection"))
        self.infoLabel.setText(_translate("centroidAreaSelection", "Select area to calculate the centroid"))
        self.centroidButton.setText(_translate("centroidAreaSelection", "Select centroid"))
        self.zoomButton.setText(_translate("centroidAreaSelection", "Zoom"))
        self.panButton.setText(_translate("centroidAreaSelection", "Pan"))
        self.zoomResetButton.setText(_translate("centroidAreaSelection", "Zoom Reset"))
