# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from .viewers.cube_ans import CubeAns

def main():
    app = QApplication(sys.argv)
    cbans = CubeAns()
    cbans.setWindowFlags(cbans.windowFlags() |
                         Qt.WindowMinimizeButtonHint |
                         Qt.WindowMaximizeButtonHint |
                         Qt.WindowSystemMenuHint)
    cbans.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
