"""
# Axis labels

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
axis_label_format = '{label} [{unit}]'


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
        An axis label formatted from `label` and `unit`.
    """
    if not unit:
        return label
    else:
        return axis_label_format.format(label=label, unit=unit)


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
    ax.set_xlabel_orig(__axis_label(label, unit), **kwargs)

        
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
    ax.set_ylabel_orig(__axis_label(label, unit), **kwargs)

        
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
    ax.set_zlabel_orig(__axis_label(label, unit), **kwargs)



def demo():
    """ Run a demonstration of the axislabels module.
    """
    fig, ax = plt.subplots()
    x = np.linspace(0.0, 4.0*np.pi, 200)
    y = np.sin(x)
    ax.plot(x, y)
    ax.set_ylim(-1.1, 1.5)
    ax.text(1.0, 1.3, "ax.set_xlabel('Time', 'ms')")
    ax.text(1.0, 1.15, "ax.set_ylabel('Amplitude', 'Pa')")
    ax.set_xlabel('Time', 'ms')
    global axis_label_format
    axis_label_format = '{label} / {unit}'   # usually you would do this before any plotting!
    ax.set_ylabel('Amplitude', 'Pa')
    plt.show()


# make the functions available as member variables:
mpl.axes.Axes.set_xlabel_orig = mpl.axes.Axes.set_xlabel
mpl.axes.Axes.set_xlabel = set_xlabel
mpl.axes.Axes.set_ylabel_orig = mpl.axes.Axes.set_ylabel
mpl.axes.Axes.set_ylabel = set_ylabel
Axes3D.set_zlabel_orig = Axes3D.set_zlabel
Axes3D.set_zlabel = set_zlabel


if __name__ == "__main__":
    demo()
