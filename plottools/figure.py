"""
# Figure

Size and margins of a figure.

- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def cm_size(*args):
    """ Convert dimensions from cm to inch.

    Use this function to set the size of a figure in centimeter:
    ```
    fig = plt.figure(figsize=cm_size(16.0, 10.0))
    ```

    Parameters
    ----------
    args: one or many float
        Size in centimeter.

    Returns
    -------
    inches: float or list of floats
        Input arguments converted to inch.
    """
    cm_per_inch = 2.54
    if len(args) == 1:
        return args[0]/cm_per_inch
    else:
        return [v/cm_per_inch for v in args]


def adjust_fs(fig=None, left=5.5, right=0.5, bottom=2.8, top=0.5):
    """ Compute plot margins from multiples of the current font size.

    Parameters
    ----------
    fig: matplotlib.figure or None
        The figure from which the figure size is taken. If None use the current figure.
    left: float
        the left margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
    right: float
        the right margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
        *Note:* in contrast to the matplotlib `right` parameters, this specifies the
        width of the right margin, not its position relative to the origin.
    bottom: float
        the bottom margin of the plots given in multiples of the height of a character
        (the current font size).
    top: float
        the right margin of the plots given in multiples of the height of a character
        (the current font size).
        *Note:* in contrast to the matplotlib `top` parameters, this specifies the
        width of the top margin, not its position relative to the origin.

    Example
    -------
    ```
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    fig.subplots_adjust(**adjust_fs(fig, left=4.5))   # no matter what the figsize is!
    ```
    """
    if fig is None:
        fig = plt.gcf()
    ppi = 72.0 # points per inch:
    w, h = fig.get_size_inches()*ppi
    fs = plt.rcParams['font.size']
    return { 'left': left*0.6*fs/w,
             'right': 1.0 - right*0.6*fs/w,
             'bottom': bottom*fs/h,
             'top': 1.0 - top*fs/h }


def demo():
    """ Run a demonstration of the figure module.
    """
    fig, ax = plt.subplots(figsize=cm_size(16.0, 10.0))
    fig.subplots_adjust(**adjust_fs(fig, left=5.0, bottom=2.0, top=1.0, right=2.0))
    x = np.linspace(0.0, 2.0, 200)
    ax.plot(x, np.sin(2.0*np.pi*x))
    plt.show()


if __name__ == "__main__":
    demo()
