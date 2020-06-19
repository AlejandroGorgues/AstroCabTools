# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from .viewers.mrs_det_plot import MrsDetPlot

def main():
    app = QApplication(sys.argv)
    mrss = MrsDetPlot()
    mrss.setWindowFlags(mrss.windowFlags() |
                        Qt.WindowMinimizeButtonHint |
                        Qt.WindowMaximizeButtonHint |
                        Qt.WindowSystemMenuHint)
    mrss.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
	main()
