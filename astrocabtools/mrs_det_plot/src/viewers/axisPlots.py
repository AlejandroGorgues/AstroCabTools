"""
Object that represent the values of Y axis along X axis and vice versa
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec

from .canvas_interaction.panZoom import figure_pz
import astrocabtools.mrs_det_plot.src.ui.ui_axis_plot


class MrsAxisPlot(QDialog, astrocabtools.mrs_det_plot.src.ui.ui_axis_plot.Ui_MrsAxisPlot):

    def __init__(self, parent=None ):
        super(MrsAxisPlot, self).__init__(parent)
        self.setupUi(self)
        self.create_axis_plots()
        plt.style.use('seaborn')

        self.saveButton.clicked.connect(self.save_plots_images)

    def create_axis_plots(self):

        self.axisFigure, self.axisCanvas = figure_pz()

        #Create grid plots with gridspec
        #To change size of subplots
        spec = gridspec.GridSpec(
            ncols=1, nrows=2, figure=self.axisFigure)

        self.axisAx1 = self.axisFigure.add_subplot(spec[0, 0])
        self.axisAx2 = self.axisFigure.add_subplot(spec[1, 0])

        self.axis_vbox.addWidget(self.axisCanvas)

        self.axisAx1.set_visible(False)
        self.axisAx2.set_visible(False)

    def axis_plot(self, xValues, yValues, xLabel, yLabel, zUnit, filename):
        """ Draw the values from the both axis based on the position where the user clicked
        :param NumpyArray xValues: All values along the xAxis
        :param NumpyArray yValues: All values along the yAxis
        :param string xLabel: X value selected
        :param string yLabel: Y value selected
        """
        # discards the old graph
        self.axisAx1.clear()
        self.axisAx2.clear()

        # create two axis on a canvas with 2 rows, one column and in order
        self.axisAx1.set_visible(True)
        self.axisAx2.set_visible(True)

        #Axis 1
        self.axisAx1.set_title(
            "Flux values along Y axis with X value: {} \n from {}".format(xLabel, os.path.basename(filename)), fontsize=10)

        self.axisAx1.plot(xValues)

        self.axisAx1.set_ylabel("{}".format(zUnit))

        #Axis 2
        self.axisAx2.set_title(
            "Flux values along X axis with Y value:  {} \n from {}".format(yLabel , os.path.basename(filename)), fontsize=10)

        self.axisAx2.plot(yValues)

        self.axisAx2.set_ylabel("{}".format(zUnit))

        self.axisFigure.tight_layout(pad=2)

        self.axisCanvas.draw()

    @pyqtSlot()
    def save_plots_images(self):
        """ Save the plots as a .png file """
        fileSave = QFileDialog()
        fileSave.setNameFilter("PNG files (*.png)")
        name = fileSave.getSaveFileName(self, 'Save File')
        if name[0] !=""  :
            self.axisFigure.savefig(name[0], dpi = 600)
