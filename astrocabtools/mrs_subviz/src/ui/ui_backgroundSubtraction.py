# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backgroundSubtraction.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_backgroundSubtraction(object):
    def setupUi(self, backgroundSubtraction):
        backgroundSubtraction.setObjectName("backgroundSubtraction")
        backgroundSubtraction.resize(675, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backgroundSubtraction.sizePolicy().hasHeightForWidth())
        backgroundSubtraction.setSizePolicy(sizePolicy)
        backgroundSubtraction.setMinimumSize(QtCore.QSize(650, 0))
        self.gridLayout_2 = QtWidgets.QGridLayout(backgroundSubtraction)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtWidgets.QLabel(backgroundSubtraction)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.wedgesXCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.wedgesXCenterLineEdit.setEnabled(True)
        self.wedgesXCenterLineEdit.setReadOnly(True)
        self.wedgesXCenterLineEdit.setObjectName("wedgesXCenterLineEdit")
        self.horizontalLayout.addWidget(self.wedgesXCenterLineEdit)
        self.label_4 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.wedgesYCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.wedgesYCenterLineEdit.setEnabled(True)
        self.wedgesYCenterLineEdit.setReadOnly(True)
        self.wedgesYCenterLineEdit.setObjectName("wedgesYCenterLineEdit")
        self.horizontalLayout.addWidget(self.wedgesYCenterLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 3, 1, 1)
        self.wedgesApplyButton = QtWidgets.QPushButton(backgroundSubtraction)
        self.wedgesApplyButton.setEnabled(True)
        self.wedgesApplyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.wedgesApplyButton.setObjectName("wedgesApplyButton")
        self.gridLayout.addWidget(self.wedgesApplyButton, 4, 0, 1, 2)
        self.heightLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.heightLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.gridLayout.addWidget(self.heightLineEdit, 3, 4, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.rectangleXCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.rectangleXCenterLineEdit.setObjectName("rectangleXCenterLineEdit")
        self.horizontalLayout_2.addWidget(self.rectangleXCenterLineEdit)
        self.label_6 = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.rectangleYCenterLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.rectangleYCenterLineEdit.setObjectName("rectangleYCenterLineEdit")
        self.horizontalLayout_2.addWidget(self.rectangleYCenterLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 3, 1, 2)
        self.innerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.innerRadiusLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.innerRadiusLineEdit.setObjectName("innerRadiusLineEdit")
        self.gridLayout.addWidget(self.innerRadiusLineEdit, 2, 1, 1, 1)
        self.outerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.outerRadiusLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.outerRadiusLineEdit.setObjectName("outerRadiusLineEdit")
        self.gridLayout.addWidget(self.outerRadiusLineEdit, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(backgroundSubtraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.rectangleApplyButton = QtWidgets.QPushButton(backgroundSubtraction)
        self.rectangleApplyButton.setObjectName("rectangleApplyButton")
        self.gridLayout.addWidget(self.rectangleApplyButton, 4, 3, 1, 2)
        self.widthLineEdit = QtWidgets.QLineEdit(backgroundSubtraction)
        self.widthLineEdit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.widthLineEdit.setObjectName("widthLineEdit")
        self.gridLayout.addWidget(self.widthLineEdit, 2, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(backgroundSubtraction)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 3, 1, 2)
        self.line = QtWidgets.QFrame(backgroundSubtraction)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 5, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(backgroundSubtraction)
        QtCore.QMetaObject.connectSlotsByName(backgroundSubtraction)

    def retranslateUi(self, backgroundSubtraction):
        _translate = QtCore.QCoreApplication.translate
        backgroundSubtraction.setWindowTitle(_translate("backgroundSubtraction", "backgroundSubtraction"))
        self.label_9.setText(_translate("backgroundSubtraction", "Coordinates to perform annulus background subtraction"))
        self.label_2.setText(_translate("backgroundSubtraction", "Radius of outer circle"))
        self.label_3.setText(_translate("backgroundSubtraction", "X Center"))
        self.label_4.setText(_translate("backgroundSubtraction", "Y Center"))
        self.label_8.setText(_translate("backgroundSubtraction", "Height"))
        self.label_7.setText(_translate("backgroundSubtraction", "Width"))
        self.wedgesApplyButton.setText(_translate("backgroundSubtraction", "Apply wedges background subtraction to each cube"))
        self.heightLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.label_5.setText(_translate("backgroundSubtraction", "X Center"))
        self.rectangleXCenterLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.label_6.setText(_translate("backgroundSubtraction", "Y Center"))
        self.rectangleYCenterLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.innerRadiusLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.outerRadiusLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.label.setText(_translate("backgroundSubtraction", "Radius of inner circle"))
        self.rectangleApplyButton.setText(_translate("backgroundSubtraction", "Apply rectangle background subtraction to each cube"))
        self.widthLineEdit.setPlaceholderText(_translate("backgroundSubtraction", "0"))
        self.label_10.setText(_translate("backgroundSubtraction", "Coordinates to perform rectangle background subtraction"))

