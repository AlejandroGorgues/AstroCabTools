# -*- coding: utf-8 -*-
"""
Main clas that generate the interface of the mrs_det_chan tool
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys
import traceback

from astropy.io import fits
from astropy.visualization import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal,pyqtSlot
from PyQt5.QtGui import QPalette
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as font_manager

from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


import astrocabtools.mrs_det_plot.src.viewers.axisPlots as ap
import astrocabtools.mrs_det_plot.src.viewers.pointPlot as pp
import astrocabtools.mrs_det_plot.src.viewers.imagesFits as isfs
import astrocabtools.mrs_det_plot.src.ui.ui_mrs_det_plot

from .canvas_interaction.panZoom import figure_pz

from ..utils.imgPlot import imgPlot
from ..utils.globalStats import globalStats
from ..utils.fits import fitsClass

__all__= ["MrsDetPlot"]

class MrsDetPlot(QMainWindow, astrocabtools.mrs_det_plot.src.ui.ui_mrs_det_plot.Ui_MrsDetPlot):

    def __init__(self, parent=None):
        """Initializer
        :param Parent parent: The parent asocciated to the QDialog
        """
        super(MrsDetPlot, self).__init__(parent)
        self.setupUi(self)

        self.hduls = {}
        self.fitsObjList = {}

        self.xWidgets = {}
        self.yWidgets = {}
        self.zWidgets = {}
        self.zUnitWidgets = {}
        self.showButtonWidgets = {}
        self.showPointButtonWidgets = {}


        self.frameSliderWidgets = {}
        self.integrationSliderWidgets = {}
        self.frameLineEditWidgets = {}
        self.integrationLineEditWidgets = {}
        self.frameMinimunWidgets = {}
        self.frameMaximunWidgets = {}
        self.integrationMinimunWidgets = {}
        self.integrationMaximunWidgets = {}

        self.axisPlot = ap.MrsAxisPlot()
        self.pointPlot = pp.MrsPointPlot()
        self.imagesFits = isfs.MrsImagesFits()

        plt.style.use('seaborn')

        #Create the canvas to load the plot

        self.create_middle_plot()
        self.create_top_sliders_widgets()
        self.create_top_right_menu()
        self.create_bottom_info()

        self.midButton.clicked.connect(self.show_images_fits)
        self.show_images_fits()

    def create_top_sliders_widgets(self):

        #SLIDER 1
        #If text change, updagte slider
        self.frameLineEdit1.returnPressed.connect(
            lambda: self.update_sliders_widgets(1,1))

        self.frameLineEditWidgets[1] = self.frameLineEdit1

        #If slider change, updagte text
        self.frameSlider1.valueChanged.connect(lambda: self.update_frame_text(1))

        self.frameSliderWidgets[1] = self.frameSlider1

        self.frameMinimunWidgets[1] = self.frameMinimumLabel1

        self.frameMaximunWidgets[1] = self.frameMaximumLabel1

        #If text change, updagte slider
        self.integrationLineEdit1.returnPressed.connect(
            lambda: self.update_sliders_widgets(1,2))

        self.integrationLineEditWidgets[1] = self.integrationLineEdit1

        #If slider change, updagte text
        self.integrationSlider1.valueChanged.connect(lambda: self.update_integr_text(1))

        self.integrationSliderWidgets[1] = self.integrationSlider1

        self.integrationMinimunWidgets[1] = self.integrationMinimumLabel1

        self.integrationMaximunWidgets[1] = self.integrationMaximumLabel1

        self.fileButton1.clicked.connect(lambda: self.search_file(1))
        #------------------------------------------------#
        #SLIDER 2
        #If text change, updagte slider
        self.frameLineEdit2.returnPressed.connect(
            lambda: self.update_sliders_widgets(2,1))

        self.frameLineEditWidgets[2] = self.frameLineEdit2

        #If slider change, updagte text
        self.frameSlider2.valueChanged.connect(lambda: self.update_frame_text(2))

        self.frameSliderWidgets[2] = self.frameSlider2

        self.frameMinimunWidgets[2] = self.frameMinimumLabel2

        self.frameMaximunWidgets[2] = self.frameMaximumLabel2

        #If text change, updagte slider
        self.integrationLineEdit2.returnPressed.connect(
            lambda: self.update_sliders_widgets(2,2))

        self.integrationLineEditWidgets[2] = self.integrationLineEdit2

        #If slider change, updagte text
        self.integrationSlider2.valueChanged.connect(lambda: self.update_integr_text(2))

        self.integrationSliderWidgets[2] = self.integrationSlider2

        self.integrationMinimunWidgets[2] = self.integrationMinimumLabel2

        self.integrationMaximunWidgets[2] = self.integrationMaximumLabel2

        self.fileButton2.clicked.connect(lambda: self.search_file(2))
        #------------------------------------------------#
        #SLIDER 3
        #If text change, updagte slider
        self.frameLineEdit3.returnPressed.connect(
            lambda: self.update_sliders_widgets(3,1))

        self.frameLineEditWidgets[3] = self.frameLineEdit3

        #If slider change, updagte text
        self.frameSlider3.valueChanged.connect(lambda: self.update_frame_text(3))

        self.frameSliderWidgets[3] = self.frameSlider3

        self.frameMinimunWidgets[3] = self.frameMinimumLabel3

        self.frameMaximunWidgets[3] = self.frameMaximumLabel3


        #If text change, updagte slider
        self.integrationLineEdit3.returnPressed.connect(
            lambda: self.update_sliders_widgets(3,2))

        self.integrationLineEditWidgets[3] = self.integrationLineEdit3

        #If slider change, updagte text
        self.integrationSlider3.valueChanged.connect(lambda: self.update_integr_text(3))

        self.integrationSliderWidgets[3] = self.integrationSlider3

        self.integrationMinimunWidgets[3] = self.integrationMinimumLabel3

        self.integrationMaximunWidgets[3] = self.integrationMaximumLabel3

        self.fileButton3.clicked.connect(lambda: self.search_file(3))

        #------------------------------------------------#
        #SLIDER 4
        #If text change, updagte slider
        self.frameLineEdit4.returnPressed.connect(
            lambda: self.update_sliders_widgets(4,1))

        self.frameLineEditWidgets[4] = self.frameLineEdit4

        #If slider change, updagte text
        self.frameSlider4.valueChanged.connect(lambda: self.update_frame_text(4))

        self.frameSliderWidgets[4] = self.frameSlider4

        self.frameMinimunWidgets[4] = self.frameMinimumLabel4

        self.frameMaximunWidgets[4] = self.frameMaximumLabel4

        #If text change, updagte slider
        self.integrationLineEdit4.returnPressed.connect(
            lambda: self.update_sliders_widgets(4,2))

        self.integrationLineEditWidgets[4] = self.integrationLineEdit4

        #If slider change, updagte text
        self.integrationSlider4.valueChanged.connect(lambda: self.update_integr_text(4))

        self.integrationSliderWidgets[4] = self.integrationSlider4

        self.integrationMinimunWidgets[4] = self.integrationMinimumLabel4

        self.integrationMaximunWidgets[4] = self.integrationMaximumLabel4

        self.fileButton4.clicked.connect(lambda: self.search_file(4))

    def create_top_right_menu(self):
        """  Create the tab widget
        that contain three tabs with different options for each one
        that will afect the middle plot
        """
        self.minMaxRadioB.clicked.connect(
            lambda: self.change_scale('minmax'))
        self.zscaleRadioB.clicked.connect(
            lambda: self.change_scale('zscale'))

        self.radioBScale1.clicked.connect(
            lambda: self.change_stretch("Linear"))
        self.radioBScale2.clicked.connect(
            lambda: self.change_stretch("Log"))
        self.radioBScale3.clicked.connect(
            lambda: self.change_stretch("Sqrt"))

        self.radioBColor1.clicked.connect(lambda: self.change_color("gray"))
        self.radioBColor2.clicked.connect(lambda: self.change_color("coolwarm"))
        self.radioBColor3.clicked.connect(lambda: self.change_color("Accent"))
        self.radioBColor4.clicked.connect( lambda: self.change_color("gist_heat"))
        self.radioBColor5.clicked.connect(lambda: self.change_color("rainbow"))

        self.centerButton.clicked.connect(self.zoom_fit)

    def create_middle_plot(self):
        """ Create the middle layout that will show the x,y,z values selected on the middle plot"""

        self.midFigure, self.midFigure.canvas = figure_pz()

        #Create grid plots with gridspec
        #To change size of subplots to be able to make bigger the imow than the colorbar
        spec = gridspec.GridSpec(
            ncols=1, nrows=1, figure=self.midFigure)

        self.colorbarAxes = self.midFigure.add_subplot(spec[0,0])
        self.colorbarAxes.set_visible(False)

        #To allow the user to move through the plot, it need to be focused (in this case when the user click on image)
        self.midFigure.canvas.setFocusPolicy(Qt.ClickFocus)

        self.midFigure.tight_layout(pad = 3)

        self.midFigure.canvas.setSizePolicy(QSizePolicy.Expanding,
                                             QSizePolicy.Preferred)

        self.midLayout_vbox.addWidget(self.midFigure.canvas)

    def create_bottom_info(self):
        """ Show the x,y,z values clicked and allow to show the plots of x,y axis"""

        self.xWidgets[1] = self.xlineEdit1
        self.yWidgets[1] = self.ylineEdit1
        self.zWidgets[1] = self.zlineEdit1
        self.zUnitWidgets[1] = self.zUnitLabel1

        self.xWidgets[2] = self.xlineEdit2
        self.yWidgets[2] = self.ylineEdit2
        self.zWidgets[2] = self.zlineEdit2
        self.zUnitWidgets[2] = self.zUnitLabel2

        self.xWidgets[3] = self.xlineEdit3
        self.yWidgets[3] = self.ylineEdit3
        self.zWidgets[3] = self.zlineEdit3
        self.zUnitWidgets[3] = self.zUnitLabel3

        self.xWidgets[4] = self.xlineEdit4
        self.yWidgets[4] = self.ylineEdit4
        self.zWidgets[4] = self.zlineEdit4
        self.zUnitWidgets[4] = self.zUnitLabel4

        self.showAxisButton1.clicked.connect(lambda: self.show_axis_plot(1))
        self.showPointButton1.clicked.connect(lambda: self.show_point_plot(1))

        self.showAxisButton2.clicked.connect(lambda: self.show_axis_plot(2))
        self.showPointButton2.clicked.connect(lambda: self.show_point_plot(2))

        self.showAxisButton3.clicked.connect(lambda: self.show_axis_plot(3))
        self.showPointButton3.clicked.connect(lambda: self.show_point_plot(3))

        self.showAxisButton4.clicked.connect(lambda: self.show_axis_plot(4))
        self.showPointButton4.clicked.connect(lambda: self.show_point_plot(4))

        self.showButtonWidgets[1] = self.showAxisButton1
        self.showPointButtonWidgets[1] = self.showPointButton1

        self.showButtonWidgets[2] = self.showAxisButton2
        self.showPointButtonWidgets[2] = self.showPointButton2

        self.showButtonWidgets[3] = self.showAxisButton3
        self.showPointButtonWidgets[3] = self.showPointButton3

        self.showButtonWidgets[4] = self.showAxisButton4
        self.showPointButtonWidgets[4] = self.showPointButton4

    def show_images_fits(self):
        self.imagesFits.show()
        self.imagesFits.open()


    @pyqtSlot()
    def show_axis_plot(self, index):
        """ Show the axis plots
        :param str xText: x value selected
        :param str yText: y value selected
        """

        imgObj = self.imagesFits.get_image_obj_selected(index)

        self.axisPlot.axis_plot(imgObj.xValues, imgObj.yValues,
                      self.xWidgets[index].text(), self.yWidgets[index].text(), self.fitsObjList[index].fitsZUnit, self.fitsObjList[index].filename)
        self.axisPlot.show()
        self.axisPlot.open()

    @pyqtSlot()
    def show_point_plot(self, index):
        """Show the pixel alue along time plot
        :param int index: fits selected
        """
        imgObj = self.imagesFits.get_image_obj_selected(index)

        self.pointPlot.point_plot(self.fitsObjList[index].maxFrame, self.fitsObjList[index].maxIntegration,
        self.xWidgets[index].text(), self.yWidgets[index].text(),imgObj.zValues,
        self.fitsObjList[index].fitsZUnit, self.fitsObjList[index].filename)
        self.pointPlot.show()
        self.pointPlot.open()

    def set_widgets_values(self, index):

        self.frameMaximunWidgets[index].setText(str(self.fitsObjList[index].maxFrame))
        self.frameMinimunWidgets[index].setText("1")

        #Because Slider and edittext cause to redraw initially the middle_plot11 multe times
        #The signals that enable to redraw it are blocked
        self.frameSliderWidgets[index].blockSignals(True)
        self.integrationSliderWidgets[index].blockSignals(True)
        self.frameLineEditWidgets[index].blockSignals(True)
        self.integrationLineEditWidgets[index].blockSignals(True)


        self.frameSliderWidgets[index].setMinimum(1)
        self.frameSliderWidgets[index].setMaximum(self.fitsObjList[index].maxFrame)
        self.frameSliderWidgets[index].setValue(1)

        self.frameSliderWidgets[index].setEnabled(True)
        self.frameLineEditWidgets[index].setEnabled(True)
        self.frameLineEditWidgets[index].setText("1")

        self.integrationMaximunWidgets[index].setText(str(self.fitsObjList[index].maxIntegration))
        self.integrationMinimunWidgets[index].setText("1")

        self.integrationSliderWidgets[index].setMinimum(1)
        self.integrationSliderWidgets[index].setMaximum(self.fitsObjList[index].maxIntegration)
        self.integrationSliderWidgets[index].setValue(1)

        self.integrationSliderWidgets[index].setEnabled(True)
        self.integrationLineEditWidgets[index].setEnabled(True)
        self.integrationLineEditWidgets[index].setText("1")

        #Unblocks signals
        self.frameSliderWidgets[index].blockSignals(False)
        self.integrationSliderWidgets[index].blockSignals(False)
        self.frameLineEditWidgets[index].blockSignals(False)
        self.integrationLineEditWidgets[index].blockSignals(False)

    def init_fits_obj(self, hdul, index, filename):
        """ Initialize fits object based on fits value from the file selected
        :param int index: current axis selected
        """
        fitsObj = fitsClass(0, 0, -1, -1, 0, 0, 0, 0, '', 0, 0, '')


        #Frames and integration could change positions, because of that
        #I look into the first position to check the order
        if hdul[1].header["CUNIT3"] == "groups":

            fitsObj.maxFrame = int(hdul[1].header["NAXIS3"])
            fitsObj.maxIntegration = int(hdul[1].header["NAXIS4"])

        else:
            fitsObj.maxFrame = int(hdul[1].header["NAXIS4"])
            fitsObj.maxIntegration = int(hdul[1].header["NAXIS3"])

        fitsObj.maxXAxis = int(hdul[1].header["NAXIS1"]) - 1
        fitsObj.maxYAxis = int(hdul[1].header["NAXIS2"]) - 1

        #Because the value of the x and y axis could not be 1,
        #Which would correspond with the values from the image axis,
        #The values are obtained to use it
        fitsObj.shidXValue = float(hdul[1].header["CDELT1"])
        fitsObj.shidYValue = float(hdul[1].header["CDELT2"])

        #The value of the center could also not be the same, so it's also obtained
        fitsObj.fitsXCenter = int(hdul[1].header["CRVAL1"])
        fitsObj.fitsYCenter = int(hdul[1].header["CRVAL2"])

        fitsObj.fitsZUnit = hdul[1].header["BUNIT"]

        fitsObj.filename = filename

        self.fitsObjList[index] = fitsObj

        self.set_widgets_values(index)

        if len(self.hduls) == 1:
            self.set_interface_state(True)
            self.imagesFits.crossed.connect(self.update_clicked_values)
            self.imagesFits.changeBar.connect(self.create_colorbar)

    @pyqtSlot()
    def search_file(self, index):
        """ Search for the file that contains the fits image and draw it with the zoom, enable
        and update several widgets to use them
        :param int index: current axis selected
        """
        fileSearch = QFileDialog()
        fileSearch.setFileMode(QFileDialog.AnyFile)
        fileSearch.setNameFilter("Fits files (*.fits)")
        try:
            if fileSearch.exec_():
                filenames = fileSearch.selectedFiles()

                hdul = fits.open(filenames[0])
                self.hduls[index] = hdul

                #Clear the pixel lines and the bottom line edits
                self.reset_pixel_values(index)

                self.init_fits_obj(hdul, index,filenames[0])

                globalStats = self.imagesFits.get_global_stats()
                norm = self.get_norm(index, globalStats)

                self.imagesFits.draw_plot(index, self.fitsObjList[index], hdul, norm)

                self.imagesFits.update_canvas()

        except Exception as e:
            self.show_file_alert()

    def reset_pixel_values(self, index):
        """Clear the pixel lines and the bottom line edits
        :param int index: current axis selected
        """

        self.imagesFits.check_pixel_line_exist(index)
        self.xWidgets[index].setText('')
        self.yWidgets[index].setText('')
        self.zWidgets[index].setText('')
        self.zUnitWidgets[index].setText('')
        self.showButtonWidgets[index].setEnabled(False)
        self.showPointButtonWidgets[index].setEnabled(False)

    def update_sliders_widgets(self, index, typeSlider):
        """Check if the limit of char of a TextEdit is reached to allow or not to write more into the EditText
        and update slider values if TextEdit edited or update editText if slider edited
        :param int typeslider: Slider edited
        """
        if typeSlider == 1:

            frameValue = int(self.frameLineEditWidgets[index].text())

            try:
                if 1 <= frameValue <= self.fitsObjList[index].maxFrame:
                    #Update the frame value, slider value and draw the plot
                    self.frameSliderWidgets[index].setValue(frameValue)

                elif (frameValue > self.fitsObjList[index].maxFrame) or (frameValue< 1):
                    self.values_alert("Only value range between 1 and {}".format(
                        self.frameSliderWidgets[index].maximum()))

            except:
                self.values_alert("Error: non-numeric characters")

        #If its the integration editText, edit integration slider
        else:

            integrValue= int(self.integrationLineEditWidgets[index].text())


            try:
                if 1 <= integrValue <= self.fitsObjList[index].maxIntegration:

                    #Update the integration value, slider value and draw the plot
                    self.integrationSliderWidgets[index].setValue(integrValue)

                elif (integrValue > self.fitsObjList[index].maxIntegration) or (integrValue< 1):

                    self.values_alert("Only value range between 1 and {}".format(
                        self.integrationSliderWidgets[index].maximum()))
            except:
                self.values_alert("Error: non-numeric characters")

    def update_frame_text(self, index):
        """ Update current frame text and write it"""

        #Update current frame value
        self.fitsObjList[index].currFrame = self.frameSliderWidgets[index].value() -1
        self.frameLineEditWidgets[index].setText(str(self.frameSliderWidgets[index].value()))

        #Update current frame of the object selected
        self.fitsObjList[index].currFrame = \
            self.frameSliderWidgets[index].value() -1

        globalStats = self.imagesFits.get_global_stats()
        norm = self.get_norm(index, globalStats)

        self.imagesFits.draw_plot(index, self.fitsObjList[index], self.hduls[index], norm)

    def update_integr_text(self, index):
        """ Update current integration text and wirte it"""

        #Update current integration value
        self.fitsObjList[index].currIntegration = self.integrationSliderWidgets[index].value() -1
        self.integrationLineEditWidgets[index].setText(str(self.integrationSliderWidgets[index].value()))

        #Update current integration of the object selected
        self.fitsObjList[index].currIntegration = \
            self.integrationSliderWidgets[index].value() -1

        globalStats = self.imagesFits.get_global_stats()
        norm = self.get_norm(index, globalStats)


        self.imagesFits.draw_plot(index, self.fitsObjList[index], self.hduls[index], norm)

    @pyqtSlot(float,float,int, name="makeCross")
    def update_clicked_values(self, xdata, ydata, index):
        """ Update pixel data widgets and image object attributes
            :param list xdata: list of xvalues
            :param list ydata: list of yvalues
            :param int i: current axis selected
        """
        imgObj = self.imagesFits.get_image_obj_selected(index)
        #Because the shiof the values corresponds to 1.0 each one
        #And the center of the image is 0 on x,y,z, the values on pixels are the same
        #However, as it's decided by the Fits file header, the y axis comes first instead of the x
        #Instead of beeing a coord (x,y) it's (y,x)

        xdataRound = self.set_round_value(xdata)
        ydataRound = self.set_round_value(ydata)

        xValueTransformed = int(xdataRound-self.fitsObjList[index].fitsXCenter*self.fitsObjList[index].shidXValue)
        yValueTransformed = int(ydataRound-self.fitsObjList[index].fitsYCenter*self.fitsObjList[index].shidYValue)

        imgObj.xValues = self.hduls[index][1].data[self.fitsObjList[index].currIntegration,
                                                self.fitsObjList[index].currFrame,
                                                yValueTransformed,\
                                                 0:self.fitsObjList[index].maxXAxis]
        imgObj.yValues = self.hduls[index][1].data[self.fitsObjList[index].currIntegration,
                                                self.fitsObjList[index].currFrame,
                                                0:self.fitsObjList[index].maxYAxis,
                                                xValueTransformed]


        #Get z value along time
        imgObj.zValues = self.hduls[index][1].data[:,:,
        yValueTransformed,
        xValueTransformed]

        self.xWidgets[index].setText(str(xdata +1))
        self.yWidgets[index].setText(str(ydata +1))
        self.zWidgets[index].setText(str(self.hduls[index][1].data[self.fitsObjList[index].currIntegration,
                                                         self.fitsObjList[index].currFrame,
                                                         yValueTransformed,
                                                         xValueTransformed]))

        self.zUnitWidgets[index].setText(self.fitsObjList[index].fitsZUnit)
        self.showButtonWidgets[index].setDisabled(False)
        self.showPointButtonWidgets[index].setDisabled(False)

        self.imagesFits.set_image_obj_selected(index, imgObj)

    @pyqtSlot()
    def zoom_fit(self):
        """Zoom to fit the original image size """
        for key in self.fitsObjList.keys():

            imageAxe = self.imagesFits.get_image_axes_selected(key)

            imageAxe.set_xlim(0, self.fitsObjList[key].maxXAxis)
            imageAxe.set_ylim(0, self.fitsObjList[key].maxYAxis)

            self.imagesFits.set_image_axes_selected(key, imageAxe)

        self.imagesFits.update_canvas()

    def get_norm(self, index, globalStats):
        """ Obtain the norm with the new normalization
        :param int index: current axis selected
        :return: the new norm
        """

        if globalStats.scale == "minmax":
            interval = MinMaxInterval()

        else:
            interval = ZScaleInterval()

        if globalStats.stretch == "Linear":
            stretch = LinearStretch()

        elif globalStats.stretch == "Log":
            stretch = Loretch()

        else:
            stretch = SqrtStretch()

        minV, maxV = interval.get_limits(
            self.hduls[index][1].data[self.fitsObjList[index].currIntegration, self.fitsObjList[index].currFrame])
        norm = ImageNormalize(vmin=minV, vmax=maxV, stretch=stretch)
        return norm

    @pyqtSlot()
    def change_scale(self, typeScale):

        globalStats = self.imagesFits.get_global_stats()
        globalStats.scale = typeScale

        for key in self.hduls.keys():
            image = self.imagesFits.get_image_selected(key)

            norm = self.get_norm(key, globalStats)
            image.set_norm(norm)

            self.imagesFits.set_image_selected(key, image)

        self.imagesFits.set_global_stats(globalStats)
        self.create_colorbar()
        self.imagesFits.update_canvas()


    @pyqtSlot()
    def change_stretch(self, typeStretch):
        """ Modify norm based on scale and stretch
        :param str typeScl: new scale selected
        :param str typeStr: new stretch selected
        """

        globalStats = self.imagesFits.get_global_stats()
        globalStats.stretch = typeStretch

        for key in self.hduls.keys():

            image = self.imagesFits.get_image_selected(key)
            image.set_norm(norm)
            norm = self.get_norm(key, globalStats)

            self.imagesFits.set_image_selected(key, image)

        self.imagesFits.set_global_stats(globalStats)
        self.create_colorbar()
        self.imagesFits.update_canvas()



    @pyqtSlot()
    def change_color(self, color):
        """ Modify cmap based on color
        :param str color: new color selected
        """
        for i in self.hduls.keys():

            globalStats = self.imagesFits.get_global_stats()
            image = self.imagesFits.get_image_selected(i)

            image.set_cmap(plt.get_cmap(color))
            globalStats.color = color


            self.imagesFits.set_image_selected(i, image)

        self.create_colorbar()
        self.imagesFits.update_canvas()

    @pyqtSlot()
    def create_colorbar(self):
        """ Remove previous colorbar to add the new one"""


        if len(self.midFigure.axes) > 1:

            self.midFigure.axes[1].remove()

        index = self.imagesFits.get_img_selected_index()

        self.set_flux_values(index)
        cb = self.colorbar(index)
        cb.ax.tick_params(labelsize=10)
        self.midFigure.axes[1].set_label("cbar")
        self.midFigure.canvas.draw()

    def colorbar(self, index):
        """ Create the colorbar based on an image
        :param Mappeable mappeable: image based to make the colorbar
        :return: colorbar
        """
        mappable = self.imagesFits.get_image_selected(index)
        imgObj = self.imagesFits.get_image_obj_selected(index)

        ticksValues = []
        #Obtain polar axes, axes and figure of the plot or image
        #last_axes = plt.gca()
        ax = mappable.axes
        fig = ax.figure

        #Make possible to create a divider between the colorbar and the plot
        #And adjust the size of the colorbar to the size of the plot
        #Which in this case it's not necessary
        #divider = make_axes_locatable(ax)

        #Select the position of the colorbar and draw it
        #cax = divider.append_axes("bottom", size="5%", pad=0.05)
        #cbar = fig.colorbar(mappable, cax=cax, orientation = "horizontal")

        axCenter = inset_axes(self.colorbarAxes,
                              width="100%",  # width = 100% of parent_bbox width
                              height="20%",  # height : 20%
                              loc=10)

        #TODO
        cbar = fig.colorbar(mappable, cax=axCenter,
                            orientation="horizontal", label=self.fitsObjList[index].fitsZUnit)

        #Select number of ticks to draw near the colorbar
        ticks = np.linspace(0, 1, 6)

        ticksValues.append(imgObj.minFValue)

        [ticksValues.append(
            i*(imgObj.maxFValue-imgObj.minFValue)/5.0 + imgObj.minFValue) for i in range(1,5)]
        ticksValues.append(imgObj.maxFValue)
        #The colorbar values goes from 0. to 1. but, the values that are assigned to each ticks
        #can be drawn by set_xticklabels

        #If the tick values goes from values differents of 0 to 1, the colorbar will not be represented correctly
        cbar.ax.xaxis.set_ticks(ticks)
        cbar.ax.set_xticklabels(ticksValues)

        font = font_manager.FontProperties(size = 10)
        #cbar.ax.xaxis.label.set_font_properties(font)
        #plt.sca(last_axes)

        return cbar

    def set_flux_values(self, index):
        """Update the max and min values and get the middle values to be drawn
        into the colorbar
        :param int index: current axis selected
        """

        imgObj = self.imagesFits.get_image_obj_selected(index)

        imgObj.maxFValue = (
            self.hduls[index][1].data[self.fitsObjList[index].currIntegration, self.fitsObjList[index].currFrame]).max()
        imgObj.minFValue = (
            self.hduls[index][1].data[self.fitsObjList[index].currIntegration, self.fitsObjList[index].currFrame]).min()

        self.imagesFits.set_image_obj_selected(index, imgObj)

    def set_interface_state(self, state):
        """ Disable or enable the different widgets of the interface
        :param bool state: state that is going to be applied
        """

        self.minMaxRadioB.setChecked(state)
        self.radioBColor1.setChecked(state)

        self.radioBScale1.setChecked(state)
        self.radioBScale2.setChecked(not state)
        self.radioBScale3.setChecked(not state)

    def values_alert(self, message):
        alert = QMessageBox()
        alert.setText("Error: non-numeric characters")
        alert.setDetailedText(traceback.format_exc(limit=1))
        alert.exec_()

    def show_file_alert(self):

        alert = QMessageBox()
        alert.setText("Error: wrong file parameters")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()

    def set_round_value(self, data):
        if data %1 >= 0.5:
            return math.ceil(data)
        else:
            return round(data)

    def closeEvent(self, event):
        self.imagesFits.close()
