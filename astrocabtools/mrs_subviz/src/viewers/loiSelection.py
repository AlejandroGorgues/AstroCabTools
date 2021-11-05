"""
Object that contain each line of interest widget from the list widget and it's corresponding
methods
"""
import numpy as np
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import uic
from PyQt5 import QtGui


import astrocabtools.mrs_subviz.src.viewers.lineOfInterestSelectionListWidget as loiw

from ..utils.constants import LOID

import astrocabtools.mrs_subviz.src.ui.ui_loiSelection


class LoiSelection(QDialog, astrocabtools.mrs_subviz.src.ui.ui_loiSelection.Ui_loiSelection):

    def __init__(self, parent=None ):
        super(LoiSelection, self).__init__(parent)
        self.setupUi(self)

        self.loiListSelected = []
        self.redshiftLineEdit.setValidator(QtGui.QDoubleValidator())

        self.setModal(False)
        self.load_data()

    def load_data(self):
        for key, value in LOID.items():
            loidInfo = value[0]+": "+str(key)
            self.add_loi(loidInfo)

    def add_loi(self, key):

        it = QListWidgetItem()
        self.loiW.addItem(it)
        widget = loiw.loiListwidget(title = key)
        widget.checked.connect(self.check_loi)
        self.loiW.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())

    @pyqtSlot()
    def check_loi(self):
        """Append or remove data base on checkbox state"""
        widget = self.sender()

        if widget.checkbox_state:
            self.loiListSelected.append(widget.loi_text())

        else:
            self.loiListSelected.remove(widget.loi_text())

    def get_list(self):

        for i in self.loiListSelected:
            self.uncheck_list(i)
        return self.loiListSelected

    def get_redshift(self):
        redshift = self.redshiftLineEdit.text()
        if redshift == '':
            return 0
        else:
            return redshift

    def clear_list(self):
        self.loiListSelected.clear()

    def uncheck_list(self, i):
        for itemIndex in range(self.loiW.count()):
            item = self.loiW.item(itemIndex)
            itemWidget = self.loiW.itemWidget(item)
            if  itemWidget.loi_text() == i:
                itemWidget.set_checkbox_state(False)
