import numpy as np
import matplotlib.pyplot as plt

import sys
import glob
from os.path import expanduser

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot,QIdentityProxyModel


import mrs_spec_chan.src.spectrumSelectionListWidget as pltw
import mrs_spec_chan.src.fileDialogProxyModel as proxyModel


class MrsPltList(QDialog):

    def __init__(self, parent=None ):
        super(MrsPltList, self).__init__(parent)

        self.setMinimumSize(500,500)
        self.pltDictSelected = {}
        self.directoryPath = []

        self.setModal(False)
        self.create_plt_list()
        self.create_bottom_options()

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.pltList,  0, 0)
        mainLayout.addWidget(self.buttomOpt, 1,0)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setColumnStretch(0, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle("mrs_spec_chan_plt")

    def create_plt_list(self):
        self.pltList = QGroupBox("Spectra")

        plt_vbox = QVBoxLayout()

        self.fileButton = QPushButton("Select Directory")
        self.plotListWidget = QListWidget()
        self.fileButton.clicked.connect(self.load_directory)

        plt_vbox.addWidget(self.fileButton)
        plt_vbox.addWidget(self.plotListWidget)

        self.pltList.setLayout(plt_vbox)

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

    def add_plt(self, key):

        it = QListWidgetItem()

        self.plotListWidget.addItem(it)
        widget = pltw.spectrumListWidget(title = key)
        widget.checked.connect(self.check_plt)
        widget.changed.connect(self.modified_line_edit)

        self.plotListWidget.setItemWidget(it, widget)

        it.setSizeHint(widget.sizeHint())

    @pyqtSlot()
    def load_directory(self):
        self.plotListWidget.clear()
        directorySearch = QFileDialog()
        directorySearch.setFileMode(QFileDialog.Directory)
        directorySearch.setOption(QFileDialog.DontUseNativeDialog, True)
        proxy = proxyModel.ProxyModel(directorySearch)
        directorySearch.setProxyModel(proxy)

        if directorySearch.exec_():
            self.directoryPath = directorySearch.selectedFiles()

            filterPath = f'{self.directoryPath[0]}/*.txt'

            [self.add_plt(f) for f in glob.glob(filterPath)]

            self.check_state_spec()

    @pyqtSlot()
    def check_plt(self):
        widget = self.sender()

        if widget.checkbox_state:

            self.pltDictSelected[widget.path_text] = widget.redshift_value

        else:

            widget.set_redshift_value('')

    @pyqtSlot()
    def modified_line_edit(self):
        widget = self.sender()

        if widget.checkbox_state == True and widget.redshift_value != '':
            self.pltDictSelected[widget.path_text] = widget.redshift_value

        if widget.redshift_value == '':

            widget.set_checkbox_state(False)
            widget.set_checkbox_checked(False)
            key = self.pltDictSelected.pop(widget.path_text, None)
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
        for i in range(self.plotListWidget.count()):
            item = self.plotListWidget.item(i)
            itemWidget = self.plotListWidget.itemWidget(item)
            if itemWidget.path_text in self.pltDictSelected.keys():
                itemWidget.set_redshift_value(self.pltDictSelected[itemWidget.path_text])
                itemWidget.set_checkbox_checked(True)

    def reload_directory(self):
        if self.directoryPath:

            self.plotListWidget.clear()
            filterPath = f'{self.directoryPath[0]}/*.txt'
            [self.add_plt(f) for f in glob.glob(filterPath)]

    def get_data(self):
        return self.pltDictSelected

    def clear_list(self):
        self.pltDictSelected.clear()

    def uncheck_list(self):

        for itemIndex in range(self.plotListWidget.count()):
            item = self.plotListWidget.item(itemIndex)
            itemWidget = self.plotListWidget.itemWidget(item)
            itemWidget.set_redshift_value('')
