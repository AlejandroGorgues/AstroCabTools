"""
Object that represent all four fits images
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec

from .canvas_interaction.panZoom import figure_pz
import astrocabtools.mrs_det_plot.src.ui.ui_images_fits

from ..utils.imgPlot import imgPlot
from ..utils.globalStats import globalStats


class MrsImagesFits(QDialog, astrocabtools.mrs_det_plot.src.ui.ui_images_fits.Ui_MrsImagesFits):
    crossed = pyqtSignal(float, float, int, name='makeCross')
    changeBar = pyqtSignal()

    def __init__(self, parent=None ):
        super(MrsImagesFits, self).__init__(parent)
        self.setupUi(self)

        plt.style.use('seaborn')

        self.imageAxes = {}
        self.images = {}
        self.imgObjList = {}
        self.globalStats = globalStats('minmax', 'Linear', 'gray')
        self.fitsObjList = {}

        self.pixelLines = {}

        self.imageSelectedIndex = 0

        self.create_images_plot()

    def create_images_plot(self):
        """ Create the middle layout that will show the x,y,z values selected on the middle plot"""

        self.imagesFigure, self.imagesFigure.canvas = figure_pz()
        k = 1

        #Create grid plots with gridspec
        #To change size of subplots to be able to make bigger the imgshow than the colorbar

        spec = gridspec.GridSpec(
            ncols=2, nrows=2, figure=self.imagesFigure)

        for i in range (2):
            for j in range(2):
                midAx = self.imagesFigure.add_subplot(spec[i, j])
                midAx.set_visible(False)
                self.imgObjList[k] =  imgPlot([], [], [],0, 0)
                self.imageAxes[k] = midAx
                self.click_factory(midAx, k)
                k += 1

        self.mouse_over_axes_factory()
        midAx.set_visible(False)

        self.imagesFigure.set_size_inches(30.5, 20.5)

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.imagesFigure.canvas.setFocusPolicy(Qt.ClickFocus)

        self.imagesFigure.tight_layout(pad=8)

        self.mainLayout.addWidget(self.imagesFigure.canvas)

    def draw_plot(self, index, fitsObj, hdul, norm):

        """ Draw the middle plot and the colorbar asocciated
        :param int index: current axis selected
        """
        exist = False
        limits = ()


        #Check if there was a image before to maintain the same get_limits
        #after autoscaling
        if index in self.images:
            exist = True
            limits = self.imageAxes[index].axis()

        #Check if pixel selection lines where selected to get the index and
        #add it after the image change
        key = next((key for key, value in self.pixelLines.items() if value[0] in
        self.imageAxes[index].lines), None)

        self.imageAxes[index].set_visible(True)
        self.imageAxes[index].clear()

        self.imageAxes[index].grid(False)
        self.imageAxes[index].set_xticks([])
        self.imageAxes[index].set_yticks([])

        self.imageAxes[index].set_title(
            "{}".format(os.path.basename(fitsObj.filename), fontsize=10))

        im = self.imageAxes[index].imshow(hdul[1].data[fitsObj.currIntegration, fitsObj.currFrame],
                                     norm = norm, cmap=plt.get_cmap(self.globalStats.color), origin='lower')

        #If pixel lines where drawn, add it again to the axes because with clear() the lines were deleted
        if key != None:
            self.imageAxes[index].add_line(self.pixelLines[index][0])
            self.imageAxes[index].add_line(self.pixelLines[index][1])

        self.images[index] = (im)
        self.imageAxes[index].lines
        self.imageSelectedIndex = index

        if exist:
            self.imageAxes[index].axis(limits)

        self.imagesFigure.canvas.draw()

        self.changeBar.emit()

    def click_factory(self, axis, index):
        """ Obtain data where the user clicked
            :param Axis axis: the axis where the user clicked
            :param int index: current axis selected
        """
        #Return click funct to axis
        def click_fun(event):
            if event.inaxes == axis and event.dblclick:

                #print(event.xdata, event.ydata)
                xdata = event.xdata
                ydata = event.ydata

                self.add_lines(xdata, ydata, index)
                self.crossed.emit(xdata, ydata, index)

            self.imagesFigure.canvas.draw()

        #Obtain data on click event
        self.imagesFigure.canvas.mpl_connect('button_press_event', lambda event: click_fun(
            event))

    def mouse_over_axes_factory(self):
        """ Obtain data where the user clicked
            :param Axis axis: the axis where the user clicked
            :param int index: current axis selected
        """
        #Return click funct to axis
        def mouse_over_fun(event):
            if event.inaxes in self.imageAxes.values():

                index_aux = list(self.imageAxes.keys())[list(self.imageAxes.values()).index(event.inaxes)]


                if index_aux in self.images.keys():
                    self.imageSelectedIndex = index_aux


                    self.changeBar.emit()

            self.imagesFigure.canvas.draw()

        #Obtain data on click event
        self.imagesFigure.canvas.mpl_connect('axes_enter_event', lambda event: mouse_over_fun(
            event))

    def add_lines(self, xdata, ydata, index):
        """ Draw two lines on the pixel selected
        :param float xdata: X value on cursor clicked
        :param float ydata: Y value on cursor clicked
        :param int index: current axis selected
        """

        keyIndex = next((key for key,value in self.pixelLines.items() if value[0] in self.imageAxes[index].lines and value[1] in self.imageAxes[index].lines), None)

        if keyIndex != None:
            self.imageAxes[index].lines.remove(self.pixelLines[keyIndex][0])
            self.imageAxes[index].lines.remove(self.pixelLines[keyIndex][1])
            del self.pixelLines[keyIndex]

        vLine = self.imageAxes[index].axvline(x = xdata, color= 'r')
        hLine = self.imageAxes[index].axhline(y = ydata, color = 'r')

        self.pixelLines[index] = [vLine, hLine]

    def get_img_selected_index(self):
        return self.imageSelectedIndex

    def update_canvas(self):
        self.imagesFigure.canvas.draw()

    def get_image_obj_selected(self, index):
        return self.imgObjList[index]

    def set_image_obj_selected(self, index, imgObj):
        self.imgObjList[index] = imgObj

    def get_image_selected(self, index):
        return self.images[index]

    def set_image_selected(self, index, image):
        self.images[index] = image

    def get_image_axes_selected(self, index):
        return self.imageAxes[index]

    def set_image_axes_selected(self, index, imageAxes):
        self.imageAxes[index] = imageAxes

    def get_global_stats(self):
        return self.globalStats

    def set_global_stats(self, globalStats):
        self.globalStats = globalStats

    def check_pixel_line_exist(self, index):
        #Check if the image selected a pixel before, to be able to delete it
        if index in self.pixelLines:
            del self.pixelLines[index]
