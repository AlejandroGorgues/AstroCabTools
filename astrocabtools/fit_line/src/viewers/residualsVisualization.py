import numpy as np
import matplotlib.pyplot as plt
import lmfit

import sys
import re
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .canvas_interaction.panZoomResiduals import figure_pz

import astrocabtools.fit_line.src.ui.ui_residualsVisualization

class MrsResidualsV(QDialog, astrocabtools.fit_line.src.ui.ui_residualsVisualization.Ui_residualsVisualization):

    def __init__(self, parent=None ):
        super(MrsResidualsV, self).__init__(parent)
        self.setupUi(self)

        self.residualsAttr_list = []

        self.create_middle_plot()

    def create_middle_plot(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = figure_pz()

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212, sharex=self.ax1)

        self.ax1.set_visible(False)
        self.ax2.set_visible(False)

        self.residualsGroupbox.setLayout(layout)


    def draw_plot_area(self):
        """Create the axes"""
        # discards the old graph
        self.ax1.clear()
        self.ax2.clear()

        #Set text and range of the axes
        self.ax1.set_xlabel(r'$Wavelength(\mu m)$')
        self.ax2.set_xlabel(r'$Wavelength(\mu m)$')

        self.ax1.set_ylabel(r'$f_\lambda ( \frac{erg}{s\enspace cm^2\>\mu m} )$')
        self.ax2.set_ylabel(r'$f_\lambda ( \frac{erg}{s\enspace cm^2\>\mu m} )$')

        self.ax1.grid(True)
        self.ax2.grid(True)

    def draw_plot(self, result, wValues, fValues, residuals):
        """ Draw the plot
        :param list wValues: list lambdas values selected
        :param list fValues: flux values along wValues
        :param ModelResult Object result: object that contains all result parameters
        from the fitted model
        """
        self.ax1.set_visible(True)
        self.ax2.set_visible(True)

        self.ax1.plot(wValues, fValues, c='#4c72b0',label='Spectrum')
        self.ax1.plot(wValues, result.best_fit, 'r-',label='Best fit')
        self.ax2.plot(wValues, residuals,linestyle='',color= 'b', marker='o',label='Residuals')
        self.ax2.axhline(y=0, color = "#fc0a0a", linestyle = "--")

        self.draw_legends()

        self.figure.tight_layout()

        self.figure.canvas.draw()

    def get_residuals(self, result, fValues):
        """Get the residuals subtractinc the y values of best fit result with
        the initial flux values
        :param ModelResult Object result: object that contains all result parameters
        from the fitted model
        :param list fValues: flux values along wValues
        """
        return result.best_fit - fValues

    def set_residuals(self, result, wValues, fValues):
        residualsAttr = {}
        residualsAttr['result'] = result
        residualsAttr['wValues'] = wValues
        residualsAttr['fValues'] = fValues
        self.residualsAttr_list.append(residualsAttr)

    def set_residuals_index(self, index):
        result = self.residualsAttr_list[index]['result']
        wValues = self.residualsAttr_list[index]['wValues']
        fValues = self.residualsAttr_list[index]['fValues']
        residuals = self.get_residuals(result, fValues)

        self.draw_plot_area()
        self.draw_plot(result, wValues, fValues, residuals)

    def delete_last_residuals(self):
        if len(self.residualsAttr_list)> 0:
            self.residualsAttr_list.pop()

    def delete_all_residuals(self):
        self.residualsAttr_list.clear()

    def draw_legends(self):
        h, labels = self.ax1.get_legend_handles_labels()
        self.ax1.legend(labels=labels, loc="upper right", frameon=True, framealpha = 1, facecolor = 'white')

        h, labels = self.ax2.get_legend_handles_labels()
        self.ax2.legend(labels=labels, loc="upper right", frameon=True, framealpha = 1, facecolor = 'white')

    def generate_all_residuals(self, path):
        """
        Generate each of the residuals plots to save each one on a different file
        :param str path: Path of the generic file name where the images
        are gonna be saved
        """

        for residuals_index_data in range(len(self.residualsAttr_list)):
            result = self.residualsAttr_list[residuals_index_data]['result']
            wValues = self.residualsAttr_list[residuals_index_data]['wValues']
            fValues = self.residualsAttr_list[residuals_index_data]['fValues']

            residuals = self.get_residuals(result, fValues)

            self.draw_plot_area()
            self.draw_plot(result, wValues, fValues, residuals)
            self.save_residual_on_path(path, residuals_index_data)


    def save_residual_on_path(self, path, index):
        path = path + "_resid" + str(index)
        self.figure.savefig(path, dpi = 600, bbox_inches='tight')
