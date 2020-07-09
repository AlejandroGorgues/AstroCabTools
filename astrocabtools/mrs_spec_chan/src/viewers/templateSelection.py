"""
Object that contains the defult spectrum files that are avaliable to select
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
import pathlib
from os.path import expanduser
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import uic


import astrocabtools.mrs_spec_chan.src.viewers.spectrumSelectionListWidget as pltw
import astrocabtools.mrs_spec_chan.src.ui.ui_template_selection


class MrsTmpltList(QDialog, astrocabtools.mrs_spec_chan.src.ui.ui_template_selection.Ui_MrsTmpltList):

    def __init__(self, parent=None ):
        super(MrsTmpltList, self).__init__(parent)
        self.setupUi(self)

        self.setMinimumSize(500,500)
        self.tmpltDictSelected = {}

        self.setModal(False)
        self.load_directory()

    def add_tmplt(self, key):

        it = QListWidgetItem()
        self.templateListWidget.addItem(it)
        widget = pltw.spectrumListWidget(title = key)
        widget.checked.connect(self.check_spectrum)
        widget.changed.connect(self.modified_line_edit)

        self.templateListWidget.setItemWidget(it, widget)

        it.setSizeHint(widget.sizeHint())

    def load_directory(self):

        filterPath = str(os.path.dirname(os.path.realpath(__file__))) + '/templates/*.txt'

        [self.add_tmplt(f) for f in glob.glob(filterPath)]

        self.check_state_spec()

    @pyqtSlot()
    def check_spectrum(self):
        widget = self.sender()

        if widget.checkbox_state():

            self.tmpltDictSelected[widget.path_text()] = widget.redshift_value()

        else:

            widget.set_redshift_value('')

    @pyqtSlot()
    def modified_line_edit(self):
        widget = self.sender()

        if widget.checkbox_state() == True and widget.redshift_value() != '':
            self.tmpltDictSelected[widget.path_text()] = widget.redshift_value()

        if widget.redshift_value() == '':

            widget.set_checkbox_state(False)
            widget.set_checkbox_checked(False)
            key = self.tmpltDictSelected.pop(widget.path_text(), None)
            del key
        else:
            widget.set_checkbox_state(True)

    def check_state_spec(self):
        for i in range(self.templateListWidget.count()):
            item = self.templateListWidget.item(i)
            itemWidget = self.templateListWidget.itemWidget(item)
            if itemWidget.path_text() in self.tmpltDictSelected.keys():
                itemWidget.set_redshift_value(self.tmpltDictSelected[itemWidget.path_text()])
                itemWidget.set_checkbox_checked(True)

    def get_data(self):
        return self.tmpltDictSelected

    def clear_list(self):
        self.tmpltDictSelected.clear()

    def uncheck_list(self):

        for itemIndex in range(self.templateListWidget.count()):
            item = self.templateListWidget.item(itemIndex)
            itemWidget = self.templateListWidget.itemWidget(item)
            itemWidget.set_redshift_value('')
