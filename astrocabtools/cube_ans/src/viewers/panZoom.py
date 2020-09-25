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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ..models.rectangleSelection import rectangle_selection

__all__ = ["figure_pz"]

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
        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._cids_callback_rectangle = {}

        self.rectangleStats = rectangle_selection(0,0,0,0)

        self._rectangle_selector = None
        self._callback_rectangle = None

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

    def _add_connection_rectangle(self, event_name, callback):
        """Called to add a connection of type rectangle release to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_rectangle[event_name] = callback

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

    def disconnect_rectangle(self):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_rectangle:
                    figure.canvas.mpl_disconnect(cid)
            self._disable_rectangle()
            self._cids_rectangle.clear()

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

    def disconnect(self):
        """Disconnect interaction from Figure."""
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids:
                    figure.canvas.mpl_disconnect(cid)
            self._fig_ref = None

    def _enable_rectangle(self):
            if not self._rectangle_selector.active:
                self._rectangle_selector.set_active(True)

            if not self._rectangle_selector.visible:
                self._rectangle_selector.set_visible(True)

    def connect_rectangle(self):
        for event_name, callback in self._cids_callback_rectangle.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_rectangle.append(cid)
        self._enable_rectangle()

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
                x_axes.add(ax)
                y_axes.add(ax)

        return x_axes, y_axes

    def create_rectangle_ax(self, ax):
        rectprops = dict(facecolor = 'red', edgecolor = 'black', alpha = 0.1,
                         fill = True, linewidth = 1, linestyle= '-')

        self._rectangle_selector = RectangleSelector(ax, self._callback_rectangle,
                                    drawtype= 'box', useblit= True, rectprops= rectprops,
                                    button= [1,3], minspanx = 5, minspany=5,
                                    spancoords='pixels', interactive=True)
        self._disable_rectangle()

    def update_rectangle(self, coord1_1, coord1_2, coord2_1, coord2_2):
        """
        Set coordinates of the rectangle to be drawed, and send message to
        draw the new spectrum
        :param int coord1_1: initial x value of the coordinate
        :param int coord1_2: initial y value of the coordinate
        :param int coord2_1: end x value of the coordinate
        :param int coord2_2: end y value of the coordinate
        """
        #self.disconnect_zoom()
        #self.disconnect_pan()
        self.connect_rectangle()
        self.figure.canvas.clearFocus()
        self._rectangle_selector.extents = (coord1_1, coord2_1, coord1_2, coord2_2)

        self.rectangleStats.ix = coord1_1
        self.rectangleStats.iy = coord1_2
        self.rectangleStats.ex = coord2_1
        self.rectangleStats.ey = coord2_2

        pub.sendMessage('rectangleSelected', ix = coord1_1, iy =coord1_2
                        , ex = coord2_1, ey= coord2_2)
        #self.disconnect_rectangle()

    def redraw_rectangle_without_interaction_tool(self):
        """
        Redraw the rectangle on the axe that does not require to activate tools(pan or zoom)
        after it and to emit the signal named rectangleSelected
        """

        if self.rectangleStats.ix != 0:
            self.connect_rectangle()
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)

            pub.sendMessage('rectangleSelected', ix = self.rectangleStats.ix, iy =self.rectangleStats.iy
                            , ex = self.rectangleStats.ex, ey= self.rectangleStats.ey)


    def redraw_rectangle_from_slider(self):
        """
        Redraw the rectangle on the axe and maintain the state of the active tool when
        a slice had been changed
        """

        if self.rectangleStats.ix != 0:
            self._enable_rectangle()
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)

        pub.sendMessage('rectangleSelected', ix = self.rectangleStats.ix, iy =self.rectangleStats.iy
                            , ex = self.rectangleStats.ex, ey= self.rectangleStats.ey)

    def redraw_rectangle_with_interaction_tool(self):
        """
        Redraw the rectangle  on the axe that requiere to activate tools (pan or zoom) after
        it and to prevent the signal emission
        """

        if self.rectangleStats.ix != 0:
            self._rectangle_selector.set_visible(True)
            self._rectangle_selector.extents = (self.rectangleStats.ix, self.rectangleStats.ex,
                                                self.rectangleStats.iy, self.rectangleStats.ey)

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.canvas.draw()

class ZoomOnWheel(MplInteraction):
    """Class providing zoom on wheel interaction to a matplotlib Figure.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(ZoomOnWheel, self).__init__(figure)
        self._add_connection_zoom('scroll_event', self._on_mouse_wheel)

        self.scale_factor = scale_factor

    @staticmethod
    def _zoom_range(begin, end, center, scale_factor, scale):
        """Compute a 1D range zoomed around center.
        :param float begin: The begin bound of the range.
        :param float end: The end bound of the range.
        :param float center: The center of the zoom (i.e., invariant point)
        :param float scale_factor: The scale factor to apply.
        :param str scale: The scale of the axis
        :return: The zoomed range (min, max)
        """
        if begin < end:
            min_, max_ = begin, end
        else:
            min_, max_ = end, begin

        old_min, old_max = min_, max_

        offset = (center - old_min) / (old_max - old_min)
        range_ = (old_max - old_min) / scale_factor
        new_min = center - offset * range_
        new_max = center + (1. - offset) * range_

        if begin < end:
            return new_min, new_max
        else:
            return new_max, new_min

    def _on_mouse_wheel(self, event):
        """Select scale factor to apply to change limits of axes"""
        if event.step > 0:
            scale_factor = self.scale_factor
        else:
            scale_factor = 1. / self.scale_factor

        # Go through all axes to enable zoom for multiple axes subplots
        x_axes, y_axes = self._axes_to_update(event)

        for ax in x_axes:
            transform = ax.transData.inverted()
            xdata, ydata = transform.transform_point((event.x, event.y))

            xlim = ax.get_xlim()
            xlim = self._zoom_range(xlim[0], xlim[1],
                                    xdata, scale_factor,
                                    ax.get_xscale())
            ax.set_xlim(xlim)

        for ax in y_axes:
            ylim = ax.get_ylim()
            ylim = self._zoom_range(ylim[0], ylim[1],
                                    ydata, scale_factor,
                                    ax.get_yscale())
            ax.set_ylim(ylim)

        if x_axes or y_axes:
            self._draw()
            self.redraw_rectangle_with_interaction_tool()


