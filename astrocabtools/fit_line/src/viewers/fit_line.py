# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the fit_line tool
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import weakref
import pandas as pd

import sys
import traceback
import io

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pubsub import pub

import astrocabtools.fit_line.src.viewers.spectrumSelection as stmS
import astrocabtools.fit_line.src.viewers.modelDataVisualization as modelV
import astrocabtools.fit_line.src.ui.ui_fit_line

from .canvas_interaction.panZoomFitLine import figure_pz

from ..io.ascii_load import apply_redshift_to_txt
from ..io.fits_load import apply_redshift_to_fits
from ..io.spec_cube_load import apply_redshift_to_cube

from ..models.lineModelCreation import lineModel
from ..models.quadraticModelCreation import quadraticModel
from ..models.gaussModelCreation import gaussModel
from ..models.exponentialModelCreation import exponentialModel
from ..models.powerLawModelCreation import powerLawModel
from ..models.doubleGaussModelCreation import doubleGaussModel
from ..models.lorentzModelCreation import lorentzModel
from ..models.lorentzGaussModelCreation import lorentzGaussModel
from ..models.voigtModelCreation import voigtModel
from ..models.pseudoVoigtModelCreation import pseudoVoigtModel
from ..models.moffatModelCreation import moffatModel

__all__=["MrsFitLine"]

