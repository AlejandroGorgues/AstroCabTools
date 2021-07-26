# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the fit_line tool
"""
import numpy as np
import matplotlib.pyplot as plt

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

import astrocabtools.quick_spec.src.viewers.spectrumSelection as stmS
import astrocabtools.quick_spec.src.ui.ui_quick_spec

from .canvas_interaction.panZoomQuickSpec import figure_pz

from ..io.ascii_load import get_data_from_txt

__all__=["SpecVisualization"]

class SpecVisualization(QMainWindow, astrocabtools.quick_spec.src.ui.ui_quick_spec.Ui_QuickSpec):

    def __init__(self, parent=None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(SpecVisualization, self).__init__(parent)
        self.setupUi(self)

        plt.style.use('seaborn')

        self.initialLimits = {}

        self.spectrumSelection = stmS.SpectrumSelection()
        self.spectrumSelection.finished.connect(self.get_plot)

        #Create the canvas to load the plot
        self.create_middle_plot()

        self.actionLoad_Spec.triggered.connect(self.select_plot)
        self.actionSave_as_png.triggered.connect(self.save_plot_image)

        self.zoomResetButton.clicked.connect(self.zoom_reset)
        self.zoomButton.clicked.connect(self.activate_zoom)
        self.panButton.clicked.connect(self.activate_pan)
        self.clickNormalButton.clicked.connect(self.activate_click)
        self.undoButton.clicked.connect(self.undo_action)

        self.actionReset_window.triggered.connect(self.reset_window)

    def create_middle_plot(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = figure_pz()
        #Subscribe method to setStateUndo event
        pub.subscribe(self.change_state_undo_button,'setStateUndo')

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax = self.figure.add_subplot(111)

        #Create rectangle selector
        self.create_rectangle(self.ax)

        self.ax.set_visible(False)

        self.middlePlot.setLayout(layout)

    def draw_plot_axes(self, wUnits, fUnits):
        """Create the axes"""
        # discards the old graph
        self.ax.clear()

        #Set text and range of the axes
        self.ax.set_xlabel(wUnits)

        self.ax.set_ylabel(fUnits)

        self.ax.grid(True)

    def draw_plot(self):

        self.ax.set_visible(True)


        for i, wCol in enumerate(self.wavelength_cols):

            for fCol in self.fluxList[i]:

            #if col != "Fitted_model":
            #print(col)
            #print(self.fluxList[col], self.wavelength)
                self.ax.plot(wCol, fCol, label=fCol.name)
            #self.ax.plot(self.wavelength, self.fluxList[col])

        self.update_legend()
        self.update_buttons()
        self.update_pan_zoom_data()


        self.figure.tight_layout()

        self.figure.canvas.draw()

    def load_file(self, path):
        """ Load the data from the path and transform the values
        :param string path: path of the file
        """
        try:
            self.wavelength_cols, self.fluxList, wUnits, fUnits = get_data_from_txt(path)
            self.draw_plot_axes(wUnits, fUnits)
            self.draw_plot()
            self.set_interface_state(True)


        except Exception as e:
            self.show_file_alert()

    def set_interface_state(self, state):
        """ Disable or enable the different widgets of the interface
        :param bool state: state that is going to be applied
        """
        self.zoomButton.setEnabled(state)
        self.zoomResetButton.setEnabled(state)
        self.panButton.setEnabled(state)
        self.clickNormalButton.setEnabled(state)

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
                path= self.spectrumSelection.get_data()
                self.load_file(path)
                self.activate_click()
        except Exception as e:
            self.show_file_extension_alert()

    @pyqtSlot()
    def reset_window(self):

        self.set_interface_state(False)
        self.ax.set_visible(False)
        self.figure.canvas.draw()

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

    def closeEvent(self, event):
        """
        Close other windows when main window is closed
        """
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
        self.ax.legend(by_label.values(), by_label.keys(), loc="upper right", frameon=True, framealpha = 1, facecolor = 'white', fontsize='small')

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
