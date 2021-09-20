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
        self.customSubbandCheckBox.stateChanged.connect(self.custom_subband_activation)

        self.subband = 0
        self.cubePath = None

        self.directoryPath = ""

        self.useCustomSubband = False

    def load_file(self):
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("files ({})".format(self.extension))

        if fileSearch.exec():
            self.cubePath = fileSearch.selectedFiles()[0]
            self.filePathLabel.setText(self.cubePath)

            self.set_interface_state(True)

            self.filterLineEdit.setEnabled(False)
            self.filterLabel.setEnabled(False)
            self.filterLineEdit.setText("")

            self.directoryPath = ""
            self.customSubbandCheckBox.setEnabled(True)

    def load_directory(self):
        directorySearch = QFileDialog()
        directorySearch.setFileMode(QFileDialog.Directory)
        directorySearch.setOption(QFileDialog.DontUseNativeDialog, True)
        proxy = ProxyModel(directorySearch)
        directorySearch.setProxyModel(proxy)
        if directorySearch.exec_():
            self.directoryPath = directorySearch.selectedFiles()

            self.filePathLabel.setText(self.directoryPath[0])

            self.set_interface_state(True)
            self.customSubbandCheckBox.setEnabled(False)



    def subband_selection(self, index):
        self.subband = index


    def custom_subband_activation(self):
        if self.customSubbandCheckBox.isChecked():
            self.useCustomSubband = True
        else:
            self.useCustomSubband = False

    def get_data(self):
        #If a directory is gonna be loaded instead of a single file
        if self.directoryPath != "":
            if self.filterLineEdit.text() != "":
                filterPath = f'{self.directoryPath[0]}/'+ self.filterLineEdit.text()
                self.filePathLabel.setText(filterPath)

            else:
                filterPath = f'{self.directoryPath[0]}/*.fits'
                self.filePathLabel.setText(filterPath)

            self.cubePath = [f for f in glob.glob(filterPath)]

            #If the list is empty, throw error
            if not self.cubePath:
                raise Exception("There are no files associated with the filter")

            self.directoryPath = ""
            return self.cubePath, None

        #If a single file is gonna be loaded
        else:
            if self.useCustomSubband:
                return self.cubePath, self.subband
            else:
                return self.cubePath, None

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
        self.filterLineEdit.setEnabled(state)
        self.filterLabel.setEnabled(state)