class MrsFitLine(QMainWindow, astrocabtools.fit_line.src.ui.ui_fit_line.Ui_FitLine):

    def __init__(self, parent=None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(MrsFitLine, self).__init__(parent)
        self.setupUi(self)

        plt.style.use('seaborn')

        self.microIcon = u"\u03BC"
        self.lambdaIcon = u"\u03BB"
        self.nuIcon = u"\u03BD"

        self.models = []
        self.currLabels = []
        self.initialLimits = {}
        self.model = None
        self.typeModel = "singleGauss"
        self.typeCont = "line"

        self.spectrumSelection = stmS.SpectrumSelection()
        self.modelDataV = modelV.ModelDataVisualization()
        self.spectrumSelection.finished.connect(self.get_plot)

        self.modelDataV.savePlot.connect(self.save_plot_on_path)

        #Create the canvas to load the plot
        self.create_middle_plot()

        self.actionLoad_Spectrum.triggered.connect(self.select_plot)
        self.actionSave_as_png.triggered.connect(self.save_plot_image)

        self.zoomResetButton.clicked.connect(self.zoom_reset)
        self.zoomButton.clicked.connect(self.activate_zoom)
        self.panButton.clicked.connect(self.activate_pan)
        self.clickNormalButton.clicked.connect(self.activate_click)
        self.undoButton.clicked.connect(self.undo_action)

        self.actionReset_window.triggered.connect(self.reset_window)
        self.actionClear_last_fitted_model.triggered.connect(self.clear_last_fitted_model)
        self.actionClear_fitted_models.triggered.connect(self.clear_fitted_models)
        self.actionShow_fitted_data_parameters.triggered.connect(self.show_model_fit_data)

        self.markPointsToolButton.clicked.connect(self.manage_generation_points)

        self.modelSelectionComboBox.currentIndexChanged.connect(self.set_model)
        self.continuumSelectionComboBox.currentIndexChanged.connect(self.set_continuum)

    def create_middle_plot(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = figure_pz()
        #Subscribe method to setStateUndo event
        pub.subscribe(self.change_state_undo_button,'setStateUndo')
        pub.subscribe(self.draw_fitted_models, 'fittedModelShow')

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax = self.figure.add_subplot(111)

        #Create rectangle selector
        self.create_rectangle(self.ax)

        self.ax.set_visible(False)

        self.middlePlot.setLayout(layout)

    def show_model_selection(self):
        """Show the model list dialog"""
        self.modelDataV.show()
        self.modelDataV.open()

    def draw_plot_area(self):
        """Create the axes"""
        # discards the old graph
        self.ax.clear()

        #Set text and range of the axes
        self.ax.set_xlabel(r'$Wavelength(\mu m)$')

        self.ax.set_ylabel(r'$f_\lambda ( \frac{erg}{s\enspace cm^2\>\mu m} )$')

        self.ax.grid(True)

    def draw_plot(self):

        self.ax.set_visible(True)
        #Clear all previous lines and markers that do not belong to the spectrum
        for i in range(len(self.ax.lines)):
            line = self.ax.lines.pop(i)
            del line

        for i in range(len(self.ax.collections)):
            marker = self.ax.collections.pop(i)
            del marker

        #Clear legend list
        self.modelDataV.delete_all()
        self.currLabels.clear()

        self.set_spectrum_ranges(self.wavelength, self.flux)
        self.update_legend()
        self.update_buttons()
        self.update_pan_zoom_data()


        self.figure.tight_layout()

        self.figure.canvas.draw()


    def load_spectrum_from_cube_ans(self, spectrum_data):
        """ Load the data from the parameters passed from cube_ans and transform the
        values to represent them
        :param list wValues: wavelength values
        :param list fValues: flux values
        :param str wUnits: units of the wavelength values
        :param str fUnits: units of the flux values
        :param float z: redshift value
        :param str path: path of the file
        """
        self.path = spectrum_data["path"]

        #Convert wValues and fValues to np.ndarray to be able to use numpy arithmetic operations
        self.wavelength, self.flux, z = apply_redshift_to_cube(spectrum_data["redshift"],
                                                               np.array(spectrum_data["wValues"]),np.array(spectrum_data["fValues"]),
                                                               spectrum_data["wUnits"], spectrum_data["fUnits"])

        #Print the plot
        self.draw_plot_area()
        self.draw_plot()
        self.set_interface_state(True)

    def load_file(self, path, z, wColumn, fColumn, wUnits, fUnits, fileExt):
        """ Load the data from the path and transform the values
        :param string z: redshift value
        :param string path: path of the file
        :param int wColumn: column where the wavelength values are located
        :param int fColumn: column where the flux values are located
        :param str wUnits: units of the wavelength values
        :param str fUnits: units of the flux values
        """
        try:
            self.path = path
            if fileExt =='*.txt':
                self.wavelength, self.flux, z = apply_redshift_to_txt(path, z, wColumn, fColumn, wUnits, fUnits)
            elif fileExt == '*.fits':

                self.wavelength, self.flux, z = apply_redshift_to_fits(path, z, wColumn, fColumn, wUnits, fUnits)


            #Print the plot
            self.draw_plot_area()
            self.draw_plot()
            self.set_interface_state(True)


        except Exception as e:
            self.show_file_alert()

    def set_spectrum_ranges(self, wavelength, flux):
        """
        :param np.ndarray wavelength: array of wavelength values
        :param np.ndarray flux: array of flux values
        Get initial limits of the spectrum and set it them on the axe. This is
        because when a user change spectrum after zooming a previous spectrum,
        the zoom limits on axes does not change to adjust the full new spectrum
        """
        #minW , maxW  = np.amin(wavelength), np.amax(wavelength)
        #minF , maxF  = np.amin(flux), np.amax(flux)

        #Set additional range on plot for better visualization

        #self.ax.set_xlim(minW*0.9, maxW*1.1)
        #self.ax.set_ylim(minF, maxF)

        self.spectrum = self.ax.plot(wavelength, flux, c='#4c72b0',label='Spectrum')

        #self.initialLimits["xlim"] = (minW, maxW)
        #self.initialLimits["ylim"] = (minF, maxF)

    def manage_generation_points(self, checked):
        """If pointsGenerationButton is pressed, allow to draw the markers
        otherwise, it disallow the option to draw them until pointsGenerationButton
        is pressed again
        """
        if checked:
            self.modelSelectionComboBox.setEnabled(False)
            self.markPointsToolButton.setText("Cancel process")
            if self.typeModel == "singleGauss":
                text_lines = ["Mark right continuum", "Mark left sigma", "Mark right sigma", "Mark top (center and height)", ""]
                self.model = gaussModel(text_lines, self.typeCont)
            elif self.typeModel == "doubleGauss":
                text_lines = ["Mark right continuum", "Mark left sigma from left gaussian", "Mark right sigma from left gaussian", "Mark top (center and height) from left gaussian", "Mark left sigma from right gaussian", "Mark right sigma from right gaussian", "Mark top (center and height) from right gaussian", ""]
                self.model = doubleGaussModel(text_lines, self.typeCont)
            elif self.typeModel == "lorentz":
                text_lines = ["Mark right continuum", "Mark left sigma", "Mark right sigma", "Mark top (center and height)", ""]
                self.model = lorentzModel(text_lines, self.typeCont)
            elif self.typeModel == "lorentzGauss":
                text_lines = ["Mark right continuum", "Mark left sigma from lorentz", "Mark right sigma from lorentz", "Mark top (center and height) from lorentz", "Mark left sigma from gaussian", "Mark right sigma from gaussian", "Mark top (center and height) from gaussian", ""]
                self.model = lorentzGaussModel(text_lines, self.typeCont)
            elif self.typeModel == "voigt":
                text_lines = ["Mark right continuum", "Mark left sigma", "Mark right sigma", "Mark top (center and height)", ""]
                self.model = voigtModel(text_lines, self.typeCont)
            elif self.typeModel == "pseudoVoigt":
                text_lines = ["Mark right continuum", "Mark left sigma", "Mark right sigma", "Mark top (center and height)", ""]
                self.model = pseudoVoigtModel(text_lines, self.typeCont)
            elif self.typeModel == "moffat":
                text_lines = ["Mark right continuum", "Mark left sigma", "Mark right sigma", "Mark top (center and height)", ""]
                self.model = moffatModel(text_lines, self.typeCont)
            elif self.typeModel == "noline":
                if self.typeCont == "line":
                    text_lines = ["Mark right continuum", ""]
                    self.model = lineModel(text_lines, self.typeCont)
                elif self.typeCont == "quadratic":
                    text_lines = ["Mark right continuum", ""]
                    self.model = quadraticModel(text_lines, self.typeCont)
                elif self.typeCont == "exponential":
                    text_lines = ["Mark right continuum", ""]
                    self.model = exponentialModel(text_lines, self.typeCont)
                elif self.typeCont == "powerLaw":
                    text_lines = ["Mark right continuum", ""]
                    self.model = powerLawModel(text_lines, self.typeCont)

            self.model.init_data_points()
            self.indicationLabel.setText("Mark left continuum")

        else:
            self.markPointsToolButton.setText("Mark points")
            self.delete_previous_markers()
            self.indicationLabel.setText("")
            self.modelSelectionComboBox.setEnabled(True)
            self.figure.canvas.draw()

    def show_model_fit_data(self):
        self.show_model_selection()

    def draw_fitted_models(self, xdata, ydata):

        try:
            if self.markPointsToolButton.isChecked():
                self.indicationLabel.setText(next(self.model.add_data_points(xdata, ydata)))
                self.add_crosshair(xdata, ydata)

                if self.indicationLabel.text() == "":

                    self.markPointsToolButton.setText("Mark points")
                    self.markPointsToolButton.setChecked(False)
                    self.delete_previous_markers()

                    #Initialize parameters that determine the model
                    label_model_list = []
                    num_model = 0

                    #Set the parameters that determined the type of model and the legend labels based on the model
                    if isinstance(self.model, astrocabtools.fit_line.src.models.lineModelCreation.lineModel):
                        label_model_list.insert(len(label_model_list),"Fitted Line")
                        num_model = 1

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.quadraticModelCreation.quadraticModel):
                        label_model_list.insert(len(label_model_list),"Fitted Quadratic")
                        num_model = 1

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.exponentialModelCreation.exponentialModel):
                        label_model_list.insert(len(label_model_list),"Fitted Exponential")
                        num_model = 1
                    elif isinstance(self.model, astrocabtools.fit_line.src.models.powerLawModelCreation.powerLawModel):
                        label_model_list.insert(len(label_model_list),"Power Law")
                        num_model = 1

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.gaussModelCreation.gaussModel):
                        label_model_list.insert(len(label_model_list),"Fitted Gaussian")
                        num_model = 2

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.lorentzModelCreation.lorentzModel):
                        label_model_list.insert(len(label_model_list),"Fitted Lorentzian")
                        num_model = 2

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.voigtModelCreation.voigtModel):
                        label_model_list.insert(len(label_model_list),"Fitted Voigt")
                        num_model = 2

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.pseudoVoigtModelCreation.pseudoVoigtModel):
                        label_model_list.insert(len(label_model_list),"Fitted PseudoVoigt")
                        num_model = 2

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.moffatModelCreation.moffatModel):
                        label_model_list.insert(len(label_model_list),"Fitted Moffat")
                        num_model = 2

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.doubleGaussModelCreation.doubleGaussModel):
                        label_model_list.insert(len(label_model_list),"Left fitted Gaussian")
                        label_model_list.insert(len(label_model_list),"Right fitted Gaussian")
                        num_model = 3

                    elif isinstance(self.model, astrocabtools.fit_line.src.models.lorentzGaussModelCreation.lorentzGaussModel):
                        label_model_list.insert(len(label_model_list),"Fitted Lorentzian")
                        label_model_list.insert(len(label_model_list),"Fitted Gaussian")
                        num_model = 3


                    #Draw when there is only one model fitted
                    if num_model == 1:

                        result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = self.model.draw_model_fit(self.path, self.wavelength, self.flux)
                        self.modelDataV.add_spectrum_values(result, wavelengthValues, fluxValues, num_model)
                        self.modelDataV.add_model_data(resultText)
                        self.modelDataV.add_delimiter_line()
                        comps = result.eval_components()

                        self.model.lines = self.ax.plot(wavelengthValues, result.best_fit, 'r-',label='Best fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, initial_y1_values, 'y--',label='Initial fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, comps['model1'], 'k:',label=label_model_list.pop(0))[0]

                    elif num_model == 2:

                        result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = self.model.draw_model_fit(self.path, self.wavelength, self.flux)
                        self.modelDataV.add_spectrum_values(result, wavelengthValues, fluxValues, num_model)
                        self.modelDataV.add_model_data(resultText)
                        self.modelDataV.add_delimiter_line()
                        comps = result.eval_components()

                        self.model.lines = self.ax.plot(wavelengthValues, result.best_fit, 'r-',label='Best fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, initial_y1_values+ comps['continuum_fitting_function'], 'y--',label='Initial fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, comps['continuum_fitting_function'], 'g--',label='Fitted Continuum')[0]

                        self.model.lines = self.ax.plot(wavelengthValues, comps['model1'] + comps['continuum_fitting_function'], 'k:',label=label_model_list.pop(0))[0]

                    #Draw when there are two models fitted
                    elif num_model == 3:

                        result, resultText, wavelengthValues, fluxValues, initial_y1_values, initial_y2_values = self.model.draw_model_fit(self.path, self.wavelength, self.flux)
                        self.modelDataV.add_spectrum_values(result, wavelengthValues, fluxValues, num_model)
                        self.modelDataV.add_model_data(resultText)
                        self.modelDataV.add_delimiter_line()
                        comps = result.eval_components()

                        self.model.lines = self.ax.plot(wavelengthValues, result.best_fit,'r-',label='Best fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, initial_y1_values+ comps['continuum_fitting_function'],'y--',label='Initial fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, initial_y2_values+ comps['continuum_fitting_function'], 'y:',label='Initial fit')[0]
                        self.model.lines = self.ax.plot(wavelengthValues, comps['continuum_fitting_function'],'g--',label='Fitted Continuum')[0]
                        self.model.lines =self.ax.plot(wavelengthValues, comps['p1_'] + comps['continuum_fitting_function'], 'k--',label=label_model_list.pop(0))[0]
                        self.model.lines = self.ax.plot(wavelengthValues, comps['p2_'] + comps['continuum_fitting_function'], 'k:',label=label_model_list.pop(0))[0]

                    self.modelSelectionComboBox.setEnabled(True)
                    self.models.append(self.model)
                    self.update_legend()

            self.figure.canvas.draw()
        except Exception as e:
            self.generic_alert()
            self.delete_previous_markers()
            self.figure.canvas.draw()
            self.modelSelectionComboBox.setEnabled(True)

    def add_crosshair(self, xdata, ydata):
        """ Draw marker on specified point
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        marker = self.ax.scatter(xdata, ydata, marker='+', c= 'red')
        self.model.markers = marker


    def check_repeat_model_labels(self):
        """
        Check if specified labels have been used before to not duplicate the legend box
        """
        setList = set(['Initial fit', 'Best fit', 'Fitted gaussian', 'Fitted line'])
        setCurr = set(self.currLabels)
        if len(setList.intersection(setCurr))  == 0:
            self.currLabels.append('Initial fit')
            self.currLabels.append('Best fit')
            self.currLabels.append('Fitted gaussian')
            self.currLabels.append('Fitted line')
            self.update_legend()

    def set_interface_state(self, state):
        """ Disable or enable the different widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.markPointsToolButton.setEnabled(state)
        self.zoomButton.setEnabled(state)
        self.zoomResetButton.setEnabled(state)
        self.panButton.setEnabled(state)
        self.clickNormalButton.setEnabled(state)
        self.modelSelectionComboBox.setEnabled(state)
        self.modelSelectionLabel.setEnabled(state)
        self.continuumSelectionComboBox.setEnabled(state)
        self.continuumSelectionLabel.setEnabled(state)

        self.menuVisualization.setEnabled(state)
        self.actionSave_as_png.setEnabled(state)

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

    @pyqtSlot(str)
    def save_plot_on_path(self, path):
        path = path + "_ajuste"
        plt.savefig(path, dpi = 600, bbox_inches='tight')

    @pyqtSlot()
    def select_plot(self):
        """
        Load dialog that allow to select the spectrum to be loaded
        """
        self.spectrumSelection.show()
        self.spectrumSelection.open()

    @pyqtSlot(int)
    def get_plot(self, int):
        try:
            if int == QDialog.Accepted:
                path, redshift, wColumn, fColumn, wUnits, fUnits, fileExt = self.spectrumSelection.get_data()
                self.load_file(path, redshift, wColumn, fColumn, wUnits, fUnits, fileExt)
                self.activate_click()
                self.modelDataV.delete_model_data()
            self.figure.canvas.draw()
        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def clear_last_fitted_model(self):
        """
        Becuase for each model, 4 lines, 5 markers and 4 legends labels are created,
        deleting the last of them requires to delete the ones that has been created with it also
        """
        if len(self.models) > 0:
            model = self.models.pop()
            for i in range(len(model.lines)):
                line = model.lines[-1]
                self.ax.lines.remove(line)
                model.del_line(line)
                del line


            for i in range(len(model.markers)):
                marker = model.markers[-1]
                self.ax.collections.remove(marker)
                model.del_marker(marker)
                del marker

            if len(self.ax.lines) ==1:
                self.update_legend()
                self.currLabels.clear()
            self.figure.canvas.draw()
            self.modelDataV.delete_model_data()
            del model


    @pyqtSlot()
    def clear_fitted_models(self):
        """ Delete only the models and markers from the canvas"""

        for i in reversed(range(len(self.models))):
            model = self.models[i]
            for j in range(len(model.lines)):
                line = next((line for line in self.ax.lines if line in model.lines), None)
                if line != None:
                    self.ax.lines.remove(line)
                    model.del_line(line)
                    del line

            for j in reversed(range(len(model.markers))):
                marker = next((marker for marker in self.ax.collections if marker in model.markers), None)
                if marker != None:
                    self.ax.collections.remove(marker)
                    model.del_marker(marker)
                    del marker
            self.models.remove(model)
            del model

        self.update_legend()
        self.figure.canvas.draw()
        #Delete all list items in the modelDataV Dialog
        self.modelDataV.delete_all()
        self.currLabels.clear()


    @pyqtSlot()
    def reset_window(self):

        self.set_interface_state(False)
        self.modelDataV.delete_all()
        self.models.clear()
        self.currLabels.clear()
        self.ax.set_visible(False)
        self.figure.canvas.draw()

    def set_model(self, index):
        if index == 0:
            self.typeModel = "singleGauss"
        elif index == 1:
            self.typeModel = "doubleGauss"
        elif index == 2:
            self.typeModel = "lorentz"
        elif index == 3:
            self.typeModel = "lorentzGauss"
        elif index == 4:
            self.typeModel = "voigt"
        elif index == 5:
            self.typeModel = "pseudoVoigt"
        elif index == 6:
            self.typeModel = "moffat"
        elif index == 7:
            self.typeModel = "noline"

    def set_continuum(self, index):
        if index == 0:
            self.typeCont = "line"
        elif index == 1:
            self.typeCont = "quadratic"
        elif index == 2:
            self.typeCont = "exponential"
        elif index == 3:
            self.typeCont = "powerLaw"

    @pyqtSlot()
    def activate_click(self):
        """
        Allow only to click on the canvas
        """
        self.figure.pan_zoom.disconnect_pan()
        self.figure.pan_zoom.disconnect_zoom()

    @pyqtSlot()
    def activate_zoom(self):
        """
        Allow only to zoom on the canvas
        """
        self.figure.pan_zoom.disconnect_pan()
        self.figure.pan_zoom.connect_zoom()

    @pyqtSlot()
    def activate_pan(self):
        """
        Allow only to pan on the canvas
        """
        self.figure.pan_zoom.disconnect_zoom()
        self.figure.pan_zoom.connect_pan()

    @pyqtSlot()
    def zoom_reset(self):
        """Zoom to fit the original spectrum size """
        self.figure.pan_zoom.add_zoom_reset()

    @pyqtSlot()
    def undo_action(self):
        self.figure.pan_zoom.undo_last_action()

    def delete_previous_markers(self):
        while True:
            marker = next((marker for marker in self.ax.collections if marker is self.model.markers[len(self.model.markers)-1]), None)
            if marker is None:
                break;
            self.ax.collections.remove(marker)
            self.model.del_marker(marker)
            del marker

    def closeEvent(self, event):
        """
        Close other windows when main window is closed
        """
        self.modelDataV.close()
        self.spectrumSelection.close()

    def create_rectangle(self,ax):
        self.figure.pan_zoom.create_rectangle_ax(ax)

    def change_state_undo_button(self, state):
        """
        Set state of the undo based on the command list size
        """
        self.undoButton.setEnabled(state)

    def update_buttons(self):
        """
        Once the specturm is loaded, set click button by default
        """
        self.clickNormalButton.setChecked(True)
        if self.undoButton.isEnabled():
            self.undoButton.setEnabled(False)
            self.figure.pan_zoom.clear_commands()

    def update_legend(self):
        h, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, h))
        self.ax.legend(by_label.values(), by_label.keys(), loc="upper right", frameon=True, framealpha = 1, facecolor = 'white')

    def update_pan_zoom_data(self):
        """
        When a new spectrum has been loaded, the limits need to be updated,
        and the zoom commands list cleared
        """
        self.figure.pan_zoom.set_axes_limits(self.ax.get_xlim(), self.ax.get_ylim())
        self.figure.pan_zoom.clear_commands()

    def show_file_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Input or file values incorrect")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def generic_alert(self):

        alert = QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n in case \
        of being the error in the extension, it must be blank or .png ")
        alert.exec_()

    def error_reduction_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Zero-size array to reduction operation minimum which has no identity ")
        alert.exec_()
