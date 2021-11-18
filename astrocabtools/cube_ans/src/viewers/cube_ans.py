# -*- coding: utf-8 -*-

"""
Main class that generate the interface of the cube_ans tool
"""

import numpy as np
import matplotlib.pyplot as plt

import copy

import pandas as pd

import sys
import traceback
import io

from astropy.visualization import (MinMaxInterval, ZScaleInterval, SqrtStretch, LinearStretch, LogStretch, ImageNormalize)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QEvent
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib import widgets
from matplotlib.patches import Wedge
from matplotlib.ticker import FormatStrFormatter

from pubsub import pub

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..utils.rectangle_xy_transformations import transform_xy_rectangle
from ..utils.ellipse_xy_transformations import transform_xy_ellipse
from ..utils.basic_transformations import slice_to_wavelength, wavelength_to_slice

from ..io.miri_cube_load import get_miri_cube_data
from ..io.muse_cube_load import get_muse_cube_data
from ..io.megara_cube_load import get_megara_cube_data

from .canvas_interaction.cubeAnsCanvas.panZoom import figure_pz

from ..models.globalStats import global_stats


import astrocabtools.cube_ans.src.viewers.cubeSelection as cubeSelect
import astrocabtools.cube_ans.src.viewers.spectrumVisualization as spectrumV
import astrocabtools.cube_ans.src.viewers.rectangleCoordinates as rectCoord
import astrocabtools.cube_ans.src.viewers.rectangleCreation as rectCreat
import astrocabtools.cube_ans.src.viewers.ellipseCreation as ellCreat
import astrocabtools.cube_ans.src.viewers.ellipseCoordinates as ellCoord
import astrocabtools.cube_ans.src.viewers.backgroundSubtraction as backgSub
import astrocabtools.cube_ans.src.ui.ui_cube_ans


__all__=["CubeAns"]

