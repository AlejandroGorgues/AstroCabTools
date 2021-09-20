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
from matplotlib.patches import Wedge
import matplotlib.gridspec as gridspec

from pubsub import pub

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..io.miri_cube_load import get_miri_cube_data
from ..utils.centroid_operations import calculate_centroid
from ..utils.basic_transformations import set_round_value

from .canvas_interaction.centroidAreaSelectionCanvas.panZoom import figure_pz

import astrocabtools.mrs_subviz.src.ui.ui_centroidAreaSelection


__all__=["CentroidAreaSelection"]

class CentroidAreaSelection(QDialog,
             astrocabtools.mrs_subviz.src.ui.ui_centroidAreaSelection.Ui_centroidAreaSelection):

    def __init__(self):
        super(CentroidAreaSelection, self).__init__()

        self.setupUi(self)

        self.create_axes()
        self.zoomButton.clicked.connect(self.zoomOrders)
        self.panButton.clicked.connect(self.panOrders)
        self.zoomResetButton.clicked.connect(self.zoomResetOrders)

        pub.subscribe(self.emit_data, 'emit_range_data')

        self.centroidButton.clicked.connect(self.manageCentroid)

        self.cubeFigure.pan_zoom.connect_rectangle_selection()

    def zoomOrders(self):
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_rectangle_selection()
        self.cubeFigure.pan_zoom.connect_zoom()
        self.cubeFigure.canvas.clearFocus()

    def panOrders(self):
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.disconnect_rectangle_selection()
        self.cubeFigure.pan_zoom.connect_pan()
        self.cubeFigure.canvas.clearFocus()

    def zoomResetOrders(self):
        self.cubeFigure.pan_zoom.zoom_reset()

    def manageCentroid(self):
        self.cubeFigure.pan_zoom.disconnect_pan()
        self.cubeFigure.pan_zoom.disconnect_zoom()
        self.cubeFigure.pan_zoom.connect_rectangle_selection()

    def get_data_from_centroid_wave(self, order, cubeParams, subband, data, additionalOrder = None):

        """
        Draw the cube each time this method is called in case the slice or
        subband changed
        """
        self.order = order
        self.additionalOrder = additionalOrder
        self.cubeParams = cubeParams
        self.data = data
        self.draw_cube(cubeParams.path, data, cubeParams.cubeModel, cubeParams.style,
                       cubeParams.axis[0].get_xlim(), cubeParams.axis[0].get_ylim())

    def modify_image(self, typeStyle, objStyle):
        im = self.ax.get_images()[0]

        if typeStyle == "color":
            im.set_cmap(objStyle)
        elif typeStyle == "stretch":
            im.set_norm(objStyle)
        elif typeStyle == "scale":
            im.set_norm(objStyle)

        self.cubeFigure.canvas.draw()

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
        self.ax.set_zorder(5)

        self.cubeFigure.pan_zoom.create_rectangle_ax(self.ax)

        self.cubeGroupBox.setLayout(layout)

    def draw_cube(self, path, data, cubeModel, style, xlim, ylim):
        self.ax.images.clear()

        self.ax.set_visible(True)
        self.ax.grid(False)

        self.ax_twiny.set_visible(True)
        self.ax_twinx.set_visible(True)

        self.ax.set_title("{}".format(cubeModel.meta.filename))
        self.ax.set_xlabel("pixel - 1")
        self.ax.set_ylabel("pixel - 1")

        self.ax_twiny.set_xlabel(r'$arcsec$')
        self.ax_twinx.set_ylabel(r'$arcsec$')

        im = self.ax.imshow(data, origin='lower',aspect='auto')
        im.set_cmap(plt.get_cmap((style.color)))
        norm = self.get_norm(style.stretch, style.scale)
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

    def emit_data(self, order = None, rangeData =None):
        """
        Calculate and send the centroid coordinates to the main window
        :param str order: type of order to be executed
        :param dict rangeData: dictionary that contains the coordinates of the area selected
        """
        x, y = calculate_centroid(self.data[set_round_value(rangeData["iy"]):set_round_value(rangeData["ey"]),set_round_value(rangeData["ix"]):set_round_value(rangeData["ex"])])
        pub.sendMessage('centroidCoords', patchesData={'xCoordinate': x+rangeData["ix"], 'yCoordinate':y+rangeData["iy"]}, additionalOrder = self.additionalOrder)

    def generic_alert(self):
        alert=QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def clear_data(self):
        """Clear all the data generated from the cube loaded previously"""

        self.ax.clear()
        self.ax.set_visible(False)

        self.cubeFigure.pan_zoom.clear_elements_axes(self.ax)

        self.close()
