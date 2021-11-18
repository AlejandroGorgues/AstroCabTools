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

import astrocabtools.cube_ans.src.viewers.spectrumParametersSelection as specPars

import astrocabtools.fit_line.src.viewers.fit_line as fitLine
import astrocabtools.cube_ans.src.ui.ui_spectrumVisualization
import astrocabtools.cube_ans.src.viewers.wavelengthRangeSelection as rangeSelect

__all__=["SpectrumV"]

class SpectrumV(QDialog, astrocabtools.cube_ans.src.ui.ui_spectrumVisualization.Ui_spectrumVisualization):

    def __init__(self, parent=None):
        super(SpectrumV, self).__init__(parent)
        self.setupUi(self)


        self.fitLine = fitLine.MrsFitLine()
        self.figureData = {"data": None, "type":None}
        self.spectra_dict ={}
        self.wavelength_range_limits = [None, None]

        self.create_spectrum_plot()

        self.saveTextButton.clicked.connect(self.save_spectrum_as_text)
        self.savePNGButton.clicked.connect(self.save_plot_as_png)
        self.loadButton.clicked.connect(self.select_parameters)

        self.specPars = specPars.SpectrumParametersSelection()
        self.specPars.finished.connect(self.load_fitLine)

        self.rangeSelect = rangeSelect.WavelengthRangeSelection()

        self.createRangeButton.clicked.connect(self.create_range)
        self.moveRangeButton.clicked.connect(self.move_range)

        self.rangeImageButton.clicked.connect(self.show_range_image)

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

    def update_wavelength_line(self, x):
        """Update the position where the line that shows the current wavelength in the
        spectrum is
        :param float x: wavelength value
        """
        self.spectrumFigure.pan_zoom.draw_line_position(x)

    def draw_spectrum(self, path, fValues, wValues, wUnits, fUnits):
        """
        :param string path: path of the cube which is the same as the spectrum
        :param list fValues: list of flux values along the wavelengths
        :param list wValues: list of wavelength values
        :param string wUnits: units of the wavelength
        :param string fUnits: units of the flux values
        """
        self.spectra_dict["Aperture spectrum"] = fValues
        self.wValues = wValues

        self.spectrumFigure.pan_zoom.set_rectangle_yAxis_limits(min(fValues), max(fValues))

        if self.wavelength_range_limits[0] is not None:

            yAxis_range_limits = self.get_yAxis_from_range(self.wavelength_range_limits[0],\
                                                           self.wavelength_range_limits[1])
            self.spectrumFigure.pan_zoom.update_rectangle_yAxis_limits_on_spectrum_update(yAxis_range_limits)

        #This array is created for the purpose of using it in the circle positioning
        #which allows to get the 'y' value
        self.wValuesRounded = np.round(np.asarray(wValues),5)

        self.wUnits = wUnits
        self.fUnits = fUnits

        self.path = path

        line = next((line for line in self.ax.lines if line.get_gid() == "aperture"), None)

        if line is None:

            self.draw_plot_axes()

            self.ax.set_visible(True)

            self.ax.plot(wValues, fValues, 'b-', gid="aperture", label="Aperture spectrum")

            self.update_legend()

            self.set_interface_state(True)

        else:
            line.remove()
            del line
            self.ax.plot(wValues, fValues, 'b-', gid="aperture", label="Aperture spectrum")


        self.spectrumFigure.pan_zoom.set_rectangle_yAxis_limits(self.ax.get_ylim()[0], self.ax.get_ylim()[1])
        self.spectrumFigure.pan_zoom.set_initial_limits(self.ax.get_xlim(), self.ax.get_ylim())

        self.spectrumFigure.set_tight_layout(True)
        self.spectrumFigure.canvas.draw()

    def draw_background(self, fValues_sub, bkg_sum):
        self.spectra_dict["Background spectrum"] = bkg_sum
        self.spectra_dict["Background subtracted spectrum"] = fValues_sub

        self.delete_duplicated_lines()
        self.ax.plot(self.wValues, bkg_sum, 'r-', gid="sum", label="Sum background")
        self.ax.plot(self.wValues, fValues_sub, 'g-', gid="subtr", label="Background subtracted spectrum")
        self.update_legend()

        self.spectrumFigure.canvas.draw()

    def delete_duplicated_lines(self):
        """ Delete the sum background and background subtraction spectrum
        to be able to load again without duplicate them
        """
        lines = [line for line in self.ax.lines if line.get_gid() == "sum" or line.get_gid() == "subtr"]
        for line in lines:
            self.ax.lines.remove(line)

    @pyqtSlot()
    def select_parameters(self):
        """Load the dialog where the parameters to be applied to the spectrum to load           the fitLine tool will be used"""
        self.specPars.update_path(self.path)
        self.specPars.show()
        self.specPars.open()

    def show_range_data(self, iw, ew, data):
        """Draw the image from the sum of the wavelength range values and
        draw the current figure drawed in the main window (No rectangle or ellipse selector)
        :param str iw: initial wavelength value of the range
        :param str ew: ending wavelength value of the range
        :param data:
        """
        self.rangeImageButton.setEnabled(True)

        self.wavelength_range_limits[0] = iw
        self.wavelength_range_limits[1] = ew
        #Set the height of the rectangle range to be the one delimited for the min
        #and max values that the rectangle takes from the spectrum
        yAxis_range_limits = self.get_yAxis_from_range(iw, ew)
        self.spectrumFigure.pan_zoom.update_rectangle_yAxis_limits_on_range_update(yAxis_range_limits)

        self.rangeSelect.draw_image(iw, ew, data)

        self.rangeSelect.show()
        self.rangeSelect.open()

    def show_range_image(self):
        """
        Instead of using the show_range_data, this method only shows the range dialog
        """
        self.rangeSelect.show()
        self.rangeSelect.open()

    @pyqtSlot(int)
    def load_fitLine(self, int):
        try:
            if int == QDialog.Accepted:

                redshift, wUnits, fUnits, spectrumType = self.specPars.get_data()
                if spectrumType in self.spectra_dict:
                    spectrum_structure = {"wValues" : self.wValues,
                            "wUnits" : wUnits,
                            "fValues" : self.spectra_dict[spectrumType],
                            "fUnits": fUnits,
                            "redshift": redshift,
                            "path": self.path}
                    #Check if fitLine is already loaded to prevent to create a new one
                    if self.fitLine.isHidden():
                        self.fitLine.show()
                    self.fitLine.load_spectrum_from_cube_ans(spectrum_structure)
                else:
                    self.spectrum_warning()

        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def save_spectrum_as_text(self):
        """ Save the spectrum as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')
            path_file_txt = ""
            spectra_txt_dict = {}
            if "Background spectrum" in self.spectra_dict:

                spectra_txt_dict["Wavelength("+self.wUnits+")"]= self.wValues
                spectra_txt_dict["Flux("+self.fUnits+")"]= self.spectra_dict["Aperture spectrum"]
                spectra_txt_dict["Background("+self.fUnits+")"]=self.spectra_dict["Background spectrum"]
                spectra_txt_dict["Background subtracted spectrum(mJy)"]=self.spectra_dict["Background subtracted spectrum"]
            else:

                spectra_txt_dict["Wavelength("+self.wUnits+")"]= self.wValues
                spectra_txt_dict["Flux("+self.fUnits+")"]=self.spectra_dict["Aperture spectrum"]

            df_spectra = pd.DataFrame(data=spectra_txt_dict)

            path_file_txt = name[0] + ".txt"

            self.spectrumFigure.savefig(name[0], dpi = 600, bbox_inches="tight")

            df_spectra.to_csv(path_file_txt, sep=' ', index=False)
            #np.savetxt(path_file_txt, df_spectra.values, delimiter="     ", \
            #           header='             '.join(df_spectra.columns.values.tolist()), comments='')
        except Exception as e:
            self.show_file_extension_alert()

    def save_plot_as_png(self):
        """ Save the plot as a .png file """
        try:
            fileSave = QFileDialog()
            fileSave.setNameFilter("PNG files (*.png)")
            name = fileSave.getSaveFileName(self, 'Save File')
            if name[0] !="":
                self.spectrumFigure.savefig(name[0], dpi = 600, bbox_inches='tight')
        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def create_range(self):
        """Activate or desactivate the option to select a wavelength range to create
        the figure"""
        if self.createRangeButton.isChecked():
            if self.moveRangeButton.isChecked():
                self.moveRangeButton.setChecked(False)
            self.spectrumFigure.pan_zoom.disconnect_pan()
            self.spectrumFigure.pan_zoom.disconnect_rectangle_interaction()
            self.spectrumFigure.pan_zoom.connect_rectangle_creation()

        #Activate pan when both buttons are unchecked
        else:
            self.spectrumFigure.pan_zoom.disconnect_rectangle_creation()
            self.spectrumFigure.pan_zoom.connect_pan()

    @pyqtSlot()
    def move_range(self):
        """ Activate or desactivate the option to be able to move the figure created
        previously"""
        if self.moveRangeButton.isChecked():
            if self.createRangeButton.isChecked():
                self.createRangeButton.setChecked(False)
            self.spectrumFigure.pan_zoom.disconnect_pan()
            self.spectrumFigure.pan_zoom.disconnect_rectangle_creation()
            self.spectrumFigure.pan_zoom.connect_rectangle_interaction()

        #Activate pan when both buttons are unchecked
        else:
            self.spectrumFigure.pan_zoom.disconnect_rectangle_interaction()
            self.spectrumFigure.pan_zoom.connect_pan()

    def get_yAxis_from_range(self, iw, ew):

        range_xValues = [self.wValues.index(x) for x in self.wValues if float(iw) <= x <= float(ew)]
        elements_yValues = [self.spectra_dict["Aperture spectrum"][y] for y in range_xValues]

        min_yValue = min(elements_yValues)
        max_yValue = max(elements_yValues)

        return min_yValue, max_yValue

    def draw_plot_axes(self):

        #Discard the old graph
        self.ax.clear()

        #Set text and range of the axes
        self.ax.set_xlabel(r'$Wavelength(\mu m)$')
        self.ax.set_ylabel(r'$mJy$')

        self.ax.grid(True)

    def set_interface_state(self, state):
        """ Disable or enable the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.createRangeButton.setEnabled(state)
        self.moveRangeButton.setEnabled(state)
        self.zoomResetButton.setEnabled(state)
        self.saveTextButton.setEnabled(state)
        self.savePNGButton.setEnabled(state)
        self.loadButton.setEnabled(state)

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

    def unselect_buttons(self):
        self.moveRangeButton.setChecked(False)
        self.createRangeButton.setChecked(False)

    def clear_data(self):
        self.ax.clear()
        self.ax.set_visible(False)
        self.spectrumFigure.pan_zoom.clear_elements_axes()
        self.spectrumFigure.canvas.draw()
        self.rangeImageButton.setEnabled(False)
        self.set_interface_state(False)
        self.unselect_buttons()
        self.rangeSelect.clear_data()
        self.specPars.clear_data()
        self.close()

    def closeEvent(self, event):
        if isinstance(self.fitLine, astrocabtools.fit_line.src.viewers.fit_line.MrsFitLine):
            self.fitLine.close()
        self.specPars.close()
        self.rangeSelect.close()
