"""
Setting grid appearance.


## Settings

- `grid_params()`: set some default grid parameter via matplotlib's rc settings.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def grid_params(grid=None, axis=None, which=None,
                color=None, linestyle=None, linewidth=None, alpha=None):
    """ Set some default grid parameter via matplotlib's rc settings.
                  
    Only parameters that are not `None` are updated.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    grid: bool
        Turn grid lines on or off. Sets rcParam `axes.grid`.
    axis: {'both', 'x', 'y'}
        For which axis grid lines should be shown. Sets rcParam `axes.grid.axis`.
    which: {'major', 'minor', 'both'}
        Grid lines for major, minor or both ticks. Sets rcParam `axes.grid.which`.
    color: matplotlib color
        Color of grid lines. Sets rcParam `grid.color`.
    linestyle: string or tuple
        Linestyle of grid lines. Sets rcParam `grid.linestyle`.
    lineswidth: float
        Width of grid lines in points. Sets rcParam `grid.linewidth`.
    alpha: float
        Transparency of grid lines between 0 and 1. Sets rcParam `grid.alpha`.
    """
    if grid is not None:
        mpl.rcParams['axes.grid'] = grid
    if 'axes.grid.axis' in mpl.rcParams and axis is not None:
        mpl.rcParams['axes.grid.axis'] = axis
    if 'axes.grid.which' in mpl.rcParams and which is not None:
        mpl.rcParams['axes.grid.which'] = which
    if color is not None:
        mpl.rcParams['grid.color'] = color
    if linestyle is not None:
        mpl.rcParams['grid.linestyle'] = linestyle
    if linewidth is not None:
        mpl.rcParams['grid.linewidth'] = linewidth
    if alpha is not None:
        mpl.rcParams['grid.alpha'] = alpha


def demo():
    """ Run a demonstration of the grid module.
    """
    grid_params(grid=True, axis='both', which='major',
                color='gray', linestyle='--', linewidth=2, alpha=1)
    fig, ax = plt.subplots()
    fig.suptitle('plottools.grid')
    x = np.linspace(0, 20, 200)
    y = np.sin(x)
    ax.plot(x, y)
    ax.set_ylim(-1.2, 2.0)
    ax.set_xlabel('Time [ms]')
    ax.set_ylabel('Amplitude')
    plt.show()
    grid_params(grid=False)


if __name__ == "__main__":
    demo()
