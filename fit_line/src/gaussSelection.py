"""
Object that show data related to each fitting
"""
import numpy as np
import matplotlib.pyplot as plt

import sys
import re
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal
from PyQt5 import uic


import fit_line.src.gaussDataCreatedListWidget as gausslw
import fit_line.src.ui_gaussSelection


class MrsFitLineData(QDialog, fit_line.src.ui_gaussSelection.Ui_gaussSelection):
    savePlot = pyqtSignal(str)

    def __init__(self, parent=None ):
        super(MrsFitLineData, self).__init__(parent)
        self.setupUi(self)

        self.gaussDataCreated = []

        self.setModal(False)

        self.saveButton.clicked.connect(self.save_data)

    def add_gauss_data(self, data):
        """
        Add model data to the list widget
        :param str data: data obtained from the model
        """
        if self.gaussListWidget.count() > 0:
            self.saveButton.setEnabled(True)

        it = QListWidgetItem()
        self.gaussListWidget.addItem(it)
        widget = gausslw.gaussListwidget(text = data)
        self.gaussListWidget.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())
        it.setFlags(Qt.NoItemFlags)

        self.gaussDataCreated.append(data)

    def add_delimiter_line(self):
        it = QListWidgetItem()

        self.gaussListWidget.addItem(it)
        widget = QFrame()
        widget.setFrameShape(QFrame.HLine)
        it.setSizeHint(widget.sizeHint())
        it.setFlags(Qt.NoItemFlags)
        self.gaussListWidget.setItemWidget(it, widget)

        self.gaussDataCreated.append("----------------------------------------------------")

    def delete_gauss_data(self):
        for i in range(9):
            item = self.gaussListWidget.takeItem(self.gaussListWidget.count()-1)
            del item

    def delete_all(self):
        self.gaussListWidget.clear()

    @pyqtSlot()
    def save_data(self):
        """ Save the data as txt file and an image of current figure zoom.
        If the extension is different from .txt or is it blank, it throws an error
        """
        try:
            fileSave = QFileDialog()
            fileSave.setNameFilter("txt files (*.txt)")
            name = fileSave.getSaveFileName(self, 'Save File')
            if name[0] !=""  :
                file = name[0] + '.txt' if not name[0].endswith('.txt') else name[0]
                with open(file, 'w+') as dataFile:
                    for data in self.gaussDataCreated:
                        dataFile.write(data + '\n')
                self.savePlot.emit(file[:-4])
        except Exception as e:
            self.show_file_extension_alert()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n in case \
        of being the error in the extension, it must be blank or .txt ")
        alert.exec_()
