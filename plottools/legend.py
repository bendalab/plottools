"""
Enhanced legend.


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


def legend_params(legend_size='x-small'):
    """ Set default parameter for the legend module.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    legend_size: float or string or None
        If not None set font size for legend. Either the font size in points,
        or a string like 'medium', 'small', 'x-small', 'large', 'x-large'.
    """
    if legend_size is not None:
        mpl.rcParams['legend.fontsize'] = legend_size


def install_legend():
    """ Patch the `mpl.axes.Axes.legend()` function.

    See also
    --------
    `uninstall_legend()`
    """
    if not hasattr(mpl.axes.Axes, '__legend_orig_legend'):
        mpl.axes.Axes.__legend_orig_legend = mpl.axes.Axes.legend
        mpl.axes.Axes.legend = legend
    

def uninstall_legend():
    """ Uninstall code for legend.

    Call this code to disable anything that was installed by `install_legend()`.

    See also
    --------
    `install_legend()`
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
    legend_params(legend_size='x-small')
    fig, ax = plt.subplots()
    slope1 = 0.5
    slope2 = 0.2
    x = np.linspace(0, 2, 10)
    ax.plot(x, slope1*x-0.2, label='0.2\,\micro m')
    ax.plot(x, slope2*x+0.1, label='whatever')
    ax.legend(loc='upper left')
    plt.show()
    

if __name__ == "__main__":
    demo()


