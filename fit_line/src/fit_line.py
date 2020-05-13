# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the fit_line tool
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import weakref
import pandas as pd
from lmfit import Parameters

import sys
import traceback
import io

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QPoint, QEvent
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pubsub import pub

import fit_line.src.panZoom as pz
import fit_line.src.spectrumSelection as stmS
import fit_line.src.txt_transform as tTrans
import fit_line.src.fitting_model_creation as cf
import fit_line.src.pointsData as pdata
import fit_line.src.gaussSelection as gaussS
import fit_line.src.ui_fit_line

class MrsFitLine(QMainWindow, fit_line.src.ui_fit_line.Ui_FitLine):

    def __init__(self, parent=None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(MrsFitLine, self).__init__(parent)
        self.setupUi(self)

        self.microIcon = u"\u03BC"
        self.lambdaIcon = u"\u03BB"
        self.nuIcon = u"\u03BD"



        self.gaussFitResultList = []
        self.markerElementsList = []
        self.fitting_lines = []
        self.currLabels = []
        self.initialLimits = {}
        self.counterState = False

        self.spectrumSelection = stmS.MrsPltList()
        self.gaussSelection = gaussS.MrsFitLineData()

        self.gaussSelection.savePlot.connect(self.save_plot_on_path)

        #Create the canvas to load the plot
        self.create_middle_plot()

        self.loadPltButton.clicked.connect(self.get_plot)

        self.saveButton.clicked.connect(self.save_plot_image)

        self.generationPointsButton.clicked.connect(self.manage_generation_points)

        self.showPointsButton.clicked.connect(self.show_gauss_fit_data)

        self.clearButton.clicked.connect(self.clear_all)
        self.clearLastButton.clicked.connect(self.clear_last_fitting_model)
        self.clearFittingButton.clicked.connect(self.clear_fitting_models)
        self.zoomFitButton.clicked.connect(self.zoom_fit)

        self.zoomButton.toggled.connect(self.activate_zoom)
        self.panButton.toggled.connect(self.activate_pan)
        self.clickNormalButton.toggled.connect(self.activate_click)

        self.undoButton.clicked.connect(self.undoAction)


    def create_middle_plot(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = pz.figure_pz()
        #Subscribe method to setStateUndo event
        pub.subscribe(self.changeStateUndoButton,'setStateUndo')

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax1 = self.figure.add_subplot(111)
        self.click_factory()

        #Create rectangle selector
        self.create_rectangle(self.ax1)

        self.ax1.set_visible(False)

        self.middlePlot.setLayout(layout)
        self.draw_plot_area()

    def show_gauss_selection(self):
        """Show the gauss list dialog"""
        self.gaussSelection.show()
        self.gaussSelection.open()

    def draw_plot_area(self):
        """Create the axes"""
        # discards the old graph
        self.ax1.clear()

        #Set text and range of the axes
        self.ax1.set_xlabel(r'$\mu m$')

        self.ax1.set_ylabel(r'$f_\nu$')

        self.ax1.set_xlim([0, 30])
        self.ax1.set_ylim([0, 20])
        self.ax1.grid()

    def draw_plot(self, redshift, filename):
        """ Draw the plot
        :param list waveL: set of lambdas observed
        :param list fluxL: set of flux
        :param list redshift: redshift value selected
        :param str filename: Path of the spectrum
        """
        self.ax1.cla()
        self.ax1.set_visible(True)

        #Clear all previous lines and markers that do not belong to the spectrum
        for i, line in enumerate(self.ax1.lines):
            self.ax1.lines.pop(i)
            line.remove()

        for i, marker in enumerate(self.ax1.collections):
            self.ax1.collections.pop(i)
            marker.remove()

        #Clear legend list
        self.currLabels.clear()

        self.spectrum = self.ax1.plot(self.wavelength, self.flux, c='#4c72b0',label='Spectrum')
        self.initialLimits["xlim"] = self.ax1.get_xlim()
        self.initialLimits["ylim"] = self.ax1.get_ylim()

        self.update_legend()
        self.update_buttons()
        self.update_pan_zoom_data()

        self.figure.tight_layout()

        self.figure.canvas.draw()

    def load_file(self, path, z):
        """ Load the data from the path and transform the values
        :param string z: redshift value
        :param string path: path of the file
        """
        try:

            self.fitting_lines.clear()
            self.markerElementsList.clear()
            self.wavelength, self.flux, z = tTrans.apply_redshift_to_txt(path, z)


            #Print the plot
            self.draw_plot(z, path)
            self.set_interface_state(True)

        except Exception as e:
            self.show_alert()

    def manage_generation_points(self):
        """If generationPointsButton is pressed, allow to draw the markers
        otherwise, it disallow the option to draw them until generationPointsButton
        is pressed again
        """
        self.generationPointsButton.setText("Cancel the action")

        if self.counterState:
            #Delete previous markers if the user pressed to start to select new points again
            for i in range(self.counter -1):

                marker = next((marker for marker in self.ax1.collections if marker is self.markerElementsList[len(self.markerElementsList)-1]), None)
                self.ax1.collections.remove(marker)
                self.markerElementsList.pop()
                del marker

            self.indicationLabel.setText("")
            self.generationPointsButton.setText("Mark points")
            self.counterState = False
            self.figure.canvas.draw()
        else:
            self.indicationLabel.setText("Mark first continium coordinates")
            self.counter = 1
            self.counterState = True
            self.gaussFitPoints = pdata.pointsData(leftX=0.0,rightX=0.0,topX=0.0,sigma1X=0.0,sigma2X=0.0, leftY=0.0,rightY=0.0,topY=0.0,sigma1Y=0.0,sigma2Y=0.0)

    def show_gauss_fit_data(self):
        self.show_gauss_selection()

    def click_factory(self):
        """ Obtain data where the user clicked
            :param Axis axis: the axis where the user clicked
            :param int index: current axis selected
        """

        #Return click funct to axis
        def click_fun(event):
            if event.inaxes == self.ax1 and event.dblclick:


                if self.counterState == True:
                    xdata = event.xdata
                    ydata = event.ydata

                    self.add_crosshair(xdata, ydata)
                    self.add_data_points(xdata, ydata)
                    self.counter += 1

                else:
                    self.draw_points_alert()
                    self.figure.pan_zoom.enable_rectangle()

            self.figure.canvas.draw()

        #Obtain data on click event
        self.figure.canvas.mpl_connect('button_press_event', lambda event: click_fun(
            event))

    def add_crosshair(self, xdata, ydata):
        """ Draw marker on specified point
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        marker = self.ax1.scatter(xdata, ydata, marker='+', c= 'red')
        self.markerElementsList.append(marker)

    def add_data_points(self, xdata, ydata):
        """ Update specific coordinate values based on order value of counter
        :param float xdata: X coordinate
        :param float ydata: Y coordinate
        """

        if self.counter==1:

            self.gaussFitPoints.leftX = xdata
            self.gaussFitPoints.leftY = ydata
            self.indicationLabel.setText("Mark second continium coordinates")

        elif self.counter==2:

            self.gaussFitPoints.rightX = xdata
            self.gaussFitPoints.rightY = ydata
            self.indicationLabel.setText("Mark first sigma coordinates")

        elif self.counter==3:
            self.gaussFitPoints.sigma1X = xdata
            self.gaussFitPoints.sigma1Y = ydata
            self.indicationLabel.setText("Mark second sigma coordinates")

        elif self.counter==4:
            self.gaussFitPoints.sigma2X = xdata
            self.gaussFitPoints.sigma2Y = ydata
            self.indicationLabel.setText("Mark top (mean and height) coordinates")

        else:

            self.gaussFitPoints.topX = xdata
            self.gaussFitPoints.topY = ydata
            self.indicationLabel.setText("")
            self.counterState=False
            self.draw_figures()
            self.generationPointsButton.setText("Mark points")

    def draw_figures(self):
        self.draw_gauss_curve_fit()


    def draw_gauss_curve_fit(self):
        """ Generate the gauss model, draw the model results based on x value range
        and update the table that shows the results parameters"""

        #Obtain the wavelength values on given range
        wavelengthValues = self.wavelength[(self.wavelength >= self.gaussFitPoints.leftX) & (self.wavelength <= self.gaussFitPoints.rightX)]
        #Obtain de indexes from the initial wavelength array
        #based on the min a max values of the slice made previously
        index1 = np.where(self.wavelength == np.amin(wavelengthValues))
        index2 = np.where(self.wavelength == np.amax(wavelengthValues))
        #Obtain the flux values between the indexes obtained previously
        fluxValues = self.flux[index1[0][0]:(index2[0][0]+1)]

        guesses = Parameters()
        guesses.add(name='a', value = cf.calculate_intercept(cf.calculate_slope(self.gaussFitPoints.leftX,
            self.gaussFitPoints.leftY,self.gaussFitPoints.rightX,self.gaussFitPoints.rightY), self.gaussFitPoints.leftX, self.gaussFitPoints.leftY))
        guesses.add(name='b', value = cf.calculate_slope(self.gaussFitPoints.leftX,
            self.gaussFitPoints.leftY,self.gaussFitPoints.rightX,self.gaussFitPoints.rightY))
        guesses.add(name='h', value = self.gaussFitPoints.topY - (self.gaussFitPoints.leftY + self.gaussFitPoints.rightY)/2.)
        guesses.add(name='c', value = np.mean(wavelengthValues))
        guesses.add(name='sigma', value = abs(self.gaussFitPoints.sigma2X-self.gaussFitPoints.sigma1X)/2.355)
        #Obtain the model
        result = cf.curve_fitting(wavelengthValues, fluxValues, guesses)
        #Update table of results parameters
        self.gaussSelection.add_gauss_data("Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['mean'].value), str(result.params['sigma'].value)))
        self.gaussSelection.add_gauss_data("Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value)))
        gaussFitResultList = [key + " = " + str(result.params[key].value) + " +/- " + str(result.params[key].stderr) for key in result.params]

        #Add item to the gaussSelection list
        for resultParams in gaussFitResultList:
            self.gaussSelection.add_gauss_data("".join(resultParams))

        self.gaussSelection.add_delimiter_line()

        #Draw the plots
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, result.init_fit, 'y--',label='Initial fit')[0])
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, result.best_fit, 'r-',label='Best fit')[0])
        comps = result.eval_components()
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, comps['gauss_fitting_function'], 'k--',label='Fitted gaussian')[0])
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, comps['line_fitting_function'], 'g--',label='Fitted line')[0])

        self.check_repeat_fitting_model_labels()

    def check_repeat_fitting_model_labels(self):
        """
        Check if specified labels have been used befor to not duplicate the legend box
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
        self.generationPointsButton.setEnabled(state)
        self.showPointsButton.setEnabled(state)
        self.saveButton.setEnabled(state)
        self.clearButton.setEnabled(state)
        self.clearLastButton.setEnabled(state)
        self.clearFittingButton.setEnabled(state)
        self.zoomButton.setEnabled(state)
        self.zoomFitButton.setEnabled(state)
        self.panButton.setEnabled(state)
        self.clickNormalButton.setEnabled(state)
        #self.undoButton.setEnabled(state)

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
        plt.savefig(path, dpi = 600, bbox_inches='tight')

    @pyqtSlot()
    def get_plot(self):
        """
        Load dialog that allow to select the spectrum to be loaded
        """
        self.spectrumSelection.show()
        self.spectrumSelection.open()
        if self.spectrumSelection.exec_() == QDialog.Accepted:

            path, redshift = self.spectrumSelection.get_data()
            self.load_file(path, redshift)
        self.figure.canvas.draw()

    @pyqtSlot()
    def clear_last_fitting_model(self):
    """
    Becuase for each model, 4 lines, 5 markers and 4 legends labels are created,
    deleting the last of them requires to delete the ones that has been created with it also
    """
        for i in range(4):
            line = self.fitting_lines[-1]
            self.ax1.lines.remove(line)
            self.fitting_lines.remove(line)
            del line

        for i in range(5):
            marker = self.markerElementsList[-1]
            self.ax1.collections.remove(marker)
            self.markerElementsList.pop()
            del marker
        if len(self.fitting_lines) == 0:
            self.update_legend()
            self.currLabels.clear()
        self.figure.canvas.draw()
        self.gaussSelection.delete_gauss_data()


    @pyqtSlot()
    def clear_fitting_models(self):
        """ Delete only the models and markers from the canvas"""
        for i in range(len(self.fitting_lines)):
            line = next((line for line in self.ax1.lines if line in self.fitting_lines), None)
            if line != None:
                self.ax1.lines.remove(line)
                self.fitting_lines.remove(line)
                del line


        for i in range(len(self.markerElementsList)):
            marker = next((marker for marker in self.ax1.collections), None)
            self.ax1.collections.remove(marker)
            self.markerElementsList.pop()
            del marker
        self.update_legend()
        self.figure.canvas.draw()
        #Delete all list items in the gaussSelection Dialog
        self.gaussSelection.delete_all()
        self.currLabels.clear()


    @pyqtSlot()
    def clear_all(self):

        self.set_interface_state(False)
        self.markerElementsList.clear()
        self.counterState = False
        self.ax1.set_visible(False)
        self.figure.canvas.draw()
        self.gaussSelection.delete_all()
        self.currLabels.clear()

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
    def zoom_fit(self):
        """Zoom to fit the original spectrum size """
        self.ax1.set_xlim(self.initialLimits["xlim"])
        self.ax1.set_ylim(self.initialLimits["ylim"])
        self.figure.canvas.draw()

    @pyqtSlot()
    def undoAction(self):
        self.figure.pan_zoom.undoLastAction()

    def closeEvent(self, event):
        """
        Close other windows when main window is closed
        """
        self.gaussSelection.close()
        self.spectrumSelection.close()

    def create_rectangle(self,ax):
        self.figure.pan_zoom.create_rectangle_ax(ax)

    def changeStateUndoButton(self, state):
        """
        Set state of the undo based on the command list size
        """
        self.undoButton.setEnabled(state)

    def update_buttons(self):
        """
        Once the specturm is loaded, set click button by default
        """
        self.clickNormalButton.setChecked(True)

    def update_legend(self):
        h, labels = self.ax1.get_legend_handles_labels()
        self.ax1.legend(labels=labels, loc="upper right", frameon=True, framealpha = 1, facecolor = 'white')

    def update_pan_zoom_data(self):
        """
        When a new spectrum has been loaded, the limits need to be updated,
        and the zoom commands list cleared
        """
        self.figure.pan_zoom.set_axes_limits(self.initialLimits["xlim"], self.initialLimits["ylim"])
        self.figure.pan_zoom.clear_commands()

    def show_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Input or file values incorrect")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def draw_points_alert(self):

        alert = QMessageBox()
        alert.setText("Error: To fit new points,\n 'draw points' button need to be pressed again")
        alert.exec_()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n in case \
        of being the error in the extension, it must be blank or .txt ")
        alert.exec_()

def main():
    plt.style.use('seaborn')
    app = QApplication(sys.argv)
    mrss = MrsFitLine()
    mrss.setWindowFlags(mrss.windowFlags() |
                        Qt.WindowMinimizeButtonHint |
                        Qt.WindowMaximizeButtonHint |
                        Qt.WindowSystemMenuHint)

    mrss.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
	main()
