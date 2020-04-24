# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import mrs_chan.src.subbandRange as sR


class MrsChanell(QDialog):

    def __init__(self, parent = None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(MrsChanell, self).__init__(parent)

        self.lambdaIcon = u"\u03BC"
        self.microIcon = u"\u03BB"

        #Create the widgets to save and plot the results
        self.create_mid_groupbox()
        self.create_bottom_plot()

        #Add the widgets that allow to insert values
        topLayout = QHBoxLayout()



        lambdaLabel = QLabel("λemit:")
        lambdaUnitLabel = QLabel("μm")
        lambdaEdit = QLineEdit('')
        lambdaEdit.setValidator(QtGui.QDoubleValidator())

        zLabel = QLabel("z:")
        zEdit = QLineEdit('')
        zEdit.setValidator(QtGui.QDoubleValidator())

        #Left, top, right, bottom
        lambdaUnitLabel.setContentsMargins(0,0,40,0)

        chanellButton = QPushButton("Calculate")
        chanellButton.setDefault(True)
        chanellButton.clicked.connect(lambda: self.print_Results(lambdaEdit.text(), zEdit.text()))

        topLayout.addStretch(1)
        topLayout.addWidget(lambdaLabel)
        topLayout.addWidget(lambdaEdit)
        topLayout.addWidget(lambdaUnitLabel)

        topLayout.addWidget(zLabel)
        topLayout.addWidget(zEdit)

        topLayout.addWidget(chanellButton)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()

        #Add 3 rows and 1 column
        #Expand 2 rows and 1 column
        mainLayout.addLayout(topLayout,0,0,1,0)
        mainLayout.addWidget(self.midGroupBox, 1, 0)
        mainLayout.addWidget(self.bottomPlot, 2, 0)

        #Add space between boxes on rows and columns
        mainLayout.setRowStretch(1,0)
        mainLayout.setRowStretch(1,0)
        mainLayout.setColumnStretch(0,0)
        mainLayout.setColumnStretch(1,0)

        self.setLayout(mainLayout)

        self.setWindowTitle("mrs_chan.py")


    def create_mid_groupbox(self):
        """ Create the line edit widgets """
        self.midGroupBox = QGroupBox("Results")

        channellLabel = QLabel("Channel:")
        self.channelEdit = QLineEdit()

        lambdaObsLabel = QLabel("λobs:")
        lambdaObsUnitLabel = QLabel("μm")
        self.lambdaObsEdit = QLineEdit()

        self.channelEdit.setReadOnly(True)
        self.lambdaObsEdit.setReadOnly(True)

        self.channelEdit.setContentsMargins(0, 0, 40, 0)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(channellLabel)
        layout.addWidget(self.channelEdit)

        layout.addWidget(lambdaObsLabel)
        layout.addWidget(self.lambdaObsEdit)
        layout.addWidget(lambdaObsUnitLabel)

        layout.addStretch(1)
        self.midGroupBox.setLayout(layout)

    def create_bottom_plot(self):
        """ Create the canvas where the plot will be drawn """
        self.bottomPlot = QGroupBox("Plot")

        self.figure = Figure()

        # Create the canvas from the figure
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)

        self.ax1.set_visible(False)
        self.ax2.set_visible(False)

        self.bottomPlot.setLayout(layout)

    #Draw the axis
    def draw_plot(self, minL, maxL, chan, lambdaObs):
        """ Draw the plots
        :param int minL: min value of the axis limit
        :param int maxL: max value of the axis limit
        :param string chan: channel where the lambda is located
        :param int lambdaObs: lambda transformed
        """
        try:
            # discards the old graph
            self.ax1.clear()
            self.ax2.clear()


            if len(chan) > 1:
                # create two axis on a canvas with 2 rows, one column and in order

                #Check visibility
                if not self.ax2.get_visible():
                    self.ax1.set_visible(True)
                    self.ax2.set_visible(True)

                #Axis 1
                self.ax1.set_title(chan[0])
                self.ax1.set_xlabel("Wavelength range("+self.lambdaIcon+"m)")
                self.ax1.axvline(x=lambdaObs, color='r', label='\u03BBobs')

                h, labels = self.ax1.get_legend_handles_labels()
                self.ax1.legend(labels=labels, loc="upper right",
                                bbox_to_anchor=(1, 1.5))

                self.ax1.set_xlim([minL[0], maxL[0]])

                self.ax1.get_yaxis().set_visible(False)

                #Axis 2
                self.ax2.set_title(chan[1])
                self.ax2.set_xlabel("Wavelength range("+self.lambdaIcon+"m)")
                self.ax2.axvline(x=lambdaObs, color='r', label=self.microIcon+'obs')

                h, labels = self.ax2.get_legend_handles_labels()
                self.ax2.legend(labels=labels, loc="upper right",
                                bbox_to_anchor=(1, 1.5))

                self.ax2.set_xlim([minL[1], maxL[1]])

                self.ax2.get_yaxis().set_visible(False)

            elif len(chan) == 1:

                # Create axis 1 and hide axis 2

                #Check visibility
                if not self.ax1.get_visible():
                    self.ax1.set_visible(True)

                if self.ax2.get_visible():
                    self.ax2.set_visible(False)

                self.ax1.set_title(chan[0])
                self.ax1.set_xlabel("Wavelength range("+self.lambdaIcon+"m)")
                self.ax1.axvline(x=lambdaObs, color='r',
                                 label=self.microIcon+'obs')

                h, labels = self.ax1.get_legend_handles_labels()
                self.ax1.legend(labels=labels, loc="center left"
                , bbox_to_anchor=(0.8, 1.1))

                self.ax1.set_xlim([minL[0], maxL[0]])

                self.ax1.get_yaxis().set_visible(False)

                self.ax2.set_visible(False)


            self.figure.tight_layout(pad=1)

            self.canvas.draw()
        except:
            self.show_alert()

    def print_Results(self, emit, z):
        """ Calculate the channel and the lambda transformed
        :param string emit: lambda emitted
        :param string z: redshift value
        """
        chan = []
        minL = []
        maxL = []
        try:

            obs = float(emit)*(1+float(z))
            #Obtain the channel of the value and it's subbands
            #If the value is between two channels, the subbands will be on subbands C and A
            #If not obtain it calling function obtain_sub_band() that obtain the subbands inside a channel
            if 4.87 <= obs <= 7.76:
                if obs >= 7.45:
                    channel = "1,2"
                    chan = ['1C', '2A']
                    minL = [6.49, 7.45]
                    maxL = [7.76, 8.90]

                else:
                    channel = '1'
                    chan, minL, maxL = sR.obtain_sub_band(obs, channel)
            elif 7.76 < obs <= 11.87:
                if obs >= 11.47:
                    channel = "2,3"
                    chan = ['2C', '3A']
                    minL = [9.91, 11.47]
                    maxL = [11.87, 13.67]
                else:
                    channel = '2'
                    chan, minL, maxL = sR.obtain_sub_band(obs, channel)
            elif 11.87 < obs <= 18.24:
                if obs >= 17.54:
                    channel = "3,4"
                    chan = ['3C', '4A']
                    minL = [15.30, 17.54]
                    maxL = [18.24, 21.10]
                else:
                    channel = '3'
                    chan, minL, maxL = sR.obtain_sub_band(obs, channel)
            elif 8.24 < obs <= 28.82:
                channel = '4'
                chan, minL, maxL = sR.obtain_sub_band(obs, channel)
            else:
                channel = "Out of range values"

            if channel.isdigit():
                self.channelEdit.setText(','.join(chan))
            else:
                self.channelEdit.setText(channel)
            self.lambdaObsEdit.setText(str(obs))

            self.draw_plot(np.array(minL),  np.array(maxL), np.array(chan), obs)
        except ValueError:
            alert = QMessageBox()
            alert.setText("Error: field formats not valid")
            alert.exec_()



    def show_alert(self, type_err, message):

        alert = QMessageBox()
        alert.setText("Error: incorrect input values")
        alert.setDetailedText(traceback.format_exc(limit=1))
        alert.exec_()

def main():
    plt.style.use('seaborn')
    app = QApplication(sys.argv)
    mrss = MrsChanell()
    mrss.setWindowFlags(mrss.windowFlags() |
                        Qt.WindowMinimizeButtonHint |
                        Qt.WindowMaximizeButtonHint |
                        Qt.WindowSystemMenuHint)
    mrss.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
	main()
