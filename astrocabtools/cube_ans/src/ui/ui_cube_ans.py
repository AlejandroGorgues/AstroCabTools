# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cube_ans.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cube_ans(object):
    def setupUi(self, cube_ans):
        cube_ans.setObjectName("cube_ans")
        cube_ans.resize(1100, 800)
        cube_ans.setMinimumSize(QtCore.QSize(1100, 800))
        self.widget = QtWidgets.QWidget(cube_ans)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setVerticalSpacing(1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.sliceSpinBox = QtWidgets.QSpinBox(self.widget)
        self.sliceSpinBox.setEnabled(False)
        self.sliceSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.sliceSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.sliceSpinBox.setWrapping(False)
        self.sliceSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sliceSpinBox.setMinimum(0)
        self.sliceSpinBox.setProperty("value", 0)
        self.sliceSpinBox.setObjectName("sliceSpinBox")
        self.gridLayout_3.addWidget(self.sliceSpinBox, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.sliceMaximumValue = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliceMaximumValue.sizePolicy().hasHeightForWidth())
        self.sliceMaximumValue.setSizePolicy(sizePolicy)
        self.sliceMaximumValue.setText("")
        self.sliceMaximumValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sliceMaximumValue.setObjectName("sliceMaximumValue")
        self.gridLayout_3.addWidget(self.sliceMaximumValue, 2, 3, 1, 1)
        self.sliceSlider = QtWidgets.QSlider(self.widget)
        self.sliceSlider.setEnabled(False)
        self.sliceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sliceSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliceSlider.setTickInterval(50)
        self.sliceSlider.setObjectName("sliceSlider")
        self.gridLayout_3.addWidget(self.sliceSlider, 0, 2, 2, 2)
        self.wavelengthLineEdit = QtWidgets.QLineEdit(self.widget)
        self.wavelengthLineEdit.setEnabled(False)
        self.wavelengthLineEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.wavelengthLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.wavelengthLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.wavelengthLineEdit.setObjectName("wavelengthLineEdit")
        self.gridLayout_3.addWidget(self.wavelengthLineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.sliceMinimumValue = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliceMinimumValue.sizePolicy().hasHeightForWidth())
        self.sliceMinimumValue.setSizePolicy(sizePolicy)
        self.sliceMinimumValue.setText("")
        self.sliceMinimumValue.setObjectName("sliceMinimumValue")
        self.gridLayout_3.addWidget(self.sliceMinimumValue, 2, 2, 1, 1)
        self.spaceCubePlot = QtWidgets.QGroupBox(self.widget)
        self.spaceCubePlot.setTitle("")
        self.spaceCubePlot.setObjectName("spaceCubePlot")
        self.gridLayout_3.addWidget(self.spaceCubePlot, 3, 0, 1, 4)
        self.gridLayout.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        cube_ans.setCentralWidget(self.widget)
        self.menuBar = QtWidgets.QMenuBar(cube_ans)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1100, 21))
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setEnabled(False)
        self.menuTools.setObjectName("menuTools")
        self.menuStyle = QtWidgets.QMenu(self.menuBar)
        self.menuStyle.setEnabled(False)
        self.menuStyle.setObjectName("menuStyle")
        self.menuColor = QtWidgets.QMenu(self.menuStyle)
        self.menuColor.setEnabled(False)
        self.menuColor.setObjectName("menuColor")
        self.menuStretch = QtWidgets.QMenu(self.menuStyle)
        self.menuStretch.setObjectName("menuStretch")
        self.menuScale = QtWidgets.QMenu(self.menuStyle)
        self.menuScale.setObjectName("menuScale")
        cube_ans.setMenuBar(self.menuBar)
        self.actionOpen = QtWidgets.QAction(cube_ans)
        self.actionOpen.setObjectName("actionOpen")
        self.actionRectangle = QtWidgets.QAction(cube_ans)
        self.actionRectangle.setEnabled(True)
        self.actionRectangle.setObjectName("actionRectangle")
        self.actionZoom = QtWidgets.QAction(cube_ans)
        self.actionZoom.setEnabled(True)
        self.actionZoom.setObjectName("actionZoom")
        self.actionPan = QtWidgets.QAction(cube_ans)
        self.actionPan.setEnabled(True)
        self.actionPan.setObjectName("actionPan")
        self.actionMinMax_Interval = QtWidgets.QAction(cube_ans)
        self.actionMinMax_Interval.setObjectName("actionMinMax_Interval")
        self.actionZScale_Interval = QtWidgets.QAction(cube_ans)
        self.actionZScale_Interval.setObjectName("actionZScale_Interval")
        self.actionSqrt = QtWidgets.QAction(cube_ans)
        self.actionSqrt.setObjectName("actionSqrt")
        self.actionLog = QtWidgets.QAction(cube_ans)
        self.actionLog.setObjectName("actionLog")
        self.actionLinear = QtWidgets.QAction(cube_ans)
        self.actionLinear.setObjectName("actionLinear")
        self.actionGray = QtWidgets.QAction(cube_ans)
        self.actionGray.setObjectName("actionGray")
        self.actionAccent = QtWidgets.QAction(cube_ans)
        self.actionAccent.setObjectName("actionAccent")
        self.actionHeat = QtWidgets.QAction(cube_ans)
        self.actionHeat.setObjectName("actionHeat")
        self.actionRainbow = QtWidgets.QAction(cube_ans)
        self.actionRainbow.setObjectName("actionRainbow")
        self.actionCoolWarm = QtWidgets.QAction(cube_ans)
        self.actionCoolWarm.setObjectName("actionCoolWarm")
        self.actionRectangle_coordinates = QtWidgets.QAction(cube_ans)
        self.actionRectangle_coordinates.setObjectName("actionRectangle_coordinates")
        self.actionCreation_Rectangle = QtWidgets.QAction(cube_ans)
        self.actionCreation_Rectangle.setObjectName("actionCreation_Rectangle")
        self.actionSpectrum_visualization = QtWidgets.QAction(cube_ans)
        self.actionSpectrum_visualization.setObjectName("actionSpectrum_visualization")
        self.actionEllipse = QtWidgets.QAction(cube_ans)
        self.actionEllipse.setObjectName("actionEllipse")
        self.actionBackground_subtraction = QtWidgets.QAction(cube_ans)
        self.actionBackground_subtraction.setEnabled(False)
        self.actionBackground_subtraction.setObjectName("actionBackground_subtraction")
        self.actionUnselect = QtWidgets.QAction(cube_ans)
        self.actionUnselect.setObjectName("actionUnselect")
        self.actionCreation_Ellipse = QtWidgets.QAction(cube_ans)
        self.actionCreation_Ellipse.setObjectName("actionCreation_Ellipse")
        self.actionZoom_reset = QtWidgets.QAction(cube_ans)
        self.actionZoom_reset.setObjectName("actionZoom_reset")
        self.actionEllipse_coordinates = QtWidgets.QAction(cube_ans)
        self.actionEllipse_coordinates.setObjectName("actionEllipse_coordinates")
        self.menuFile.addAction(self.actionOpen)
        self.menuTools.addAction(self.actionUnselect)
        self.menuTools.addAction(self.actionRectangle)
        self.menuTools.addAction(self.actionEllipse)
        self.menuTools.addAction(self.actionZoom)
        self.menuTools.addAction(self.actionPan)
        self.menuTools.addAction(self.actionZoom_reset)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionRectangle_coordinates)
        self.menuTools.addAction(self.actionCreation_Rectangle)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionEllipse_coordinates)
        self.menuTools.addAction(self.actionCreation_Ellipse)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionSpectrum_visualization)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionBackground_subtraction)
        self.menuColor.addAction(self.actionGray)
        self.menuColor.addAction(self.actionAccent)
        self.menuColor.addAction(self.actionHeat)
        self.menuColor.addAction(self.actionRainbow)
        self.menuColor.addAction(self.actionCoolWarm)
        self.menuStretch.addAction(self.actionSqrt)
        self.menuStretch.addAction(self.actionLog)
        self.menuStretch.addAction(self.actionLinear)
        self.menuScale.addAction(self.actionMinMax_Interval)
        self.menuScale.addAction(self.actionZScale_Interval)
        self.menuStyle.addAction(self.menuColor.menuAction())
        self.menuStyle.addAction(self.menuScale.menuAction())
        self.menuStyle.addAction(self.menuStretch.menuAction())
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuStyle.menuAction())

        self.retranslateUi(cube_ans)
        QtCore.QMetaObject.connectSlotsByName(cube_ans)

    def retranslateUi(self, cube_ans):
        _translate = QtCore.QCoreApplication.translate
        cube_ans.setWindowTitle(_translate("cube_ans", "cube_ans"))
        self.label.setText(_translate("cube_ans", "Slice"))
        self.label_3.setText(_translate("cube_ans", "Wavelengt Value"))
        self.label_2.setText(_translate("cube_ans", "Slice Value"))
        self.menuFile.setTitle(_translate("cube_ans", "File"))
        self.menuTools.setTitle(_translate("cube_ans", "Tools"))
        self.menuStyle.setTitle(_translate("cube_ans", "Style"))
        self.menuColor.setTitle(_translate("cube_ans", "Color"))
        self.menuStretch.setTitle(_translate("cube_ans", "Stretch"))
        self.menuScale.setTitle(_translate("cube_ans", "Scale"))
        self.actionOpen.setText(_translate("cube_ans", "Open"))
        self.actionRectangle.setText(_translate("cube_ans", "Rectangle aperture"))
        self.actionZoom.setText(_translate("cube_ans", "Zoom"))
        self.actionPan.setText(_translate("cube_ans", "Pan"))
        self.actionMinMax_Interval.setText(_translate("cube_ans", "MinMax Interval"))
        self.actionZScale_Interval.setText(_translate("cube_ans", "ZScale Interval"))
        self.actionSqrt.setText(_translate("cube_ans", "Sqrt"))
        self.actionLog.setText(_translate("cube_ans", "Log"))
        self.actionLinear.setText(_translate("cube_ans", "Linear"))
        self.actionGray.setText(_translate("cube_ans", "Gray"))
        self.actionAccent.setText(_translate("cube_ans", "Accent"))
        self.actionHeat.setText(_translate("cube_ans", "Heat"))
        self.actionRainbow.setText(_translate("cube_ans", "Rainbow"))
        self.actionCoolWarm.setText(_translate("cube_ans", "CoolWarm"))
        self.actionRectangle_coordinates.setText(_translate("cube_ans", "Rectangle coordinates"))
        self.actionCreation_Rectangle.setText(_translate("cube_ans", "Creation of Rectangle parameterized"))
        self.actionSpectrum_visualization.setText(_translate("cube_ans", "Spectrum visualization"))
        self.actionEllipse.setText(_translate("cube_ans", "Ellipse aperture"))
        self.actionBackground_subtraction.setText(_translate("cube_ans", "Background subtraction"))
        self.actionUnselect.setText(_translate("cube_ans", "Unselect current tool"))
        self.actionCreation_Ellipse.setText(_translate("cube_ans", "Creation of Ellipse parameterized"))
        self.actionZoom_reset.setText(_translate("cube_ans", "Zoom reset"))
        self.actionEllipse_coordinates.setText(_translate("cube_ans", "Ellipse coordinates"))

