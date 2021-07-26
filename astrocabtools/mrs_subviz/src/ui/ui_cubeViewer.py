# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cubeViewer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cubeViewer(object):
    def setupUi(self, cubeViewer):
        cubeViewer.setObjectName("cubeViewer")
        cubeViewer.resize(700, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cubeViewer.sizePolicy().hasHeightForWidth())
        cubeViewer.setSizePolicy(sizePolicy)
        cubeViewer.setMinimumSize(QtCore.QSize(700, 700))
        self.gridLayout_2 = QtWidgets.QGridLayout(cubeViewer)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.unselectButton = QtWidgets.QToolButton(cubeViewer)
        self.unselectButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.unselectButton.setObjectName("unselectButton")
        self.horizontalLayout.addWidget(self.unselectButton)
        self.zoomButton = QtWidgets.QToolButton(cubeViewer)
        self.zoomButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.zoomButton.setObjectName("zoomButton")
        self.horizontalLayout.addWidget(self.zoomButton)
        self.panButton = QtWidgets.QToolButton(cubeViewer)
        self.panButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.panButton.setObjectName("panButton")
        self.horizontalLayout.addWidget(self.panButton)
        self.zoomResetButton = QtWidgets.QToolButton(cubeViewer)
        self.zoomResetButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.horizontalLayout.addWidget(self.zoomResetButton)
        self.figureButton = QtWidgets.QToolButton(cubeViewer)
        self.figureButton.setEnabled(False)
        self.figureButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.figureButton.setObjectName("figureButton")
        self.horizontalLayout.addWidget(self.figureButton)
        self.saveButton = QtWidgets.QPushButton(cubeViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.cubeGroupBox = QtWidgets.QGroupBox(cubeViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cubeGroupBox.sizePolicy().hasHeightForWidth())
        self.cubeGroupBox.setSizePolicy(sizePolicy)
        self.cubeGroupBox.setTitle("")
        self.cubeGroupBox.setObjectName("cubeGroupBox")
        self.gridLayout.addWidget(self.cubeGroupBox, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(cubeViewer)
        QtCore.QMetaObject.connectSlotsByName(cubeViewer)

    def retranslateUi(self, cubeViewer):
        _translate = QtCore.QCoreApplication.translate
        cubeViewer.setWindowTitle(_translate("cubeViewer", "cubeViewer"))
        self.unselectButton.setText(_translate("cubeViewer", "Unselect current tool"))
        self.zoomButton.setText(_translate("cubeViewer", "Zoom"))
        self.panButton.setText(_translate("cubeViewer", "Pan"))
        self.zoomResetButton.setText(_translate("cubeViewer", "Zoom reset"))
        self.figureButton.setText(_translate("cubeViewer", "Current figure"))
        self.saveButton.setText(_translate("cubeViewer", "Save as png"))

