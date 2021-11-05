# -*- coding: utf-8 -*-

"""
Main class that generate the interface of the sub_viz tool
"""

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

import sys
import traceback
import io

from astropy.visualization import (MinMaxInterval, ZScaleInterval, SqrtStretch, LinearStretch, LogStretch, ImageNormalize)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QMainWindow, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QEvent
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib import widgets
from matplotlib.patches import Wedge, Rectangle
import matplotlib.gridspec as gridspec

from pubsub import pub

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..utils.rectangle_xy_transformations import transform_xy_rectangle
from ..utils.ellipse_xy_transformations import transform_xy_ellipse
from ..utils.basic_transformations import slice_to_wavelength, wavelength_to_slice

from ..io.miri_cube_load import get_miri_cube_data

from .canvas_interaction.cubeViewerCanvas.panZoom import figure_pz

import astrocabtools.mrs_subviz.src.viewers.styleManagerCubeViewer as styleCube
import astrocabtools.mrs_subviz.src.ui.ui_cubeViewer


__all__=["CubeViewer"]

class CubeViewer(QDialog,
             astrocabtools.mrs_subviz.src.ui.ui_cubeViewer.Ui_cubeViewer):
    update_modified_slice = pyqtSignal([str, dict, dict], [str, dict], name= 'cubeModified')


    def __init__(self):
        super(CubeViewer, self).__init__()

        self.setupUi(self)

        self.create_axes()

        self.styleCube = styleCube.StyleManagerCubeViewer()

        self.zoomButton.clicked.connect(self.zoomOrders)
        self.panButton.clicked.connect(self.panOrders)
        self.zoomResetButton.clicked.connect(self.zoomResetOrders)
        self.unselectButton.clicked.connect(self.unSelectOrders)
        self.styleButton.clicked.connect(self.styleOrders)
        self.apertureButton.clicked.connect(self.apertureOrders)
        self.saveButton.clicked.connect(self.save_figure)

        self.styleCube.cubeColorChanged.connect(self.colorOrders)
        self.styleCube.cubeStretchChanged.connect(self.stretchOrders)

        #pub.subscribe(self.draw_rectangle_coordinates, 'rectangleCreation')
        #pub.subscribe(self.draw_ellipse_coordinates, 'ellipseCreation')

        pub.subscribe(self.emit_data, 'emit_data')

        self.figureButton.clicked.connect(self.manageFigure)

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

    def manageFigure(self):
        if self.figureButton.text() == "Rectangle":
            #self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_ellipse(True)
            self.cubeFigure.pan_zoom.connect_rectangle()
            #self.cubeFigure.canvas.clearFocus()
            self.cubeFigure.pan_zoom.redraw_rectangle_from_rectButton()

        elif self.figureButton.text() == "Ellipse":
            #self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_rectangle(True)
            self.cubeFigure.pan_zoom.connect_ellipse()
            #self.cubeFigure.canvas.clearFocus()
            self.cubeFigure.pan_zoom.redraw_ellipse_from_elliButton()

    def styleOrders(self):
        self.styleCube.show()
        self.styleCube.open()

    def apertureOrders(self):
        """
        Make the aperture when the user press the button
        """
        try:
            self.update_modified_slice[str, dict, dict].emit(self.modifiedData['order'], self.modifiedData['axisData'], self.modifiedData['patchesData'])
        except Exception as e:
            self.missing_data_alert()

    def colorOrders(self, colorText):
        im = self.ax.get_images()[0]
        if colorText == "Accent":
            im.set_cmap(plt.get_cmap("Accent"))
        elif colorText == "Heat":
            im.set_cmap(plt.get_cmap("gist_heat"))
        else:
            im.set_cmap(plt.get_cmap(colorText.lower()))
        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_figure_with_interaction()

    def scaleOrders(self, scale):
        im = self.ax.get_images()[0]
        _,_, stretch = self.styleCube.get_data()
        norm = self.get_norm(stretch, scale)
        im.set_norm(norm)
        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_figure_with_interaction()

    def stretchOrders(self, stretch):
        im = self.ax.get_images()[0]
        _,scale, _ = self.styleCube.get_data()
        norm = self.get_norm(stretch, scale)
        im.set_norm(norm)
        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_figure_with_interaction()

    def get_data_from_sub_viz(self, order, cubeParams, figureData=None):

        """
        Draw the cube each time this method is called in case the slice or
        subband changed
        :param str order: operation to be made
        :param dict cubeParams: data of the cube
        :param dict figureData: data of the figure to be draw if needed
        """
        self.order = order
        self.cubeParams = cubeParams
        self.draw_cube(cubeParams.path, cubeParams.currSlice, cubeParams.cubeModel, cubeParams.style,
                       cubeParams.axis[0].get_xlim(), cubeParams.axis[0].get_ylim())

        if order == "rectangleAp":
        #Check if rectangle is not activate previously to not duplicate it
            self.figureButton.setEnabled(True)
            self.apertureButton.setEnabled(True)
            self.figureButton.setText("Rectangle")
            self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_ellipse(True)
            self.cubeFigure.pan_zoom.disconnect_rectangle()
            self.cubeFigure.pan_zoom.connect_rectangle()
            self.cubeFigure.canvas.clearFocus()

            self.cubeFigure.pan_zoom.update_rectangle(figureData.ix, figureData.iy, figureData.ex, figureData.ey)

        elif order == "ellipseAp":
        #Check if ellipse is not activate previously to not duplicate it
            self.figureButton.setEnabled(True)
            self.apertureButton.setEnabled(True)
            self.figureButton.setText("Ellipse")
            self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_rectangle(True)
            self.cubeFigure.pan_zoom.connect_ellipse()
            self.cubeFigure.canvas.clearFocus()

            self.cubeFigure.pan_zoom.update_ellipse(figureData.centerX, figureData.centerY, figureData.aAxis, figureData.bAxis)

        elif order == "wedgesBackg":
            self.delete_patch("rectangleBackg")
            self.draw_wedges(figureData.centerX, figureData.centerY, figureData.innerRadius, figureData.outerRadius)

        elif order == "rectangleBackg":
            self.delete_patch("first_wedge")
            self.delete_patch("second_wedge")
            self.draw_rectangleBackg(figureData.centerX, figureData.centerY, figureData.width, figureData.height)

        elif order == "interactive":
            self.figureButton.setEnabled(False)
            self.apertureButton.setEnabled(False)
            self.cubeFigure.pan_zoom.disconnect_pan()
            self.cubeFigure.pan_zoom.disconnect_zoom()
            self.cubeFigure.pan_zoom.disconnect_rectangle()
            self.cubeFigure.pan_zoom.disconnect_ellipse()
            self.figureButton.setText("No figure")
            self.cubeFigure.canvas.draw()
            self.cubeFigure.pan_zoom.redraw_figure_without_interaction(figureData)

    def change_figure_from_sub_viz(self, order):

        """
        Change the current figure selector that is currently displayed in the
        QDialog
        :param str order: operation to be made
        """
        self.order = order
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.canvas.clearFocus()

        if order == "rectangleAp":
        #Check if rectangle is not activate previously to not duplicate it
            self.figureButton.setEnabled(True)
            self.apertureButton.setEnabled(True)
            self.figureButton.setText("Rectangle")
            self.cubeFigure.pan_zoom.disconnect_ellipse(True)
            self.cubeFigure.pan_zoom.connect_rectangle()
            self.cubeFigure.pan_zoom.redraw_rectangle_with_interaction()

        elif order == "ellipseAp":
        #Check if ellipse is not activate previously to not duplicate it
            self.figureButton.setEnabled(True)
            self.apertureButton.setEnabled(True)
            self.figureButton.setText("Ellipse")
            self.cubeFigure.pan_zoom.disconnect_rectangle(True)
            self.cubeFigure.pan_zoom.connect_ellipse()
            self.cubeFigure.pan_zoom.redraw_ellipse_with_interaction()

    def redraw_slice(self, cubeParams):
        """
        Draw new slice when a cube subtitute another cube
        """
        self.cubeParams = cubeParams
        self.draw_cube(cubeParams.path, cubeParams.currSlice, cubeParams.cubeModel, cubeParams.style,
                       cubeParams.axis[0].get_xlim(), cubeParams.axis[0].get_ylim())
        self.cubeFigure.canvas.draw()

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


    def draw_rectangleBackg(self, centerX, centerY, width, height):
        """
        Draw the rectangle used in the background operatiion
        :param float centerX:
        :param float centerY:
        :param float width:
        :param float height:
        """
        self.update_rectangle("rectangleBackg",centerX = centerX, centerY = centerY, width = width, height = height)
        self.cubeFigure.canvas.draw()


    def draw_centroid(self, xdata, ydata):
        """ Draw marker on specified point
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        marker = next((marker for marker in enumerate(self.ax.collections) if marker[1].get_gid() == "centroid"), None)

        if marker is not None:
            self.ax.collections[marker[0]].set_offsets(np.array([xdata, ydata], ndmin = 2))
            self.cubeFigure.canvas.draw()
        else:
            self.ax.scatter(xdata, ydata, marker='+', c= 'red', gid="centroid")


    def modify_image(self, typeStyle, objStyle):
        im = self.ax.get_images()[0]

        if typeStyle == "color":
            im.set_cmap(objStyle)
        elif typeStyle == "stretch":
            im.set_norm(objStyle)
        elif typeStyle == "scale":
            im.set_norm(objStyle)

        self.cubeFigure.canvas.draw()
        self.cubeFigure.pan_zoom.redraw_figure_with_interaction()

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
        self.ax.set_zorder(-5)
        self.ax_twinx.set_zorder(-6)
        self.ax_twiny.set_zorder(-7)

        self.cubeFigure.pan_zoom.create_rectangle_ax(self.ax)
        self.cubeFigure.pan_zoom.create_ellipse_ax(self.ax)

        self.cubeGroupBox.setLayout(layout)

    def draw_cube(self, path, currSlice, cubeModel, style, xlim, ylim):
        self.ax.images.clear()

        self.ax.set_visible(True)
        self.ax.grid(False)

        self.ax_twiny.set_visible(True)
        self.ax_twinx.set_visible(True)
        self.ax_twiny.grid(False)
        self.ax_twinx.grid(False)

        self.ax.set_title("{}".format(cubeModel.meta.filename))
        self.ax.set_xlabel("pixel - 1")
        self.ax.set_ylabel("pixel - 1")

        self.ax_twiny.set_xlabel(r'$arcsec$')
        self.ax_twinx.set_ylabel(r'$arcsec$')

        im = self.ax.imshow(cubeModel.data[currSlice], origin='lower',aspect='auto')

        color, scale, stretch = self.styleCube.get_data()

        if color == "Accent":
            im.set_cmap(plt.get_cmap("Accent"))
        elif color == "Heat":
            im.set_cmap(plt.get_cmap("gist_heat"))
        else:
            im.set_cmap(plt.get_cmap(color.lower()))
        norm = self.get_norm(stretch, scale)
        im.set_norm(norm)

        self.cubeFigure.pan_zoom.set_initial_limits(xlim, ylim, cubeModel.meta.wcsinfo.crpix1, cubeModel.meta.wcsinfo.crpix2, cubeModel.meta.wcsinfo.cdelt1, cubeModel.meta.wcsinfo.cdelt2, cubeModel.meta.wcsinfo.crval1, cubeModel.meta.wcsinfo.crval2)

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        self.ax_twiny.set_xlim((xlim[0]- cubeModel.meta.wcsinfo.crpix1)*cubeModel.meta.wcsinfo.cdelt1*3600 + cubeModel.meta.wcsinfo.crval1*3600, (xlim[1]- cubeModel.meta.wcsinfo.crpix1)*cubeModel.meta.wcsinfo.cdelt1*3600 + cubeModel.meta.wcsinfo.crval1*3600)
        self.ax_twinx.set_ylim((ylim[0]- cubeModel.meta.wcsinfo.crpix2)*cubeModel.meta.wcsinfo.cdelt2*3600 + cubeModel.meta.wcsinfo.crval2*3600, (ylim[1]- cubeModel.meta.wcsinfo.crpix2)*cubeModel.meta.wcsinfo.cdelt2*3600 + cubeModel.meta.wcsinfo.crval2*3600)

    def get_norm(self, stretch_text, scale_text):
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

        minV, maxV = scale.get_limits(self.cubeParams.cubeModel.data[self.cubeParams.currSlice])
        norm = ImageNormalize(vmin=minV, vmax=maxV, stretch=stretch)
        return norm

    def update_wedges(self, typeWedge, centerX = None, centerY = None, radius = None):
        """ Draw wedges after it has been selected or the wavelength change
        :param bool redraw: decide if the image changed because of wavelenth or not
        :param float centerX: center x value of the wedge
        :param float centerY: center y value of the wedge
        :parame float radius: radius of the wedge
        """

        wedge = next((patch for patch in enumerate(self.ax.patches) if patch[1].get_gid() == typeWedge), None)

        if wedge is not None:
            if self.ax.patches[wedge[0]].r != radius:
                self.ax.patches[wedge[0]].set_center((centerX, centerY))
                self.ax.patches[wedge[0]].set_radius(radius)
        else:
            wedge= Wedge((centerX, centerY),
                radius, 0, 360, width=0.2, gid=typeWedge)
            self.ax.add_patch(wedge)

    def update_rectangle(self, typeRectangle, centerX = None, centerY = None, width = None, height = None):
        """ Draw rectangle after it has been selected or the wavelength change
        :param bool redraw: decide if the image changed because of wavelenth or not
        :param float centerX: center x value of the rectangle
        :param float centerY: center y value of the rectangle
        :param float width: width of the rectangle
        :param float height: height of the rectangle
        """

        rectangle = next((patch for patch in enumerate(self.ax.patches) if patch[1].get_gid() == typeRectangle), None)

        if rectangle is not None:
            self.ax.patches[rectangle[0]].set_center((centerX, centerY))
            self.ax.patches[rectangle[0]].set_width(width)
            self.ax.patches[rectangle[0]].set_height(height)
        else:
            rectangle= Rectangle((centerX, centerY),
                width, height, lw=1.5, facecolor='none', edgecolor='white', gid=typeRectangle)
            self.ax.add_patch(rectangle)


    def delete_patch(self, typePatch):
        if typePatch == "rectangleBackg":
            [self.ax.patches.remove(patch) for patch in reversed(self.ax.patches) if isinstance(patch, Rectangle) and patch.get_gid() == typePatch]
        else:
            [self.ax.patches.remove(patch) for patch in reversed(self.ax.patches) if isinstance(patch, Wedge) and patch.get_gid() == typePatch]

    def emit_data(self, order = None, patchesData = None):
        """
        Update the limits and current image if any interaction have been made
        """
        axisData = {}
        axisData['xlim'] = self.ax.get_xlim()
        axisData['ylim'] = self.ax.get_ylim()
        axisData['twin_ylim'] = self.ax_twinx.get_ylim()
        axisData['twin_xlim'] = self.ax_twiny.get_xlim()
        if patchesData is None:
            self.update_modified_slice[str, dict].emit(order, axisData)
        else:
            self.modifiedData = {}
            self.modifiedData['axisData'] = axisData
            self.modifiedData['order'] = order
            self.modifiedData['patchesData'] = patchesData

            #self.update_modified_slice[str, dict, dict].emit(order, axisData, patchesData)



    def generic_alert(self):
        alert=QMessageBox()
        alert.setText("Error")
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

        self.ax.set_visible(False)
        self.modifiedData = {}

        #Disconnect all events
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_rectangle(True)
        self.cubeFigure.pan_zoom.disconnect_ellipse(True)
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.delete_patch("rectangleBackg")
        self.delete_patch("first_wedge")
        self.delete_patch("second_wedge")
        self.cubeFigure.pan_zoom.clear_elements_axes(self.ax)

        self.styleCube.clear_data()
        self.close()

    def save_figure(self):
        """ Save the figure as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')
            self.cubeFigure.savefig(name[0], dpi = 600, bbox_inches="tight")

        except Exception as e:
            self.show_file_extension_alert()

    def missing_data_alert(self):
        alert = QMessageBox()
        alert.setWindowTitle("Error")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("No aperture has been made")
        alert.exec_()

    def closeEvent(self, event):
        self.styleCube.close()
