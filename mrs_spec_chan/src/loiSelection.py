import numpy as np
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import uic


import mrs_spec_chan.src.lineOfInterestSelectionListWidget as loiw
import mrs_spec_chan.src.constants as const
import mrs_spec_chan.src.ui_loi_selection


class MrsLoiList(QDialog, mrs_spec_chan.src.ui_loi_selection.Ui_MrsLoiList):

    def __init__(self, parent=None ):
        super(MrsLoiList, self).__init__(parent)
        self.setupUi(self)

        self.loiListSelected = []

        self.setModal(False)
        self.load_data()
        self.create_bottom_options()

    def create_bottom_options(self):

        self.acceptButton.clicked.connect(self.accept_loi)
        self.cancelButton.clicked.connect(self.cancel_loi)

    def load_data(self):
        for key in const.LOID.keys():
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
        widget = self.sender()

        if widget.checkbox_state:
            self.loiListSelected.append(widget.loi_text())

        else:
            self.loiListSelected.remove(widget.loi_text())


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
        for itemIndex in range(self.loiW.count()):
            item = self.loiW.item(itemIndex)
            itemWidget = self.loiW.itemWidget(item)
            if  itemWidget.loi_text() == i:
                itemWidget.set_checkbox_state(False)
