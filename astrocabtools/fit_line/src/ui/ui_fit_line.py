# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_line.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FitLine(object):
    def setupUi(self, FitLine):
        FitLine.setObjectName("FitLine")
        FitLine.resize(908, 830)
        self.centralwidget = QtWidgets.QWidget(FitLine)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(100, -1, 100, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.modelSelectionLabel = QtWidgets.QLabel(self.centralwidget)
        self.modelSelectionLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelSelectionLabel.sizePolicy().hasHeightForWidth())
        self.modelSelectionLabel.setSizePolicy(sizePolicy)
        self.modelSelectionLabel.setObjectName("modelSelectionLabel")
        self.horizontalLayout_3.addWidget(self.modelSelectionLabel)
        self.modelSelectionComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.modelSelectionComboBox.setEnabled(False)
        self.modelSelectionComboBox.setMinimumSize(QtCore.QSize(0, 0))
        self.modelSelectionComboBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.modelSelectionComboBox.setObjectName("modelSelectionComboBox")
        self.modelSelectionComboBox.addItem("")
        self.modelSelectionComboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.modelSelectionComboBox)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.continiumSelectionComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.continiumSelectionComboBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continiumSelectionComboBox.sizePolicy().hasHeightForWidth())
        self.continiumSelectionComboBox.setSizePolicy(sizePolicy)
        self.continiumSelectionComboBox.setObjectName("continiumSelectionComboBox")
        self.continiumSelectionComboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.continiumSelectionComboBox)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pointsGenerationButton = QtWidgets.QPushButton(self.centralwidget)
        self.pointsGenerationButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pointsGenerationButton.sizePolicy().hasHeightForWidth())
        self.pointsGenerationButton.setSizePolicy(sizePolicy)
        self.pointsGenerationButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pointsGenerationButton.setObjectName("pointsGenerationButton")
        self.horizontalLayout_2.addWidget(self.pointsGenerationButton)
        self.indicationLabel = QtWidgets.QLabel(self.centralwidget)
        self.indicationLabel.setEnabled(True)
        self.indicationLabel.setMinimumSize(QtCore.QSize(400, 0))
        self.indicationLabel.setMaximumSize(QtCore.QSize(400, 16777215))
        self.indicationLabel.setText("")
        self.indicationLabel.setObjectName("indicationLabel")
        self.horizontalLayout_2.addWidget(self.indicationLabel)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.middlePlot = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.middlePlot.sizePolicy().hasHeightForWidth())
        self.middlePlot.setSizePolicy(sizePolicy)
        self.middlePlot.setTitle("")
        self.middlePlot.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.middlePlot.setFlat(False)
        self.middlePlot.setObjectName("middlePlot")
        self.gridLayout.addWidget(self.middlePlot, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.clickNormalButton = QtWidgets.QPushButton(self.centralwidget)
        self.clickNormalButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clickNormalButton.sizePolicy().hasHeightForWidth())
        self.clickNormalButton.setSizePolicy(sizePolicy)
        self.clickNormalButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clickNormalButton.setCheckable(True)
        self.clickNormalButton.setAutoExclusive(True)
        self.clickNormalButton.setObjectName("clickNormalButton")
        self.horizontalLayout_4.addWidget(self.clickNormalButton)
        self.zoomButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomButton.sizePolicy().hasHeightForWidth())
        self.zoomButton.setSizePolicy(sizePolicy)
        self.zoomButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomButton.setCheckable(True)
        self.zoomButton.setAutoExclusive(True)
        self.zoomButton.setObjectName("zoomButton")
        self.horizontalLayout_4.addWidget(self.zoomButton)
        self.panButton = QtWidgets.QPushButton(self.centralwidget)
        self.panButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panButton.sizePolicy().hasHeightForWidth())
        self.panButton.setSizePolicy(sizePolicy)
        self.panButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.panButton.setCheckable(True)
        self.panButton.setAutoExclusive(True)
        self.panButton.setObjectName("panButton")
        self.horizontalLayout_4.addWidget(self.panButton)
        self.zoomResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomResetButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomResetButton.sizePolicy().hasHeightForWidth())
        self.zoomResetButton.setSizePolicy(sizePolicy)
        self.zoomResetButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomResetButton.setObjectName("zoomResetButton")
        self.horizontalLayout_4.addWidget(self.zoomResetButton)
        self.undoButton = QtWidgets.QPushButton(self.centralwidget)
        self.undoButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.undoButton.sizePolicy().hasHeightForWidth())
        self.undoButton.setSizePolicy(sizePolicy)
        self.undoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.undoButton.setObjectName("undoButton")
        self.horizontalLayout_4.addWidget(self.undoButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathLabel = QtWidgets.QLabel(self.centralwidget)
        self.pathLabel.setText("")
        self.pathLabel.setObjectName("pathLabel")
        self.horizontalLayout.addWidget(self.pathLabel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)
        FitLine.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(FitLine)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 908, 21))
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuVisualization = QtWidgets.QMenu(self.menuBar)
        self.menuVisualization.setEnabled(False)
        self.menuVisualization.setObjectName("menuVisualization")
        FitLine.setMenuBar(self.menuBar)
        self.actionLoad_Spectrum = QtWidgets.QAction(FitLine)
        self.actionLoad_Spectrum.setObjectName("actionLoad_Spectrum")
        self.actionSave_as_png = QtWidgets.QAction(FitLine)
        self.actionSave_as_png.setEnabled(False)
        self.actionSave_as_png.setObjectName("actionSave_as_png")
        self.actionReset_window = QtWidgets.QAction(FitLine)
        self.actionReset_window.setObjectName("actionReset_window")
        self.actionClear_last_fitted_model = QtWidgets.QAction(FitLine)
        self.actionClear_last_fitted_model.setObjectName("actionClear_last_fitted_model")
        self.actionClear_fitted_models = QtWidgets.QAction(FitLine)
        self.actionClear_fitted_models.setObjectName("actionClear_fitted_models")
        self.actionShow_fitted_data_parameters = QtWidgets.QAction(FitLine)
        self.actionShow_fitted_data_parameters.setObjectName("actionShow_fitted_data_parameters")
        self.menuFile.addAction(self.actionLoad_Spectrum)
        self.menuFile.addAction(self.actionSave_as_png)
        self.menuVisualization.addAction(self.actionClear_last_fitted_model)
        self.menuVisualization.addAction(self.actionClear_fitted_models)
        self.menuVisualization.addAction(self.actionReset_window)
        self.menuVisualization.addSeparator()
        self.menuVisualization.addAction(self.actionShow_fitted_data_parameters)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuVisualization.menuAction())

        self.retranslateUi(FitLine)
        QtCore.QMetaObject.connectSlotsByName(FitLine)

    def retranslateUi(self, FitLine):
        _translate = QtCore.QCoreApplication.translate
        FitLine.setWindowTitle(_translate("FitLine", "FitLine"))
        self.modelSelectionLabel.setText(_translate("FitLine", "Choose model to be fitted"))
        self.modelSelectionComboBox.setItemText(0, _translate("FitLine", "One gaussian"))
        self.modelSelectionComboBox.setItemText(1, _translate("FitLine", "Two gaussians"))
        self.label.setText(_translate("FitLine", "Choose continium to use"))
        self.continiumSelectionComboBox.setItemText(0, _translate("FitLine", "Line Continium"))
        self.pointsGenerationButton.setText(_translate("FitLine", "Mark points"))
        self.clickNormalButton.setText(_translate("FitLine", "Click"))
        self.zoomButton.setText(_translate("FitLine", "Zoom"))
        self.panButton.setText(_translate("FitLine", "Pan"))
        self.zoomResetButton.setText(_translate("FitLine", "Zoom reset"))
        self.undoButton.setText(_translate("FitLine", "Undo last zoom"))
        self.menuFile.setTitle(_translate("FitLine", "File"))
        self.menuVisualization.setTitle(_translate("FitLine", "Visualization"))
        self.actionLoad_Spectrum.setText(_translate("FitLine", "Load Spectrum"))
        self.actionSave_as_png.setText(_translate("FitLine", "Save as png"))
        self.actionReset_window.setText(_translate("FitLine", "Reset window"))
        self.actionClear_last_fitted_model.setText(_translate("FitLine", "Clear last fitted model"))
        self.actionClear_fitted_models.setText(_translate("FitLine", "Clear fitted models"))
        self.actionShow_fitted_data_parameters.setText(_translate("FitLine", "Show fitted data parameters"))

