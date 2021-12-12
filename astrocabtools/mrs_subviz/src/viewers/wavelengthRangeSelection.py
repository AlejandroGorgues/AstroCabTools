import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
import os


import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pubsub import pub

from .canvas_interaction.imageRangeCanvas.panZoom import figure_pz

import astrocabtools.mrs_subviz.src.ui.ui_wavelengthRangeSelection

__all__=["WavelengthRangeSelection"]

class WavelengthRangeSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_wavelengthRangeSelection.Ui_wavelengthRangeSelection):

    def __init__(self, parent=None):
        super(WavelengthRangeSelection, self).__init__(parent)
        self.setupUi(self)

        self.create_spectrum_range_plot()

        self.saveFITSButton.clicked.connect(self.save_as_fits)
        self.zoomResetButton.clicked.connect(self.zoom_reset)

    def create_spectrum_range_plot(self):

        self.imageRangeFigure, self.imageRangeFigure.canvas = figure_pz()
        self.imageRangeFigure.pan_zoom.connect_zoom()
        self.imageRangeFigure.pan_zoom.connect_pan()
        self.ax = self.imageRangeFigure.add_subplot(111)
        self.ax.set_visible(False)

        self.waveSelect_vbox.addWidget(self.imageRangeFigure.canvas)

    def draw_image(self, iw, ew, data):
        """Draw the image after operations have been applied
        :param int iw: left x wavelength value
        :param int ew: right x wavelength value
        :param np.ndarray data: sum of the data across all the slices
        """
        range_text = "Initial wavelength: "+iw+" - End wavelength:"+ew
        self.data = data
        self.rangeLabel.setText(range_text)
        self.ax.set_visible(True)
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        #Set color map of the image to be gray for better visualization of the image
        plt.set_cmap(plt.get_cmap(("gray")))

        self.ax.imshow(data, origin='lower', aspect='auto')
        self.imageRangeFigure.pan_zoom.set_initial_limits(data.shape[0], data.shape[1])
        self.imageRangeFigure.pan_zoom.zoom_reset()

    def save_as_fits(self):
        """ Save the plot as a .fits file """
        try:
            fileSave = QFileDialog()
            fileSave.setNameFilter("FITS files (*.fits)")
            name = fileSave.getSaveFileName(self, 'Save File')
            if name[0] !="":
                hdu = fits.PrimaryHDU(self.data)
                hdul = fits.HDUList([hdu])
                hdul.writeto(name[0], overwrite=True)
        except Exception as e:
            self.show_file_extension_alert()

    def zoom_reset(self):
        self.imageRangeFigure.pan_zoom.zoom_reset()

    def clear_data(self):
        self.ax.set_visible(False)
        self.ax.clear()
        self.rangeLabel.setText('')


    def show_file_extension_alert(self):
        alert = QMessageBox()
        alert.setText("Error: File extension error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
