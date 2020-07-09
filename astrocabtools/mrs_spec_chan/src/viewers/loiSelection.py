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


import astrocabtools.mrs_spec_chan.src.viewers.lineOfInterestSelectionListWidget as loiw

from ..utils.constants import LOID

import astrocabtools.mrs_spec_chan.src.ui.ui_loi_selection


class MrsLoiList(QDialog, astrocabtools.mrs_spec_chan.src.ui.ui_loi_selection.Ui_MrsLoiList):

    def __init__(self, parent=None ):
        super(MrsLoiList, self).__init__(parent)
        self.setupUi(self)

        self.loiListSelected = []

        self.setModal(False)
        self.load_data()

    def load_data(self):
        for key in LOID.keys():
            self.add_loi(key)

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

    def clear_list(self):
        self.loiListSelected.clear()

    def uncheck_list(self, i):
        for itemIndex in range(self.loiW.count()):
            item = self.loiW.item(itemIndex)
            itemWidget = self.loiW.itemWidget(item)
            if  itemWidget.loi_text() == i:
                itemWidget.set_checkbox_state(False)
