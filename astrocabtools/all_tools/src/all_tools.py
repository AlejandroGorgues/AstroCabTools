# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the all_tools tool
"""
import sys
import traceback
import io

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

import mrs_chan
import mrs_spec_chan
import mrs_det_plot
import fit_line

import astrocabtools.all_tools.src.ui.ui_all_tools
import astrocabtools.mrs_chan.src.viewers.mrs_chan as chan
import astrocabtools.fit_line.src.viewers.fit_line as fitLine
import astrocabtools.mrs_spec_chan.src.viewers.mrs_spec_chan as specChan
import astrocabtools.mrs_det_plot.src.viewers.mrs_det_plot as detPlot

class AllTools(QMainWindow, astrocabtools.all_tools.src.ui.ui_all_tools.Ui_all_tools):

    def __init__(self, parent=None):
        """Initializer
        :param Class parent: The parent that inherits the interface.
        """
        super(AllTools, self).__init__(parent)
        self.setupUi(self)

        self.mrsChanButton.clicked.connect(self.load_mrs_chan)
        self.mrsSpecChanButton.clicked.connect(self.load_mrs_spec_chan)
        self.mrsDetPlotButton.clicked.connect(self.load_mrs_det_plot)
        self.fitLineButton.clicked.connect(self.load_fit_line)

        self.mrsChan = None
        self.mrsSpecChan = None
        self.mrsDetPlot = None
        self.fitLine = None

    @pyqtSlot()
    def load_mrs_chan(self):
        self.mrsChan = chan.MrsChanell()
        self.mrsChan.show()

    @pyqtSlot()
    def load_mrs_spec_chan(self):
        self.mrsSpecChan = specChan.MrsSpecChanell()
        self.mrsSpecChan.show()

    @pyqtSlot()
    def load_mrs_det_plot(self):
        self.mrsDetPlot = detPlot.MrsDetPlot()
        self.mrsDetPlot.show()

    @pyqtSlot()
    def load_fit_line(self):
        self.fitLine = fitLine.MrsFitLine()
        self.fitLine.show()

    def closeEvent(self, event):
        if isinstance(self.mrsChan, astrocabtools.mrs_chan.src.viewers.mrs_chan.MrsChanell):
            self.mrsChan.close()
        if isinstance(self.mrsSpecChan, astrocabtools.mrs_spec_chan.src.viewers.mrs_spec_chan.MrsSpecChanell):
            self.mrsSpecChan.close()
        if isinstance(self.mrsDetPlot, astrocabtools.mrs_det_plot.src.viewers.mrs_det_plot.MrsDetPlot):
            self.mrsDetPlot.close()
        if isinstance(self.fitLine, astrocabtools.fit_line.src.viewers.fit_line.MrsFitLine):
            self.fitLine.close()

def main():
    plt.style.use('seaborn')
    app = QApplication(sys.argv)
    mrss = AllTools()
    mrss.setWindowFlags(mrss.windowFlags() |
                        Qt.WindowMinimizeButtonHint |
                        Qt.WindowMaximizeButtonHint |
                        Qt.WindowSystemMenuHint)

    mrss.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
	main()
