"""
Object that contain each widget from the list widget and it's corresponding
methods
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QIdentityProxyModel
from PyQt5 import uic


import astrocabtools.mrs_spec_chan.src.viewers.spectrumSelectionListWidget as pltw

import astrocabtools.mrs_spec_chan.src.ui.ui_spectrum_selection

from ..utils.fileDialogProxyModel import ProxyModel


class MrsSpctrmList(QDialog, astrocabtools.mrs_spec_chan.src.ui.ui_spectrum_selection.Ui_MrsSpctrmList):

    def __init__(self, parent=None ):
        super(MrsSpctrmList, self).__init__(parent)
        self.setupUi(self)

        self.setMinimumSize(500,500)
        self.pltDictSelected = {}
        self.directoryPath = []

        self.setModal(False)
        self.fileButton.clicked.connect(self.load_directory)

    def add_spectrum(self, key):

        it = QListWidgetItem()

        self.spectraListWidget.addItem(it)
        widget = pltw.spectrumListWidget(title = key)
        widget.checked.connect(self.check_spectrum)
        widget.changed.connect(self.modified_line_edit)

        self.spectraListWidget.setItemWidget(it, widget)

        it.setSizeHint(widget.sizeHint())

    @pyqtSlot()
    def load_directory(self):
        self.spectraListWidget.clear()
        directorySearch = QFileDialog()
        directorySearch.setFileMode(QFileDialog.Directory)
        directorySearch.setOption(QFileDialog.DontUseNativeDialog, True)
        proxy = ProxyModel(directorySearch)
        directorySearch.setProxyModel(proxy)

        if directorySearch.exec_():
            self.directoryPath = directorySearch.selectedFiles()

            filterPath = f'{self.directoryPath[0]}/*.txt'

            [self.add_spectrum(f) for f in glob.glob(filterPath)]

            self.check_state_spec()

    @pyqtSlot()
    def check_spectrum(self):
        widget = self.sender()

        if widget.checkbox_state():

            self.pltDictSelected[widget.path_text()] = widget.redshift_value()

        else:

            widget.set_redshift_value('')

    @pyqtSlot()
    def modified_line_edit(self):
        widget = self.sender()

        if widget.checkbox_state() == True and widget.redshift_value() != '':

            self.pltDictSelected[widget.path_text()] = widget.redshift_value()

        if widget.redshift_value() == '':

            widget.set_checkbox_state(False)
            widget.set_checkbox_checked(False)
            key = self.pltDictSelected.pop(widget.path_text(), None)
            del key
        else:
            widget.set_checkbox_state(True)

    def check_state_spec(self):
        for i in range(self.spectraListWidget.count()):
            item = self.spectraListWidget.item(i)
            itemWidget = self.spectraListWidget.itemWidget(item)
            if itemWidget.path_text() in self.pltDictSelected.keys():
                itemWidget.set_redshift_value(self.pltDictSelected[itemWidget.path_text()])
                itemWidget.set_checkbox_checked(True)

    def reload_directory(self):
        if self.directoryPath:

            self.spectraListWidget.clear()
            filterPath = f'{self.directoryPath[0]}/*.txt'
            [self.add_spectrum(f) for f in glob.glob(filterPath)]

    def get_data(self):
        return self.pltDictSelected

    def clear_list(self):
        self.pltDictSelected.clear()

    def uncheck_list(self):

        for itemIndex in range(self.spectraListWidget.count()):
            item = self.spectraListWidget.item(itemIndex)
            itemWidget = self.spectraListWidget.itemWidget(item)
            itemWidget.set_redshift_value('')
