"""
Object that show data related to each fitting
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import re
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal
from PyQt5 import uic


import astrocabtools.fit_line.src.viewers.modelDataCreatedListWidget as modellw
import astrocabtools.fit_line.src.viewers.residualsVisualization as ressV
import astrocabtools.fit_line.src.ui.ui_modelDataVisualization


class ModelDataVisualization(QDialog, astrocabtools.fit_line.src.ui.ui_modelDataVisualization.Ui_modelDataVisualization):
    savePlot = pyqtSignal(str)

    def __init__(self, parent=None ):
        super(ModelDataVisualization, self).__init__(parent)
        self.setupUi(self)

        #List that will containt data of the best fit model and params of that model
        #inside the dict
        self.modelDataCreated = []
        self.modelDict = {}


        self.residualsV = ressV.MrsResidualsV()

        self.saveButton.clicked.connect(self.save_data)
        self.modelListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.modelListWidget.customContextMenuRequested.connect(self.modelContext)

    def modelContext(self, position):
        popMenu = QMenu()
        showResiduals = QAction("Show residuals", self)
        saveDataModel = QAction("Save model data", self)


        showResiduals.triggered.connect(self.show_residuals)
        #saveDataModel.triggered.connect(lambda: self.save_data_model(self.modelDataCreated[self.modelListWidget.currentRow()]['best_fit'], self.modelDataCreated[self.modelListWidget.currentRow()]['wValues']))
        saveDataModel.triggered.connect(lambda: self.save_data_model(self.modelDataCreated[self.modelListWidget.currentRow()]))

        popMenu.addAction(showResiduals)
        popMenu.addAction(saveDataModel)

        popMenu.exec_(self.modelListWidget.mapToGlobal(position))

    def add_spectrum_values(self, result, wValues, fValues, num_model):
        self.residualsV.set_residuals(result, wValues, fValues)
        comps = result.eval_components()

        self.modelDict['Wavelength (um)'] = wValues
        self.modelDict['Initial_Spectrum (f_lambda(erg/(s*cm^2*um)))'] = fValues
        self.modelDict['Best_Fit_Model (f_lambda(erg/(s*cm^2*um)))'] = result.best_fit

        if num_model == 1:
            self.modelDict['Fitted_line (f_lambda(erg/(s*cm^2*um)))'] = comps['model1']

        elif num_model == 2:
            self.modelDict['Fitted_line (f_lambda(erg/(s*cm^2*um)))'] = comps['model1'] +  comps['continuum_fitting_function']
            self.modelDict['Fitted_continuum (f_lambda(erg/(s*cm^2*um)))'] = comps['continuum_fitting_function']

        elif num_model == 3:
            self.modelDict['Fitted_line_1 (f_lambda(erg/(s*cm^2*um)))'] = comps['p1_'] +  comps['continuum_fitting_function']
            self.modelDict['Fitted_line_2 (f_lambda(erg/(s*cm^2*um)))'] = comps['p2_'] +  comps['continuum_fitting_function']
            self.modelDict['Fitted_continuum (f_lambda(erg/(s*cm^2*um)))'] = comps['continuum_fitting_function']

        self.modelDict['Residuals (f_lambda(erg/(s*cm^2*um)))'] = result.best_fit - fValues

    def add_model_data(self, data):
        """
        Add model data to the list widget
        :param str data: data obtained from the model
        """


        it = QListWidgetItem()
        self.modelListWidget.addItem(it)
        widget = modellw.modelListwidget(text = data)
        self.modelListWidget.setItemWidget(it, widget)
        it.setSizeHint(widget.sizeHint())

        self.modelDict['param'] = data
        self.modelDataCreated.append(self.modelDict.copy())
        self.saveButton.setEnabled(True)


    def add_delimiter_line(self):
        it = QListWidgetItem()

        self.modelListWidget.addItem(it)
        widget = QFrame()
        widget.setFrameShape(QFrame.HLine)
        it.setSizeHint(widget.sizeHint())
        it.setFlags(Qt.NoItemFlags)
        self.modelListWidget.setItemWidget(it, widget)

        self.modelDataCreated.append("----------------------------------------------------")

    def delete_model_data(self):
        """
        Delete last model created
        """
        for i in range(2):
            item = self.modelListWidget.takeItem(self.modelListWidget.count()-1)
            del item
        self.residualsV.delete_last_residuals()
        if self.modelListWidget.count() == 0:
            self.saveButton.setEnabled(False)

    def delete_all(self):
        self.modelListWidget.clear()
        self.modelDataCreated.clear()
        self.residualsV.delete_all_residuals()
        self.saveButton.setEnabled(False)

    def save_all_residuals_images(self, path):
        self.residualsV.generate_all_residuals(path)

    def save_data_model(self, modelSelected):
        """
        Save the data of the fitted model selected
        """
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save best model')
            path_file_txt = ""

            df_model = pd.DataFrame(data = dict(list(modelSelected.items())[:-1]))

            path_file_txt = name[0] + ".txt"


            #np.savetxt(path_file_txt, df_model.values, delimiter="      ", \
            #           header = '           '.join(df_model.columns.values.tolist()), comments='')
            df_model.to_csv(path_file_txt, sep=' ', index=False)
        except Exception as e:
            self.show_file_extension_alert()


    def show_residuals(self):
        """
        Load dialog that visualice the residuals of the fitting function and
        set the row of the item selected to get the residuals
        """
        self.residualsV.set_residuals_index(self.modelListWidget.currentRow())
        self.modelListWidget.currentItem().setSelected(False)
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
                    for data in self.modelDataCreated:
                        data['param'].write(data + '\n')
                #Emit signal to main window to save current figure as png

                self.savePlot.emit(file)
                self.residualsV.generate_all_residuals(file)
        except Exception as e:
            self.show_file_extension_alert()

    def closeEvent(self, event):
        """
        Close other windows when dialog is closed
        """
        self.residualsV.close()

    def show_file_extension_alert(self):

        alert = QMessageBox()
        alert.setText("Error: Filename name or extension not correct, \n it must be blank or .txt ")
        alert.exec_()
