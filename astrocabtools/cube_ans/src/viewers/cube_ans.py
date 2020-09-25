# -*- coding: utf-8 -*-

"""
Main class that generate the interface of the cube_ans tool
"""

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

import sys
import traceback
import io

from astropy.visualization import (MinMaxInterval, ZScaleInterval, SqrtStretch, LinearStretch, LogStretch, ImageNormalize)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib import widgets

from pubsub import pub

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..utils.transform_xy_values import transform_xy_rectangle
from ..utils.basic_transformations import slice_to_wavelength, wavelength_to_slice
from ..io.miri_cube_load import get_miri_cube_data
from .panZoom import figure_pz
from ..models.globalStats import global_stats


import astrocabtools.cube_ans.src.viewers.cubeSelection as cubeSelect
import astrocabtools.cube_ans.src.viewers.spectrumVisualization as spectrumV
import astrocabtools.cube_ans.src.viewers.rectangleCoordinates as rectCoord
import astrocabtools.cube_ans.src.viewers.rectangleCreation as rectCreat
import astrocabtools.cube_ans.src.ui.ui_cube_ans


__all__=["CubeAns"]

class CubeAns(QMainWindow,
             astrocabtools.cube_ans.src.ui.ui_cube_ans.Ui_cube_ans):

    def __init__(self):
        super(CubeAns, self).__init__()

        self.setupUi(self)

        plt.style.use('seaborn')
        self.globalStats = global_stats('MinMax', 'Linear', 'gray')

        self.actionOpen.triggered.connect(self.fileOrders)
        self.actionRectangle.triggered.connect(self.rectangleOrders)
        self.actionZoom.triggered.connect(self.zoomOrders)
        self.actionPan.triggered.connect(self.panOrders)

        self.actionRectangle_coordinates.triggered.connect(self.rectCoordOrders)
        self.actionCreation_of_Rectangle_parameterized.triggered.connect(self.rectCreatOrders)

        self.actionSpectrum_visualization.triggered.connect(self.spectrumVisOrders)

        self.menuColor.triggered.connect(self.colorOrders)
        self.menuStretch.triggered.connect(self.stretchOrders)
        self.menuScale.triggered.connect(self.scaleOrders)

        self.initialize_slice_widgets()

        self.create_axes()

        self.cubeSelection = cubeSelect.CubeList()
        self.cubeSelection.finished.connect(self.get_cube)

        self.spectrumV = spectrumV.SpectrumV()
        self.rectCoord = rectCoord.RectangleCoordinates()
        self.rectCreat = rectCreat.RectangleCreation()

        pub.subscribe(self.select_area, 'rectangleSelected')

        pub.subscribe(self.draw_rectangle_coordinates, 'rectangleCoordinates')

        self.wavelengthLineEdit.setValidator(QtGui.QDoubleValidator())

    def initialize_slice_widgets(self):
        #If text change, update slider and viceversa
        self.sliceSpinBox.valueChanged.connect(
            lambda: self.update_from_spinBox())

        self.sliceSlider.valueChanged.connect(
            lambda: self.update_from_slider())

        self.wavelengthLineEdit.returnPressed.connect(lambda:self.update_from_lineEdit())

    def set_widgets_values(self):

        self.sliceSpinBox.blockSignals(True)
        self.sliceSlider.blockSignals(True)
        self.sliceMaximumValue.setText(str(slice_to_wavelength(self.cubeObj.maxSlice, self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)))
        self.sliceMinimumValue.setText(str(slice_to_wavelength(1, self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)))

        self.sliceSpinBox.setMinimum(1)
        self.sliceSpinBox.setMaximum(self.cubeObj.maxSlice)

        self.sliceSlider.setMinimum(1)
        self.sliceSlider.setMaximum(self.cubeObj.maxSlice)

        self.wavelengthLineEdit.setText(str(slice_to_wavelength(1, self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)))

        self.sliceSlider.blockSignals(False)
        self.sliceSpinBox.blockSignals(False)

    def update_from_spinBox(self):
        """Update the slider and the wavelength line edit from the spinBox value"""
        slice_value = self.sliceSpinBox.value()
        self.sliceSlider.setValue(slice_value)
        self.wavelengthLineEdit.setText(str(slice_to_wavelength(slice_value, self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)))

    def update_from_slider(self):
        """Update slice spin box and wavelength line edit from slice slider value"""

        slice_value = self.sliceSlider.value() -1

        self.cubeObj.currSlice = slice_value
        self.sliceSpinBox.blockSignals(True)
        self.sliceSpinBox.setValue(slice_value+1)
        self.sliceSpinBox.blockSignals(False)

        self.wavelengthLineEdit.setText(str(slice_to_wavelength(slice_value+1, self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)))
        self.draw_cube(self.ax1.get_xlim(), self.ax1.get_ylim())

        self.cubeFigure.pan_zoom.redraw_rectangle_from_slider()

    def update_from_lineEdit(self):

        slice_value = wavelength_to_slice(float(self.wavelengthLineEdit.text()), self.cubeObj.cubeZCPix, self.cubeObj.cubeWValue, self.cubeObj.cubeZCRVal)
        self.sliceSlider.setValue(slice_value)
        self.sliceSpinBox.setValue(slice_value)


    def fileOrders(self):
        self.cubeSelection.show()
        self.cubeSelection.open()

    def rectangleOrders(self):
        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.connect_rectangle()
        self.cubeFigure.canvas.clearFocus()


    def zoomOrders(self):
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_rectangle()
        self.cubeFigure.pan_zoom.connect_zoom()
        self.cubeFigure.canvas.clearFocus()

    def panOrders(self):
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.disconnect_rectangle()
        self.cubeFigure.pan_zoom.connect_pan()
        self.cubeFigure.canvas.clearFocus()

    def rectCoordOrders(self):
        self.rectCoord.show()
        self.rectCoord.open()

    def rectCreatOrders(self):
        self.rectCreat.show()
        self.rectCreat.open()

    def spectrumVisOrders(self):
        self.spectrumV.show()
        self.spectrumV.open()

    def colorOrders(self, color_text):
        color_text = color_text.text()
        if color_text == "Accent":
            [image.set_cmap(plt.get_cmap(color_text)) for image in self.ax1.get_images()]
            self.globalStats.color = color_text
        elif color_text == "Heat":
            [image.set_cmap(plt.get_cmap("gist_heat")) for image in self.ax1.get_images()]
            self.globalStats.color = "gist_heat"
        else:
            [image.set_cmap(plt.get_cmap(color_text.lower())) for image in self.ax1.get_images()]
            self.globalStats.color = color_text.lower()

        self.cubeFigure.canvas.draw()

    def stretchOrders(self, stretch_text):

        image = self.ax1.get_images()[0]
        self.globalStats.stretch = stretch_text.text()

        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)
        image.set_norm(norm)

        self.cubeFigure.canvas.draw()

    def scaleOrders(self, scale_text):

        image = self.ax1.get_images()[0]
        self.globalStats.scale = scale_text.text()

        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)
        image.set_norm(norm)

        self.cubeFigure.canvas.draw()

    def get_norm(self, stretch_text, scale_text):

        image = self.ax1.get_images()[0]
        scale = None

        if scale_text == "MinMax":
            scale = MinMaxInterval()

        else:
            scale = ZScaleInterval()

        if stretch_text == "Linear":
            stretch = LinearStretch()

        elif stretch_text == "Log":
            stretch = LogStretch()

        else:
            stretch = SqrtStretch()

        minV, maxV = scale.get_limits(self.cubeObj.data_cube[self.cubeObj.currSlice])

        norm = ImageNormalize(vmin=minV, vmax=maxV, stretch=stretch)

        return norm


    def select_area(self, ix, iy, ex, ey):
        """Draw the spectrum based on the coordinates of the rectangle
        :param int ix: initial x value of the rectangle
        :param int iy: initial y value of the rectangle
        :param int ex: end x value of the rectangle
        :param int ey: end y value of the rectangle
        """
        if self.spectrumV.isHidden():
            self.spectrumV.show()
            self.spectrumV.open()
        fValues, wValues = transform_xy_rectangle(ix, iy, ex, ey, self.cubeObj)
        self.spectrumV.draw_spectrum(self.path, fValues, wValues, self.cubeObj.cubeWavelengthUnit, self.cubeObj.cubeFluxUnit)

    @pyqtSlot(int)
    def get_cube(self, int):
        try:
            if int == QDialog.Accepted:
                self.path = self.cubeSelection.get_data()
                self.cubeSelection.reset_widget()
                self.load_file(self.path)
            self.cubeFigure.canvas.draw()
        except Exception as e:
            self.show_file_alert()

    def create_axes(self):
        """Create the layout that will show the slice selected of a cube"""
        self.cubeFigure, self.cubeFigure.cavas = figure_pz()
        self.cubeFigure.constrained_layout = True
        self.ax1 = self.cubeFigure.add_subplot(111)
        self.ax1.set_visible(False)
        self.cubeFigure.pan_zoom.create_rectangle_ax(self.ax1)

        self.spaceCubeLayout_vbox.addWidget(self.cubeFigure.canvas)

    def draw_cube(self, x_lim = None, y_lim = None):

        self.ax1.set_visible(True)
        self.ax1.clear()
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.set_title("{}".format(self.cubeObj.filename))

        plt.set_cmap(plt.get_cmap((self.globalStats.color)))
        im = self.ax1.imshow(self.cubeObj.data_cube[self.cubeObj.currSlice])

        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)

        im.set_norm(norm)

        #Set x and y limits in case the previous figure had been zoomed or moved
        if x_lim is not None:
            self.ax1.set_xlim(x_lim)
            self.ax1.set_ylim(y_lim)

        self.cubeFigure.canvas.draw()

    def draw_rectangle_coordinates(self,coord1, coord2):
        self.cubeFigure.pan_zoom.update_rectangle(coord1[0], coord1[1], coord2[0], coord2[1])

    def load_file(self, path):
        self.path = path
        self.cubeObj = get_miri_cube_data(path)

        self.set_widgets_values()

        #Print the slice of the cube
        self.draw_cube()
        self.set_interface_state(True)

    def set_interface_state(self, state):
        """ Disable or enble the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.menuTools.setEnabled(state)
        self.menuStyle.setEnabled(state)
        self.menuColor.setEnabled(state)
        self.sliceSlider.setEnabled(state)
        self.sliceSpinBox.setEnabled(state)
        self.wavelengthLineEdit.setEnabled(state)

    def generic_alert(self):
        alert=QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_file_alert(self):
        alert = QMessageBox()
        alert.setText("Error: File values or properties incorrect")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def values_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def closeEvent(self, event):
        self.spectrumV.close()
        self.cubeSelection.close()
        self.rectCoord.close()
        self.rectCreat.close()