class PanAndZoom(ZoomOnWheel):
    """Class providing pan & zoom interaction to a matplotlib Figure.
    Left button for pan and zoom on wheel.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(PanAndZoom, self).__init__(figure, scale_factor=1.1)
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
            if ax.contains(event)[0]:
                x_axes.add(ax)
                y_axes.add(ax)
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                if self._pressed_button == 1:  # pan
                    self._pan(event)

    def _on_mouse_release(self, event):
        if self._pressed_button == 1:  # pan
            self.redraw_rectangle_with_interaction_tool()
            self._pan(event)

        self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            self._pan(event)

class Interactions(PanAndZoom):

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(Interactions, self).__init__(figure, scale_factor=1.1)
        self._add_connection_rectangle('button_release_event', self._on_rectangle_release)

        self._add_rectangle_callback(self._line_select_callback)

        self._pressed_button = None

        self._initialx = -1
        self._initialy = -1
        self._endx = -1
        self._endy = -1

    def _on_rectangle_release(self, event):
        """
        Apply the selection on initial and final values of the rectangle
        selector and send message to update the coordinates values on the coordinates window
        """

        if self._initialx == -1 and self._initialy == -1 and self._endx == -1 and self._endy == -1:
            pressed_button = None
            return
        self.rectangleStats.ix = self._initialx
        self.rectangleStats.iy = self._initialy
        self.rectangleStats.ex = self._endx
        self.rectangleStats.ey = self._endy
        pub.sendMessage('rectangleSelected', ix = self._initialx, iy =
                        self._initialy, ex = self._endx, ey= self._endy)

    def _line_select_callback(self, eclick, erelease):
        """
        Obtain initial and final x and y values with the button pressed
        """
        self._initialx, self._initialy = eclick.xdata, eclick.ydata
        self._endx, self._endy = erelease.xdata, erelease.ydata
        self._pressed_button = eclick.button

def figure_pz(*args, **kwargs):
    """matplotlib.pyplot.figure with pan and zoom interaction"""
    fig = _plt.figure(*args, **kwargs)
    fig.pan_zoom = Interactions(fig)
    return fig, fig.canvas
