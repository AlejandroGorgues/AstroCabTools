"""
Allow to select the cube to be loaded
"""

import sys
import glob
import traceback
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QIdentityProxyModel
from PyQt5 import QtGui
from PyQt5 import uic

from .cubeFileDialogProxyModel import ProxyModel

import astrocabtools.mrs_subviz.src.ui.ui_cubeLoader

class CubeLoader(QDialog, astrocabtools.mrs_subviz.src.ui.ui_cubeLoader.Ui_cubeLoader):

    def __init__(self, parent = None):
        super(CubeLoader, self).__init__(parent)
        self.setupUi(self)

        self.extension = "*.fits"

        self.subbandComboBox.currentIndexChanged.connect(self.subband_selection)
        self.selectFileButton.clicked.connect(self.load_file)
        self.selectDirectoryButton.clicked.connect(self.load_directory)
        self.subband = 0
        self.cubePath = None

        self.filterPath = ""

    def load_file(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("files ({})".format(self.extension))

        if fileSearch.exec():
            self.cubePath = fileSearch.selectedFiles()[0]
            self.filePathLabel.setText(self.cubePath)
            self.set_interface_state(True)

    def load_directory(self):
        directorySearch = QFileDialog()
        directorySearch.setFileMode(QFileDialog.Directory)
        directorySearch.setOption(QFileDialog.DontUseNativeDialog, True)
        proxy = ProxyModel(directorySearch)
        directorySearch.setProxyModel(proxy)
        if directorySearch.exec_():
            self.directoryPath = directorySearch.selectedFiles()

            self.filterPath = f'{self.directoryPath[0]}/*.fits'
            self.filePathLabel.setText(self.filterPath)
            self.set_interface_state(True)

    def subband_selection(self, index):
        self.subband = index

    def get_data(self):
        if self.filterPath != "":
            self.cubePath = [f for f in glob.glob(self.filterPath)]
            self.filterPath = ""
            return self.cubePath, None
        else:
            return self.cubePath, self.subband

    def reset_widget(self):
        self.filePathLabel.setText("")
        self.cubePath = None
        self.subband = 0
        self.subbandComboBox.setCurrentIndex(0)
        self.set_interface_state(False)

    def set_interface_state(self, state):
        """ Disable or enble the widgets of the interface
            :param bool state: state that is going to be applied
        """
        self.acceptButton.setEnabled(state)
