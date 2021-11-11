import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from pubsub import pub

from .canvas_interaction.spectrumCanvas.panZoom import figure_pz

from ..utils.constants import LOID
from ..utils.basic_transformations import apply_redshift, wavelength_from_redshift, set_round_lines

import astrocabtools.fit_line.src.viewers.fit_line as fitLine
import astrocabtools.mrs_subviz.src.viewers.spectrumParametersSelection as specPars
import astrocabtools.mrs_subviz.src.viewers.loiSelection as loiS

import astrocabtools.mrs_subviz.src.ui.ui_spectrumVisualization

__all__=["SpectrumV"]

class SpectrumV(QDialog, astrocabtools.mrs_subviz.src.ui.ui_spectrumVisualization.Ui_spectrumVisualization):

    def __init__(self, parent=None):
        super(SpectrumV, self).__init__(parent)
        self.setupUi(self)

        self.fitLine = fitLine.MrsFitLine()
        self.specPars = specPars.SpectrumParametersSelection()
        self.specPars.finished.connect(self.load_fitLine)

        self.loiSelection = loiS.LoiSelection()
        self.loiSelection.finished.connect(self.get_loi)

        self.figureData = {"data": None, "type":None}
        self.spectra_dict ={}
        self.wavelength_range_limits = [None, None]

        self.loiISelected = []
        self.loiLines = []

        self.xAxisRangeLimits = [-float('Inf'),float('Inf')]
        self.yAxisRangeLimits = [-float('Inf'),float('Inf')]

        self.create_spectrum_plot()

        self.saveButton.clicked.connect(self.save_spectra)
        self.savePNGButton.clicked.connect(self.save_png_spectra)

        self.loadButton.clicked.connect(self.select_parameters)
        self.selectLinesButton.clicked.connect(self.select_loi)

        self.zoomButton.clicked.connect(self.zoomOrders)
        self.panButton.clicked.connect(self.panOrders)
        self.zoomResetButton.clicked.connect(self.zoom_reset)

    def zoomOrders(self):
        self.spectrumFigure.pan_zoom.connect_zoom()
        self.spectrumFigure.pan_zoom.disconnect_pan()

    def panOrders(self):
        self.spectrumFigure.pan_zoom.connect_pan()
        self.spectrumFigure.pan_zoom.disconnect_zoom()

    def create_spectrum_plot(self):

        self.spectrumFigure, self.spectrumFigure.canvas = figure_pz()
        #self.spectrumFigure.canvas.setFocusPolicy(Qt.ClickFocus)
        #self.spectrumFigure.pan_zoom.disconnect_zoom()
        #self.spectrumFigure.pan_zoom.disconnect_pan()
        self.ax = self.spectrumFigure.add_subplot(111)
        #self.spectrumFigure.pan_zoom.create_rectangle_ax(self.ax)
        self.create_rectangle(self.ax)
        self.ax.clear()
        self.ax.set_visible(False)

        self.spectrumLayout_vbox.addWidget(self.spectrumFigure.canvas)

    def zoom_reset(self):
        self.spectrumFigure.pan_zoom.zoom_reset()


    def load_fitLine(self, int):
        try:
            if int == QDialog.Accepted:
                wUnits, fUnits, spectrumType, subbandList = self.specPars.get_data()

                wavelengthValue = []
                fluxValue = []
                for subband in subbandList:
                    if subband in self.spectra_dict:
                        for data in self.spectra_dict[subband]:
                            for key, value in data.items():
                                if key == 'Wavelength':
                                    wavelengthValue = wavelengthValue + value
                                elif key == spectrumType:
                                    fluxValue = fluxValue + value

                spectra_df = pd.DataFrame(data={'wValue': wavelengthValue, 'fValue': fluxValue})
                spectra_df.set_index('wValue')
                spectra_df.sort_index(inplace = True)


                spectrum_structure = {"wValues" : spectra_df.index.values.tolist(),
                        "wUnits" : wUnits,
                        "fValues" : spectra_df['fValue'].values.tolist(),
                        "fUnits": fUnits,
                        "redshift": 0,
                        "path": ''}
                #Check if fitLine is already loaded to prevent to create a new one
                if self.fitLine.isHidden():
                    self.fitLine.show()
                    self.fitLine.load_spectrum_from_cube_ans(spectrum_structure)
                else:
                    self.spectrum_warning()
        except Exception as e:
            self.missing_data_warning()

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

        apertureLabel = "aperture"+label
        line = next((line for line in self.ax.lines if line.get_gid() == apertureLabel), None)

        if len(self.ax.lines) == 0:
            self.draw_plot_axes(r'$Wavelength(\mu m)$', r'$mJy$')

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
        self.spectrumFigure.canvas.draw()

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

    def save_spectra(self):
        """ Save the spectra as a .txt file"""
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

        except Exception as e:
            self.show_file_extension_alert()

    def save_png_spectra(self):
        """ Save the plot as a .png file """
        try:
            fileSave = QFileDialog()
            fileSave.setNameFilter("PNG files (*.png)")
            name = fileSave.getSaveFileName(self, 'Save File')
            if name[0] !="":
                self.spectrumFigure.savefig(name[0], dpi = 600, bbox_inches='tight')
        except Exception as e:
            self.show_file_extension_alert()

    def get_yAxis_from_range(self, iw, ew):

        range_xValues = [self.wValues.index(x) for x in self.wValues if float(iw) <= x <= float(ew)]
        elements_yValues = [self.spectra_dict["Aperture spectrum"][y] for y in range_xValues]

        min_yValue = min(elements_yValues)
        max_yValue = max(elements_yValues)

        return min_yValue, max_yValue

    def draw_plot_axes(self, wUnits, fUnits):

        #Set text and range of the axes
        self.ax.set_xlabel(wUnits)
        self.ax.set_ylabel(fUnits)

        self.ax.grid(True)
        self.ax.set_visible(True)
        self.set_interface_state(True)

        #Create shared y axes to draw x bottom axis and
        #x top values from the optional wavelengths
        self.ax2 = self.ax.twiny()
        self.ax2.set_zorder(-15)
        self.ax2.set_xticks([])
        self.ax2.set_xlim(self.ax.get_xlim())
        self.ax2.grid()

    def print_loi(self, loiSelected, redshift):
        """ Draw the line of interest on the canvas
        :param string loiItem: line of interest
        """
        loiValues = []
        for i, loi in enumerate(loiSelected):
            loiSep = loi.split(": ")
            loiTrans = apply_redshift(float(loiSep[1]), redshift)
            loiRounded = set_round_lines(loiTrans, loiSep[0])

            loiSelected[i] = loiSep[0] + ": "+str(loiRounded)
            #LOID[float(loiSep[1])][1] = float(redshift)
            #LOID[float(loiSep[1])][2] = float(loiTrans)
            loiValues.append(loiTrans)
            loiLine = self.ax.axvline(x=loiTrans,  color="#8442f5")
            #loiLine.set_clip_on(False)
            loiLine.set_gid(loi)
            self.loiLines.append(loiLine)
        self.add_ticks(loiSelected, loiValues)


    def add_ticks(self,loiSelected, loiValues):
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
        for i in range(len(loiSelected)):
            Dticks[loiSelected[i]]=loiValues[i]

        # Get back tick lists
        locs=[*Dticks.values()]
        labels=[*Dticks.keys()]

        # Generate new ticks
        self.ax2.set_xticks(locs)
        self.ax2.set_xticklabels(labels)

        xticks = self.ax2.get_xticklines()
        #Because the elements outside of the xlims and ylims are small
        #the use of clipping to False do not create a problem
        #However if the data increases, this should be watch
        #Anyway, the use of setting clipping to False is because if an xline
        #is created outside of the xlim, before using the zoom or pan element,
        #the tick of the xvline appears, which leads to an ugly view of the representation
        #and to prevent it, clipping of the tick is set to False
        for tick in xticks:
            tick.set_clip_on(False)

    def remove_loi_ticks(self):
        """ Remove all top xaxis ticks related to line of interest """
        # Get existing ticks
        locs = self.ax2.get_xticks().tolist()
        labels=[x.get_text() for x in self.ax2.get_xticklabels()]

        # Build dictionary of ticks
        Dticks=dict(zip(labels,locs))

        for i in Dticks.copy():
            #key = [key for key, value in LOID.items() if value[2] == float(i.split(": ")[1])][0]
            #wValue = wavelength_from_redshift(float(i.split(": ")[1]), )
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
            self.ax.lines.remove(line)
            self.loiLines.remove(line)
            del line

    @pyqtSlot()
    def select_loi(self):
        self.loiSelection.show()
        self.loiSelection.open()

    @pyqtSlot(int)
    def get_loi(self, int):
        if int == QDialog.Accepted:
            #Delete previous loi ticks to show only the new ones
            self.remove_loi_ticks()
            self.remove_loi_lines()
            self.loiISelected = self.loiSelection.get_list()
            redshift = self.loiSelection.get_redshift()
            self.print_loi(self.loiISelected, redshift)

            self.loiSelection.clear_list()

            self.ax2.set_xlim(self.ax.get_xlim())
            self.spectrumFigure.canvas.draw()


    @pyqtSlot()
    def select_parameters(self):
        """Load the dialog where the parameters to be applied to the spectrum to load the
        fitLine tool will be used"""
        self.specPars.show()
        self.specPars.open()

    def set_interface_state(self, state):
        """ Disable or enable the widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.zoomResetButton.setEnabled(state)
        self.saveButton.setEnabled(state)
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

    def missing_data_warning(self):
        warning = QMessageBox()
        warning.setWindowTitle("Warning")
        warning.setIcon(QMessageBox.Warning)
        warning.setDetailedText(traceback.format_exc())
        warning.setText("There is no data associated with the subband selected")
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

    def create_rectangle(self,ax):
        self.spectrumFigure.pan_zoom.create_rectangle_ax(ax)


    def clear_data(self):
        self.ax.clear()
        self.ax.set_visible(False)
        self.reset_range_axis()
        self.spectrumFigure.canvas.draw()
        self.set_interface_state(False)
        self.close()


    def closeEvent(self, event):
        if isinstance(self.fitLine, astrocabtools.fit_line.src.viewers.fit_line.MrsFitLine):
            self.fitLine.close()
        self.specPars.close()
