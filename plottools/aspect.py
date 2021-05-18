"""
Adapting plots to aspect ratio of axes.


## Axes member functions

- `aspect_ratio()`: aspect ratio of axes.
- `set_xlim_equal()`: ensure equal aspect ratio by appropriately setting x limits.
- `set_ylim_equal()`: ensure equal aspect ratio by appropriately setting y limits.


## Install/uninstall aspect functions

You usually do not need to call these functions. Upon loading the aspect
module, `install_aspect()` is called automatically.

- `install_aspect()`: install functions of the aspect module in matplotlib.
- `uninstall_aspect()`: uninstall all code of the aspect module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def aspect_ratio(ax):
    """Aspect ratio of axes.

    Parameters
    ----------
    ax: matplotlib axes
        Axes of which aspect ratio is computed.

    Returns
    -------
    aspect: float
        Aspect ratio (height in inches relative to width).
    """
    figw, figh = ax.get_figure().get_size_inches()
    _, _, w, h = ax.get_position().bounds
    return (figh * h) / (figw * w)


def set_xlim_equal(ax, xmin_frac=0.0, xmax_frac=1.0):
    """ Ensure equal aspect ratio by appropriately setting x limits.

    If you need both axis equally scaled, such that on the plot a unit
    on the x-axis covers the same distance as a unit on the y-axis, one
    usually calls `ax.set_aspect('equal')`. This mechanism scales the
    physical dimensions of the plot to make the units on both axis
    equal.  Problem is, that then the physical dimensions of the plot
    differ from other plots in the grid.

    The `set_xlim_equal()` function uses a different approach. Instead
    of scaling the physical dimensions of the plot, the limits of the
    x-axis are adapted to the aspect-ratio of the full plot. This way
    the dimensions of the plot are not scaled.

    Call this function *after* setting the limits of the x-axis.

    Parameters
    ----------
    ax: matplotlib axes
        Axes of which aspect ratio is computed.
    xmin_frac: float
        Fraction of the total range of the x-axis for the minimum value of the x-axis.
    xmax_frac: float
        Fraction of the total range of the x-axis for the maximum value of the x-axis.

    See Also
    --------
    - `set_ylim_equal()`
    - `aspect_ratio()`
    """
    yrange = np.diff(ax.get_ylim())[0]
    xrange = yrange/(xmax_frac-xmin_frac)/ax.aspect_ratio()
    ax.set_xlim(xmin_frac*xrange, xmax_frac*xrange)


def set_ylim_equal(ax, ymin_frac=0.0, ymax_frac=1.0):
    """ Ensure equal aspect ratio by appropriately setting y limits.

    If you need both axis equally scaled, such that on the plot a unit
    on the x-axis covers the same distance as a unit on the y-axis, one
    usually calls `ax.set_aspect('equal')`. This mechanism scales the
    physical dimensions of the plot to make the units on both axis
    equal.  Problem is, that then the physical dimensions of the plot
    differ from other plots in the grid.

    The `set_ylim_equal()` function uses a different approach. Instead
    of scaling the physical dimensions of the plot, the limits of the
    y-axis are adapted to the aspect-ratio of the full plot. This way
    the dimensions of the plot are not scaled.

    Call this function *after* setting the limits of the x-axis.

    Parameters
    ----------
    ax: matplotlib axes
        Axes of which aspect ratio is computed.
    ymin_frac: float
        Fraction of the total range of the y-axis for the minimum value of the y-axis.
    ymax_frac: float
        Fraction of the total range of the y-axis for the maximum value of the y-axis.

    See Also
    --------
    - `set_xlim_equal()`
    - `aspect_ratio()`
    """
    xrange = np.diff(ax.get_xlim())[0]
    yrange = ax.aspect_ratio()*xrange/(ymax_frac-ymin_frac)
    ax.set_ylim(ymin_frac*yrange, ymax_frac*yrange)


def install_aspect():
    """ Install functions of the aspect module in matplotlib.

    See also
    --------
    uninstall_aspect()
    """
    if not hasattr(mpl.axes.Axes, 'aspect_ratio'):
        mpl.axes.Axes.aspect_ratio = aspect_ratio
    if not hasattr(mpl.axes.Axes, 'set_xlim_equal'):
        mpl.axes.Axes.set_xlim_equal = set_xlim_equal
    if not hasattr(mpl.axes.Axes, 'set_ylim_equal'):
        mpl.axes.Axes.set_ylim_equal = set_ylim_equal


def uninstall_aspect():
    """ Uninstall all code of the aspect module from matplotlib.

    See also
    --------
    install_aspect()
    """
    if hasattr(mpl.axes.Axes, 'aspect_ratio'):
        delattr(mpl.axes.Axes, 'aspect_ratio')
    if hasattr(mpl.axes.Axes, 'set_xlim_equal'):
        delattr(mpl.axes.Axes, 'set_xlim_equal')
    if hasattr(mpl.axes.Axes, 'set_ylim_equal'):
        delattr(mpl.axes.Axes, 'set_ylim_equal')


install_aspect()


def demo():
    """ Run a demonstration of the aspect module.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.subplots_adjust(hspace=0.4)
    fig.suptitle('plottools.aspect')
    for ax in (ax1, ax2, ax3):
        ax.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2])
        ax.plot([-50, 50, -50, 50], [-50, 50, 50, -50])
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
    ax1.text(0.02, 0.8, 'aspect ratio = %.2f' % ax1.aspect_ratio(), transform=ax1.transAxes)
    ax1.text(0.02, 0.6, 'ax1.set_xlim(-10, 10)', transform=ax1.transAxes)
    ax1.text(0.02, 0.4, 'ax1.set_ylim(-10, 10)', transform=ax1.transAxes)
    ax2.set_xlim_equal(-0.5, 0.5)
    ax2.text(0.02, 0.8, 'aspect ratio = %.2f' % ax2.aspect_ratio(), transform=ax2.transAxes)
    ax2.text(0.02, 0.6, 'ax2.set_xlim_equal(-0.5, 0.5)', transform=ax2.transAxes)
    ax3.set_ylim_equal(-0.5, 0.5)
    ax3.text(0.02, 0.8, 'aspect ratio = %.2f' % ax3.aspect_ratio(), transform=ax3.transAxes)
    ax3.text(0.02, 0.6, 'ax3.set_ylim_equal(-0.5, 0.5)', transform=ax3.transAxes)
    plt.show()
        

if __name__ == "__main__":
    demo()
