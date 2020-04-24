import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
import pathlib
from os.path import expanduser
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QIdentityProxyModel


import mrs_spec_chan.src.spectrumSelectionListWidget as pltw
import mrs_spec_chan.src.fileDialogProxyModel as proxyModel


class MrsTmpltList(QDialog):

    def __init__(self, parent=None ):
        super(MrsTmpltList, self).__init__(parent)

        self.setMinimumSize(500,500)
        self.tmpltDictSelected = {}

        self.setModal(False)
        self.create_tmplt_list()
        self.create_bottom_options()

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.tmpltList,  0, 0)
        mainLayout.addWidget(self.buttomOpt, 1,0)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setColumnStretch(0, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle("mrs_spec_chan_plt")

    def create_tmplt_list(self):
        self.tmpltList = QGroupBox("Spectra")

        plt_vbox = QVBoxLayout()

        self.templateListWidget = QListWidget()
        self.load_directory()

        plt_vbox.addWidget(self.templateListWidget)

        self.tmpltList.setLayout(plt_vbox)

    def create_bottom_options(self):
        self.buttomOpt = QGroupBox("Options")

        options_hbox = QHBoxLayout()
        self.acceptButton = QPushButton("Accept")
        self.cancelButton = QPushButton("Cancel")

        self.acceptButton.clicked.connect(self.accept_plt)
        self.cancelButton.clicked.connect(self.cancel_plt)

        options_hbox.addWidget(self.acceptButton)
        options_hbox.addWidget(self.cancelButton)

        self.buttomOpt.setLayout(options_hbox)

    def add_tmplt(self, key):

        it = QListWidgetItem()

        self.templateListWidget.addItem(it)
        widget = pltw.spectrumListWidget(title = key)
        widget.checked.connect(self.check_plt)
        widget.changed.connect(self.modified_line_edit)

        self.templateListWidget.setItemWidget(it, widget)

        it.setSizeHint(widget.sizeHint())

    def load_directory(self):

        filterPath = str(os.path.dirname(os.path.realpath(__file__))) + '/templates/*.txt'

        [self.add_tmplt(f) for f in glob.glob(filterPath)]

        self.check_state_spec()

    @pyqtSlot()
    def check_plt(self):
        widget = self.sender()

        if widget.checkbox_state:

            self.tmpltDictSelected[widget.path_text] = widget.redshift_value

        else:

            widget.set_redshift_value('')

    @pyqtSlot()
    def modified_line_edit(self):
        widget = self.sender()

        if widget.checkbox_state == True and widget.redshift_value != '':
            self.tmpltDictSelected[widget.path_text] = widget.redshift_value

        if widget.redshift_value == '':

            widget.set_checkbox_state(False)
            widget.set_checkbox_checked(False)
            key = self.tmpltDictSelected.pop(widget.path_text, None)
            del key
        else:
            widget.set_checkbox_state(True)

    @pyqtSlot()
    def accept_plt(self):
        self.accept()

    @pyqtSlot()
    def cancel_plt(self):
        self.reject()

    def check_state_spec(self):
        for i in range(self.templateListWidget.count()):
            item = self.templateListWidget.item(i)
            itemWidget = self.templateListWidget.itemWidget(item)
            if itemWidget.path_text in self.tmpltDictSelected.keys():
                itemWidget.set_redshift_value(self.tmpltDictSelected[itemWidget.path_text])
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
