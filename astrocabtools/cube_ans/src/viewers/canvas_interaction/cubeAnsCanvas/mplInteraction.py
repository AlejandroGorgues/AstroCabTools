# This Copyright is paste from https://gist.github.com/t20100/e5a9ba1196101e618883
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
import numpy
import weakref

from pubsub import pub

import matplotlib.pyplot as _plt

from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import EllipseSelector
from ....models.ellipseSelection import ellipse_selection

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ....models.rectangleSelection import rectangle_selection



class MplInteraction(object):

    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param Canvas FigureCanvas: The matplotlib PyQT canvas to allow focus after declaration
        """
        self._fig_ref = weakref.ref(figure)
        self.canvas = FigureCanvas(figure)
        self._cids_zoom = []
        self._cids_pan = []
        self._cids_rectangle = []
        self._cids_ellipse = []
        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._cids_callback_rectangle = {}
        self._cids_callback_ellipse = {}

        self.rectangleStats = rectangle_selection(-1,-1,-1,-1)
        self.ellipseStats = ellipse_selection(-1,-1,-1,-1)

        self._widget_selector = None

        self._rectangle_selector = None
        self._callback_rectangle = None

        self._ellipse_selector = None
        self._callback_ellipse = None

        self._cids = []

    def __del__(self):
        self.disconnect()

    def _add_connection(self, event_name, callback):
        """Called to add a connection to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        cid = self.canvas.mpl_connect(event_name, callback)
        self._cids.append(cid)

    def _add_rectangle_callback(self, callback):
        """
        Because the callback method can only be created when the Zoom event is
        created and the axis can only be known after the creation if it, this
        method allow to assign the callback before the creation fo the
        rectangle selector object
        """
        self._callback_rectangle = callback

    def _add_ellipse_callback(self, callback):
        """
        Because the callback method can only be created when the Zoom event is
        created and the axis can only be known after the creation if it, this
        method allow to assign the callback before the creation fo the
        ellipse selector object
        """
        self._callback_ellipse = callback


    def _add_connection_rectangle(self, event_name, callback):
        """Called to add a connection of type rectangle release to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_rectangle[event_name] = callback

    def _add_connection_ellipse(self, event_name, callback):
        """Called to add a connection of type ellipse release to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_ellipse[event_name] = callback


    def _add_connection_zoom(self, event_name, callback):
        """Called to add a connection of type zoom to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """

        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_zoom.append(cid)
        self._cids_callback_zoom[event_name] = callback

    def _add_connection_pan(self, event_name, callback):
        """Called to add a connection of type pan to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_pan.append(cid)
        self._cids_callback_pan[event_name] = callback

    def disconnect_rectangle(self, changeFigure=False):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_rectangle:
                    figure.canvas.mpl_disconnect(cid)
            #If the figure is on the image, do not disable it, otherwise, do it
            if not changeFigure :
                self._rectangle_selector.set_active(False)
            else:
                self._disable_rectangle()
            self._cids_rectangle.clear()

    def disconnect_ellipse(self, changeFigure=False):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_ellipse:
                    figure.canvas.mpl_disconnect(cid)
            #If the figure is on the image, do not disable it, otherwise, do it
            if not changeFigure:
                self._ellipse_selector.set_active(False)
            else:
                self._disable_ellipse()
            self._cids_ellipse.clear()

    def disconnect_zoom(self):
        """
        Disconnect all zoom events and disable the rectangle selector
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_zoom:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_zoom.clear()

    def disconnect_pan(self):
        """
        Disconnect all pan events
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_pan:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_pan.clear()

    def _disable_rectangle(self):
        self._rectangle_selector.set_visible(False)
        self._rectangle_selector.set_active(False)


    def _disable_ellipse(self):
        self._ellipse_selector.set_visible(False)
        self._ellipse_selector.set_active(False)

    def disconnect(self):
        """Disconnect interaction from Figure."""
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids:
                    figure.canvas.mpl_disconnect(cid)
            self._fig_ref = None

    def _enable_rectangle(self):
        self._rectangle_selector.set_active(True)

        self._rectangle_selector.set_visible(True)

    def _enable_ellipse(self):
        self._ellipse_selector.set_active(True)

        self._ellipse_selector.set_visible(True)

    def connect_rectangle(self):
        for event_name, callback in self._cids_callback_rectangle.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_rectangle.append(cid)
        self._enable_rectangle()

    def connect_ellipse(self):
        for event_name, callback in self._cids_callback_ellipse.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_ellipse.append(cid)
        self._enable_ellipse()

    def connect_zoom(self):
        """
        Assign all callback zoom events to the mpl
        """
        for event_name, callback in self._cids_callback_zoom.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_zoom.append(cid)

    def connect_pan(self):
        """
        Assign all callback pan events to the mpl
        """
        for event_name, callback in self._cids_callback_pan.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_pan.append(cid)

    @property
    def figure(self):
        """The Figure this interaction is connected to or
        None if not connected."""
        return self._fig_ref() if self._fig_ref is not None else None

    def _axes_to_update(self, event):
        """Returns two sets of Axes to update according to event.
        :param MouseEvent event: Matplotlib event to consider
        :return: Axes for which to update xlimits and ylimits
        :rtype: 2-tuple of set (xaxes, yaxes)
        """
        x_axes, y_axes = set(), set()

        for ax in self.figure.axes:
            if ax.contains(event)[0]:
                shared_x_axes = set(ax.get_shared_x_axes().get_siblings(ax))
                if x_axes.isdisjoint(shared_x_axes):
                    x_axes.add(ax)

                shared_y_axes = set(ax.get_shared_y_axes().get_siblings(ax))
                if y_axes.isdisjoint(shared_y_axes):
                    y_axes.add(ax)

        return x_axes, y_axes

    def create_rectangle_ax(self, ax):
        rectprops = dict(edgecolor = 'red',fill = False,
                         linewidth = 5, linestyle= '-')

        self._rectangle_selector = RectangleSelector(ax, self._callback_rectangle,
                                    drawtype= 'box', useblit= False, rectprops= rectprops,
                                    button= [1,3], minspanx = 5, minspany=5,
                                    spancoords='pixels', interactive=True)

        self._disable_rectangle()

    def create_ellipse_ax(self, ax):
        elliprops = dict(edgecolor = 'red', fill = False,
                         linewidth = 5, linestyle= '-')

        self._ellipse_selector = EllipseSelector(ax, self._callback_ellipse,
                                    drawtype= 'box', useblit= False, rectprops= elliprops,
                                    button= [1,3], minspanx = 5, minspany=5,
                                        spancoords='pixels', interactive=True)

        self._disable_ellipse()

    def update_rectangle(self, left_bottomX, left_bottomY, right_topX, right_topY):
        """
        Set coordinates of the rectangle to be drawed, and send message to
        draw the new spectrum
        :param int coord1_1: initial x value of the coordinate
        :param int coord1_2: initial y value of the coordinate
        :param int coord2_1: end x value of the coordinate
        :param int coord2_2: end y value of the coordinate
        """
        self._draw()
        self.connect_rectangle()
        self._rectangle_selector.extents = (left_bottomX, right_topX, left_bottomY, right_topY)

        self.rectangleStats.ix = left_bottomX
        self.rectangleStats.iy = left_bottomY
        self.rectangleStats.ex = right_topX
        self.rectangleStats.ey = right_topY

        pub.sendMessage('rectangleSelected')

        #Update coordinates window parameters of the rectangle
        pub.sendMessage('rectangleUpdateCoordinates', ix = left_bottomX, iy =left_bottomY
                        , ex = right_topX, ey= right_topY)

    def redraw_rectangle_without_interaction(self):
        """
        Redraw the rectangle on the axe that does not require to interact with it
        """
        if self._rectangle_selector.visible or self._rectangle_selector.active:
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)

    def redraw_rectangle_with_interaction(self):
        """
        Redraw the rectangle on the axe and maintain the state of the active tool when
        a slice had been changed
        """
        if  self._rectangle_selector.active:
            self._enable_rectangle()
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)
            if self.rectangleStats.ix != -1:
                pub.sendMessage('rectangleSelected')

        elif self._rectangle_selector.visible:
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)

    def redraw_rectangle_from_rectButton(self):


        if self.rectangleStats.ix != -1:
            self._enable_rectangle()
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)
            pub.sendMessage('rectangleSelected')

    def update_ellipse(self, centerX, centerY, aAxis, bAxis):
        """
        Set coordinates of the ellipse to be drawed, and send message to
        draw the new spectrum
        :param int centerX: center x value of the coordinate
        :param int centerY: center y value of the coordinate
        :param int aAxis: long axis value
        :param int bAxis: short axis value
        """
        self.connect_ellipse()

        xmax = centerX + aAxis/2
        xmin = centerX - aAxis/2
        ymax = centerY + bAxis/2
        ymin = centerY - bAxis/2

        self._ellipse_selector.extents = (xmin, xmax, ymin, ymax)
        self.ellipseStats.centerX = centerX
        self.ellipseStats.centerY = centerY
        self.ellipseStats.aAxis = aAxis
        self.ellipseStats.bAxis = bAxis

        pub.sendMessage('ellipseUpdateCoordinates', cx = centerX, cy =centerY, aAxis = aAxis, bAxis= bAxis)
        pub.sendMessage('ellipseSelected')

    def redraw_ellipse_without_interaction(self):
        """
        Redraw the ellipse on the axe that does not require to activate tools(pan or zoom)
        after it and to emit the signal
        """

        if self._ellipse_selector.active or self._ellipse_selector.visible:
            xmax = self.ellipseStats.centerX + self.ellipseStats.aAxis/2
            xmin = self.ellipseStats.centerX - self.ellipseStats.aAxis/2
            ymax = self.ellipseStats.centerY + self.ellipseStats.bAxis/2
            ymin = self.ellipseStats.centerY - self.ellipseStats.bAxis/2

            self._ellipse_selector.extents = (xmin, xmax, ymin, ymax)

    def redraw_ellipse_with_interaction(self):

        """
        Redraw the ellipse on the axe and maintain the state of the active tool when
        a slice had been changed
        """

        if self._ellipse_selector.active:
            self._enable_ellipse()
            xmax = self.ellipseStats.centerX + self.ellipseStats.aAxis/2
            xmin = self.ellipseStats.centerX - self.ellipseStats.aAxis/2
            ymax = self.ellipseStats.centerY + self.ellipseStats.bAxis/2
            ymin = self.ellipseStats.centerY - self.ellipseStats.bAxis/2

            self._ellipse_selector.extents = (xmin, xmax, ymin, ymax)
            if self.ellipseStats.aAxis != -1:
                pub.sendMessage('ellipseSelected')

        elif self._ellipse_selector.visible:
            xmax = self.ellipseStats.centerX + self.ellipseStats.aAxis/2
            xmin = self.ellipseStats.centerX - self.ellipseStats.aAxis/2
            ymax = self.ellipseStats.centerY + self.ellipseStats.bAxis/2
            ymin = self.ellipseStats.centerY - self.ellipseStats.bAxis/2

            self._ellipse_selector.extents = (xmin, xmax, ymin, ymax)

    def redraw_ellipse_from_elliButton(self):

        if self.ellipseStats.centerX != -1:
            self._enable_ellipse()

            xmax = self.ellipseStats.centerX + self.ellipseStats.aAxis/2
            xmin = self.ellipseStats.centerX - self.ellipseStats.aAxis/2
            ymax = self.ellipseStats.centerY + self.ellipseStats.bAxis/2
            ymin = self.ellipseStats.centerY - self.ellipseStats.bAxis/2

            self._ellipse_selector.extents = (xmin, xmax, ymin, ymax)
            pub.sendMessage('ellipseSelected')

    def rectangle_active(self):
        return self._rectangle_selector.active
    def ellipse_active(self):
        return self._ellipse_selector.active

    def get_ellipse_data(self):
        return self._ellipse_selector._rect_bbox, self._ellipse_selector.center
    def get_rectangle_data(self):
        return self._rectangle_selector._rect_bbox, self._rectangle_selector.center

    def set_initial_limits(self, xlim, ylim, cubeXCPix, cubeYCPix, cubeRAValue, cubeDValue, cubeXCRVal, cubeYCRVal):
        """
        Matplotlib cannot display the pixel of the image given integer numbers,
        because of that, the range of the pixel representation  is  (x.5 to x+1.5)
        and instead of starting in 0, it starts in -0.5
        """

        #self.initial_xlim = (1.0, xlim+1.0)
        #self.initial_ylim = (1.0, ylim+1.0)
        self.initial_xlim = xlim
        self.initial_ylim = ylim
        self.twin_initial_xlim = ((self.initial_xlim[0]- cubeXCPix)*cubeRAValue*3600 + cubeXCRVal*3600, (self.initial_xlim[1]- cubeXCPix)*cubeRAValue*3600 + cubeXCRVal*3600)
        self.twin_initial_ylim = ((self.initial_ylim[0]- cubeYCPix)*cubeDValue*3600 + cubeYCRVal*3600, (self.initial_ylim[1]- cubeYCPix)*cubeDValue*3600 + cubeYCRVal*3600)

    def zoom_reset(self):
        for ax in self.figure.axes:
            if ax.get_gid() == 'main_axis':
                ax.set_xlim(self.initial_xlim)
                ax.set_ylim(self.initial_ylim)
            elif ax.get_gid() == 'twinx_axis':
                ax.set_ylim(self.twin_initial_ylim)
            elif ax.get_gid() == 'twiny_axis':
                ax.set_xlim(self.twin_initial_xlim)

        self._draw()

    def clear_elements_axes(self, ax):
        self.create_ellipse_ax(ax)
        self.create_rectangle_ax(ax)

        self.rectangleStats = rectangle_selection(-1,-1,-1,-1)
        self.ellipseStats = ellipse_selection(-1,-1,-1,-1)

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.figure.canvas.draw()
