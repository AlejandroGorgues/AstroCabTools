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
import numpy as np
import weakref

import matplotlib.pyplot as _plt
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self._rectangles = []
        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._callback_rectangle = None

    def create_rectangle_ax(self, ax):
        rectprops = dict(facecolor = None, edgecolor = 'black', alpha = 1,
         fill=False, linewidth = 1, linestyle = '--')
        self._rectangles.append(RectangleSelector(ax, self._callback_rectangle,
                                           drawtype='box', useblit=True,
                                           rectprops = rectprops,
                                           button=[1, 3],  # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=False))

    def __del__(self):
        self.disconnect()

    def _add_rectangle_callback(self, callback):
        self._callback_rectangle = callback

    def _add_connection_zoom(self, event_name, callback):
        """Called to add a connection to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """

        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_zoom.append(cid)
        self._cids_callback_zoom[event_name] = callback
    def _add_connection_pan(self, event_name, callback):
        """Called to add a connection to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_pan.append(cid)
        self._cids_callback_pan[event_name] = callback

    def disconnect_zoom(self):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_zoom:
                    figure.canvas.mpl_disconnect(cid)
                for rectangle in self._rectangles:
                    rectangle.set_active(False)

        self._cids_zoom.clear()

    def disconnect_pan(self):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_pan:
                    figure.canvas.mpl_disconnect(cid)
        self._cids_pan.clear()

    def connect_zoom(self):
        for event_name, callback in self._cids_callback_zoom.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_zoom.append(cid)
        for rectangle in self._rectangles:
            rectangle.set_active(True)

    def connect_pan(self):
        for event_name, callback in self._cids_callback_pan.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_pan.append(cid)

    def disconnect(self):
        """Disconnect interaction from Figure."""
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_zoom:
                    figure.canvas.mpl_disconnect(cid)
                for cid in self._cids_pan:
                    figure.canvas.mpl_disconnect(cid)
            self._fig_ref = None

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
            if ax.contains(event)[0] and ax.get_label() != "cbar":
                x_axes.add(ax)
                y_axes.add(ax)

        return x_axes, y_axes

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.canvas.draw()


class ZoomWithMouse(MplInteraction):
    """Class providing zoom with elft and right button interaction to a matplotlib Figure.
    """

    def __init__(self, figure=None):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        """
        super(ZoomWithMouse, self).__init__(figure)
        self._add_connection_zoom('button_release_event', self._rectangle_release)
        #Because the rectangle selector can only be created when an axe is created, it passes
        #the callback function that is gonna be added to the rectangle selector properties
        self._add_rectangle_callback(self._line_select_callback)

        self._pressed_button = None  # To store active button
        self._initial_x = -1
        self._initial_y = -1
        self._end_x = -1
        self._end_y = -1


    def _rectangle_release(self, event):
        """
        Apply the zoom base on initial and final values of the rectangle selector
        """

        #Set threshold to limit zoom in for 5 units
        if (abs(self._end_x - self._initial_x) < 5 or abs(self._end_y - self._initial_y) < 5) and self._pressed_button == 1:
            self._pressed_button = None
            return

        #check if there are twin axes
        x_axes, y_axes = self._axes_to_update(event)

        if self._pressed_button == 1:  # Zoom in

            for ax in x_axes:
                xmin0, xmax0 = ax.get_xbound()
                xmin, xmax = np.clip(sorted([self._initial_x, self._end_x]), xmin0, xmax0)
                ax.set_xbound(xmin, xmax)

            for ax in y_axes:
                ymin0, ymax0 = ax.get_ybound()
                ymin, ymax = np.clip(sorted([self._initial_y, self._end_y]), ymin0, ymax0)
                ax.set_ybound(ymin, ymax)

        elif self._pressed_button == 3: #Zoom out

            #For each axes, get the bounds, create an np array between selected values
            #and the bound values. Get the transformation function and apply it to
            #each of the values between the limits and the selected one. Get the
            #factor that need to be applied to the values and apply it
            for ax in x_axes:
                xmin0, xmax0 = ax.get_xbound()
                xmin, xmax = np.clip(sorted([self._initial_x, self._end_x]), xmin0, xmax0)
                x_trf = ax.get_xaxis().get_transform()
                sxmin0, sxmax0, sxmin, sxmax = x_trf.transform(
                    [xmin0, xmax0, xmin, xmax])  # To screen space.
                factor = (sxmax0 - sxmin0) / (sxmax - sxmin)  # Unzoom factor.
                # Move original bounds away by
                # (factor) x (distance between unzoom box and axes bbox).
                sxmin1 = sxmin0 - factor * (sxmin - sxmin0)
                sxmax1 = sxmax0 + factor * (sxmax0 - sxmax)
                # And back to data space.
                new_xbound = x_trf.inverted().transform([sxmin1, sxmax1])
                ax.set_xbound(new_xbound)

                #repeat for y axes
            for ax in y_axes:
                ymin0, ymax0 = ax.get_ybound()
                ymin, ymax = np.clip(sorted([self._initial_y, self._end_y]), ymin0, ymax0)

                y_trf = ax.get_yaxis().get_transform()
                symin0, symax0, symin, symax = y_trf.transform(
                    [ymin0, ymax0, ymin, ymax])
                factor = (symax0 - symin0) / (symax - symin)
                symin1 = symin0 - factor * (symin - symin0)
                symax1 = symax0 + factor * (symax0 - symax)
                new_ybound = y_trf.inverted().transform([symin1, symax1])
                ax.set_ybound(new_ybound)

        self._draw()
        self._pressed_button = None


    def _line_select_callback(self, eclick, erelease):
        """
        Obtain initial x and y values, end x and y values and button pressed
        """
        self._initial_x, self._initial_y = eclick.xdata, eclick.ydata
        self._end_x, self._end_y  = erelease.xdata, erelease.ydata

        self._pressed_button = eclick.button



class PanAndZoom(ZoomWithMouse):
    """Class providing pan & zoom interaction to a matplotlib Figure.
    Left button for pan and left and right button to zoom in and out.
    """

    def __init__(self, figure=None):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(PanAndZoom, self).__init__(figure)
        self._add_connection_pan('button_press_event', self._on_mouse_press)
        self._add_connection_pan('button_release_event', self._on_mouse_release)
        self._add_connection_pan('motion_notify_event', self._on_mouse_motion)

        self._pressed_button = None  # To store active button
        self._axes = None  # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction

    def _pan_update_limits(self, ax, axis_id, event, last_event):
        """Compute limits with applied pan."""
        if axis_id == 0:
            lim = ax.get_xlim()
        else:
            lim = ax.get_ylim()

        #TransData make it possible to transform data values to display values (display of the screen)
        #Inverted allows to transform from a data point to the data point based on the display inverted

        #Because this is possible, we can make for every pad made, transform every value of the image to
        #the ones that will fit on the screen based on the initial (x,y) and the final(x,y)
        #the initial x,y correspond to the button_press_event values, and the final correspond to the button_release_event
        #For each time the motion_notify_event ocurrs, the previous values will be saved and update the image
        pixel_to_data = ax.transData.inverted()
        data = pixel_to_data.transform_point((event.x, event.y))
        last_data = pixel_to_data.transform_point((last_event.x, last_event.y))

        #Otbtain the delta and apply it to update the limits of the figure into the plot
        delta = data[axis_id] - last_data[axis_id]
        new_lim = lim[0] - delta, lim[1] - delta
        return new_lim

    def _pan(self, event):
        """Execute function based on the name of it"""
        if event.name == 'button_press_event':  # begin pan

            self._event = event

        elif event.name == 'button_release_event':  # end pan
            self._event = None

        elif event.name == 'motion_notify_event':  # pan
            if self._event is None:
                return

            if event.x != self._event.x:
                for ax in self._axes[0]:
                    xlim = self._pan_update_limits(ax, 0, event, self._event)
                    ax.set_xlim(xlim)

            if event.y != self._event.y:
                for ax in self._axes[1]:
                    ylim = self._pan_update_limits(ax, 1, event, self._event)
                    ax.set_ylim(ylim)

            if event.x != self._event.x or event.y != self._event.y:
                self._draw()

            self._event = event

    def _on_mouse_press(self, event):
        """Set axes values based on point selected"""
        if self._pressed_button is not None:
            return  # Discard event if a button is already pressed

        x_axes = set()
        y_axes = set()
        for ax in self.figure.axes:
            #Simmilar to event.inaxis = axis
            if ax.contains(event)[0] and ax.get_label() != "cbar":
                x_axes.add(ax)
                y_axes.add(ax)
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                if self._pressed_button == 1:  # pan
                    self._pan(event)

    def _on_mouse_release(self, event):
        if self._pressed_button == 1:  # pan
            self._pan(event)
        self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            self._pan(event)

def figure_pz(*args, **kwargs):
    """matplotlib.pyplot.figure with pan and zoom interaction"""
    fig = _plt.figure(*args, **kwargs)
    fig.pan_zoom = PanAndZoom(fig)
    return fig, fig.canvas
