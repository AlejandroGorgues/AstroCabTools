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


import astrocabtools.fit_line.src.viewers.gaussDataCreatedListWidget as gausslw
import astrocabtools.fit_line.src.viewers.residualsVisualization as ressV
import astrocabtools.fit_line.src.ui.ui_gaussDataVisualization


class MrsFitLineData(QDialog, astrocabtools.fit_line.src.ui.ui_gaussDataVisualization.Ui_gaussDataVisualization):
    savePlot = pyqtSignal(str)

    def __init__(self, parent=None ):
        super(MrsFitLineData, self).__init__(parent)
        self.setupUi(self)

        self.gaussDataCreated = []

        self.residualsV = ressV.MrsResidualsV()

        self.saveButton.clicked.connect(self.save_data)
        self.gaussListWidget.itemDoubleClicked.connect(self.show_residuals)

    def add_spectrum_values(self, result, wValues, fValues):
        self.residualsV.set_residuals(result, wValues, fValues)

    def add_gauss_data(self, data):
        """
        Add model data to the list widget
        :param str data: data obtained from the model
        """


        it = QListWidgetItem()
        self.gaussListWidget.addItem(it)
        widget = gausslw.gaussListwidget(text = data)
        self.gaussListWidget.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())

        self.gaussDataCreated.append(data)
        self.saveButton.setEnabled(True)


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
        """
        Delete last model created
        """
        for i in range(2):
            item = self.gaussListWidget.takeItem(self.gaussListWidget.count()-1)
            del item
        self.residualsV.delete_last_residuals()
        if self.gaussListWidget.count() == 0:
            self.saveButton.setEnabled(False)

    def delete_all(self):
        self.gaussListWidget.clear()
        self.gaussDataCreated.clear()
        self.residualsV.delete_all_residuals()
        self.saveButton.setEnabled(False)

    def save_all_residuals_images(self, path):
        self.residualsV.generate_all_residuals(path)

    @pyqtSlot(QListWidgetItem)
    def show_residuals(self, item):
        """
        Load dialog that visualice the residuals of the fitting function and
        set the row of the item selected to get the residuals
        """

        self.residualsV.set_residuals_index(int(self.gaussListWidget.indexFromItem(item).row()/2))
        item.setSelected(False)
        self.residualsV.show()
        self.residualsV.open()


    @pyqtSlot()
    def save_data(self):
        """ Save the data as txt file and an image of current figure zoom.
        If the extension is different from .txt or is it blank, it throws an error
        """
        try:
            fileSave = QFileDialog()
            fileSave.setNameFilter("txt files (*.txt)")
            name = fileSave.getSaveFileName(self, 'Save File')
            file = ""
            if name[0] !=""  :

                if name[0].endswith('.txt'):
                    file = name[0][:-4]
                else:
                    file = name[0]
                file_fitted = file + "_ajuste"
                final_file_name = file_fitted + ".txt"
                with open(final_file_name, 'w+') as dataFile:
                    for data in self.gaussDataCreated:
                        dataFile.write(data + '\n')
                #Emit signal to main window to save current figure as png

                self.savePlot.emit(file)
                self.residualsV.generate_all_residuals(file)
        except Exception as e:
            self.show_file_extension_alert()

    def close_event(self, event):
        """
        Close other windows when dialog is closed
        """
        self.residualsV.close()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n it must be blank or .txt ")
        alert.exec_()
