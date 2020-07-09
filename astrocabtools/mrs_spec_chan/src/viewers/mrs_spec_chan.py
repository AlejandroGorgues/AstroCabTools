# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the mrs_sec_chan tool
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import weakref
import pandas as pd

import sys
import traceback
import re
import io

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QPoint, QEvent
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import astrocabtools.mrs_spec_chan.src.viewers.spectrumManageListWidget as slw
import astrocabtools.mrs_spec_chan.src.viewers.loiSelection as loiS
import astrocabtools.mrs_spec_chan.src.viewers.spectrumSelection as pltS
import astrocabtools.mrs_spec_chan.src.viewers.templateSelection as tmpltS
import astrocabtools.mrs_spec_chan.src.ui.ui_mrs_spec_chan

from .canvas_interaction.panZoom import figure_pz

from ..utils.operations import transform_spectrum, divide_op_wavelength
from ..utils.constants import LOID

__all__= ["MrsSpecChanell"]

class MrsSpecChanell(QMainWindow, astrocabtools.mrs_spec_chan.src.ui.ui_mrs_spec_chan.Ui_MrsSpecChan):

    def __init__(self, parent=None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(MrsSpecChanell, self).__init__(parent)
        self.setupUi(self)

        plt.style.use('seaborn')

        self.microIcon = u"\u03BC"
        self.lambdaIcon = u"\u03BB"
        self.nuIcon = u"\u03BD"

        self.mrsChan = []
        self.nirsChan = []
        self.gap = []

        self.loiISelected = []
        self.loiLines = []

        self.specISelected = []
        self.spectrumLines = {}

        self.maxFlux = 0
        self.minFlux = 0

        self.loiSelection = loiS.MrsLoiList()
        self.spectrumSelection = pltS.MrsSpctrmList()
        self.templateSelection = tmpltS.MrsTmpltList()

        self.templateSelection.finished.connect(self.get_templates)
        self.spectrumSelection.finished.connect(self.get_spectrum)
        self.loiSelection.finished.connect(self.get_loi)

        self.create_top_widgets()
        self.create_middle_spectrum()
        self.create_bottom_chan_data()

    def create_top_widgets(self):
        self.lambdaLabel.setText('λemit(μm):')

        self.zEdit.setValidator(QtGui.QDoubleValidator())

        self.loadSpectra.clicked.connect(self.select_spectrum)

        self.loadOpWavelengthButton.clicked.connect(
            lambda: self.load_op_wavelength(self.lambdaEdit.text(),self.zEdit.text()))

        self.loadLoi.clicked.connect(self.select_loi)

        self.loadTemplate.clicked.connect(self.select_templates)

        self.saveButton.clicked.connect(self.save_plot_image)

        self.clearButton.clicked.connect(self.clear_all)

    def create_middle_spectrum(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = figure_pz()

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax1 = self.figure.add_subplot(111)

        self.ax1.set_visible(False)

        self.middlePlot.setLayout(layout)
        self.draw_spectrum_area()

    def create_bottom_chan_data(self):

        self.mrsCheckbox.toggled.connect(self.show_MRS_chan)
        self.nirSpecCheckbox.toggled.connect(self.show_NIRS_chan)
        self.nirSpecGapCheckbox.toggled.connect(self.show_Gap)

    def print_MRS_Chan(self):
        """ Draw on the plot the  MRS channels"""
        #Three list are create on this method in order to not create them every time the plot is called
        #Create a list of values for each channel
        subBandsValues = np.array([[4.87, 5.82], [5.62, 6.73], [6.49, 7.76], [7.45, 8.90], [8.61, 10.28],
        [9.91, 11.87], [11.47, 13.67], [13.25, 15.80], [15.30, 18.24], [17.54, 21.10], [20.44, 24.72], [23.84, 28.82]])

        #Add colors
        subBandsColors = np.array([["#d3ff00", "#00ff18", "#034500"],
                                        ["#439cfe", "#2673b8", "#2946bd"],
                                        ["#ffbb3b", "#ffab0b", "#e19e1e"],
                                        ["#ff7373", "#f84031", "#94261d"]])

        #Draw MRS subbands on the plot
        for i in range(0,12):

            rect = patches.Rectangle(
                (subBandsValues[i, 0],self.minFlux -7),
                subBandsValues[i,1] - subBandsValues[i, 0], self.maxFlux - self.minFlux  +7,
                facecolor=subBandsColors[int(i/3), (i) % 3], alpha=0.5)

            self.ax1.add_patch(rect)
            self.mrsChan.append(rect)

    def print_MRS_Chan_names(self):
        """ Draw on the plot the  MRS channels names"""
        subBandsValues = np.array([[4.87, 5.82], [5.62, 6.73], [6.49, 7.76], [7.45, 8.90], [8.61, 10.28],
        [9.91, 11.87], [11.47, 13.67], [13.25, 15.80], [15.30, 18.24], [17.54, 21.10], [20.44, 24.72], [23.84, 28.82]])
        subBandsNames = np.array([["1A", "1B", "1C"],
                                        ["2A", "2B", "2C"],
                                        ["3A", "3B", "3C"],
                                        ["4A", "4B", "4C"]])

        for i in range(0,12):

            subBandName = self.ax1.text((subBandsValues[i,1] + subBandsValues[i, 0])/2, -2, subBandsNames[int(i/3), (i) % 3],clip_on=True)
            self.mrsChan.append(subBandName)
    def print_NIRS_Chan(self):
        """ Draw on the plot the  NIRSpec channels"""
        nirsSpecValues = np.array([[0.9, 1.27], [0.97, 1.89],
         [1.66,3.17], [2.87, 5.27]])

        #Add colors
        nirsSepcColors = np.array(["#f2705c", "#bbf24e", "#58ed9d",
                                        "#6354f0"])

        #Draw NIR spec values
        for i in range(0,4):

            rect = patches.Rectangle(
                (nirsSpecValues[i, 0], self.minFlux-7),
                nirsSpecValues[i,1] - nirsSpecValues[i, 0], self.maxFlux - self.minFlux +7,
                facecolor=nirsSepcColors[i], alpha = 0.5)

            self.ax1.add_patch(rect)
            self.nirsChan.append(rect)

    def print_NIRS_Chan_lines(self):
        """ Draw on the plot the  NIRSpec channels lines"""
        nirsSpecValues = np.array([0.6, 5.3])

        self.nirsChan.append(self.ax1.axvline(x=float(nirsSpecValues[0]), color = "#fc0a0a", linestyle = "--"))

        self.nirsChan.append(self.ax1.axvline(x=float(nirsSpecValues[1]), color = "#fc0a0a", linestyle = "--"))

    def print_GAP(self):
        """ Draw on the plot the gap ranges"""
        gapValues = np.array([[1.40892, 1.48484], [2.36159, 2.48933],
         [3.98629,4.20176]])

        #Add colors
        gapColors = np.array(["#cc33ff", "#00b300", "#0040ff"])

        #Draw NIR spec values
        for i in range(0,3):

            self.gap.append(self.ax1.axvline(x=float(gapValues[i,0]), color = gapColors[i], linestyle = "dashdot"))
            self.gap.append(self.ax1.axvline(x=float(gapValues[i,1]), color = gapColors[i], linestyle = "dashdot"))

    def draw_spectrum_area(self):
        """Create the axes"""
        # discards the old graph

        self.ax1.clear()

        self.print_MRS_Chan_names()
        self.print_NIRS_Chan_lines()
        self.print_GAP()

        #Set text and range of the axes
        self.ax1.set_xlabel(r'$\mu m$')

        self.ax1.set_ylabel(r'$f_\nu$')

        self.ax1.set_xlim([0, 30])
        self.ax1.set_ylim([0, 20])
        self.ax1.grid()

        #Create shared y axes to draw x bottom axis and
        #x top values from the optional wavelengths
        self.ax2 = self.ax1.twiny()

        self.ax2.set_xticks([])
        self.ax2.set_xlim(self.ax1.get_xlim())
        self.ax2.grid()

    def draw_plot(self, waveL, fluxL, redshift, filename):
        """ Draw the plot
        :param list waveL: set of lambdas observed
        :param list fluxL: set of flux
        :param list opWaveL: optional lambdas observed
        :param str filename: Path of the spectrum
        """
        self.ax1.set_visible(True)

        line = self.ax1.plot(waveL, fluxL,gid=filename)
        self.spectrumLines[line[0]] = redshift
        self.delete_rect()

        self.figure.tight_layout(pad = 2)

        self.figure.canvas.draw()

    def delete_rect(self):
        """ Delete all rectangles to draw new ones based on max and min flux values"""
        self.set_max_min_flux()
        for x in reversed(range(len(self.ax1.patches))):
            patch = self.ax1.patches[x]

            if patch in self.mrsChan:
                self.mrsChan.remove(patch)

            elif patch in self.nirsChan:
                self.nirsChan.remove(patch)

            self.ax1.patches.remove(patch)
            del patch


        self.print_MRS_Chan()
        self.print_NIRS_Chan()
        self.show_MRS_chan()
        self.show_NIRS_chan()

    def set_max_min_flux(self):
        """Get max and min flux vales"""
        line_ydata = [line.get_ydata() for line in self.spectrumLines.keys()]
        for line in line_ydata:

            if min(line) < self.minFlux:

                self.minFlux = min(line)
            if max(line) > self.maxFlux:
                self.maxFlux = max(line)

    def plot_op_wavelength(self, opWaveL):
        """ Draw the optional wavelengths
        :param list opWaveL: optional lambdas
        """
        #Draw optional wavelengths
        self.print_op_wavelength(opWaveL)

    def load_file(self, path, z):
        """ Load the data from the path and transform the values
        :param string z: redshift value
        :param string path: path of the file
        """

        try:
            data = pd.read_csv(path, sep=' ', comment = '#', header=None)

            wavelengthValues, fluxValues, z = transform_spectrum(data, z)
            #Print the plot
            #line = next((x for x in self.ax1.lines if x.get_gid() == path), None)
            line = next((key for key, value in self.spectrumLines.items() if key.get_gid() == path and value == z), None)

            if line != None:

                self.repeat_line_alert()
            else:

                self.add_plt(path, z)

                self.draw_plot(wavelengthValues, fluxValues , z, path)

            if self.spectraListWidget.count() > 0 :
                self.set_interface_state(True)

        except Exception as e:
            self.show_alert()

    def print_loi(self, list ):
        """ Draw the line of interest on the canvas
        :param string loiItem: line of interest
        """
        loiValues = []
        for i in list:
            loiValue = LOID[i]
            loiValues.append(loiValue)
            loiLine = self.ax1.axvline(x=loiValue,  color="#8442f5")
            loiLine.set_gid(i)
            self.loiLines.append(loiLine)
        self.add_ticks(list, loiValues)

    def add_plt(self, filename, z):
        """ Add the plot to the manage list widget
        :param string z: redshift value
        :param string filename: path of the file
        """
        it = QListWidgetItem()
        self.spectraListWidget.addItem(it)
        widget = slw.listWidget(title = filename, redshift = z)
        widget.clicked.connect(self.remove_spectrum)
        widget.checked.connect(self.check_spectrum)
        self.spectraListWidget.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())

    def set_interface_state(self, state):
        """ Disable or enable the different widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.saveButton.setEnabled(state)
        self.loadOpWavelengthButton.setEnabled(state)
        self.lambdaEdit.setEnabled(state)
        self.zEdit.setEnabled(state)
        self.lambdaLabel.setEnabled(state)
        self.zLabel.setEnabled(state)
        self.spectraData.setEnabled(state)

        self.mrsCheckbox.setChecked(state)
        self.nirSpecCheckbox.setChecked(state)
        self.nirSpecGapCheckbox.setChecked(state)
        self.bottomChanData.setEnabled(state)
        self.clearButton.setEnabled(state)
        self.loadLoi.setEnabled(state)

    def print_op_wavelength(self, opWaveL ):
        """ Draw the optional wavelengths and
        its corresponding labels on the top x axis
        :param list opWaveL: list of optional wavelengths transformed
        """
        self.delete_line_by_gid("vline")
        self.remove_not_loi_ticks()

        opWaveLName = [str(x)+" "+self.microIcon+'mobs' for x in opWaveL]

        #Draw the vertical lines and save the positions to assign them to the labels
        for waveLenght in opWaveL:
            self.ax1.axvline(x=waveLenght, color="#ff1aa6").set_gid("vline")

        self.add_ticks(opWaveLName, opWaveL)

    def delete_line_by_gid(self, gid):
        """Delete only the previous axvline, not the plot line"""
        for x in reversed(range(len(self.ax1.lines))):
            line = self.ax1.lines[x]
            if line.get_gid() == gid:
                self.ax1.lines.remove(line)
                del line

    def add_ticks(self,list, loiValues):
        """ Add new ticks to the top x axis where the
        optional wavelength values will be drawn
        :param float newLoc: location of the tick
        :param string newLabel: line of interest text
        """

        # Get existing ticks
        locs = self.ax2.get_xticks().tolist()
        labels=[x.get_text() for x in self.ax2.get_xticklabels()]

        # Build dictionary of ticks
        Dticks=dict(zip(labels,locs))

        # Add new ticks
        for i in range(len(list)):
            Dticks[list[i]]=loiValues[i]

        # Get back tick lists
        locs=[*Dticks.values()]
        labels=[*Dticks.keys()]

        # Generate new ticks
        self.ax2.set_xticks(locs)
        self.ax2.set_xticklabels(labels)

    def remove_not_loi_ticks(self):
        """ Remove all top xaxis ticks that are not related to line of interest
        """
        # Get existing ticks
        locs = self.ax2.get_xticks().tolist()
        labels=[x.get_text() for x in self.ax2.get_xticklabels()]

        # Build dictionary of ticks
        Dticks=dict(zip(labels,locs))

        #Delete all ticks not loid
        for i in Dticks.copy():
            if i not in LOID:
                Dticks.pop(i)

        # Get back tick lists
        locs=list(Dticks.values())
        labels=list(Dticks.keys())

        # Generate new ticks
        self.ax2.set_xticks(locs)
        self.ax2.set_xticklabels(labels)

    def remove_loi_ticks(self):
        """ Remove all top xaxis ticks related to line of interest """
        # Get existing ticks
        locs = self.ax2.get_xticks().tolist()
        labels=[x.get_text() for x in self.ax2.get_xticklabels()]

        # Build dictionary of ticks
        Dticks=dict(zip(labels,locs))

        for i in Dticks.copy():

            if i in LOID:
                Dticks.pop(i)

        # Get back tick lists
        locs=list(Dticks.values())
        labels=list(Dticks.keys())

        # Generate new ticks
        self.ax2.set_xticks(locs)
        self.ax2.set_xticklabels(labels)

    def remove_loi_lines(self):
        """ Remove all vertical lines related to lines of interests """
        for x in reversed(range(len(self.loiLines))):
            line = self.loiLines[x]
            self.ax1.lines.remove(line)
            self.loiLines.remove(line)
            del line


    @pyqtSlot()
    def save_plot_image(self):
        """ Save the plot as a .png file """
        try:

            fileSave = QFileDialog()
            fileSave.setNameFilter("PNG files (*.png)")
            name = fileSave.getSaveFileName(self, 'Save File')
            if name[0] !="":
                self.figure.savefig(name[0], dpi = 600)
        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def load_op_wavelength(self, emWaveL, z):
        """ Reload the plot to print new emitted wavelength """
        try:

            self.ax2.set_xlim(self.ax1.get_xlim())
            if emWaveL != '' and z != '':
                z = float(z)

                opWaveL = divide_op_wavelength(emWaveL, z)
                self.print_op_wavelength(opWaveL)
                self.figure.canvas.draw()
            else:
                self.remove_not_loi_ticks()
                self.delete_line_by_gid("vline")

        except Exception as e:
            self.show_alert()

    @pyqtSlot()
    def select_templates(self):
        """Clear selection and list made previously to allow to select the same
        template with different redshift
        """
        self.templateSelection.uncheck_list()
        self.templateSelection.clear_list()
        self.templateSelection.show()
        self.templateSelection.open()

    @pyqtSlot()
    def select_spectrum(self):
        """Clear selection and list made previously to allow to select the same
        spectrum with different redshift
        """
        self.spectrumSelection.uncheck_list()
        self.spectrumSelection.clear_list()
        self.spectrumSelection.show()
        self.spectrumSelection.open()
        self.spectrumSelection.reload_directory()

    @pyqtSlot()
    def select_loi(self):
        self.loiSelection.show()
        self.loiSelection.open()

    @pyqtSlot(int)
    def get_templates(self, int):
        if int == QDialog.Accepted:

            self.specISelected = self.templateSelection.get_data()

            for key, values in self.specISelected.items():

                self.load_file(key, values)

        self.figure.canvas.draw()

    @pyqtSlot(int)
    def get_spectrum(self, int):

        if int == QDialog.Accepted:

            self.specISelected = self.spectrumSelection.get_data()

            for key, values in self.specISelected.items():

                self.load_file(key, values)
        self.figure.canvas.draw()

    @pyqtSlot(int)
    def get_loi(self, int):
        if int == QDialog.Accepted:
            #Delete previous loi ticks to show only the new ones
            self.remove_loi_ticks()
            self.remove_loi_lines()
            self.loiISelected = self.loiSelection.get_list()
            self.print_loi(self.loiISelected)

            self.loiSelection.clear_list()

            self.ax2.set_xlim(self.ax1.get_xlim())
            self.figure.canvas.draw()

    @pyqtSlot()
    def show_MRS_chan(self):
        if self.mrsCheckbox.isChecked():
            [e.set_visible(True) for e in self.mrsChan]
        else:
            [e.set_visible(False) for e in self.mrsChan]

        self.figure.canvas.draw()

    @pyqtSlot()
    def show_NIRS_chan(self):

        if self.nirSpecCheckbox.isChecked():
            [e.set_visible(True) for e in self.nirsChan]
        else:
            [e.set_visible(False) for e in self.nirsChan]

        self.figure.canvas.draw()


    @pyqtSlot()
    def show_Gap(self):
        if self.nirSpecGapCheckbox.isChecked():
            [e.set_visible(True) for e in self.gap]
        else:
            [e.set_visible(False) for e in self.gap]

        self.figure.canvas.draw()

    @pyqtSlot()
    def remove_spectrum(self):
        """Delete the spectrum selected, if it's the last one, delete all"""
        self.maxFlux = 0
        self.minFlux = 0

        widget = self.sender()

        line = next((key for key, value in self.spectrumLines.items() if key.get_gid() == re.sub('Path: ','',widget.path_text()) and \
            value == float(re.sub('z: ','',widget.redshift_text()))), None)

        self.ax1.lines.remove(line)
        gp = widget.mapToGlobal(QPoint())
        lp = self.spectraListWidget.viewport().mapFromGlobal(gp)
        row = self.spectraListWidget.row(self.spectraListWidget.itemAt(lp))
        t_it = self.spectraListWidget.takeItem(row)
        del self.spectrumLines[line]
        del line
        del t_it

        if self.spectraListWidget.count() == 0:
            self.set_interface_state(False)
            self.remove_not_loi_ticks()
            self.delete_line_by_gid("vline")
            self.remove_loi_ticks()
            self.remove_loi_lines()
            self.ax1.set_visible(False)
            self.lambdaEdit.setText('')
            self.zEdit.setText('')

        self.delete_rect()

        self.figure.canvas.draw()

    @pyqtSlot()
    def check_spectrum(self):
        """Set current enable state of the line to be visible or not"""
        widget = self.sender()
        line = next((key for key, value in self.spectrumLines.items() if key.get_gid() == re.sub('Path: ','',widget.path_text()) and \
            value == float(re.sub('z: ','',widget.redshift_text()))), None)

        if widget.checkbox_state():
            line.set_visible(True)

        else:
            line.set_visible(False)
        self.figure.canvas.draw()

    @pyqtSlot()
    def clear_all(self):

        for line, value in self.spectrumLines.items():
            self.ax1.lines.remove(line)
            del line

        self.spectrumLines.clear()
        self.spectraListWidget.clear()
        self.set_interface_state(False)
        self.remove_not_loi_ticks()
        self.delete_line_by_gid("vline")
        self.remove_loi_ticks()
        self.remove_loi_lines()
        self.ax1.set_visible(False)
        self.lambdaEdit.setText('')
        self.zEdit.setText('')
        self.delete_rect()
        self.figure.canvas.draw()

    def repeat_line_alert(self):

        alert = QMessageBox()
        alert.setText("Warning: The file you tried to load already exist")
        alert.exec_()

    def show_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Input or file values incorrect")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n in case \
        of being the error in the extension, it must be blank or .txt ")
        alert.exec_()
