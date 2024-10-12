"""
Annotate axis with label and unit.


## Axes member functions

- `set_xlabel()`: format the xlabel from a label and an unit.
- `set_ylabel()`: format the ylabel from a label and an unit.
- `set_zlabel()`: format the zlabel from a label and an unit.


## Settings

- `labels_params()`: set parameters for axis labels.

`mpl.rcParams` defined by the labels module:
```py
axes.label.format: '{label} [{unit}]'
xaxis.labelrotation: 'horizontal'
yaxis.labelrotation: 'vertical'
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
import matplotlib.rcsetup as mrc
try:
    from mpl_toolkits.mplot3d import Axes3D
    has_zlabel = True
except ImportError:
    has_zlabel = False


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
        the `rcParams['axes.label.format']` string.
    """
    if not unit:
        return label
    else:
        return mpl.rcParams['axes.label.format'].format(label=label, unit=unit)


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
    if not 'rotation' in kwargs:
        kwargs.update(rotation=mpl.rcParams['xaxis.labelrotation'])
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
    if not 'rotation' in kwargs:
        kwargs.update(rotation=mpl.rcParams['yaxis.labelrotation'])
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


def labels_params(labelformat=None, labelsize=None, labelweight=None,
                  labelcolor='axes', labelpad=None,
                  xlabelloc=None, ylabelloc=None,
                  xlabelrot=None, ylabelrot=None):
    """ Set parameters for axis labels.
                  
    Only parameters that are not `None` are updated.
    
    Parameters
    ----------
    labelformat: string
        Set the string specifying how axes labels are formatted.
        In this string '{label}' is replaced by the axes' label,
        and '{unit}' is replaced by the axes' unit.
        The default format string is '{label} [{unit}]'.
        Set rcParam `axes.label.format`.
    labelsize: float or string
        Set font size for x- and y-axis labels.
        Sets rcParam `axes.labelsize`.
    labelweight: {'normal', 'bold', 'bolder', 'lighter'}
        Set font weight for x- and y-axis labels.
        Sets rcParam `axes.labelweight`.
    labelcolor: matplotlib color or 'axes'
        Color of x- and y-axis labels.
        If 'axes' set to color of axes (rcParam `axes.edgecolor`).
        Sets rcParam `axes.labelcolor`.
    labelpad: float
        Set space between x- and y-axis labels and axis in points.
        Sets rcParam `axes.labelpad`.
    xlabelloc: {'center', 'left', 'right'}
        Location of xlabels. Sets rcParams `xaxis.labellocation`.
    ylabelloc: {'center', 'bottom', 'top'}
        Location of ylabels. Sets rcParams `yaxis.labellocation`.
    xlabelrot: float, or {'horizontal', 'vertical'}
        Rotation angle of xlabels. Sets rcParams `xaxis.labelrotation`.
    ylabelrot: float, or {'horizontal', 'vertical'}
        Rotation angle of ylabels. Sets rcParams `yaxis.labelrotation`.
    """
    if labelformat is not None and 'axes.label.format' in mrc._validators:
        mpl.rcParams['axes.label.format'] = labelformat
    if labelsize is not None:
        mpl.rcParams['axes.labelsize'] = labelsize
    if labelweight is not None:
        mpl.rcParams['axes.labelweight'] = labelweight
    if labelcolor == 'axes':
        mpl.rcParams['axes.labelcolor'] = mpl.rcParams['axes.edgecolor']
    elif labelcolor is not None:
        mpl.rcParams['axes.labelcolor'] = labelcolor
    if 'axes.labelpad' in mpl.rcParams and labelpad is not None:
        mpl.rcParams['axes.labelpad'] = labelpad
    if 'xaxis.labellocation' in mpl.rcParams and xlabelloc is not None:
        mpl.rcParams['xaxis.labellocation'] = xlabelloc
    if 'yaxis.labellocation' in mpl.rcParams and ylabelloc is not None:
        mpl.rcParams['yaxis.labellocation'] = ylabelloc
    if 'xaxis.labelrotation' in mpl.rcParams and xlabelrot is not None:
        mpl.rcParams['xaxis.labelrotation'] = xlabelrot
    if 'yaxis.labelrotation' in mpl.rcParams and ylabelrot is not None:
        mpl.rcParams['yaxis.labelrotation'] = ylabelrot

            