class CubeAns(QMainWindow,
             astrocabtools.cube_ans.src.ui.ui_cube_ans.Ui_cube_ans):

    def __init__(self):
        super(CubeAns, self).__init__()

        self.setupUi(self)

        self.globalStats = global_stats('MinMax', 'Linear', 'gray', 0)

        self.actionOpen.triggered.connect(self.fileOrders)
        self.actionRectangle.triggered.connect(self.rectangleOrders)
        self.actionEllipse.triggered.connect(self.ellipseOrders)
        self.actionZoom.triggered.connect(self.zoomOrders)
        self.actionPan.triggered.connect(self.panOrders)
        self.actionUnselect.triggered.connect(self.unSelectOrders)
        self.actionZoom_reset.triggered.connect(self.zoomResetOrders)

        self.actionRectangle_coordinates.triggered.connect(self.rectCoordOrders)
        self.actionCreation_Rectangle.triggered.connect(self.rectCreatOrders)

        self.actionEllipse_coordinates.triggered.connect(self.ellCoordOrders)
        self.actionCreation_Ellipse.triggered.connect(self.ellCreatOrders)

        self.actionSpectrum_visualization.triggered.connect(self.spectrumVisOrders)

        self.actionBackground_subtraction.triggered.connect(self.backgSubOrders)

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
        self.ellCreat = ellCreat.EllipseCreation()
        self.ellCoord = ellCoord.EllipseCoordinates()
        self.backgSub = backgSub.BackgroundSubtraction()

        self.backgSub.wedgesSelected.connect(self.draw_wedges)
        self.backgSub.valuesSubstracted.connect(self.update_background_spectrum)

        pub.subscribe(self.select_area_rectangle, 'rectangleSelected')
        pub.subscribe(self.select_area_ellipse, 'ellipseSelected')

        pub.subscribe(self.draw_rectangle_coordinates, 'rectangleCreation')
        pub.subscribe(self.draw_ellipse_coordinates, 'ellipseCreation')

        pub.subscribe(self.obtain_range_data, 'rangeData')

        self.wavelengthLineEdit.setValidator(QtGui.QDoubleValidator())

    def initialize_slice_widgets(self):
        #If text change, update slider and viceversa
        self.sliceSpinBox.valueChanged.connect(self.update_from_spinBox)

        self.sliceSlider.valueChanged.connect(self.update_from_slider)

        self.wavelengthLineEdit.returnPressed.connect(self.update_from_lineEdit)

    def set_widgets_values(self):
        """
        Set all widgets values and text to initial values and text when a new cube
        is loaded
        """

        self.sliceSpinBox.blockSignals(True)
        self.sliceSlider.blockSignals(True)
        self.sliceMaximumValue.setText(str(slice_to_wavelength(self.cubeModel.data.shape[0], self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)))
        self.sliceMinimumValue.setText(str(slice_to_wavelength(1, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)))

        self.sliceSpinBox.setMinimum(1)
        self.sliceSpinBox.setMaximum(self.cubeModel.data.shape[0])

        self.sliceSlider.setMinimum(1)
        self.sliceSlider.setMaximum(self.cubeModel.data.shape[0])

        self.wavelengthLineEdit.setText(str(slice_to_wavelength(1, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)))

        self.sliceSlider.blockSignals(False)
        self.sliceSpinBox.blockSignals(False)

        """
        Set slider value to be 1 because the minimum value for a cube could be
        a common value for another
        """
        self.sliceSlider.setValue(1)

    def update_from_spinBox(self):
        """Update the slider and the wavelength line edit from the spinBox value"""
        slice_value = self.sliceSpinBox.value()
        self.sliceSlider.setValue(slice_value)
        self.wavelengthLineEdit.setText(str(slice_to_wavelength(slice_value, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)))

    def update_from_slider(self):
        """Update slice spin box and wavelength line edit from slice slider value"""

        #Because in the slider, the values goes from 1 to 500, when another
        #functionality need to use it in the cubeObj, it value must be one less to
        #acess the correct index which will be the current - 1
        slice_value = self.sliceSlider.value()-1

        #Because a subtraction had been made to the slice to make the slider use
        #the correct values previously, the slice to be converted cannot be 0
        wavelength_value = slice_to_wavelength(slice_value+1, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)

        self.globalStats.currSlice = slice_value
        self.sliceSpinBox.blockSignals(True)

        #To prevent the slice value to get an slice value of 0, the current slice will
        #be the current +1
        self.sliceSpinBox.setValue(slice_value+1)
        self.sliceSpinBox.blockSignals(False)

        self.wavelengthLineEdit.setText(str(wavelength_value))
        self.draw_cube()

        #To prevent the access when there is no spectrum made, it checks if it has been
        #created
        if not self.spectrumV.isHidden():
            #Update the position of the line to match the current wavelength and it's associated flux
            self.spectrumV.update_wavelength_line(wavelength_value)

        self.cubeFigure.pan_zoom.redraw_rectangle_with_interaction()
        self.cubeFigure.pan_zoom.redraw_ellipse_with_interaction()

    def update_from_lineEdit(self):
        slice_value = wavelength_to_slice(float(self.wavelengthLineEdit.text()), self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)
        self.sliceSlider.setValue(slice_value)
        self.sliceSpinBox.setValue(slice_value)


    def fileOrders(self):
        self.cubeSelection.show()
        self.cubeSelection.open()

    def rectangleOrders(self):
        #Check if rectangle is not activated previously to not duplicate it
        if not self.cubeFigure.pan_zoom.rectangle_active():
            self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_ellipse(True)
            self.cubeFigure.pan_zoom.connect_rectangle()
            self.cubeFigure.canvas.clearFocus()
            self.cubeFigure.pan_zoom.redraw_rectangle_from_rectButton()


    def ellipseOrders(self):
        #Check if ellipse is not activate previously to not duplicate it
        if not self.cubeFigure.pan_zoom.ellipse_active():
            self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_rectangle(True)
            self.cubeFigure.pan_zoom.connect_ellipse()
            self.cubeFigure.canvas.clearFocus()
            self.cubeFigure.pan_zoom.redraw_ellipse_from_elliButton()


    def zoomOrders(self):
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_rectangle()
        self.cubeFigure.pan_zoom.disconnect_ellipse()
        self.cubeFigure.pan_zoom.connect_zoom()
        self.cubeFigure.canvas.clearFocus()

    def panOrders(self):
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.disconnect_rectangle()
        self.cubeFigure.pan_zoom.disconnect_ellipse()
        self.cubeFigure.pan_zoom.connect_pan()
        self.cubeFigure.canvas.clearFocus()

    def unSelectOrders(self):
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.disconnect_rectangle(True)
        self.cubeFigure.pan_zoom.disconnect_ellipse(True)
        self.cubeFigure.pan_zoom.disconnect_pan()

    def zoomResetOrders(self):
        self.cubeFigure.pan_zoom.zoom_reset()

    def rectCoordOrders(self):
        self.rectCoord.show()
        self.rectCoord.open()

    def rectCreatOrders(self):
        self.rectCreat.show()
        self.rectCreat.open()

    def ellCreatOrders(self):
        self.ellCreat.show()
        self.ellCreat.open()

    def ellCoordOrders(self):
        self.ellCoord.show()
        self.ellCoord.open()

    def spectrumVisOrders(self):
        self.spectrumV.show()
        self.spectrumV.open()

    def backgSubOrders(self):
        self.backgSub.show()
        self.backgSub.open()

    def colorOrders(self, color_text):
        color_text = color_text.text()
        if color_text == "Accent":
            [image.set_cmap(plt.get_cmap("Accent")) for image in self.ax.get_images()]
            self.globalStats.color = "Accent"
        elif color_text == "Heat":
            [image.set_cmap(plt.get_cmap("gist_heat")) for image in self.ax.get_images()]
            self.globalStats.color = "gist_heat"
        else:
            [image.set_cmap(plt.get_cmap(color_text.lower())) for image in self.ax.get_images()]
            self.globalStats.color = color_text.lower()

        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_ellipse_with_interaction()
        self.cubeFigure.pan_zoom.redraw_rectangle_with_interaction()

    def stretchOrders(self, stretch_text):

        image = self.ax.get_images()[0]
        self.globalStats.stretch = stretch_text.text()

        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)
        image.set_norm(norm)

        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_ellipse_with_interaction()
        self.cubeFigure.pan_zoom.redraw_rectangle_with_interaction()

    def scaleOrders(self, scale_text):

        image = self.ax.get_images()[0]
        self.globalStats.scale = scale_text.text()

        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)
        image.set_norm(norm)

        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_ellipse_with_interaction()
        self.cubeFigure.pan_zoom.redraw_rectangle_with_interaction()

    def get_norm(self, stretch_text, scale_text):

        image = self.ax.get_images()[0]
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

        minV, maxV = scale.get_limits(self.cubeModel.data[self.globalStats.currSlice])

        norm = ImageNormalize(vmin=minV, vmax=maxV, stretch=stretch)
        return norm

    def obtain_range_data(self, iw, ew):
        """Get the flux values from the wavelength range of values to visualize it
        :param int iw: left x wavelength value
        :param int ew: right x wavelength value
        """
        iw_slice = wavelength_to_slice(iw, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)
        ew_slice = wavelength_to_slice(ew, self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)

        #If the range rectangle is created outside the spectrum, show a warning
        #Otherwise, check if the initial wavelength is below the slice 0 and assign it
        #Otherwise, execute the program
        if (iw_slice < 0 or iw_slice > self.cubeModel.data.shape[0]) and (ew_slice < 0 or ew_slice > self.cubeModel.data.shape[0]):
            self.max_range_warning()
        else:
            if iw_slice < 0:
                iw_slice = 0
            data = self.cubeModel.data[iw_slice:ew_slice]
            data_converted = np.mean(data, axis=0)
            self.spectrumV.show_range_data(str(round(iw,5)), str(round(ew,5)), data_converted)

    def select_area_rectangle(self):
        """.-Draw the spectrum based on the coordinates of the rectangle
        .-Draw the wedges based on the center of the figure
        .-Set the data for the figure to be drawn in the funcExtra dialog
        .-Update the data the background operation will use
        """
        try:
            if self.spectrumV.isHidden():
                self.spectrumV.show()
                self.spectrumV.open()
            #Get flux and wavelength values from the aperture
            rectangleData = self.cubeFigure.pan_zoom.get_rectangle_data()
            fValues, wValues, aperture = transform_xy_rectangle(centerX=rectangleData[1][0], centerY= rectangleData[1][1],
                                                                width = rectangleData[0][2], height= rectangleData[0][3], cubeModel = self.cubeModel)

            #Draw the spectrum
            self.spectrumV.draw_spectrum(self.globalStats.path, fValues, wValues, self.cubeModel.meta.wcsinfo.cunit3[:3], self.cubeModel.meta.bunit_data)

            #Set the position of the circle that follows the current slice
            wavelength_value = slice_to_wavelength(self.sliceSlider.value(), self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)
            self.spectrumV.update_wavelength_line(wavelength_value)

            #Set the parameters the background operation will use
            self.backgSub.update_center_data(rectangleData, self.cubeModel, aperture, fValues)
            self.actionBackground_subtraction.setEnabled(True)

        except Exception as e:
            self.generic_alert()

    def select_area_ellipse(self):
        """.-Draw the spectrum based on the coordinates of the ellipse
        .-Draw the wedges based on the center of the figure
        .-Set the data for the figure to be drawn in the funcExtra dialog
        .-Update the data that the background operation will use
        """
        try:
            if self.spectrumV.isHidden():
                self.spectrumV.show()
                self.spectrumV.open()

            #Get flux and wavelength values from the aperture
            ellipseData = self.cubeFigure.pan_zoom.get_ellipse_data()
            fValues, wValues, aperture = transform_xy_ellipse(centerX = ellipseData[1][0], centerY = ellipseData[1][1],
                                                              aAxis = ellipseData[0][2], bAxis = ellipseData[0][3], cubeModel = self.cubeModel)

            #Draw the spectrum
            self.spectrumV.draw_spectrum(self.globalStats.path, fValues, wValues, self.cubeModel.meta.wcsinfo.cunit3[:3], self.cubeModel.meta.bunit_data)

            #Set the position of the circle that follows the current slice
            wavelength_value = slice_to_wavelength(self.sliceSlider.value(), self.cubeModel.meta.wcsinfo.crpix3, self.cubeModel.meta.wcsinfo.cdelt3, self.cubeModel.meta.wcsinfo.crval3)
            self.spectrumV.update_wavelength_line(wavelength_value)

            #Set the parameters the background operation will use
            self.backgSub.update_center_data(ellipseData, self.cubeModel, aperture, fValues)
            self.actionBackground_subtraction.setEnabled(True)

        except Exception as e:
            self.generic_alert()

    @pyqtSlot(list, list, name='backgroundParameters')
    def update_background_spectrum(self, fValues_subs, bkg_sum):
        if self.spectrumV.isHidden():
            self.spectrumV.show()
            self.spectrumV.open()
        self.spectrumV.draw_background(fValues_subs, bkg_sum)

    @pyqtSlot(float, float, float, float, name='wedgesEmit')
    def draw_wedges(self, centerX, centerY, innerRadius, outerRadius):

        """
        Draw the rings based on center, radius and range in degrees
        that covers each one, which in this case goes from 0º to 360º
        :param float centerX:
        :param float centerY:
        :param float innerRadius:
        :param float outerRadius:
        """

        self.update_wedges("first_wedge", centerX = centerX, centerY = centerY, radius = innerRadius)
        self.update_wedges("second_wedge", centerX = centerX, centerY = centerY, radius = outerRadius)
        self.cubeFigure.canvas.draw()

    @pyqtSlot(int)
    def get_cube(self, int):
        try:
            if int == QDialog.Accepted:
                self.globalStats.path, cubeModel = self.cubeSelection.get_data()
                self.cubeSelection.reset_widget()
                self.load_file(self.globalStats.path, cubeModel)
            self.cubeFigure.canvas.draw()
        except Exception as e:
            self.show_file_alert()

    def create_axes(self):
        """Create the layout that will show the slice selected of a cube"""
        self.cubeFigure = figure_pz()
        self.cubeFigure.constrained_layout = True

        layout = QVBoxLayout()
        layout.addWidget(self.cubeFigure.canvas)

        self.ax = self.cubeFigure.add_subplot()
        self.ax.set_visible(False)
        self.ax.set_gid("main_axis")

        self.ax_twinx = self.ax.twinx()
        self.ax_twiny = self.ax.twiny()

        self.ax_twinx.set_visible(False)
        self.ax_twiny.set_visible(False)

        self.ax_twinx.set_gid("twinx_axis")
        self.ax_twiny.set_gid("twiny_axis")

        #Set self.ax to the front to be able to use the figures on it
        self.ax.set_zorder(self.ax_twiny.get_zorder() + 1)

        self.cubeFigure.pan_zoom.create_rectangle_ax(self.ax)
        self.cubeFigure.pan_zoom.create_ellipse_ax(self.ax)

        self.spaceCubePlot.setLayout(layout)
        self.ax.grid(False)

    def draw_cube(self):
        self.ax.images.clear()

        #self.ax.grid(False)

        if not self.ax.get_visible():
            self.ax.set_visible(True)
            self.ax_twiny.set_visible(True)
            self.ax_twinx.set_visible(True)

            self.ax.set_title("{}".format(self.globalStats.path))
            self.ax.set_xlabel("pixel - 1")
            self.ax.set_ylabel("pixel - 1")

            self.ax_twiny.set_xlabel(r'$arcsec$')
            self.ax_twinx.set_ylabel(r'$arcsec$')

        im = self.ax.imshow(self.cubeModel.data[self.globalStats.currSlice], origin='lower', aspect='auto')
        im.set_cmap(plt.get_cmap((self.globalStats.color)))
        norm = self.get_norm(self.globalStats.stretch, self.globalStats.scale)
        im.set_norm(norm)

        #self.cubeFigure.pan_zoom.set_initial_limits(self.cubeModel.data.shape[1], self.cubeModel.data.shape[2], self.cubeModel.meta.wcsinfo.crpix1, self.cubeModel.meta.wcsinfo.crpix2, self.cubeModel.meta.wcsinfo.cdelt1, self.cubeModel.meta.wcsinfo.cdelt2, self.cubeModel.meta.wcsinfo.crval1, self.cubeModel.meta.wcsinfo.crval2)
        self.cubeFigure.pan_zoom.set_initial_limits(self.ax.get_xlim(), self.ax.get_ylim(), self.cubeModel.meta.wcsinfo.crpix1, self.cubeModel.meta.wcsinfo.crpix2, self.cubeModel.meta.wcsinfo.cdelt1, self.cubeModel.meta.wcsinfo.cdelt2, self.cubeModel.meta.wcsinfo.crval1, self.cubeModel.meta.wcsinfo.crval2)

        self.ax_twiny.set_xlim((self.ax.get_xlim()[0]- self.cubeModel.meta.wcsinfo.crpix1)*self.cubeModel.meta.wcsinfo.cdelt1*3600 + self.cubeModel.meta.wcsinfo.crval1*3600, (self.ax.get_xlim()[1]- self.cubeModel.meta.wcsinfo.crpix1)*self.cubeModel.meta.wcsinfo.cdelt1*3600 + self.cubeModel.meta.wcsinfo.crval1*3600)
        self.ax_twinx.set_ylim((self.ax.get_ylim()[0]- self.cubeModel.meta.wcsinfo.crpix2)*self.cubeModel.meta.wcsinfo.cdelt2*3600 + self.cubeModel.meta.wcsinfo.crval2*3600, (self.ax.get_ylim()[1]- self.cubeModel.meta.wcsinfo.crpix2)*self.cubeModel.meta.wcsinfo.cdelt2*3600 + self.cubeModel.meta.wcsinfo.crval2*3600)

        self.cubeFigure.pan_zoom.zoom_reset()

    def draw_rectangle_coordinates(self,left_bottom, right_top):
        self.cubeFigure.pan_zoom.update_rectangle(left_bottom[0], left_bottom[1], right_top[0], right_top[1])

    def draw_ellipse_coordinates(self,center, axis):
        self.cubeFigure.pan_zoom.update_ellipse(center[0], center[1], axis[0], axis[1])

    def update_wedges(self, typeWedge, centerX = None, centerY = None, radius = None):
        """ Draw wedges after it has been selected or the wavelength change
        :param float centerX: center x value of the wedge
        :param float centerY: center y value of the wedge
        :parame float radius: radius of the wedge
        """
        wedge = next((patch for patch in enumerate(self.ax.patches) if patch[1].get_gid() == typeWedge), None)

        if wedge is not None:
            if self.ax.patches[wedge[0]].r != radius:
                self.ax.patches[wedge[0]].set_radius(radius)
        else:
            wedge= Wedge((centerX, centerY),
                radius, 0, 360, width=0.2, gid=typeWedge)
            self.ax.add_patch(wedge)

    def load_file(self, path, cubeModel):
        cubeLoadDict = {"MIRI":get_miri_cube_data, "MUSE": get_muse_cube_data, "MEGARA": get_megara_cube_data}
        self.cubeModel = cubeLoadDict[cubeModel](path)

        self.set_widgets_values()

        #Print the slice of the cube
        self.draw_cube()
        self.set_interface_state(True)
        self.clear_data()

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

    def max_range_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("The range selected must be between the spectrum values")
        warning.exec_()

    def clear_data(self):
        """Clear all the data generated from the cube loaded previously"""

        self.actionBackground_subtraction.setEnabled(False)
        self.set_widgets_values()
        self.spectrumV.clear_data()
        self.rectCoord.clear_data()
        self.ellCreat.clear_data()
        self.ellCoord.clear_data()
        self.backgSub.clear_data()

        self.cubeFigure.pan_zoom.clear_elements_axes(self.ax)

        #Disconnect all events
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_rectangle()
        self.cubeFigure.pan_zoom.disconnect_ellipse()
        self.cubeFigure.pan_zoom.disconnect_zoom()

        #Close all dialogs
        self.spectrumV.close()
        self.cubeSelection.close()
        self.rectCoord.close()
        self.rectCreat.close()
        self.ellCreat.close()
        self.ellCoord.close()
        self.backgSub.close()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.cubeFigure.pan_zoom.redraw_rectangle_without_interaction()
            self.cubeFigure.pan_zoom.redraw_ellipse_without_interaction()

    def closeEvent(self, event):
        self.spectrumV.close()
        self.rectCoord.close()
        self.cubeSelection.close()
        self.rectCreat.close()
        self.ellCreat.close()
        self.ellCoord.close()
        self.backgSub.close()
