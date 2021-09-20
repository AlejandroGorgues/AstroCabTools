"""
Allow to modify the slice of the current subband selected
"""

import sys
import glob
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import uic

from ..utils.basic_transformations import slice_to_wavelength, wavelength_to_slice

import astrocabtools.mrs_subviz.src.ui.ui_sliceManager

__all__=["SliceManager"]

class SliceManager(QDialog, astrocabtools.mrs_subviz.src.ui.ui_sliceManager.Ui_sliceManager):
    update_slice = pyqtSignal(int, int, name ='cubeChanged')
    obtain_cube = pyqtSignal(int, name='obtainCube')


    def __init__(self, parent = None):
        super(SliceManager, self).__init__(parent)
        self.setupUi(self)

        self.subbandSelectionComboBox.currentIndexChanged.connect(self.set_subband)
        self.initialize_slice_widgets()
        self.wavelengthLineEdit.setValidator(QtGui.QDoubleValidator())

    def set_subband(self, index):
        if index > 0:
            self.index = index-1
            self.obtain_cube.emit(index-1)
        else:
            self.change_state_widgets(False)

    def reset_widgets(self):
        self.sliceMinimumValue.setText("")
        self.sliceMaximumValue.setText("")
        self.wavelengthLineEdit.setText("")
        self.sliceSpinBox.blockSignals(True)
        self.sliceSlider.blockSignals(True)
        self.sliceSlider.setValue(0)
        self.subbandSelectionComboBox.setCurrentIndex(0)
        self.sliceSpinBox.setValue(0)
        self.sliceSpinBox.blockSignals(False)

    def reset_same_cube(self, index):
        """
        Check if the subband that had been changed is the same as the selected in
        the sliceManager window and set the values to the new ones
        :param in index: index of the subband changed
        """
        if index == self.subbandSelectionComboBox.currentIndex()-1:
            self.set_subband(self.subbandSelectionComboBox.currentIndex())
            self.wavelengthLineEdit.setText("")
            self.sliceSlider.setValue(0)
            self.sliceSpinBox.setValue(0)


    def initialize_slice_widgets(self):
        #If text change, update slider and viceversa
        self.sliceSpinBox.valueChanged.connect(self.update_from_spinBox)

        self.sliceSlider.valueChanged.connect(self.update_from_slider)

        self.wavelengthLineEdit.returnPressed.connect(self.update_from_lineEdit)

    def set_widgets_values(self, cubeObj):
        """
        Set all widgets values and text to initial values and text when a new cube
        is loaded
        """
        self.cubeObj= cubeObj

        self.sliceSpinBox.blockSignals(True)
        self.sliceSlider.blockSignals(True)
        self.sliceMaximumValue.setText(str(slice_to_wavelength(cubeObj.cubeModel.weightmap.shape[0], cubeObj.cubeModel.meta.wcsinfo.crpix3, cubeObj.cubeModel.meta.wcsinfo.cdelt3, cubeObj.cubeModel.meta.wcsinfo.crval3)))
        self.sliceMinimumValue.setText(str(slice_to_wavelength(1, cubeObj.cubeModel.meta.wcsinfo.crpix3, cubeObj.cubeModel.meta.wcsinfo.cdelt3, cubeObj.cubeModel.meta.wcsinfo.crval3)))

        self.sliceSpinBox.setMinimum(1)
        self.sliceSpinBox.setMaximum(cubeObj.cubeModel.weightmap.shape[0])

        self.sliceSlider.setMinimum(1)
        self.sliceSlider.setMaximum(cubeObj.cubeModel.weightmap.shape[0])

        self.wavelengthLineEdit.setText(str(slice_to_wavelength(1, cubeObj.cubeModel.meta.wcsinfo.crpix3, cubeObj.cubeModel.meta.wcsinfo.cdelt3, cubeObj.cubeModel.meta.wcsinfo.crval3)))

        self.sliceSlider.blockSignals(False)
        self.sliceSpinBox.blockSignals(False)

        """
        Set slider value to be 1 because the minimum value for a cube could be
        a common value for another
        """
        self.sliceSlider.setValue(cubeObj.currSlice)

    def update_from_spinBox(self):
        """Update the slider and the wavelength line edit from the spinBox value"""
        slice_value = self.sliceSpinBox.value()
        self.sliceSlider.setValue(slice_value)
        self.wavelengthLineEdit.setText(str(slice_to_wavelength(slice_value, self.cubeObj.cubeModel.meta.wcsinfo.crpix3, self.cubeObj.cubeModel.meta.wcsinfo.cdelt3, self.cubeObj.cubeModel.meta.wcsinfo.crval3)))

    def update_from_slider(self):
        """Update slice spin box and wavelength line edit from slice slider value"""
        #Because in the slider, the values goes from 1 to 500, when another
        #functionality need to use it in the cubeObj.cubeData. it value must be one less to
        #acess the correct index which will be the current - 1
        slice_value = self.sliceSlider.value()-1

        #Because a subtraction had been made to the slice to make the slider use
        #the correct values previously, the slice to be converted cannot be 0
        wavelength_value = slice_to_wavelength(slice_value+1, self.cubeObj.cubeModel.meta.wcsinfo.crpix3, self.cubeObj.cubeModel.meta.wcsinfo.cdelt3, self.cubeObj.cubeModel.meta.wcsinfo.crval3)

        self.sliceSpinBox.blockSignals(True)

        #To prevent the slice value to get an slice value of 0, the current slice will
        #be the current +1
        self.sliceSpinBox.setValue(slice_value+1)
        self.sliceSpinBox.blockSignals(False)

        self.wavelengthLineEdit.setText(str(wavelength_value))
        self.update_slice.emit(slice_value, self.index)

    def update_from_lineEdit(self):
        slice_value = wavelength_to_slice(float(self.wavelengthLineEdit.text()), self.cubeObj.cubeModel.meta.wcsinfo.crpix3, self.cubeObj.cubeModel.meta.wcsinfo.cdelt3, self.cubeObj.cubeModel.meta.wcsinfo.crval3)
        self.sliceSlider.setValue(slice_value)
        self.sliceSpinBox.setValue(slice_value)

    def change_state_widgets(self, state):
        if (state and not self.wavelengthLineEdit.isEnabled()) or (not state and self.wavelengthLineEdit.isEnabled()):
            self.wavelengthLineEdit.setEnabled(state)
            self.sliceSlider.setEnabled(state)
            self.sliceSpinBox.setEnabled(state)

    def clear_data(self):
        self.sliceMinimumValue.setText("")
        self.sliceMaximumValue.setText("")
        self.wavelengthLineEdit.setText("")
        self.sliceSpinBox.blockSignals(True)
        self.sliceSlider.blockSignals(True)
        self.sliceSlider.setValue(0)
        self.subbandSelectionComboBox.setCurrentIndex(0)
        self.sliceSpinBox.setValue(0)
        self.sliceSpinBox.blockSignals(False)
        self.sliceSlider.blockSignals(False)
        self.close()
