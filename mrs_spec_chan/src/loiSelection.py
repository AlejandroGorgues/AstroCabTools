import numpy as np
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot


import mrs_spec_chan.src.lineOfInterestSelectionListWidget as loiw
import mrs_spec_chan.src.constants as const


class MrsLoiList(QDialog):

    def __init__(self, parent=None ):
        super(MrsLoiList, self).__init__(parent)

        self.loiListSelected = []

        self.setModal(False)
        self.create_loi_list()
        self.create_bottom_options()

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.loiList,  0, 0)
        mainLayout.addWidget(self.buttomOpt, 1,0)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setColumnStretch(0, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle("mrs_spec_chan_loi")


    def create_loi_list(self):
        self.loiList = QGroupBox("Lines of interest")

        list_vbox = QVBoxLayout()
        self.loiLW = QListWidget()

        list_vbox.addWidget(self.loiLW)

        self.load_data()

        self.loiList.setLayout(list_vbox)

    def create_bottom_options(self):
        self.buttomOpt = QGroupBox("Options")

        options_hbox = QHBoxLayout()
        self.acceptButton = QPushButton("Accept")
        self.cancelButton = QPushButton("Cancel")

        self.acceptButton.clicked.connect(self.accept_loi)
        self.cancelButton.clicked.connect(self.cancel_loi)

        options_hbox.addWidget(self.acceptButton)
        options_hbox.addWidget(self.cancelButton)


        self.buttomOpt.setLayout(options_hbox)

    def load_data(self):
        for key in const.LOID.keys():
            self.add_loi(key)

    def add_loi(self, key):

        it = QListWidgetItem()
        self.loiLW.addItem(it)
        widget = loiw.loiListwidget(title = key)
        widget.checked.connect(self.check_loi)
        self.loiLW.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())

    @pyqtSlot()
    def check_loi(self):
        widget = self.sender()

        if widget.checkbox_state:
            self.loiListSelected.append(widget.loi_text)

        else:
            self.loiListSelected.remove(widget.loi_text)


    @pyqtSlot()
    def accept_loi(self):
        self.accept()

    @pyqtSlot()
    def cancel_loi(self):
        self.reject()

    def get_list(self):

        for i in self.loiListSelected:
            self.uncheck_list(i)
        return self.loiListSelected

    def clear_list(self):
        self.loiListSelected.clear()

    def uncheck_list(self, i):
        for itemIndex in range(self.loiLW.count()):
            item = self.loiLW.item(itemIndex)
            itemWidget = self.loiLW.itemWidget(item)
            if  itemWidget.loi_text == i:
                itemWidget.set_checkbox_state(False)
