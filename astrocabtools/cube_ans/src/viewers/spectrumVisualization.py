import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .panZoom import figure_pz

import astrocabtools.cube_ans.src.viewers.spectrumParametersSelection as specPars

import astrocabtools.fit_line.src.viewers.fit_line as fitLine
import astrocabtools.cube_ans.src.ui.ui_spectrumVisualization

__all__=["SpectrumV"]

class SpectrumV(QDialog, astrocabtools.cube_ans.src.ui.ui_spectrumVisualization.Ui_Dialog):

    def __init__(self, parent=None):
        super(SpectrumV, self).__init__(parent)
        self.setupUi(self)
        self.fitLine = None
        self.create_spectrum_plot()

        self.saveButton.clicked.connect(self.save_spectrum)
        self.loadButton.clicked.connect(self.select_parameters)

        self.specPars = specPars.SpectrumParametersSelection()
        self.specPars.finished.connect(self.load_fitLine)

    def create_spectrum_plot(self):

        self.spectrumFigure, self.spectrumFigure.canvas = figure_pz()

        self.ax = self.spectrumFigure.add_subplot(111)
        self.ax.set_visible(False)

        self.spectrumLayout_vbox.addWidget(self.spectrumFigure.canvas)

    def draw_spectrum(self, path, fValues, wValues, wUnits, fUnits):
        """
        :param list fValues: list of flux values along the wavelengths
        :param string wUnits: units of the wavelength
        :param string fUnits: units of the flux values
        """
        self.fValues = fValues
        self.wValues = wValues

        self.wUnits = wUnits
        self.fUnits = fUnits

        self.path = path

        self.draw_plot_axes(wUnits, fUnits)

        self.ax.set_visible(True)

        self.ax.plot(wValues, fValues)
        self.spectrumFigure.tight_layout()

        self.spectrumFigure.canvas.draw()

        self.set_interface_state(True)

    @pyqtSlot()
    def select_parameters(self):

        self.specPars.update_path(self.path)
        self.specPars.show()
        self.specPars.open()

    @pyqtSlot(int)
    def load_fitLine(self, int):
        try:
            if int == QDialog.Accepted:

                redshift, wUnits, fUnits = self.specPars.get_data()
                kwargs = {"wValues" : self.wValues,
                        "wUnits" : wUnits,
                        "fValues" : self.fValues,
                        "fUnits": fUnits,
                        "redshift": redshift,
                        "path": self.path}

                self.fitLine = fitLine.MrsFitLine(**kwargs)
                self.fitLine.show()
        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def save_spectrum(self):
        """ Save the spectrum as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')
            path_file_txt = ""

            d = {self.wUnits: self.wValues, self.fUnits: self.fValues}
            df = pd.DataFrame(data=d)

            path_file_txt = name[0] + ".txt"

            self.spectrumFigure.savefig(name[0], dpi = 600)
            np.savetxt(path_file_txt, df.values, delimiter=" ", \
                       header=self.wUnits +" "+ self.fUnits)
        except Exception as e:
            self.show_file_extension_alert()

    def draw_plot_axes(self, wUnits, fUnits):

        #Discard the old graph
        self.ax.clear()

        #Set text and range of the axes
        self.ax.set_xlabel(wUnits)
        self.ax.set_ylabel(fUnits)

        self.ax.grid(True)

    def set_interface_state(self, state):
        """ Disable or enble the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.saveButton.setEnabled(state)
        self.loadButton.setEnabled(state)

    def show_file_extension_alert(self):
        alert = QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def closeEvent(self, event):
        if isinstance(self.fitLine, astrocabtools.fit_line.src.viewers.fit_line.MrsFitLine):
            self.fitLine.close()
        self.specPars.close()
