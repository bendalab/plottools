"""
Enhance legend text.


## Enhanced axes member functions

- `legend()`: legend function with LaTeX support.


## Settings

- `legend_params()`: set default parameter for the legend module.


## Install/uninstall legend functions

You usually do not need to call these functions. Upon loading the legend
module, `install_legend()` is called automatically.

- `install_legend()`: install functions of the legend module in matplotlib.
- `uninstall_legend()`: uninstall all code of the legend module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .latex import translate_latex_text


def legend(ax, *args, **kwargs):
    """ Legend function with LaTeX support.
    
    Uses `latex.translate_latex_text()` to improve LaTeX mode of legend
    labels.

    Parameters
    ----------
    Same as `mpl.axes.Axes.legend()`.
    """
    handles, labels = ax.get_legend_handles_labels()
    for k in range(len(labels)):
        labels[k], newkwargs = translate_latex_text(labels[k], **kwargs)
    lgd = ax.__legend_orig_legend(handles, labels, *args, **newkwargs)
    return lgd


def legend_params(fontsize=None, frameon=None, borderpad=None,
                  handlelength=None, handletextpad=None,
                  numpoints=None, scatterpoints=None,
                  labelspacing=None, columnspacing=None):
    """ Set default parameter for the legend module.
                  
    Only parameters that are not `None` are updated.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    fontsize: float or string
        Set font size for legend. Either the font size in points,
        or a string like 'medium', 'small', 'x-small', 'large', 'x-large'.
        Sets rcParam `legend.fontsize`.
    frameon: bool
        Control whether to show a frame around the legend or not.
        Sets rcParam `legend.frameon`.
    borderpad: float
        Whitespace between legend and frame in font size units.
        Sets rcParam `legend.borderpad`.
    handlelength: float
        Length of the legend handles in font size units.
        Sets rcParam `legend.handlelength`.
    handletextpad: float
        White space between legend handles and text in font size units.
        Sets rcParam `legend.handletextpad`.
    numpoints: int
        The number of marker points in the legend handle.
        Sets rcParam `legend.numpoints`.
    scatterpoints: int
        The number of scatter points in the legend handle.
        Sets rcParam `legend.scatterpoints`.
    labelspacing: float
        Vertical space between legend entries in font size units.
        Sets rcParam `legend.labelspacing`.
    columnspacing: float or None
        Space between columns in font size units.
        Sets rcParam `legend.columnspacing`.
    """
    if fontsize is not None:
        mpl.rcParams['legend.fontsize'] = fontsize
    if frameon is not None:
        mpl.rcParams['legend.frameon'] = frameon
    if borderpad is not None:
        mpl.rcParams['legend.borderpad'] = borderpad
    if handlelength is not None:
        mpl.rcParams['legend.handlelength'] = handlelength
    if handletextpad is not None:
        mpl.rcParams['legend.handletextpad'] = handletextpad
    if numpoints is not None:
        mpl.rcParams['legend.numpoints'] = numpoints
    if scatterpoints is not None:
        mpl.rcParams['legend.scatterpoints'] = scatterpoints
    if labelspacing is not None:
        mpl.rcParams['legend.labelspacing'] = labelspacing
    if columnspacing is not None:
        mpl.rcParams['legend.columnspacing'] = columnspacing


def install_legend():
    """ Patch the `mpl.axes.Axes.legend()` function.

    See also
    --------
    uninstall_legend()
    """
    if not hasattr(mpl.axes.Axes, '__legend_orig_legend'):
        mpl.axes.Axes.__legend_orig_legend = mpl.axes.Axes.legend
        mpl.axes.Axes.legend = legend
    

def uninstall_legend():
    """ Uninstall code for legend.

    Call this code to disable anything that was installed by `install_legend()`.

    See also
    --------
    install_legend()
    """
    if hasattr(mpl.axes.Axes, '__legend_orig_legend'):
        mpl.axes.Axes.legend = mpl.axes.Axes.__legend_orig_legend
        delattr(mpl.axes.Axes, '__legend_orig_legend')

                
install_legend()


def demo(usetex=False):
    """ Run a demonstration of the legend module.

    Parameters
    ----------
    usetex: bool
        If `True` use LaTeX mode.
    """
    legend_params(fontsize='x-small', frameon=False, borderpad=0,
                  handlelength=2, handletextpad=4,
                  numpoints=1, scatterpoints=1, labelspacing=2)
    fig, ax = plt.subplots()
    fig.suptitle('plottools.legend')
    slope1 = 0.5
    slope2 = 0.2
    x = np.linspace(0, 2, 10)
    ax.plot(x, slope1*x-0.2, label=r'0.2\,\micro m')
    ax.plot(x, slope2*x+0.1, label=r'whatever')
    ax.legend(loc='upper left')
    plt.show()
    

if __name__ == "__main__":
    demo()


