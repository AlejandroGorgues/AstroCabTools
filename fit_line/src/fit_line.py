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

    def create_middle_plot(self):
        """ Create the canvas to draw the plot"""

        self.figure, self.figure.canvas = pz.figure_pz()

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.figure.canvas.setFocusPolicy(Qt.ClickFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.figure.canvas)

        self.ax1 = self.figure.add_subplot(111)
        self.click_factory()

        self.ax1.set_visible(False)

        self.middlePlot.setLayout(layout)
        self.draw_plot_area()

    def show_gauss_selection(self):
        """SHow the gauss list dialog"""
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

        for i, line in enumerate(self.ax1.lines):
            self.ax1.lines.pop(i)
            line.remove()

        for i, marker in enumerate(self.ax1.collections):
            self.ax1.collections.pop(i)
            marker.remove()

        self.spectrum = self.ax1.plot(self.wavelength, self.flux, c='#4c72b0')

        self.figure.tight_layout(pad = 2)

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

        #Calculate initial guesses based on previous points selected
        slope = cf.calculate_slope(self.gaussFitPoints.leftX, self.gaussFitPoints.leftY,self.gaussFitPoints.rightX,self.gaussFitPoints.rightY)
        intercept = cf.calculate_intercept(slope, self.gaussFitPoints.leftX, self.gaussFitPoints.leftY)

        sigma = abs(self.gaussFitPoints.sigma2X-self.gaussFitPoints.sigma1X)/2.355
        #mean = self.gaussFitPoints.topX
        mean = np.mean(wavelengthValues)
        height = self.gaussFitPoints.topY - (self.gaussFitPoints.leftY + self.gaussFitPoints.rightY)/2.

        guesses = Parameters()
        guesses.add(name='a', value = intercept)
        guesses.add(name='b', value = slope)
        guesses.add(name='h', value = height)
        guesses.add(name='c', value = mean)
        guesses.add(name='sigma', value = sigma)
        #Obtain the model
        result = cf.curve_fitting(wavelengthValues, fluxValues, guesses)
        #Update table of results parameters
        self.gaussSelection.add_gauss_data("Gauss model: {} * e ** ((x-{})**2/(-2*{}**2))".format(str(result.params['h'].value), str(result.params['mean'].value), str(result.params['sigma'].value)))
        self.gaussSelection.add_gauss_data("Line model: {} + {} * x".format(str(result.params['a'].value), str(result.params['b'].value)))
        gaussFitResultList = [key + " = " + str(result.params[key].value) + " +/- " + str(result.params[key].stderr) for key in result.params]

        for resultParams in gaussFitResultList:
            self.gaussSelection.add_gauss_data("".join(resultParams))

        self.gaussSelection.add_delimiter_line()

        #Draw the components
        """for x in wavelengthValues:
            cf.gauss_curve_fitting_function(x, intercept, slope, height, mean, sigma)"""
        """self.ax1.plot(wavelengthValues, cf.line_fitting_function(wavelengthValues, intercept, slope, mean) +
         cf.gauss_fitting_function(wavelengthValues, height, mean, sigma), 'y--')"""
        #self.ax1.plot(wavelengthValues, result.init_fit, 'y--')
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, result.init_fit, 'y--')[0])
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, result.best_fit, 'r-')[0])
        comps = result.eval_components()
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, comps['gauss_fitting_function'], 'k--')[0])
        self.fitting_lines.append(self.ax1.plot(wavelengthValues, comps['line_fitting_function'], 'g--')[0])


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


    def resize_event(self, event):
        QWidget.resize_event(self, event)
        self.figure.tight_layout(pad=2)

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
        self.spectrumSelection.show()
        self.spectrumSelection.open()
        if self.spectrumSelection.exec_() == QDialog.Accepted:

            path, redshift = self.spectrumSelection.get_data()
            self.load_file(path, redshift)
        self.figure.canvas.draw()

    @pyqtSlot()
    def clear_last_fitting_model(self):

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
        self.figure.canvas.draw()
        self.gaussSelection.delete_all()

    @pyqtSlot()
    def clear_all(self):

        self.set_interface_state(False)
        self.markerElementsList.clear()
        self.counterState = False
        self.ax1.set_visible(False)
        self.figure.canvas.draw()
        self.gaussSelection.delete_all()

    def closeEvent(self, event):
        self.gaussSelection.close()
        self.spectrumSelection.close()

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