def _validate_rotation(s):
    """ Validator for matplotlib.rcsetup.
    """
    if s in ('horizontal', 'vertical'):
        return s
    try:
        return float(s)
    except ValueError as e:
        raise ValueError('not a valid rotation specification for label') from e


def install_labels():
    """ Install labels functions on matplotlib axes.

    Adds `matplotlib.rcParams`:
    ```py
    axes.label.format: '{label} [{unit}]'
    xaxis.labelrotation: 'horizontal'
    yaxis.labelrotation: 'vertical'
    ```

    This function is also called automatically upon importing the module.

    See also
    --------
    set_xlabel(), uninstall_labels()
    """
    if not hasattr(mrc, 'validate_rotation'):
        mrc.validate_rotation = _validate_rotation
    if not hasattr(mpl.axes.Axes, '__set_xlabel_labels'):
        mpl.axes.Axes.__set_xlabel_labels = mpl.axes.Axes.set_xlabel
        mpl.axes.Axes.set_xlabel = set_xlabel
    if not hasattr(mpl.axes.Axes, '__set_ylabel_labels'):
        mpl.axes.Axes.__set_ylabel_labels = mpl.axes.Axes.set_ylabel
        mpl.axes.Axes.set_ylabel = set_ylabel
    if has_zlabel and not hasattr(Axes3D, '__set_zlabel_labels'):
        Axes3D.__set_zlabel_labels = Axes3D.set_zlabel
        Axes3D.set_zlabel = set_zlabel
    # add parameter to rc configuration:
    if 'axes.label.format' not in mrc._validators:
        mrc._validators['axes.label.format'] = mrc.validate_string
        mpl.rcParams['axes.label.format'] = '{label} [{unit}]'
    if 'xaxis.labelrotation' not in mrc._validators:
        mrc._validators['xaxis.labelrotation'] = mrc.validate_rotation
        mpl.rcParams['xaxis.labelrotation'] = 'horizontal'
    if 'yaxis.labelrotation' not in mrc._validators:
        mrc._validators['yaxis.labelrotation'] = mrc.validate_rotation
        mpl.rcParams['yaxis.labelrotation'] = 'vertical'
        

def uninstall_labels():
    """ Uninstall labels functions from matplotlib axes.

    Call this function to disable anything that was installed by `install_labels()`.

    See also
    --------
    install_labels()
    """
    if hasattr(mrc, 'validate_rotation'):
        delattr(mrc, 'validate_rotation')
    if hasattr(mpl.axes.Axes, '__set_xlabel_labels'):
        mpl.axes.Axes.set_xlabel = mpl.axes.Axes.__set_xlabel_labels
        delattr(mpl.axes.Axes, '__set_xlabel_labels')
    if hasattr(mpl.axes.Axes, '__set_ylabel_labels'):
        mpl.axes.Axes.set_ylabel = mpl.axes.Axes.__set_ylabel_labels
        delattr(mpl.axes.Axes, '__set_ylabel_labels')
    if has_zlabel and hasattr(Axes3D, '__set_zlabel_labels'):
        Axes3D.set_zlabel = Axes3D.__set_zlabel_labels
        delattr(Axes3D, '__set_zlabel_labels')
    # remove parameter from rc configuration:
    if hasattr(mrc._validators, 'axes.label.format'):
        mrc._validators.pop('axes.label.format', None)
    if hasattr(mrc._validators, 'xaxis.labelrotation'):
        mrc._validators.pop('xaxis.labelrotation', None)
    if hasattr(mrc._validators, 'yaxis.labelrotation'):
        mrc._validators.pop('yaxis.labelrotation', None)


install_labels()


def demo():
    """ Run a demonstration of the labels module.
    """
    labels_params(xlabelloc='right', ylabelloc='top')
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
    
    labels_params(labelformat='{label} / {unit}')   # usually you would do this before any plotting!
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
