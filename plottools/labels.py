"""
Annotate axis with label and unit.


## Axes member functions

- `set_xlabel()`: format the xlabel from a label and an unit.
- `set_ylabel()`: format the ylabel from a label and an unit.
- `set_zlabel()`: format the zlabel from a label and an unit.


## Settings

- `labels_params()`: set parameters for axis labels.

`mpl.ptParams` defined by the labels module:
```py
axes.label.format: '{label} [{unit}]'
```

## Install/uninstall labels functions

You usually do not need to call the `install_labels()` function. Upon
loading the labels module, `install_labels()` is called automatically.

- `install_labels()`: install functions of the labels module in matplotlib.
- `uninstall_labels()`: uninstall all code of the labels module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
        the `ptParams['axes.label.format']` string.
    """
    if not unit:
        return label
    else:
        return mpl.ptParams['axes.label.format'].format(label=label, unit=unit)


def set_xlabel(ax, label, unit=None, **kwargs):
    """ Format the xlabel from a label and an unit.

    Uses the `__axis_label()` function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the `set_xlabel()` function.
    """
    ax.__set_xlabel_labels(__axis_label(label, unit), **kwargs)

        
def set_ylabel(ax, label, unit=None, **kwargs):
    """ Format the ylabel from a label and an unit.

    Uses the `__axis_label()` function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the `set_ylabel()` function.
    """
    ax.__set_ylabel_labels(__axis_label(label, unit), **kwargs)

        
def set_zlabel(ax, label, unit=None, **kwargs):
    """ Format the zlabel from a label and an unit.

    Uses the `__axis_label()` function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the `set_zlabel()` function.
    """
    ax.__set_zlabel_labels(__axis_label(label, unit), **kwargs)


def labels_params(lformat=None, label_size=None):
    """ Set parameters for axis labels.
                  
    Only parameters that are not `None` are updated.
    
    Parameters
    ----------
    lformat: string
        Set the string specifying how axes labels are formatted.
        In this string '{label}' is replaced by the axes' label,
        and '{unit}' is replaced by the axes' unit.
        The default format string is '{label} [{unit}]'.
        Set ptParam `axes.label.format`.
    label_size: float or string
        Set font size for x- and y-axis labels
        Sets rcParams `xtick.labelsize` and `ytick.labelsize`.
    """
    if hasattr(mpl, 'ptParams'):
        if lformat is not None:
            mpl.ptParams['axes.label.format'] = lformat
    if label_size is not None:
        mpl.rcParams['xtick.labelsize'] = label_size
        mpl.rcParams['ytick.labelsize'] = label_size


def install_labels():
    """ Install labels functions on matplotlib axes.

    Adds mpl.ptParams:
    ```py
    axes.label.format: '{label} [{unit}]'
    ```

    This function is also called automatically upon importing the module.

    See also
    --------
    - `set_xlabel()`
    - `uninstall_labels()`
    """
    if not hasattr(mpl.axes.Axes, '__set_xlabel_labels'):
        mpl.axes.Axes.__set_xlabel_labels = mpl.axes.Axes.set_xlabel
        mpl.axes.Axes.set_xlabel = set_xlabel
    if not hasattr(mpl.axes.Axes, '__set_ylabel_labels'):
        mpl.axes.Axes.__set_ylabel_labels = mpl.axes.Axes.set_ylabel
        mpl.axes.Axes.set_ylabel = set_ylabel
    if not hasattr(Axes3D, '__set_zlabel_labels'):
        Axes3D.__set_zlabel_labels = Axes3D.set_zlabel
        Axes3D.set_zlabel = set_zlabel
    # add labels parameter to rc configuration:
    if not hasattr(mpl, 'ptParams'):
        mpl.ptParams = {}
    if 'axes.label.format' not in mpl.ptParams:
        mpl.ptParams['axes.label.format'] = '{label} [{unit}]'
        

def uninstall_labels():
    """ Uninstall labels functions from matplotlib axes.

    Call this function to disable anything that was installed by `install_labels()`.

    See also
    --------
    - `install_labels()`
    """
    if hasattr(mpl.axes.Axes, '__set_xlabel_labels'):
        mpl.axes.Axes.set_xlabel = mpl.axes.Axes.__set_xlabel_labels
        delattr(mpl.axes.Axes, '__set_xlabel_labels')
    if hasattr(mpl.axes.Axes, '__set_ylabel_labels'):
        mpl.axes.Axes.set_ylabel = mpl.axes.Axes.__set_ylabel_labels
        delattr(mpl.axes.Axes, '__set_ylabel_labels')
    if hasattr(Axes3D, '__set_zlabel_labels'):
        Axes3D.set_zlabel = Axes3D.__set_zlabel_labels
        delattr(Axes3D, '__set_zlabel_labels')
    # remove labels parameter from mpl.ptParams:
    if hasattr(mpl, 'ptParams') and 'axess.label.format' in mpl.ptParams:
        mpl.ptParams.pop('axes.label.format', None)


install_labels()


def demo():
    """ Run a demonstration of the labels module.
    """
    fig, axs = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0.5)
    fig.suptitle('plottools.labels')

    x = np.linspace(0, 20, 200)
    y = np.sin(x)
    
    axs[0].plot(x, y)
    axs[0].set_ylim(-1.0, 1.7)
    axs[0].text(1.0, 1.3, "ax.set_xlabel('Time', 'ms')")
    axs[0].text(1.0, 1.1, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[0].set_xlabel('Time', 'ms')
    axs[0].set_ylabel('Amplitude', 'Pa')
    
    labels_params(lformat='{label} / {unit}')   # usually you would do this before any plotting!
    axs[1].plot(x, 1000*y)
    axs[1].set_ylim(-1000, 1700)
    axs[1].text(1.0, 1500, "labels_params('{label} / {unit}')")
    axs[1].text(1.0, 1300, "ax.set_xlabel('Time', 'ms')")
    axs[1].text(1.0, 1100, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[1].set_xlabel('Time', 'ms')
    axs[1].set_ylabel('Amplitude', 'Pa')
    
    plt.show()

if __name__ == "__main__":
    demo()
