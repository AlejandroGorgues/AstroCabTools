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
from pubsub import pub

from astrocabtools.fit_line.src.utils.command_pattern import UndoHistoryZoomInvoker, UndoHistoryPanInvoker, ZoomFitCommand, PanCommand, ZoomCommand

__all__ = ["figure_pz"]

class MplInteraction(object):


    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        """
        self._fig_ref = weakref.ref(figure)
        self.canvas = FigureCanvas(figure)
        self._cids_zoom = []
        self._cids_pan = []
        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._callback_rectangle = None
        self._rectangle_selector = None
        self._xLimits = None
        self._yLimits = None

        #Create invokers
        self._invokerZoom = UndoHistoryZoomInvoker(figure.canvas)
        self._invokerPan = UndoHistoryPanInvoker(figure.canvas)


    def create_rectangle_ax(self, ax):
        rectprops = dict(facecolor = None, edgecolor = 'black', alpha = 1,
         fill=False, linewidth = 1, linestyle = '-')
        self._rectangle_selector = RectangleSelector(ax, self._callback_rectangle,
                                           drawtype='box', useblit=True,
                                           rectprops = rectprops,
                                           button=[1, 3],  # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=False)

        self._rectangle_selector.set_visible(False)

    def set_axes_limits(self, xLimits, yLimits):
        """
        Get initial limits to allow to adjust the last zoom command to be
        the inital limits
        """
        self._xLimits = xLimits
        self._yLimits = yLimits

    def __del__(self):
        self.disconnect()

    def _add_rectangle_callback(self, callback):
        """
        Beacuse the callback method can only be created when the
        Zoom event is created and the axe can only be know after the creation of it,
        this method allow to assign the callback before
        the creation of the rectangle selector object
        """
        self._callback_rectangle = callback

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

    def disconnect_zoom(self):
        """
        Disconnect all zoom events and disable the rectangle selector
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_zoom:
                    figure.canvas.mpl_disconnect(cid)
                self._disable_rectangle()

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

    def _enable_rectangle(self):
        self._rectangle_selector.set_visible(True)
        self._rectangle_selector.set_active(True)

    def connect_zoom(self):
        """
        Assign all callback zoom events to the mpl
        """
        for event_name, callback in self._cids_callback_zoom.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_zoom.append(cid)

        self._enable_rectangle()

    def connect_pan(self):
        """
        Assign all callback pan events to the mpl
        """
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


    def undo_last_action(self):
        """
        First, it undo the last action made by the zoom event
        Second, because the command list contains each command, the first one
        is related to adjust the zoom, which ocurred before, so the command list
        execute twice the same event, and because of that, the undo button need to
        be disabled and the command list clear
        """
        self._invokerZoom.undo()
        if self._invokerZoom.command_list_length() <= 1:
            self._invokerZoom.clear_command_list()
            pub.sendMessage('setStateUndo', state = False)

    def add_zoom_fit(self):
        if self._invokerZoom.command_list_length() == 0:
            #Send the signal to change undo button state
            pub.sendMessage('setStateUndo', state = True)

        zoomFitCommand = ZoomFitCommand(self.figure, self._xLimits, self._yLimits)
        self._invokerZoom.command(zoomFitCommand)
        self._draw()

    def _add_initial_zoom_fit(self):
        if self._invokerZoom.command_list_length() == 0:
            #Send the signal to change undo button state
            pub.sendMessage('setStateUndo', state = True)

            zoomFitCommand = ZoomFitCommand(self.figure, self._xLimits, self._yLimits)
            self._invokerZoom.command(zoomFitCommand)
            self._draw()


    def clear_commands(self):
        """
        Delete all commands
        """
        self._invokerZoom.clear_command_list()

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
        #Set initial values to the rectangle coordinates
        self._initial_x = -1
        self._initial_y = -1
        self._end_x = -1
        self._end_y = -1

    def _rectangle_release(self, event):
        """
        Apply the zoom base on initial and final values of the rectangle selector
        """
        #Because _line_select_callback is not called when user push and release on the same pixel,
        #the coordinates values change to -1 and this conditional checkif if that it's the value instead
        #of the ones from _line_select_callback
        if self._initial_x == -1 and self._initial_y == -1 and self._end_x == -1 and self._end_y == -1:
            pressed_button= None
            return

        self._add_initial_zoom_fit()
        #Create the command, and execute it
        zoomCommand = ZoomCommand(self._pressed_button, self._initial_x, self._initial_y, self._end_x, self._end_y, event, self.figure)
        self._invokerZoom.command(zoomCommand)

        self._pressed_button = None

        self._initial_x = -1
        self._initial_y = -1
        self._end_x = -1
        self._end_y = -1

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

    def _on_mouse_press(self, event):
        """Set axes values based on point selected"""
        if self._pressed_button is not None or event.dblclick:
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
                    self._event = event

    def _on_mouse_release(self, event):
        if self._pressed_button == 1 and not event.dblclick:  # pan
            self._event = None
        self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            if self._event is None:
                return
            if event.x != self._event.x or event.y != self._event.y:
                #Create the command, and execute it
                panCommand = PanCommand(event, self._event, self._axes)
                self._invokerPan.command(panCommand)
                self._event = event

def figure_pz(*args, **kwargs):
    """matplotlib.pyplot.figure with pan and zoom interaction"""
    fig = _plt.figure(*args, **kwargs)
    fig.pan_zoom = PanAndZoom(fig)
    return fig, fig.canvas
