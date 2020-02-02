"""
# Labels

Annotate axis with label and unit.

The following functions are also provided as mpl.axes.Axes member functions:
- `set_xlabel()`: format the xlabel from a label and an unit.
- `set_ylabel()`: format the ylabel from a label and an unit.
- `set_zlabel()`: format the zlabel from a label and an unit.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


""" This string defines how an axis label is formatted from a label and an unit. """
label_format = '{label} [{unit}]'


def set_label_format(labelf):
    """ Set the string for formatting the axes labels.
    
    Parameters
    ----------
    labelf: string
        A string for formatting the axes labels.
        In this string '{label}' is replaced by the axes' label,
        and '{unit}' is replaced by the axes' unit.
        The default format string is '{label} [{unit}]'.
    """
    global label_format
    label_format = labelf


def __axis_label(label, unit=None):
    """ Format an axis label from a label and a unit
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.

    Returns
    -------
    label: string
        An axis label formatted from `label` and `unit` according to
        the `label_format` string.
    """
    if not unit:
        return label
    else:
        return label_format.format(label=label, unit=unit)


def set_xlabel(ax, label, unit=None, **kwargs):
    """ Format the xlabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_xlabel() function.
    """
    ax.set_xlabel_labels(__axis_label(label, unit), **kwargs)

        
def set_ylabel(ax, label, unit=None, **kwargs):
    """ Format the ylabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_ylabel() function.
    """
    ax.set_ylabel_labels(__axis_label(label, unit), **kwargs)

        
def set_zlabel(ax, label, unit=None, **kwargs):
    """ Format the zlabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_zlabel() function.
    """
    ax.set_zlabel_labels(__axis_label(label, unit), **kwargs)


def align_labels(fig):
    # get axes positions and ticklabel widths:
    renderer = fig.canvas.get_renderer()
    xap = np.zeros(len(fig.get_axes()))
    xlw = np.zeros(len(fig.get_axes()))
    for k, ax in enumerate(fig.get_axes()):
        # XXX need to check for existing label, vertical rotation, xlabel, etc.
        ax_bbox = ax.get_window_extent().get_points()
        pixelx = np.abs(np.diff(ax_bbox[:,0]))[0]
        yax = ax.yaxis
        tw = yax.get_text_widths(renderer)[0]
        tw -= np.abs(np.diff(yax.get_label().get_window_extent(renderer).get_points()[:,0]))[0]
        xc = tw/pixelx
        xlw[k] = xc
        xap[k] = ax_bbox[0,0]
    # compute label position for axes with same position:
    for xp in set(xap):
        xlw[xap == xp] = np.max(xlw[xap == xp])
    # set label position:
    for k, ax in enumerate(fig.get_axes()):
        ax.yaxis.set_label_coords(-xlw[k], 0.5, None)


# make the functions available as member variables:
mpl.axes.Axes.set_xlabel_labels = mpl.axes.Axes.set_xlabel
mpl.axes.Axes.set_xlabel = set_xlabel
mpl.axes.Axes.set_ylabel_labels = mpl.axes.Axes.set_ylabel
mpl.axes.Axes.set_ylabel = set_ylabel
Axes3D.set_zlabel_labels = Axes3D.set_zlabel
Axes3D.set_zlabel = set_zlabel
mpl.figure.Figure.align_labels = align_labels


def demo():
    """ Run a demonstration of the axislabels module.
    """
    fig, axs = plt.subplots(2, 2)
    fig.subplots_adjust(wspace=0.5)
    x = np.linspace(0.0, 4.0*np.pi, 200)
    y = np.sin(x)
    
    axs[0, 0].plot(x, y)
    axs[0, 0].set_ylim(-1.0, 1.7)
    axs[0, 0].text(1.0, 1.3, "ax.set_xlabel('Time', 'ms')")
    axs[0, 0].text(1.0, 1.1, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[0, 0].set_xlabel('Time', 'ms')
    axs[0, 0].set_ylabel('Amplitude', 'Pa')
    
    set_label_format('{label} / {unit}')   # usually you would do this before any plotting!
    axs[1, 0].plot(x, 1000*y)
    axs[1, 0].set_ylim(-1000, 1700)
    axs[1, 0].text(1.0, 1500, "set_label_format('{label} / {unit}')")
    axs[1, 0].text(1.0, 1300, "ax.set_xlabel('Time', 'ms')")
    axs[1, 0].text(1.0, 1100, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[1, 0].set_xlabel('Time', 'ms')
    axs[1, 0].set_ylabel('Amplitude', 'Pa')

    axs[0, 1].set_ylim(-1.0, 1.0)
    axs[0, 1].set_ylabel('Velocity', 'm/s')
    
    axs[1, 1].set_ylim(-10000.0, 10000.0)
    axs[1, 1].set_ylabel('Accelaration', 'm/s^2')
    
    fig.align_labels()    
    plt.show()


if __name__ == "__main__":
    demo()
