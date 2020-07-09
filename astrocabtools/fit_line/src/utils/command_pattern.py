import numpy as np
import weakref
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

__all__ = ['PanCommand', 'ZoomCommand', 'ZoomFitCommand', 'UndoHistoryPanInvoker', 'UndoHistoryZoomInvoker']

"""
Command class interface that contains the execute method
"""
class Command(object):

    def execute(self, canvas):
        raise NotImplementedError
"""
PanCommand that inherits the command interface
"""
class PanCommand(Command):
    def __init__(self, event, global_event, axes):
        self._local_event = event
        self._global_event = global_event
        self._axes = axes

    def execute(self, canvas):
        self._pan(canvas)

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

    def _pan(self, canvas):
        """Execute function based on the name of it"""
        if self._local_event.x != self._global_event.x:
            for ax in self._axes[0]:
                xlim = self._pan_update_limits(ax, 0, self._local_event, self._global_event)
                ax.set_xlim(xlim)

        if self._local_event.y != self._global_event.y:
            for ax in self._axes[1]:
                ylim = self._pan_update_limits(ax, 1, self._local_event, self._global_event)
                ax.set_ylim(ylim)

        canvas.draw()

"""
Zoom class that inherits the command interface
"""
class ZoomCommand(Command):
    def __init__(self, pressed_button, initialX, initialY, endX, endY, event, figure):
        self._pressed_button = pressed_button
        self._initial_x = initialX
        self._initial_y = initialY
        self._end_x = endX
        self._end_y = endY
        self._event = event
        self._figure = figure

    def execute(self, canvas):
        self._zoom(canvas)
        canvas.draw()

    def _zoom(self, canvas):
        #check if there are twin axes
        x_axes, y_axes = self._axes_to_update(self._event)

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

    def _axes_to_update(self, event):
        """Returns two sets of Axes to update according to event.
        :param MouseEvent event: Matplotlib event to consider
        :return: Axes for which to update xlimits and ylimits
        :rtype: 2-tuple of set (xaxes, yaxes)
        """
        x_axes, y_axes = set(), set()

        for ax in self._figure.axes:
            if ax.contains(event)[0] and ax.get_label() != "cbar":
                x_axes.add(ax)
                y_axes.add(ax)

        return x_axes, y_axes

"""
Zoom fit class that inherits the command interface
"""
class ZoomFitCommand(Command):
    def __init__(self, figure, xLimits, yLimits):
        self._figure = figure
        self._xLimits = xLimits
        self._yLimits = yLimits

    def execute(self, canvas):
        """
        :param Canvas canvas: canvas that will be updated
        Adjust axe limits to the main one
        """
        for ax in self._figure.axes:
            ax.set_xlim(self._xLimits)
            ax.set_ylim(self._yLimits)
        canvas.draw()

"""
Invoker class that contains all actions related to zoom commands
"""
class UndoHistoryZoomInvoker(object):
    def __init__(self, canvas):
        self._commands = []
        self._canvas = canvas


    def command(self, command):
        self._commands.append(command)
        command.execute(self._canvas)

    def clear_command_list(self):
        self._commands.clear()

    def command_list_length(self):
        return len(self._commands)

    def undo(self):
        """
        Because the zoom operations on an spectrum plot does not have too much
        complexity, the undo command delete the last command from the list and
        execute all previous commands
        """
        self._commands.pop()
        for command in self._commands:
            command.execute(self._canvas)

"""
Invoker class that contains all actions related to pad commands
"""
class UndoHistoryPanInvoker(object):
    def __init__(self, canvas):
        self._canvas = canvas


    def command(self, command):
        command.execute(self._canvas)
