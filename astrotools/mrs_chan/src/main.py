# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from .viewers.mrs_chan import MrsChanell

def main():

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
