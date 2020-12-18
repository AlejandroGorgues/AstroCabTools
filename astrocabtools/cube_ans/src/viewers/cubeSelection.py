"""
Allow to select the cube to be loaded
"""

import sys
import glob
import traceback
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtGui
from PyQt5 import uic

import astrocabtools.cube_ans.src.ui.ui_cubeSelection

class CubeList(QDialog, astrocabtools.cube_ans.src.ui.ui_cubeSelection.Ui_cubeSelection):

    def __init__(self, parent = None):
        super(CubeList, self).__init__(parent)
        self.setupUi(self)

        self.extension = "*.fits"

        self.cubeSelectionButton.clicked.connect(self.load_directory)

    @pyqtSlot()
    def load_directory(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("files ({})".format(self.extension))

        if fileSearch.exec():
            self.cubePath = fileSearch.selectedFiles()[0]
            self.filePathLabel.setText(self.cubePath)
            self.set_interface_state(True)

    def get_data(self):
        return self.cubePath

    def reset_widget(self):
        self.filePathLabel.setText("")
        self.cubePath = ""
        self.set_interface_state(False)

    def set_interface_state(self, state):
        """ Disable or enble the widgets of the interface
            :param bool state: state that is going to be applied
        """
        self.acceptButton.setEnabled(state)
        self.cancelButton.setEnabled(state)
