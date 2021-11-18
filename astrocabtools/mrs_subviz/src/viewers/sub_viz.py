# -*- coding: utf-8 -*-

"""
Main class that generate the interface of the sub_viz tool
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import pandas as pd

import sys
import traceback
import io

import copy

from astropy.visualization import (MinMaxInterval, ZScaleInterval, SqrtStretch, LinearStretch, LogStretch, ImageNormalize)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QMainWindow, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QEvent
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib import widgets
from matplotlib.patches import Wedge, Rectangle, Ellipse
from matplotlib.collections import PathCollection
import matplotlib.gridspec as gridspec

from pubsub import pub

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..utils.rectangle_xy_transformations import transform_xy_rectangle, transform_rectangle_subband, transform_rectangle_subband_from_coord
from ..utils.ellipse_xy_transformations import transform_xy_ellipse, transform_ellipse_subband, transform_ellipse_subband_from_coord
from ..utils.centroid_operations import transform_centroid_subband
from ..utils.basic_transformations import slice_to_wavelength, wavelength_to_slice, rectangle_patch_to_border_coordinates, rectangle_border_to_patch_coordinates
from ..utils.background_xy_transformations import annulus_background_subtraction, rectangle_background_subtraction, transform_wedges_subband
from ..utils.constants import SUBBANDDICT, INDEXDICT, COLORDICT

from ..io.miri_cube_load import get_miri_cube_data
from ..io.directory_miri_cube_load import get_miri_cube_subband

from ..models.cubeStats import cube_stats
from ..models.cubeViewerData import cube_viewer_data
from ..models.cubePatchesData import cube_patches_data
from ..models.cubeCurrState import cube_curr_state

import astrocabtools.mrs_subviz.src.viewers.cubeSelection as cubeSelect
import astrocabtools.mrs_subviz.src.viewers.spectrumVisualization as spectrumV
import astrocabtools.mrs_subviz.src.viewers.rectangleCoordinates as rectCoord
import astrocabtools.mrs_subviz.src.viewers.rectangleCreation as rectCreat
import astrocabtools.mrs_subviz.src.viewers.ellipseCreation as ellCreat
import astrocabtools.mrs_subviz.src.viewers.ellipseCoordinates as ellCoord
import astrocabtools.mrs_subviz.src.viewers.backgroundSubtraction as backgSub
import astrocabtools.mrs_subviz.src.viewers.centroidWavelengthSelection as centWave
import astrocabtools.mrs_subviz.src.viewers.centroidCoordinates as centCoord
import astrocabtools.mrs_subviz.src.viewers.collapsedWavelengthSelection as collapsedWave
import astrocabtools.mrs_subviz.src.viewers.wavelengthRangeSelection as waveSelect

import astrocabtools.mrs_subviz.src.viewers.cubeLoader as cubeLoader
import astrocabtools.mrs_subviz.src.viewers.styleManager as styleManager
import astrocabtools.mrs_subviz.src.viewers.sliceManager as sliceManager
import astrocabtools.mrs_subviz.src.viewers.cubeViewer as cubeViewer

import astrocabtools.mrs_subviz.src.ui.ui_sub_viz


__all__=["SubViz"]

class SubViz(QMainWindow,
             astrocabtools.mrs_subviz.src.ui.ui_sub_viz.Ui_sub_viz):

    def __init__(self):
        super(SubViz, self).__init__()

        self.setupUi(self)

        self.actionOpen.triggered.connect(self.fileOrders)

        self.cubeList = {0:cube_viewer_data((0,0)), 1:cube_viewer_data((1,0)), 2:cube_viewer_data((2,0)), 3:cube_viewer_data((0,1)), 4:cube_viewer_data((1,1)), 5:cube_viewer_data((2,1)), 6:cube_viewer_data((0,2)), 7:cube_viewer_data((1,2)), 8:cube_viewer_data((2,2)), 9:cube_viewer_data((0,3)), 10:cube_viewer_data((1,3)), 11:cube_viewer_data((2,3))}

        self.cubeCurrState = cube_curr_state()

        self.actionSet_current_wavelength.triggered.connect(self.updateWavelengthOrders)
        self.actionRectangle.triggered.connect(lambda: self.selectSubbandOrders("rectangleAp"))
        self.actionEllipse.triggered.connect(lambda: self.selectSubbandOrders("ellipseAp"))
        self.actionInteractiveOp.triggered.connect(lambda: self.selectSubbandOrders("interactive"))
        self.actionRectangle_coordinates.triggered.connect(lambda: self.selectSubbandOrders("rectangleCoord"))
        self.actionEllipse_coordinates.triggered.connect(lambda: self.selectSubbandOrders("ellipseCoord"))
        self.actionNo_centroid_CR.triggered.connect(lambda: self.selectSubbandOrders("rectangleCreate"))
        self.actionCentroid_and_center_CR.triggered.connect(lambda: self.selectSubbandOrders("centroidSelect", "rectangleAndCenter"))
        self.actionCentroid_as_center_CR.triggered.connect(lambda: self.selectSubbandOrders("centroidSelect", "rectangleWithCenter"))
        self.actionNo_centroid_CE.triggered.connect(lambda: self.selectSubbandOrders("ellipseCreate"))
        self.actionCentroid_and_center_CE.triggered.connect(lambda: self.selectSubbandOrders("centroidSelect", "ellipseAndCenter"))
        self.actionCentroid_as_center_CE.triggered.connect(lambda: self.selectSubbandOrders("centroidSelect", "ellipseWithCenter"))
        self.actionDrawRectangle.triggered.connect(lambda: self.drawPatchOrders("rectangle"))
        self.actionDrawEllipse.triggered.connect(lambda: self.drawPatchOrders("ellipse"))
        self.actionSavespng.triggered.connect(self.save_figure)
        self.actionSpectrum_visualization.triggered.connect(self.spectrumVisOrders)
        self.actionBackground_subtraction.triggered.connect(lambda: self.selectSubbandOrders("backgSub"))
        self.actionCollapsed_image.triggered.connect(lambda: self.selectSubbandOrders("collapsedSelect"))
        self.actionCalculate_centroid.triggered.connect(lambda: self.selectSubbandOrders("centroidSelect"))
        self.actionShow_centroid_coordinates.triggered.connect(lambda: self.selectSubbandOrders("centroidCoord"))


        self.actionManage_style.triggered.connect(self.manageStyleOrders)

        self.create_axes()

        self.cubeLoader = cubeLoader.CubeLoader()
        self.cubeLoader.finished.connect(self.get_cube)

        self.spectrumV = spectrumV.SpectrumV()
        self.rectCoord = rectCoord.RectangleCoordinates()
        self.rectCreate = rectCreat.RectangleCreation()
        self.ellCreate = ellCreat.EllipseCreation()
        self.ellCoord = ellCoord.EllipseCoordinates()
        self.backgSub = backgSub.BackgroundSubtraction()
        self.cubeSelection = cubeSelect.CubeSelection()
        self.centCoord = centCoord.CentroidCoordinates()
        self.centWave = centWave.CentroidWavelengthSelection()
        self.collapsedWave = collapsedWave.CollapsedWavelengthSelection()
        self.waveSelect = waveSelect.WavelengthRangeSelection()
        self.styleManager = styleManager.StyleManager()
        self.sliceManager = sliceManager.SliceManager()
        self.cubeViewer = cubeViewer.CubeViewer()

        self.backgSub.wedgesSelected[object, str, bool].connect(self.calculate_background)
        self.backgSub.rectangleSelected[object, str].connect(self.calculate_background)

        self.sliceManager.update_slice.connect(self.update_cube_slice)
        self.sliceManager.obtain_cube.connect(self.send_wavelength_data)

        self.styleManager.colorChanged.connect(self.colorOrders)
        self.styleManager.scaleChanged.connect(self.scaleOrders)
        self.styleManager.stretchChanged.connect(self.stretchOrders)

        self.cubeSelection.subbandSelected.connect(self.obtain_subband)

        self.cubeViewer.update_modified_slice[str, dict].connect(self.update_cube_data_interaction)
        self.cubeViewer.update_modified_slice[str, dict, dict].connect(self.update_cube_data_interaction)

        self.rectCreate.create_rectangle[dict, int].connect(self.create_rectangle_figure_coord)
        self.ellCreate.create_ellipse[dict, int].connect(self.create_ellipse_figure_coord)

        self.collapsedWave.rangeData[int, int].connect(self.send_range_data)

        pub.subscribe(self.create_centroid, 'centroidCoords')



    def fileOrders(self):
        self.cubeLoader.show()
        self.cubeLoader.open()

    def updateWavelengthOrders(self):
        self.sliceManager.show()
        self.sliceManager.open()

    def selectSubbandOrders(self, order, additionalOrder = None):
        self.cubeSelection.set_order(order, additionalOrder)
        self.cubeSelection.show()
        self.cubeSelection.open()

    def manageOrders(self, order, data = None, additionalOrder= None):
        if order == "rectangleAp":

            self.cubeViewer.get_data_from_sub_viz(order, self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.rectangleSelection)
            if self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX != -1:
                self.cubeViewer.draw_wedges(self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX, self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerY, self.cubeList[self.subband].cubePatchesData.wedgesBackground.innerRadius, self.cubeList[self.subband].cubePatchesData.wedgesBackground.outerRadius)
            if self.cubeList[self.subband].centroidCoordinates.xCoordinate != -1:
                self.cubeViewer.draw_centroid(self.cubeList[self.subband].centroidCoordinates.xCoordinate, self.cubeList[self.subband].centroidCoordinates.yCoordinate)
            self.update_image_stats()
            self.cubeViewer.show()
            self.cubeViewer.open()

        elif order == "rectangleCreate":

            wavelength_value = slice_to_wavelength(self.cubeList[self.subband].currSlice, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

            self.rectCreate.get_data(self.cubeList[self.subband].cubeModel, wavelength_value)
            self.rectCreate.show()
            self.rectCreate.open()

        elif order == "rectangleCoord":
            rectangleData = self.cubeList[self.subband].cubePatchesData.rectangleSelection
            self.rectCoord.set_coordinates(rectangleData.ix, rectangleData.iy, rectangleData.ex, rectangleData.ey)
            self.rectCoord.show()
            self.rectCoord.open()

        elif order == "ellipseCoord":

            ellipseData = self.cubeList[self.subband].cubePatchesData.ellipseSelection
            self.ellCoord.set_coordinates(ellipseData.centerX, ellipseData.centerY, ellipseData.aAxis, ellipseData.bAxis)
            self.ellCoord.show()
            self.ellCoord.open()

        elif order == "ellipseAp":
            self.cubeViewer.get_data_from_sub_viz(order, self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.ellipseSelection)
            if self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX != -1:
                self.cubeViewer.draw_wedges(self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX, self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerY, self.cubeList[self.subband].cubePatchesData.wedgesBackground.innerRadius, self.cubeList[self.subband].cubePatchesData.wedgesBackground.outerRadius)
            if self.cubeList[self.subband].centroidCoordinates.xCoordinate != -1:
                self.cubeViewer.draw_centroid(self.cubeList[self.subband].centroidCoordinates.xCoordinate, self.cubeList[self.subband].centroidCoordinates.yCoordinate)
            self.update_image_stats()
            self.cubeViewer.show()
            self.cubeViewer.open()

        elif order == "ellipseCreate":

            wavelength_value = slice_to_wavelength(self.cubeList[self.subband].currSlice, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)
            self.ellCreate.get_data(self.cubeList[self.subband].cubeModel, wavelength_value)
            self.ellCreate.show()
            self.ellCreate.open()

        elif order == "backgSub":
            self.backgSub.show()
            self.backgSub.open()

        elif order == "collapsedSelect":
            endWave = slice_to_wavelength(self.cubeList[self.subband].cubeModel.weightmap.shape[0], self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

            initWave = slice_to_wavelength(0, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

            self.collapsedWave.clear_data()

            self.collapsedWave.get_data_from_sub_viz(initWave, endWave, self.cubeList[self.subband])
            self.collapsedWave.show()
            self.collapsedWave.open()

        elif order == "centroidSelect":
            endWave = slice_to_wavelength(self.cubeList[self.subband].cubeModel.weightmap.shape[0], self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

            initWave = slice_to_wavelength(0, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

            self.centWave.clear_data()

            self.centWave.get_data_from_sub_viz(initWave, endWave, self.subband, self.cubeList[self.subband], order, additionalOrder)
            self.centWave.show()
            self.centWave.open()

        elif order == "centroidCoord":
            self.centCoord.set_coordinates(self.cubeList[self.subband].centroidCoordinates.xCoordinate, self.cubeList[self.subband].centroidCoordinates.yCoordinate)
            self.centCoord.show()
            self.centCoord.open()


        elif order == "interactive":
            self.cubeViewer.get_data_from_sub_viz(order, self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData)
            if self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX != -1:
                self.cubeViewer.draw_wedges(self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX, self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerY, self.cubeList[self.subband].cubePatchesData.wedgesBackground.innerRadius, self.cubeList[self.subband].cubePatchesData.wedgesBackground.outerRadius)
            if self.cubeList[self.subband].centroidCoordinates.xCoordinate != -1:
                self.cubeViewer.draw_centroid(self.cubeList[self.subband].centroidCoordinates.xCoordinate, self.cubeList[self.subband].centroidCoordinates.yCoordinate)
            self.update_image_stats()
            self.cubeViewer.show()
            self.cubeViewer.open()

    def manageStyleOrders(self):
        self.styleManager.show()
        self.styleManager.open()

    def spectrumVisOrders(self):
        self.spectrumV.show()
        self.spectrumV.open()

    def drawPatchOrders(self, typePatch):
        """
        If the figure that is gonna be drawn is not the same as the active one
        change the representation inside the cubeViewer dialog
        """
        if typePatch == "rectangle" and self.cubeCurrState.active == "ellipse" and not self.cubeViewer.isHidden():
            self.cubeViewer.change_figure_from_sub_viz("rectangleAp")


        elif typePatch == "ellipse" and self.cubeCurrState.active == "rectangle" and not self.cubeViewer.isHidden():
            self.cubeViewer.change_figure_from_sub_viz("ellipseAp")

        for index in self.cubeList.keys():
            self.draw_patches(typePatch, index=index)

    @pyqtSlot(str, dict, name="cubeModified")
    @pyqtSlot(str, dict, dict, name="cubeModified")
    def update_cube_data_interaction(self, order, axesData, patchesData= None):
        """
        Update cube selected to be modified with the interactive tools (pan, zoom or rectangle creation) or
        all cubes if the interactive tools are the rectangle or ellipse aperture
        :param str order: type of modification id
        :param dict axesData: xlim and ylim new values to be applied to the cube selected
        :param dict patchesData: coordinates of the patch if drawn previously
        """
        if order == "rectangleAp":

            #Check if the patch had been drawn before to not make the transformations again
            if patchesData is None:
                self.draw_patches("rectangle", index = self.subband)
            else:
                #self.draw_patches("rectangle", patchesData, self.subband)
                self.select_area_rectangle(patchesData)

        elif order == "ellipseAp":
            #Check if the patch had been drawn before to not make the transformations again
            if patchesData is None:
                self.draw_patches("ellipse", index = self.subband)
            else:
                #self.draw_patches("ellipse", patchesData, self.subband)
                self.select_area_ellipse(patchesData)

        self.cubeList[self.subband].axis[0].set_xlim(axesData['xlim'])
        self.cubeList[self.subband].axis[0].set_ylim(axesData['ylim'])
        self.cubeList[self.subband].axis[1].set_ylim(axesData['twin_ylim'])
        self.cubeList[self.subband].axis[2].set_xlim(axesData['twin_xlim'])

        self.canvas.draw()

    @pyqtSlot(int, name="obtainCube")
    def send_wavelength_data(self, indexCube):
        """
        Send the data of the cube selected by index from the sliceManager
        :param int indexCube: index of the cube
        """
        if self.cubeList[indexCube].cubeModel:
            self.sliceManager.change_state_widgets(True)
            self.sliceManager.set_widgets_values(self.cubeList[indexCube])
        else:
            self.missing_data_warning()
            self.sliceManager.change_state_widgets(False)
            self.sliceManager.reset_widgets()

    @pyqtSlot(int, int, name="cubeChanged")
    def update_cube_slice(self, currSlice, indexCube):
        """
        Set the specific image at the slice to the  subband and update the patches on it
        :param int currSlice: slice of the cube to be accessed
        :param int indexCube: index of the cube to be accessed
        """
        self.cubeList[indexCube].currSlice = currSlice
        self.draw_cube(indexCube)
        #Draw the wedges because the image has changed
        self.draw_patches("all", index = indexCube)
        self.cubeViewer.redraw_slice(self.cubeList[indexCube])

    @pyqtSlot(str, int, name="colorChanged")
    def colorOrders(self, color_text, index):
        try:

            if index == 13:
                tupleData = [(ax, cube) for cube in self.cubeList.values() for ax in cube.axis if ax.get_gid().startswith("main_axis") and ax.has_data()]

                for data in tupleData:
                    cmap = None

                    if color_text == "Accent":
                        [image.set_cmap(plt.get_cmap("Accent")) for image in data[0].get_images()]
                        data[1].style.color = "Accent"
                        cmap = plt.get_cmap("Accent")

                    elif color_text == "Heat":
                        [image.set_cmap(plt.get_cmap("gist_heat")) for image in data[0].get_images()]
                        data[1].style.color = "gist_heat"
                        cmap = plt.get_cmap("gist_heat")

                    else:
                        [image.set_cmap(plt.get_cmap(color_text.lower())) for image in data[0].get_images()]
                        data[1].style.color = color_text.lower()
                        cmap = plt.get_cmap(color_text.lower())

            else:

                gidText = "main_axis"+str(index)
                ax = [ax for ax in self.cubeList[index].axis if ax.get_gid() == gidText][0]

                cmap = None

                if color_text == "Accent":
                    [image.set_cmap(plt.get_cmap("Accent")) for image in ax.get_images()]
                    self.cubeList[index].style.color = "Accent"
                    cmap = plt.get_cmap("Accent")

                elif color_text == "Heat":
                    [image.set_cmap(plt.get_cmap("gist_heat")) for image in ax.get_images()]
                    self.cubeList[index].style.color = "gist_heat"
                    cmap = plt.get_cmap("gist_heat")

                else:
                    [image.set_cmap(plt.get_cmap(color_text.lower())) for image in ax.get_images()]
                    self.cubeList[index].style.color = color_text.lower()
                    cmap = plt.get_cmap(color_text.lower())

            self.canvas.draw()
        except Exception as e:
            pass

    @pyqtSlot(str, int, name="stretchChanged")
    def stretchOrders(self, stretch_text, index):
        try:
            if index == 13:
                tupleData = [(ax, cube) for cube in self.cubeList.values() for ax in cube.axis if ax.get_gid().startswith("main_axis") and ax.has_data()]

                for data in tupleData:
                    index = [key for key,value in self.cubeList.items() if  data[0] in value.axis][0]

                    image = data[0].get_images()[0]
                    data[1].style.stretch = stretch_text

                    norm = self.get_norm(stretch_text, data[1].style.scale, index)
                    image.set_norm(norm)
            else:
                gidText = "main_axis"+str(index)
                ax = [ax for ax in self.cubeList[index].axis if ax.get_gid() == gidText][0]

                image = ax.get_images()[0]
                self.cubeList[index].style.stretch = stretch_text

                norm = self.get_norm(stretch_text, self.cubeList[index].style.scale, index)
                image.set_norm(norm)

            self.canvas.draw()
        except Exception as e:
            self.missing_data_warning()

    @pyqtSlot(str, int, name="scaleChanged")
    def scaleOrders(self, scale_text, index):
        try:
            if index == 13:
                tupleData = [(ax, cube) for cube in self.cubeList.values() for ax in cube.axis if ax.get_gid().startswith("main_axis") and ax.has_data()]
                for data in tupleData:

                    index = [key for key,value in self.cubeList.items() if  data[0] in value.axis][0]
                    image = data[0].get_images()[0]
                    data[1].style.scale = scale_text

                    norm = self.get_norm(data[1].style.stretch, scale_text, index)
                    image.set_norm(norm)

            else:

                gidText = "main_axis"+str(index)
                ax = [ax for ax in self.cubeList[index].axis if ax.get_gid() == gidText][0]
                image = ax.get_images()[0]
                self.cubeList[index].style.scale = scale_text

                norm = self.get_norm(self.cubeList[index].style.stretch, scale_text, index)
                image.set_norm(norm)

            self.canvas.draw()
        except Exception as e:
            pass

    def get_norm(self, stretch_text, scale_text, index):
        gidText = "main_axis"+str(index)
        ax = [ax for ax in self.cubeList[index].axis if ax.get_gid() == gidText][0]

        scale = None
        stretch = None

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

        #print(self.cubeList[index].cubeModel.data)
        minV, maxV = scale.get_limits(self.cubeList[index].cubeModel.data[self.cubeList[index].currSlice])

        norm = ImageNormalize(vmin=minV, vmax=maxV, stretch=stretch)

        return norm


    def update_image_stats(self):
        self.cubeViewer.modify_image("color", plt.get_cmap(self.cubeList[self.subband].style.color))

        norm = self.get_norm(self.cubeList[self.subband].style.stretch, self.cubeList[self.subband].style.scale, self.subband)
        #Although it modify the scale, because I got the norm from the stretch and scale,
        #it works the same as if the text would be the stretch which update the norm
        self.cubeViewer.modify_image("scale", norm)

    @pyqtSlot(int, str, str, name="subbandSelected")
    def obtain_subband(self, subband, order, additionalOrder):
        """
        Send info on what subband the interactive operation (like zoom or ellipse aperture)
        needs to be applied
        :param int subband: subband selected
        """
        self.subband = subband
        self.cubeSelection.close()
        if self.cubeList[self.subband].cubeModel:
            self.manageOrders(order, self.cubeList[self.subband], additionalOrder)
        else:
            self.missing_data_warning()

    def select_area_rectangle(self, patchesData, typeOp = 0):
        """.-Draw the spectrum based on the coordinates of the rectangle
        .-Draw the wedges based on the center of the figure
        .-Set the data for the figure to be drawn in the funcExtra dialog
        .-Update the data the background operation will use
        :param dict patchesData: rectangle data associated that will be drawed
        :param int typeOp: integer value that set if the coordinates are in pixels or
        in RA and DEC
        """
        try:

            for key in self.cubeList.keys():
                currIndex = key
                if self.cubeList[key].cubeModel is not None:
                    patchDataTrans = None
                    if key is not self.subband:
                        patchDataTrans = transform_rectangle_subband(self.cubeList[self.subband].cubeModel, self.cubeList[key].cubeModel, copy.deepcopy(patchesData), self.cubeList[key].currSlice)
                        self.draw_patches("rectangle", patchDataTrans, key)

                    else:
                        currIndex = self.subband
                        patchDataTrans = copy.deepcopy(patchesData)
                        self.draw_patches("rectangle", patchDataTrans, self.subband)


                    fValues, wValues, aperture = transform_xy_rectangle(centerX=patchDataTrans['centerX'], centerY= patchDataTrans['centerY'], width = patchDataTrans['ex'] - patchDataTrans['ix'], height= patchDataTrans['ey'] - patchDataTrans['iy'], cubeModel = self.cubeList[currIndex].cubeModel)
                    self.cubeList[currIndex].wavelengthRange = wValues
                    self.cubeList[currIndex].fluxAperture = fValues
                    self.cubeList[currIndex].aperture = aperture


                    #Draw the spectrum
                    self.spectrumV.draw_spectrum(self.cubeList[currIndex].path, fValues, wValues, color = COLORDICT[currIndex][1], label = COLORDICT[currIndex][0])
            #self.spectrumV.reset_range_axis()

            #Set the parameters the background operation will use
            if not self.actionBackground_subtraction.isEnabled():
                self.actionBackground_subtraction.setEnabled(True)

            if not self.actionRectangle_coordinates.isEnabled():
                self.actionRectangle_coordinates.setEnabled(True)

            #Set the center of the background operations
            centerX, centerY = self.get_background_center(self.subband)
            self.backgSub.update_center_data(centerX, centerY)

            #Checks if background have been made before to make the operation when the aperture change
            backgroundMade = any([cube.cubePatchesData.wedgesBackground.centerX != -1 for cube in self.cubeList.values()])

            #If background had been made before, do it
            if backgroundMade:
                #Check if there are no wedges:
                #If True, there are wedges and there is no need to update the position if the wedges
                #If False, there are no wedges and they need to be redrawn
                wedgesExist= any([isinstance(patch, Wedge) for patch in self.cubeList[self.subband].axis[0].patches])
                #Set updateWedgescenter to False to prevent the wedges to update their position
                if wedgesExist:
                    self.backgSub.apply_background_subs(False)
                else:
                    self.backgSub.apply_background_subs()


            if not self.cubeViewer.isHidden():
                self.cubeViewer.redraw_slice(self.cubeList[self.subband])

        except Exception as e:
            self.generic_alert()
            return 1
        else:
            if self.spectrumV.isHidden():
                self.spectrumV.show()
                self.spectrumV.open()

    def select_area_ellipse(self, patchesData, typeOp = 0):
        """.-Draw the spectrum based on the coordinates of the ellipse
        .-Draw the wedges based on the center of the figure
        .-Set the data for the figure to be drawn in the funcExtra dialog
        .-Update the data that the background operation will use
        :param dict patchesData: ellipse data associated that will be drawed
        :param int typeOp: integer value that set if the coordinates are in pixels or
        in RA and DEC
        """
        try:

            fValuesFinal = []
            wValuesFinal = []

            for key in self.cubeList.keys():
                currIndex = key
                if self.cubeList[key].cubeModel is not None:
                    patchDataTrans = None
                    if key is not self.subband:
                        patchDataTrans = transform_ellipse_subband(self.cubeList[self.subband].cubeModel, self.cubeList[key].cubeModel, copy.deepcopy(patchesData), self.cubeList[self.subband].currSlice)
                        self.draw_patches("ellipse", patchDataTrans, key)
                    else:
                        currIndex = self.subband
                        patchDataTrans = copy.deepcopy(patchesData)
                        self.draw_patches("ellipse", patchDataTrans, self.subband)

                    fValues, wValues, aperture = transform_xy_ellipse(centerX=patchDataTrans['centerX'], centerY= patchDataTrans['centerY'], aAxis = patchDataTrans['aAxis'], bAxis= patchDataTrans['bAxis'], cubeModel = self.cubeList[currIndex].cubeModel)
                    self.cubeList[currIndex].wavelengthRange = wValues
                    self.cubeList[currIndex].fluxAperture = fValues
                    self.cubeList[currIndex].aperture = aperture
                    #Draw the spectrum
                    self.spectrumV.draw_spectrum(self.cubeList[currIndex].path, fValues, wValues, color = COLORDICT[currIndex][1], label = COLORDICT[currIndex][0])
            #self.spectrumV.reset_range_axis()

            #Set the parameters the background operation will use
            if not self.actionBackground_subtraction.isEnabled():
                self.actionBackground_subtraction.setEnabled(True)

            if not self.actionEllipse_coordinates.isEnabled():
                self.actionEllipse_coordinates.setEnabled(True)

            #Set the center of the background operations
            centerX, centerY = self.get_background_center(self.subband)
            self.backgSub.update_center_data(centerX, centerY)

            #Because the background operation can be made previous to replace a cube, when an aperture
            #is done, it checks if it had been made before to make it
            backgroundMade = any([cube.cubePatchesData.wedgesBackground.centerX != -1 for cube in self.cubeList.values()])

            #If background had been made before, do it
            if backgroundMade:
                #Check if there are no wedges:
                #If True, there are wedges and there is no need to update the position if the wedges
                #If False, there are no wedges and they need to be redrawn
                wedgesExist= any([isinstance(patch, Wedge) for patch in self.cubeList[self.subband].axis[0].patches])
                #Set updateWedgescenter to False to prevent the wedges to update their position
                if wedgesExist:
                    self.backgSub.apply_background_subs(False)
                else:
                    self.backgSub.apply_background_subs()

        except Exception as e:
            self.generic_alert()
            return 1
        else:
            if self.spectrumV.isHidden():
                self.spectrumV.show()
                self.spectrumV.open()

    @pyqtSlot(object, str, name="rectangleEmit")
    @pyqtSlot(object, str, bool, name="wedgesEmit")
    def calculate_background(self, data, typePatch, updateWedgesCenter = None):
        """
        Calculate the background spectrum and the remaining of the subtraction from the aperture
        :param dict data: parameters of the figure
        :param str typePatch: info about the type of the figure
        :param bool updateWedgesCenter: signal to change the center of the wedges
        """
        dataTrans = copy.deepcopy(data)

        if typePatch == 'wedges':
            #To prevent the appearance of multiple wedges and rectangles on all the
            #images when a background operation is gonna be made, the opposite patch
            #is deleted instead of the one which is gonna be drawn
            self.cubeList[self.subband].cubePatchesData.reset_rectangleBackg()
            self.draw_patches("wedgesBackg", dataTrans, self.subband)

            fValues_sub, bkg_sum = annulus_background_subtraction(dataTrans['centerX'], dataTrans['centerY'], dataTrans['innerRadius'], dataTrans['outerRadius'], self.cubeList[self.subband].aperture, self.cubeList[self.subband].cubeModel, self.cubeList[self.subband].fluxAperture)
            self.spectrumV.draw_background(self.cubeList[self.subband].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[self.subband][0])

        elif typePatch == 'rectangle':
            #To prevent the appearance of multiple wedges and rectangles on all the
            #images when a background operation is gonna be made, the opposite patch
            #is deleted instead of the one which is gonna be drawn
            self.cubeList[self.subband].cubePatchesData.reset_wedgesBackg()
            dataTrans = rectangle_patch_to_border_coordinates(dataTrans)
            self.draw_patches("rectangleBackg", dataTrans, self.subband)
            fValues_sub, bkg_sum = rectangle_background_subtraction(dataTrans['centerX'], dataTrans['centerY'], abs(dataTrans['ex'] - dataTrans['ix']), abs(dataTrans['ey'] - dataTrans['iy']), self.cubeList[self.subband].aperture, self.cubeList[self.subband].cubeModel, self.cubeList[self.subband].fluxAperture)

            self.spectrumV.draw_background(self.cubeList[self.subband].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[self.subband][0])

        for key in self.cubeList.keys():

            #To prevent the appearance of multiple wedges and rectangles on all the
            #images when a background operation is gonna be made, the opposite patch
            #is deleted instead of the one which is gonna be drawn
            if typePatch == 'wedges':
                self.cubeList[self.subband].cubePatchesData.reset_rectangleBackg()
            elif typePatch == 'rectangle':
                self.cubeList[self.subband].cubePatchesData.reset_wedgesBackg()

            if self.cubeList[key].cubeModel is not None:
                dataTrans = None

                if key is not self.subband:
                    if typePatch == 'wedges':

                        dataTrans = transform_wedges_subband(self.cubeList[self.subband].cubeModel, self.cubeList[key].cubeModel, copy.deepcopy(data), self.cubeList[self.subband].currSlice)
                        self.draw_patches("wedgesBackg", dataTrans, key)
                        fValues_sub, bkg_sum = annulus_background_subtraction(dataTrans['centerX'], dataTrans['centerY'], dataTrans['innerRadius'], dataTrans['outerRadius'], self.cubeList[key].aperture, self.cubeList[key].cubeModel, self.cubeList[key].fluxAperture)
                        self.spectrumV.draw_background(self.cubeList[key].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[key][0])
                    elif typePatch == 'rectangle':

                        dataTrans = transform_rectangle_subband(self.cubeList[self.subband].cubeModel, self.cubeList[key].cubeModel, copy.deepcopy(data), self.cubeList[self.subband].currSlice)
                        self.draw_patches("rectangleBackg", dataTrans, key)
                        fValues_sub, bkg_sum = rectangle_background_subtraction(dataTrans['centerX'], dataTrans['centerY'], abs(dataTrans['ex'] - dataTrans['ix']), abs(dataTrans['ey'] - dataTrans['iy']), self.cubeList[key].aperture, self.cubeList[key].cubeModel, self.cubeList[key].fluxAperture)
                        self.spectrumV.draw_background(self.cubeList[key].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[key][0])

                    #If only the aperture is moving, dont update the center of the wedges
                    #Otherwise, do it
                    #if updateWedgesCenter:
                    #    self.draw_patches("wedges", wedgesDataTrans, key)


        if not self.cubeViewer.isHidden():
            if typePatch == 'wedges':
                self.cubeViewer.get_data_from_sub_viz("wedgesBackg", self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.wedgesBackground)
            elif typePatch == 'rectangle':
                self.cubeViewer.get_data_from_sub_viz("rectangleBackg", self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.rectangleBackground)

        if self.spectrumV.isHidden():
            self.spectrumV.show()
            self.spectrumV.open()

    def set_centroid(self, centroidData):
        """
        Calculate and draw the centroid for each cube
        :param dict centroidData: x and y coordinates of the center
        """
        centroidDataTrans = copy.deepcopy(centroidData)
        self.draw_patches("centroid", centroidDataTrans, self.subband)

        for key in self.cubeList.keys():
            if self.cubeList[key].cubeModel is not None:
                centroidDataTrans = None

                if key is not self.subband:
                    centroidDataTrans = transform_centroid_subband(self.cubeList[self.subband].cubeModel, self.cubeList[key].cubeModel, copy.deepcopy(centroidData), self.cubeList[self.subband].currSlice)

                    self.draw_patches("centroid", centroidDataTrans, key)


        self.cubeViewer.get_data_from_sub_viz("centroidCoord", self.cubeList[self.subband], self.cubeList[self.subband].centroidCoordinates)

    @pyqtSlot(dict, int, name="rectangleCreation")
    def create_rectangle_figure_coord(self, patchesData, typeOp):
        """
        Generate the rectangle based on the coordinates written previously
        :param dict patchesData: dictionary of the coordinates of the rectangle
        :param int typeOp: signal that set the type of coordinates
        """
        error = self.select_area_rectangle(patchesData, typeOp)
        if error is None:
            self.cubeViewer.get_data_from_sub_viz("rectangleAp", self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.rectangleSelection)
            if self.cubeViewer.isHidden():

                self.cubeViewer.show()
                self.cubeViewer.open()

    @pyqtSlot(dict, int, name="ellipseCreation")
    def create_ellipse_figure_coord(self, patchesData, typeOp):
        """
        Generate the ellipse based on the coordinates written previously
        :param dict patchesData: dictionary of the coordinates of the ellipse
        :param int typeOp: signal that set the type of coordinates
        """
        self.select_area_ellipse(patchesData, typeOp)
        self.cubeViewer.get_data_from_sub_viz("ellipseAp", self.cubeList[self.subband], self.cubeList[self.subband].cubePatchesData.ellipseSelection)
        if self.cubeViewer.isHidden():
            self.cubeViewer.show()
            self.cubeViewer.open()

    def get_background_center(self, index):
        """
        Return the center of the figure when background operaiton is made
        :param int index: index of the cube to obtain the center
        :return: the coordinates of the center
        """
        centerX = 0
        centerY = 0
        if self.cubeCurrState.active == 'rectangle':
            centerX = (self.cubeList[index].cubePatchesData.rectangleSelection.ex + self.cubeList[index].cubePatchesData.rectangleSelection.ix)/2.
            centerY = (self.cubeList[index].cubePatchesData.rectangleSelection.ey + self.cubeList[index].cubePatchesData.rectangleSelection.iy)/2.
        elif self.cubeCurrState.active == 'ellipse':
            centerX = self.cubeList[index].cubePatchesData.ellipseSelection.centerX
            centerY = self.cubeList[index].cubePatchesData.ellipseSelection.centerY

        return centerX, centerY

    def create_centroid(self, patchesData, additionalOrder=None):
        """
        Calculate the centroid and make the aperture if needed
        with the centroid as the center of the aperture or as
        another element
        :param dict patchesData: centroid coordinates
        :param str additionalOrder: string that contains the type of aperture to be made
        """
        if additionalOrder == 'rectangleAndCenter':
            self.rectCreate.show()
            self.rectCreate.open()
        elif additionalOrder == 'rectangleWithCenter':
            self.rectCreate.set_center_coordinates(patchesData['xCoordinate'], patchesData['yCoordinate'])
            self.rectCreate.show()
            self.rectCreate.open()
        elif additionalOrder == 'ellipseAndCenter':
            self.ellCreate.show()
            self.ellCreate.open()
        elif additionalOrder == 'ellipseWithCenter':
            self.ellCreate.set_center_coordinates(patchesData['xCoordinate'], patchesData['yCoordinate'])
            self.ellCreate.show()
            self.ellCreate.open()

        self.set_centroid(patchesData)
        self.centCoord.set_coordinates(patchesData['xCoordinate'], patchesData['yCoordinate'])
        self.cubeViewer.draw_centroid(self.cubeList[self.subband].centroidCoordinates.xCoordinate, self.cubeList[self.subband].centroidCoordinates.yCoordinate)
        self.centCoord.show()
        self.centCoord.open()


    @pyqtSlot(int)
    def get_cube(self, int):
        try:
            if int == QDialog.Accepted:
                #path, subbandIndex = self.cubeLoader.get_data()
                path, subband= self.cubeLoader.get_data()
                self.cubeLoader.reset_widget()
                #If the path obtained is a list of files,
                #load a directory instead of a single file
                if type(path) is list:
                    self.load_directory(path)
                else:
                    self.load_file(path, subband)
            self.canvas.draw()
        except Exception as e:
            self.show_file_alert()

    def create_axes(self):
        """Create the layout that will show the slice selected of a cube"""
        self.cubeFigure = Figure()
        self.cubeFigure.constrained_layout = True
        self.canvas = FigureCanvas(self.cubeFigure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.spec = gridspec.GridSpec(ncols=4, nrows=3, figure=self.cubeFigure, wspace = 0.6, hspace = 0.6)
        self.save_axis_on_index(0)
        self.save_axis_on_index(1)
        self.save_axis_on_index(2)
        self.save_axis_on_index(3)
        self.save_axis_on_index(4)
        self.save_axis_on_index(5)
        self.save_axis_on_index(6)
        self.save_axis_on_index(7)
        self.save_axis_on_index(8)
        self.save_axis_on_index(9)
        self.save_axis_on_index(10)
        self.save_axis_on_index(11)
        self.spaceCubePlot.setLayout(layout)

    def save_axis_on_index(self, index):
        main_gid = "main_axis"+str(index)
        twinx_gid = "twinx_axis"+str(index)
        twiny_gid = "twiny_axis"+str(index)

        ax = self.cubeFigure.add_subplot(self.spec[self.cubeList[index].position[0],self.cubeList[index].position[1]])
        ax.set_visible(False)
        ax.set_gid(main_gid)

        ax_twinx = ax.twinx()
        ax_twiny = ax.twiny()

        ax_twinx.set_visible(False)
        ax_twiny.set_visible(False)

        ax_twinx.set_gid(twinx_gid)
        ax_twiny.set_gid(twiny_gid)

        #Set self.ax to the front to be able to use the figures on it
        ax.set_zorder(ax_twiny.get_zorder() + 1)

        self.cubeList[index].add_axis(ax)
        self.cubeList[index].add_axis(ax_twinx)
        self.cubeList[index].add_axis(ax_twiny)

    def draw_cube(self, index):

        self.cubeList[index].axis[0].images.clear()

        self.cubeList[index].axis[0].set_visible(True)
        self.cubeList[index].axis[0].grid(False)

        self.cubeList[index].axis[1].set_visible(True)
        self.cubeList[index].axis[2].set_visible(True)

        self.cubeList[index].axis[0].set_title(SUBBANDDICT[index], fontsize = 10)

        im = self.cubeList[index].axis[0].imshow(self.cubeList[index].cubeModel.data[self.cubeList[index].currSlice],origin='lower', aspect='auto')

        im.set_cmap(plt.get_cmap((self.cubeList[index].style.color)))
        norm = self.get_norm(self.cubeList[index].style.stretch, self.cubeList[index].style.scale, index)
        im.set_norm(norm)

        self.cubeList[index].axis[2].set_xlim((self.cubeList[index].axis[0].get_xlim()[0]- self.cubeList[index].cubeModel.meta.wcsinfo.crpix1)*self.cubeList[index].cubeModel.meta.wcsinfo.cdelt1*3600 + self.cubeList[index].cubeModel.meta.wcsinfo.crval1*3600, (self.cubeList[index].axis[0].get_xlim()[1]- self.cubeList[index].cubeModel.meta.wcsinfo.crpix1)*self.cubeList[index].cubeModel.meta.wcsinfo.cdelt1*3600 + self.cubeList[index].cubeModel.meta.wcsinfo.crval1*3600)

        self.cubeList[index].axis[1].set_ylim((self.cubeList[index].axis[0].get_ylim()[0]- self.cubeList[index].cubeModel.meta.wcsinfo.crpix2)*self.cubeList[index].cubeModel.meta.wcsinfo.cdelt2*3600 + self.cubeList[index].cubeModel.meta.wcsinfo.crval2*3600, (self.cubeList[index].axis[0].get_ylim()[1]- self.cubeList[index].cubeModel.meta.wcsinfo.crpix2)*self.cubeList[index].cubeModel.meta.wcsinfo.cdelt2*3600 + self.cubeList[index].cubeModel.meta.wcsinfo.crval2*3600)

        self.canvas.draw()

    def load_directory(self, pathList):
        cubeExist = any([cube.cubeModel is not None for cube in self.cubeList.values()])

        #If any cube had been drawn individually or from the directory option
        #it clears all the windows and data
        if cubeExist:
            [cube.set_default_data() for cube in self.cubeList.values()]
            [self.clear_axis(cube.axis) for cube in self.cubeList.values()]
            self.cubeViewer.clear_data()
            self.spectrumV.clear_data()

            self.rectCoord.clear_data()
            self.rectCreate.clear_data()

            self.ellCoord.clear_data()
            self.ellCreate.clear_data()

            self.backgSub.clear_data()

            self.styleManager.clear_data()

            self.sliceManager.clear_data()

            self.cubeSelection.clear_data()

            self.centCoord.clear_data()
            self.centWave.clear_data()

            self.disable_interface_state()

        error = 0
        for path in pathList:
            try:
                subband, cubeModel = get_miri_cube_subband(path)

                self.cubeList[INDEXDICT[subband]].path = path
                self.cubeList[INDEXDICT[subband]].cubeModel = copy.deepcopy(cubeModel)
                self.draw_cube(INDEXDICT[subband])
            except Exception as e:
                error += 1
                pass

        if error > 0:
            self.jwst_alert()

        #Check if it is the first cube loaded and set all data
        axisWithData = [ax.has_data() for cube in self.cubeList.values() for ax in cube.axis if ax.get_gid().startswith("main_axis")]
        if axisWithData.count(True) > 0:
            self.set_interface_state(True)


    def load_file(self, path, subband):
        cubeModel = None
        index = -1

        if subband is None:
            subband, cubeModel= get_miri_cube_data(path)
            index = INDEXDICT[subband]
        else:
            cubeModel= get_miri_cube_data(path, ignoreHeaderSubband = True)
            index = subband

        self.cubeList[index].path = path
        #Print the slice of the cube

        self.cubeList[index].path = path
        cubeExist = any([cube.aperture is not None for cube in self.cubeList.values()])
        centroidCalculated= any([cube.centroidCoordinates.xCoordinate != -1 for cube in self.cubeList.values()])

        #If any aperture had been made and a new cube is loaded, make it
        if self.cubeList[index].cubeModel is None and cubeExist:
            self.cubeList[index].cubeModel = copy.deepcopy(cubeModel)
            self.make_aperture_from_new_cube(index)
            backgroundCalculated= any([cube.cubePatchesData.wedgesBackground.centerX != -1 or cube.cubePatchesData.rectangleBackground.centerX != -1 for cube in self.cubeList.values()])

            if backgroundCalculated:
                self.make_background_from_new_cube(index)

            if centroidCalculated:
                self.make_centroid_from_new_cube(index)

        #If no aperture had been made and a new cube is loaded, just draw it
        elif self.cubeList[index].cubeModel is None and not cubeExist:

            self.cubeList[index].cubeModel = copy.deepcopy(cubeModel)

            #If no aperture had been made, a new cube is loaded and centroid had been made
            if centroidCalculated:
                self.make_centroid_from_new_cube(index)


        #If a new cube is gonna delete the previous one, only clean all figures
        #from previous cube
        else:
            self.cubeList[index].cubeModel = copy.deepcopy(cubeModel)
            self.spectrumV.delete_duplicated_cube(SUBBANDDICT[index])
            self.clear_figures_on_cube(index)
            self.sliceManager.reset_same_cube(index)


        self.draw_cube(index)
        if not self.cubeViewer.isHidden() and index == self.subband:
            self.cubeViewer.redraw_slice(self.cubeList[self.subband])

        #Check if it is the first cube loaded and set all data
        axisWithData = [ax.has_data() for cube in self.cubeList.values() for ax in cube.axis if ax.get_gid().startswith("main_axis")]

        if axisWithData.count(True) == 1:
            self.set_interface_state(True)

    @pyqtSlot(int, int, name="getRangeData")
    def send_range_data(self, iw, ew):
        """Get the flux values from the wavelength range of values to visualize it
        :param int iw: left x wavelength value
        :param int ew: right x wavelength value
        """
        self.waveSelect.draw_image(str(iw), str(ew),np.mean(self.cubeList[self.subband].cubeModel.data[iw:ew], axis=0))
        self.waveSelect.show()
        self.waveSelect.open()

    def draw_patches(self, typePatch, patchesData=None, index=None):
        """
        When the rectangle, ellipse or wedge are modified or created, instead of manage 36 patches
        (wedges, rectangles and ellipses) the patches are redrawn based on the option selected
        :param str typePatch: type of patch to be drawn in each subband
        :param dict patchesData: data and coordinates of the patch
        :param int index: position of the cube where the patch is gonna be drawn
        """
        if typePatch == "rectangle":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]
            self.delete_current_patch(ax, "RectangleAp")
            self.delete_current_patch(ax, "EllipseAp")

            if patchesData is not None:
                ax.add_patch(Rectangle((patchesData['ix'], patchesData['iy']),
                                                patchesData['ex'] - patchesData['ix'],
                                                patchesData['ey'] - patchesData['iy'],
                                                facecolor = 'none', edgecolor='red', lw=2, gid="RectangleAp" ))
                self.cubeList[index].cubePatchesData.rectangleSelection.ix = patchesData['ix']
                self.cubeList[index].cubePatchesData.rectangleSelection.iy = patchesData['iy']
                self.cubeList[index].cubePatchesData.rectangleSelection.ex = patchesData['ex']
                self.cubeList[index].cubePatchesData.rectangleSelection.ey = patchesData['ey']

            elif  patchesData is None:
                ax.add_patch(Rectangle((self.cubeList[index].cubePatchesData.rectangleSelection.ix, self.cubeList[index].cubePatchesData.rectangleSelection.iy),
                                                self.cubeList[index].cubePatchesData.rectangleSelection.ex - self.cubeList[index].cubePatchesData.rectangleSelection.ix,
                                                self.cubeList[index].cubePatchesData.rectangleSelection.ey - self.cubeList[index].cubePatchesData.rectangleSelection.iy, facecolor = 'none', edgecolor='red', lw=2, gid="RectangleAp" ))


            #If the wedge object have positive data, the wedges are gonna be drawn,
            #otherwise it could be that the rectangle is gonna be drawn
            if self.cubeList[index].cubePatchesData.wedgesBackground.centerX != -1:

                self.delete_current_patch(ax, "WedgeBackg")
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                          self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                  self.cubeList[index].cubePatchesData.wedgesBackground.innerRadius, 0, 360, width= 0.5))
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                        self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                   self.cubeList[index].cubePatchesData.wedgesBackground.outerRadius, 0, 360, width= 0.5))

            elif self.cubeList[index].cubePatchesData.rectangleBackground.centerX != -1:

                self.delete_current_patch(ax, "RectangleBackg")
                ax.add_patch(Rectangle((self.cubeList[index].cubePatchesData.rectangleBackground.centerX,
                                          self.cubeList[index].cubePatchesData.rectangleBackground.centerY),
                                        self.cubeList[index].cubePatchesData.rectangleBackground.width,
                                        self.cubeList[index].cubePatchesData.rectangleBackground.height,
                                       lw= 1.5, facecolor='none', edgecolor='white', gid ="RectangleBackg"))

            self.cubeCurrState.active = "rectangle"

            #set the rectangle button enabled when the rectangle had been created
            #for the first time
            if not self.actionDrawRectangle.isEnabled():
                self.actionDrawRectangle.setEnabled(True)

        elif typePatch == "ellipse":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]
            self.delete_current_patch(ax, "EllipseAp")
            self.delete_current_patch(ax, "RectangleAp")

            if patchesData is not None:
                ax.add_patch(Ellipse((patchesData['centerX'], patchesData['centerY']),
                                                    patchesData['aAxis'],
                                                    patchesData['bAxis'], facecolor = 'none', edgecolor='red', lw=2 ))
                self.cubeList[index].cubePatchesData.ellipseSelection.centerX = patchesData['centerX']
                self.cubeList[index].cubePatchesData.ellipseSelection.centerY = patchesData['centerY']
                self.cubeList[index].cubePatchesData.ellipseSelection.aAxis = patchesData['aAxis']
                self.cubeList[index].cubePatchesData.ellipseSelection.bAxis = patchesData['bAxis']

            elif  patchesData is None:
                ax.add_patch(Ellipse((self.cubeList[index].cubePatchesData.ellipseSelection.centerX, self.cubeList[index].cubePatchesData.ellipseSelection.centerY),
                                                self.cubeList[index].cubePatchesData.ellipseSelection.aAxis,
                                                self.cubeList[index].cubePatchesData.ellipseSelection.bAxis, facecolor='none', edgecolor='red', lw=2 ))

            #If the wedge object have positive data, the wedges are gonna be drawn,
            #otherwise it could be that the rectangle is gonna be drawn
            if self.cubeList[index].cubePatchesData.wedgesBackground.centerX != -1:
                self.delete_current_patch(ax, "WedgeBackg")
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                            self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                      self.cubeList[index].cubePatchesData.wedgesBackground.innerRadius, 0, 360, width= 0.5))
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                            self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                      self.cubeList[index].cubePatchesData.wedgesBackground.outerRadius, 0, 360, width= 0.5))

            elif self.cubeList[index].cubePatchesData.rectangleBackground.centerX != -1:

                self.delete_current_patch(ax, "RectangleBackg")
                ax.add_patch(Rectangle((self.cubeList[index].cubePatchesData.rectangleBackground.centerX,
                                          self.cubeList[index].cubePatchesData.rectangleBackground.centerY),
                                        self.cubeList[index].cubePatchesData.rectangleBackground.width,
                                        self.cubeList[index].cubePatchesData.rectangleBackground.height,
                                       lw= 1.5, facecolor='none', edgecolor='white', gid ="RectangleBackg"))


            self.cubeCurrState.active = "ellipse"

            #set the ellipse button enabled when the ellipse had been created
            #for the first time
            if not self.actionDrawEllipse.isEnabled():
                self.actionDrawEllipse.setEnabled(True)

        elif typePatch == "wedgesBackg":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]

            self.delete_current_patch(ax, "WedgeBackg")
            self.delete_current_patch(ax, "RectangleBackg")
            centerX, centerY = self.get_background_center(index)
            ax.add_patch(Wedge((centerX, centerY),
                                  patchesData['innerRadius'], 0, 360, width= 0.5))
            ax.add_patch(Wedge((centerX, centerY),
                                  patchesData['outerRadius'], 0, 360, width= 0.5))

            self.cubeList[index].cubePatchesData.wedgesBackground.centerX = centerX
            self.cubeList[index].cubePatchesData.wedgesBackground.centerY = centerY
            self.cubeList[index].cubePatchesData.wedgesBackground.innerRadius = patchesData['innerRadius']
            self.cubeList[index].cubePatchesData.wedgesBackground.outerRadius = patchesData['outerRadius']

        elif typePatch == "rectangleBackg":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]
            self.delete_current_patch(ax, "RectangleBackg")
            self.delete_current_patch(ax, "WedgeBackg")
            ax.add_patch(Rectangle((patchesData['centerX'],
                                    patchesData['centerY']),
                                    abs(patchesData['ex']-patchesData['ix']),
                                    abs(patchesData['ey']-patchesData['iy']),
                                   lw= 1.5,facecolor = 'none', edgecolor='white',  gid ="RectangleBackg"))

            self.cubeList[index].cubePatchesData.rectangleBackground.centerX = patchesData['centerX']
            self.cubeList[index].cubePatchesData.rectangleBackground.centerY = patchesData['centerY']
            self.cubeList[index].cubePatchesData.rectangleBackground.width = abs(patchesData['ex']-patchesData['ix'])
            self.cubeList[index].cubePatchesData.rectangleBackground.height = abs(patchesData['ey']-patchesData['iy'])
            self.cubeList[index].cubePatchesData.rectangleBackground.ix = patchesData['ix']
            self.cubeList[index].cubePatchesData.rectangleBackground.iy = patchesData['iy']
            self.cubeList[index].cubePatchesData.rectangleBackground.ex = patchesData['ex']
            self.cubeList[index].cubePatchesData.rectangleBackground.ey = patchesData['ey']



        elif typePatch == "centroid":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]

            self.delete_current_patch(ax, "Centroid")
            ax.scatter(patchesData['xCoordinate'], patchesData['yCoordinate'], marker='+', c= 'red')

            self.cubeList[index].centroidCoordinates.xCoordinate = patchesData['xCoordinate']
            self.cubeList[index].centroidCoordinates.yCoordinate = patchesData['yCoordinate']

        elif typePatch == "all":
            ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]
            ax.patches.clear()
            self.delete_current_patch(ax, "Centroid")

            if self.cubeCurrState.active == "rectangle":
                ax.add_patch(Rectangle((self.cubeList[index].cubePatchesData.rectangleSelection.ix, self.cubeList[index].cubePatchesData.rectangleSelection.iy),
                                                self.cubeList[index].cubePatchesData.rectangleSelection.ex - self.cubeList[index].cubePatchesData.rectangleSelection.ix,
                                                self.cubeList[index].cubePatchesData.rectangleSelection.ey - self.cubeList[index].cubePatchesData.rectangleSelection.iy, edgecolor = 'red', facecolor='none', lw=2, gid="RectangleAp" ))

            elif self.cubeCurrState.active == "ellipse":
                ax.add_patch(Ellipse((self.cubeList[index].cubePatchesData.ellipseSelection.centerX, self.cubeList[index].cubePatchesData.ellipseSelection.centerY),
                                                self.cubeList[index].cubePatchesData.ellipseSelection.aAxis,
                                                self.cubeList[index].cubePatchesData.ellipseSelection.bAxis, edgecolor = 'red', facecolor='none', lw=2 ))

            if self.cubeList[index].cubePatchesData.wedgesBackground.centerX != -1:
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                        self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                  self.cubeList[index].cubePatchesData.wedgesBackground.innerRadius, 0, 360, width= 0.5))
                ax.add_patch(Wedge((self.cubeList[index].cubePatchesData.wedgesBackground.centerX,
                                        self.cubeList[index].cubePatchesData.wedgesBackground.centerY),
                                  self.cubeList[index].cubePatchesData.wedgesBackground.outerRadius, 0, 360, width= 0.5))

            elif self.cubeList[index].cubePatchesData.rectangleBackground.centerX != -1:

                ax.add_patch(Rectangle((self.cubeList[index].cubePatchesData.rectangleBackground.centerX,
                                          self.cubeList[index].cubePatchesData.rectangleBackground.centerY),
                                        self.cubeList[index].cubePatchesData.rectangleBackground.width,
                                        self.cubeList[index].cubePatchesData.rectangleBackground.height,
                                       lw= 1.5, facecolor='none', edgecolor='white', gid ="RectangleBackg"))


            if self.cubeList[index].centroidCoordinates.xCoordinate != -1:

                ax.scatter(self.cubeList[index].centroidCoordinates.xCoordinate, self.cubeList[index].centroidCoordinates.yCoordinate, marker='+', c= 'red')

        self.canvas.draw()

    def delete_current_patch(self, ax, typePatch):
        """
        Delete the patch or collection selected
        :param axis ax: axis to eliminate the element
        :param str typePatch: type of patch or collection to be removed
        """
        if typePatch == "Centroid":
            collectionReference = {"Centroid": PathCollection}
            [ax.collections.remove(marker) for marker in reversed(ax.collections) if isinstance(marker, collectionReference[typePatch])]

        elif typePatch == 'RectangleAp':
            patchReference = {"RectangleAp": Rectangle}
            [ax.patches.remove(patch) for patch in reversed(ax.patches) if isinstance(patch, patchReference[typePatch]) and patch.get_gid() == typePatch]

        elif typePatch == 'RectangleBackg':
            patchReference = {"RectangleBackg": Rectangle}
            [ax.patches.remove(patch) for patch in reversed(ax.patches) if isinstance(patch, patchReference[typePatch]) and patch.get_gid() == typePatch]

        else:
            patchReference = {"EllipseAp": Ellipse, "WedgeBackg": Wedge}
            [ax.patches.remove(patch) for patch in reversed(ax.patches) if isinstance(patch, patchReference[typePatch])]

    def make_aperture_from_new_cube(self, index):
        """
        Calculate the aperture spectrum on a new cube
        :param int index: position of the cube where the aperture is gonna be calculated
        """
        wavelength_value = slice_to_wavelength(self.cubeList[self.subband].currSlice, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crpix3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.cdelt3, self.cubeList[self.subband].cubeModel.meta.wcsinfo.crval3)

        wValues = None
        fValues = None
        aperture = None

        if self.cubeCurrState.active == 'rectangle':
            patchesData = self.cubeList[self.subband].cubePatchesData.rectangleSelection.asdict()

            patchDataTrans = transform_rectangle_subband(self.cubeList[self.subband].cubeModel, self.cubeList[index].cubeModel, copy.deepcopy(patchesData), self.cubeList[index].currSlice)
            self.draw_patches("rectangle", patchDataTrans, index)

            fValues, wValues, aperture = transform_xy_rectangle(centerX=patchDataTrans['centerX'], centerY= patchDataTrans['centerY'], width = patchDataTrans['ex'] - patchDataTrans['ix'], height= patchDataTrans['ey'] - patchDataTrans['iy'], cubeModel = self.cubeList[index].cubeModel)

        elif self.cubeCurrState.active == 'ellipse':
            patchesData = self.cubeList[self.subband].cubePatchesData.ellipseSelection.asdict()

            patchDataTrans = transform_ellipse_subband(self.cubeList[self.subband].cubeModel, self.cubeList[index].cubeModel, copy.deepcopy(patchesData), self.cubeList[index].currSlice)
            self.draw_patches("ellipse", patchDataTrans, index)

            fValues, wValues, aperture = transform_xy_ellipse(centerX=patchDataTrans['centerX'], centerY= patchDataTrans['centerY'], aAxis = patchDataTrans['aAxis'], bAxis= patchDataTrans['bAxis'], cubeModel = self.cubeList[currIndex].cubeModel)

        self.cubeList[index].wavelengthRange = wValues
        self.cubeList[index].fluxAperture = fValues
        self.cubeList[index].aperture = aperture

        #Draw the spectrum
        self.spectrumV.draw_spectrum(self.cubeList[index].path, fValues, wValues, color = COLORDICT[index][1], label = COLORDICT[index][0])


    def make_background_from_new_cube(self, index):
        """
        Calculate the background spectrum and the remaining of the subtraction from the aperture
        on a new cube
        :param int index: position of the cube where the background is gonna be calculated
        """

        if self.cubeList[self.subband].cubePatchesData.wedgesBackground.centerX != -1:

            wedgesData = self.cubeList[self.subband].cubePatchesData.wedgesBackground.asdict()

            wedgesDataTrans = transform_wedges_subband(self.cubeList[self.subband].cubeModel, self.cubeList[index].cubeModel, copy.deepcopy(wedgesData), self.cubeList[self.subband].currSlice)
            self.draw_patches("wedgesBackg", wedgesDataTrans, index)

            fValues_sub, bkg_sum = annulus_background_subtraction(wedgesDataTrans['centerX'], wedgesDataTrans['centerY'], wedgesDataTrans['innerRadius'], wedgesDataTrans['outerRadius'], self.cubeList[index].aperture, self.cubeList[index].cubeModel, self.cubeList[index].fluxAperture)

            self.spectrumV.draw_background(self.cubeList[index].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[index][0])

        elif self.cubeList[self.subband].cubePatchesData.rectangleBackground.centerX != -1:

            rectangleData = self.cubeList[self.subband].cubePatchesData.rectangleBackground.asdict()

            rectangleDataTrans = transform_rectangle_subband(self.cubeList[self.subband].cubeModel, self.cubeList[index].cubeModel, copy.deepcopy(rectangleData), self.cubeList[self.subband].currSlice)
            self.draw_patches("rectangleBackg", rectangleDataTrans, index)

            fValues_sub, bkg_sum = rectangle_background_subtraction(rectangleDataTrans['centerX'], rectangleDataTrans['centerY'],abs(rectangleDataTrans['ex'] - rectangleDataTrans['ix']), abs(rectangleDataTrans['ey'] - rectangleDataTrans['iy']), self.cubeList[index].aperture, self.cubeList[index].cubeModel, self.cubeList[index].fluxAperture)

            self.spectrumV.draw_background(self.cubeList[index].wavelengthRange, fValues_sub, bkg_sum, COLORDICT[index][0])


    def make_centroid_from_new_cube(self, index):
        """
        Calculate the centroid on a new cube
        :param int index: position of the cube where the centroid is gonna be calculated
        """

        centroidData = self.cubeList[self.subband].centroidCoordinates.asdict()

        centroidDataTrans = transform_centroid_subband(self.cubeList[self.subband].cubeModel, self.cubeList[index].cubeModel, copy.deepcopy(centroidData), self.cubeList[self.subband].currSlice)

        self.draw_patches("centroid", centroidDataTrans, index)

        self.cubeViewer.get_data_from_sub_viz("centroidCoord", self.cubeList[self.subband], self.cubeList[self.subband].centroidCoordinates)

    def clear_figures_on_cube(self, index):
        ax = [ax for ax in self.cubeList[index].axis if ax.get_gid().startswith("main_axis")][0]
        self.delete_current_patch(ax, "RectangleAp")
        self.delete_current_patch(ax, "EllipseAp")
        self.delete_current_patch(ax, "WedgeBackg")
        self.delete_current_patch(ax, "RectangleBackg")
        self.delete_current_patch(ax, "Centroid")

        self.cubeList[index].cubePatchesData.reset_coordinates()
        self.cubeViewer.clear_data()

    def clear_axis(self, axis):
        for ax in axis:
            ax.clear()
            ax.set_visible(False)

    def save_figure(self):
        """ Save the figure as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')
            self.cubeFigure.savefig(name[0], dpi = 600, bbox_inches="tight")

        except Exception as e:
            self.show_file_extension_alert()

    def set_interface_state(self, state):
        """ Disable or enable the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.menuTools.setEnabled(state)
        self.actionSavespng.setEnabled(state)
        self.menuShow_figure.setEnabled(state)

    def disable_interface_state(self):
        self.actionRectangle_coordinates.setEnabled(False)
        self.actionEllipse_coordinates.setEnabled(False)
        self.actionDrawRectangle.setEnabled(False)
        self.actionDrawEllipse.setEnabled(False)
        self.actionBackground_subtraction.setEnabled(False)


    def generic_alert(self):
        alert=QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def jwst_alert(self):
        alert=QMessageBox()
        alert.setText("Error, some files could not be opened")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_file_alert(self):
        alert = QMessageBox()
        alert.setText("Error: Some file/files values, names or properties are incorrect")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_file_extension_alert(self):
        alert = QMessageBox()
        alert.setText("Error: File/Files extension error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def values_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def units_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("The units of Wavelength and Flux should be 'um' and 'MJy/sr'")
        warning.exec_()

    def max_range_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("The range selected must be between the spectrum values")
        warning.exec_()

    def missing_data_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setText("There is no data associated with the subband selected")
        warning.exec_()


    def closeEvent(self, event):
        self.spectrumV.close()
        self.rectCoord.close()
        self.cubeSelection.close()
        self.rectCreate.close()
        self.ellCreate.close()
        self.cubeViewer.close()
        self.styleManager.close()
        self.sliceManager.close()
        self.backgSub.close()
        self.centCoord.close()
        self.centWave.close()
        self.collapsedWave.close()
        self.waveSelect.close()
        self.cubeLoader.close()
