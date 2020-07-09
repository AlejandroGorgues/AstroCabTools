"""
Object that represent a pixel along time
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

import astrocabtools.mrs_det_plot.src.ui.ui_point_plot


class MrsPointPlot(QDialog, astrocabtools.mrs_det_plot.src.ui.ui_point_plot.Ui_MrsPointPlot):

    def __init__(self, parent=None ):
        super(MrsPointPlot, self).__init__(parent)
        self.setupUi(self)

        self.minorXLabels = []
        self.mayorXLabels = []
        self.create_point_plot()
        plt.style.use('seaborn')


        self.saveButton.clicked.connect(self.save_plot_image)

    def create_point_plot(self):

        self.pointFigure, self.pointCanvas = figure_pz()

        #Create grid plots with gridspec
        #To change size of subplots
        spec = gridspec.GridSpec(
            ncols=1, nrows=1, figure=self.pointFigure)

        self.axis = self.pointFigure.add_subplot(spec[0, 0])

        #layout = QVBoxLayout()
        self.point_vbox.addWidget(self.pointCanvas)

        self.axis.set_visible(False)

        #self.pointPlot.setLayout(layout)

    def point_plot(self,maxFrame, maxIntegration, xValue, yValue, zValues, zUnit, filename):
        """ Draw the pixel values alngo time where the user clicked
        :param int maxFrame: Max value of frame
        :parama int maxIntegration: Max value of integration
        :param list zValues: All values along the xAxis
        :param string zUnit: X value selected
        """

        values = [zFrameValues for zIntegrationValues in zValues for zFrameValues in zIntegrationValues if zFrameValues in zIntegrationValues]

        for i in range(maxIntegration):
            self.mayorXLabels.append(i+1)
            for j in range(maxFrame):
                self.minorXLabels.append(j+1)

        # discards the old graph
        self.axis.clear()

        self.axis.set_visible(True)

        #Axis
        self.axis.set_title(
            "Values at {} - {} \n from {}".format(xValue, yValue, os.path.basename(filename), fontsize=10))

        self.axis.plot(values)

        self.axis.set_ylabel("{}".format(zUnit))
        self.axis.set_xlabel("Frames")

        self.pointFigure.tight_layout(pad=2)

        self.pointCanvas.draw()

    @pyqtSlot()
    def save_plot_image(self):
        """ Save the plot as a .png file """
        fileSave = QFileDialog()
        fileSave.setNameFilter("PNG files (*.png)")
        name = fileSave.getSaveFileName(self, 'Save File')
        if name[0] !="":
            self.pointFigure.savefig(name[0], dpi = 600)
