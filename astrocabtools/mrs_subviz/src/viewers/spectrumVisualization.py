import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pubsub import pub

from .canvas_interaction.spectrumCanvas.panZoom import figure_pz

import astrocabtools.mrs_subviz.src.ui.ui_spectrumVisualization

__all__=["SpectrumV"]

class SpectrumV(QDialog, astrocabtools.mrs_subviz.src.ui.ui_spectrumVisualization.Ui_spectrumVisualization):

    def __init__(self, parent=None):
        super(SpectrumV, self).__init__(parent)
        self.setupUi(self)


        self.figureData = {"data": None, "type":None}
        self.spectra_dict ={}
        self.wavelength_range_limits = [None, None]

        self.xAxisRangeLimits = [-float('Inf'),float('Inf')]
        self.yAxisRangeLimits = [-float('Inf'),float('Inf')]

        self.create_spectrum_plot()

        self.saveButton.clicked.connect(self.save_spectrum)

        self.zoomResetButton.clicked.connect(self.zoom_reset)

    def create_spectrum_plot(self):

        self.spectrumFigure, self.spectrumFigure.canvas = figure_pz()
        self.spectrumFigure.pan_zoom.connect_zoom()
        self.spectrumFigure.pan_zoom.connect_pan()
        self.ax = self.spectrumFigure.add_subplot(111)
        self.ax.set_visible(False)

        self.spectrumLayout_vbox.addWidget(self.spectrumFigure.canvas)

    def zoom_reset(self):
        self.spectrumFigure.pan_zoom.zoom_reset()

    def set_figure_coordinates(self, figureData, typeFigure, centerX = None, centerY = None):
        self.figureData["data"] = figureData
        self.figureData["type"] = typeFigure

        if self.figureData["type"] == "rectangle":
            self.rangeSelect.get_rectangle_data(centerX = centerX, centerY = centerY,
                                            width = figureData.ex - figureData.ix, height  = figureData.ey - figureData.iy)
        else:
            self.rangeSelect.get_ellipse_data(centerX = self.figureData["data"][1][0], centerY = self.figureData["data"][1][1],
                                            aAxis = self.figureData["data"][0][2], bAxis = self.figureData["data"][0][3])

    def draw_spectrum(self, path, fValues, wValues, color, label):
        """
        :param string path: path of the cube which is the same as the spectrum
        :param list fValues: list of flux values along the wavelengths
        :param list wValues: list of wavelength values
        """
        self.spectra_dict[label] = [{"Wavelength": wValues}, {"Aperture spectrum":fValues}]

        if self.wavelength_range_limits[0] is not None:

            yAxis_range_limits = self.get_yAxis_from_range(self.wavelength_range_limits[0],\
                                                           self.wavelength_range_limits[1])

        #This array is created for the purpose of using it in the circle positioning
        #which allows to get the 'y' value
        self.wValuesRounded = np.round(np.asarray(wValues),5)

        self.path = path
        apertureLabel = "aperture"+label
        line = next((line for line in self.ax.lines if line.get_gid() == apertureLabel), None)

        if len(self.ax.lines) == 0:
            self.ax.set_visible(True)
            self.draw_plot_axes(r'$Wavelength(\mu m)$', r'$mJy$')
            self.set_interface_state(True)


        if line is None:
            self.ax.plot(wValues, fValues, gid=apertureLabel, color = color, label=label)
            self.update_legend()
        else:

            line.set_data(wValues, fValues)


        #Select limits of x and y axis
        if self.xAxisRangeLimits[0] == -float('Inf'):
            self.xAxisRangeLimits = [min(wValues), max(wValues)]
        else:
            self.xAxisRangeLimits = [min(self.xAxisRangeLimits[0],min(wValues)), max(self.xAxisRangeLimits[1],max(wValues))]


        if self.yAxisRangeLimits[0] == -float('Inf'):
            self.yAxisRangeLimits = [min(fValues), max(fValues)]
        else:
            self.yAxisRangeLimits = [min(self.yAxisRangeLimits[0],min(fValues)), max(self.yAxisRangeLimits[1],max(fValues))]

        #Set the limits of the x and y axis
        self.spectrumFigure.pan_zoom.set_initial_limits(self.xAxisRangeLimits, self.yAxisRangeLimits)

    def draw_background(self, wValues, fValues_sub, bkg_sum, label):
        self.spectra_dict[label].append({"Background spectrum": bkg_sum})
        self.spectra_dict[label].append({"Background subtracted spectrum": fValues_sub})

        self.spectrumFigure.canvas.draw()
        label_sum = "bkgSum"
        label_gidSum = label + "_bkgSum"
        label_sub = "bkgSubtr"
        label_gidSub = label+"_bkgSubtr"

        self.delete_duplicated_lines(label_gidSum, label_gidSub)

        self.ax.plot(wValues, bkg_sum, 'r--', gid=label_gidSum, label=label_sum)
        self.ax.plot(wValues, fValues_sub, 'g--', gid=label_gidSub, label=label_sub)

        self.update_legend()
        self.spectrumFigure.canvas.draw()

    def delete_duplicated_lines(self, gid_sum, gid_sub):
        """ Delete the sum background and bacground subtraction spectrum
        to be able to load again without duplicate them
        """
        lines = [line for line in self.ax.lines if line.get_gid() == gid_sum or line.get_gid() == gid_sub]
        for line in lines:
            self.ax.lines.remove(line)
        self.spectrumFigure.canvas.draw()

    def delete_duplicated_cube(self, subband):
        label_gidAperture = "aperture"+subband
        label_gidSum = subband + "_bkgSum"
        label_gidSub = subband +"_bkgSubtr"

        lines_bkgSum = [line for line in self.ax.lines if line.get_gid() == label_gidSum]
        lines_bkgSubtr = [line for line in self.ax.lines if line.get_gid() == label_gidSub]
        lines_aperture = [line for line in self.ax.lines if line.get_gid()== label_gidAperture]

        for line in lines_bkgSum:
            self.ax.lines.remove(line)
        for line in lines_bkgSubtr:
            self.ax.lines.remove(line)
        for line in lines_aperture:
            self.ax.lines.remove(line)
        self.update_legend()
        self.spectrumFigure.canvas.draw()

    def save_spectrum(self):
        """ Save the spectrum as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')
            path_file_txt = ""
            spectra_txt_dict = {}
            spectra_df = pd.DataFrame()

            for key, spectrum_list in self.spectra_dict.items():
                for spectrum_data in spectrum_list:
                    for key_spectrum, spectrum in spectrum_data.items():
                        if key_spectrum == "Wavelength":
                            wavelengthLabel = key+"_"+key_spectrum+" (um)"
                            spectra_txt_dict[wavelengthLabel] = spectrum
                        else:
                            fluxLabel = key+"_"+key_spectrum+" (mJy)"
                            spectra_txt_dict[fluxLabel] = spectrum

                    currSpectra_df = pd.DataFrame(data=spectra_txt_dict)
                    spectra_txt_dict.clear()
                    if spectra_df.empty:
                        spectra_df = spectra_df.append(currSpectra_df)
                    else:
                        spectra_df = pd.concat([spectra_df, currSpectra_df], axis=1)

            path_file_txt = name[0] + ".txt"
            spectra_df.to_csv(path_file_txt, sep=' ', index=False)

            self.spectrumFigure.savefig(name[0], dpi = 600, bbox_inches="tight")

            #np.savetxt(path_file_txt, df_spectra.values, delimiter="     ", \
            #           header=' '.join(df_spectra.columns.values.tolist()))
        except Exception as e:
            self.show_file_extension_alert()

    def get_yAxis_from_range(self, iw, ew):

        range_xValues = [self.wValues.index(x) for x in self.wValues if float(iw) <= x <= float(ew)]
        elements_yValues = [self.spectra_dict["Aperture spectrum"][y] for y in range_xValues]

        min_yValue = min(elements_yValues)
        max_yValue = max(elements_yValues)

        return min_yValue, max_yValue

    def draw_plot_axes(self, wUnits, fUnits):

        #Discard the old graph
        self.ax.clear()

        #Set text and range of the axes
        self.ax.set_xlabel(wUnits)
        self.ax.set_ylabel(fUnits)

        self.ax.grid(True)

    def set_interface_state(self, state):
        """ Disable or enable the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.zoomResetButton.setEnabled(state)
        self.saveButton.setEnabled(state)

    def show_file_extension_alert(self):
        alert = QMessageBox()
        alert.setText("Error: File extension error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def update_legend(self):
        h, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, h))
        self.ax.legend(by_label.values(), by_label.keys(), loc="upper right", frameon=True, framealpha = 1, facecolor = 'white')

    def spectrum_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Error")
        warning.setText("The spectrum selected does not exist")
        warning.exec_()

    def reset_range_axis(self):
        """
        Set max and min range to inf values once all the spectra had been drawn
        and prevent the reuse of the previous limits when new set of spectra is gonna be
        draw
        """
        self.xAxisRangeLimits = [-float('Inf'),float('Inf')]
        self.yAxisRangeLimits = [-float('Inf'),float('Inf')]

        #Reset the current axis limits to the actual window
        self.spectrumFigure.pan_zoom.zoom_reset()

    def clear_data(self):
        self.ax.clear()
        self.ax.set_visible(False)
        self.spectrumFigure.canvas.draw()
        self.set_interface_state(False)
        self.close()
