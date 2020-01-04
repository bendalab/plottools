"""
# Plot format

Layout settings for a plot figure.

- `plot_format()`: set default plot format.
- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.
- `colors`: list of nice colors

The following function is also added as a member to mpl.axes.Axes:
- `show_spines()`: show and hide spines and ticks.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


colors = ['#BA2D22', '#F47F17', '#AAB71B', '#3673A4', '#53379B', '#DC143C', '#1E90FF']


""" Default spines to be shown. """
default_spines = 'lb'


def __axes__init__(ax, *args, **kwargs):
    """ Set some default formatting for a new Axes instance.

    Used by plot_format().
    """
    ax.__init__orig(*args, **kwargs)
    ax.show_spines(default_spines)


def plot_format(fontsize=10.0):
    """ Set default plot format.

    Call this function *before* you create a matplotlib figure.

    You most likely want to copy it and adjust it according to your needs.

    Parameters
    ----------
    fontsize: float
        Fontsize for text in points.
    """
    mpl.rcParams['figure.facecolor'] = 'white'
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.size'] = fontsize
    mpl.rcParams['xtick.labelsize'] = 'small'
    mpl.rcParams['ytick.labelsize'] = 'small'
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    mpl.rcParams['xtick.major.size'] = 2.5
    mpl.rcParams['ytick.major.size'] = 2.5
    mpl.rcParams['legend.fontsize'] = 'x-small'
    # extend Axes constructor (for show_spines()):
    mpl.axes.Subplot.__init__orig = mpl.axes.Subplot.__init__
    mpl.axes.Subplot.__init__ = __axes__init__
    default_spines = 'lbt'


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
    inch_per_cm = 2.54
    if len(args) == 1:
        return args[0]/inch_per_cm
    else:
        return [v/inch_per_cm for v in args]


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


def show_spines(ax, spines):
    """ Show and hide spines.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axis whose spines and ticks are manipulated.
        If figure, then apply manipulations on all axes of the figure.
        If list of axes, apply manipulations on each of the given axes.
    spines: string
        Specify which spines and ticks should be shown. All other ones or hidden.
        'l' is the left spine, 'r' the right spine, 't' the top one and 'b' the bottom one.
        E.g. 'lb' shows the left and bottom spine, and hides the top and and right spines,
        as well as their tick marks and labels.
        '' shows no spines at all.
        'lrtb' shows all spines and tick marks.
    """
    # collect spine visibility:
    xspines = []
    if 't' in spines:
        xspines.append('top')
    if 'b' in spines:
        xspines.append('bottom')
    yspines = []
    if 'l' in spines:
        yspines.append('left')
    if 'r' in spines:
        yspines.append('right')
    # collect axes:
    if isinstance(ax, (list, tuple)):
        axs = ax
    else:
        axs = ax.get_axes()
        if not isinstance(axs, (list, tuple)):
            axs = [axs]
    for ax in axs:
        # hide spines:
        ax.spines['top'].set_visible('top' in xspines)
        ax.spines['bottom'].set_visible('bottom' in xspines)
        ax.spines['left'].set_visible('left' in yspines)
        ax.spines['right'].set_visible('right' in yspines)
        # ticks:
        if len(xspines) == 0:
            ax.xaxis.set_ticks_position('none')
            ax.set_xticks([])
        elif len(xspines) == 1:
            ax.xaxis.set_ticks_position(xspines[0])
        else:
            ax.xaxis.set_ticks_position('both')
        if len(yspines) == 0:
            ax.yaxis.set_ticks_position('none')
            ax.set_yticks([])
        elif len(yspines) == 1:
            ax.yaxis.set_ticks_position(yspines[0])
        else:
            ax.yaxis.set_ticks_position('both')


def demo():
    """ Run a demonstration of the plotformat module.
    """
    # set default plot parameter:
    plot_format()
    # figsize in centimeter:
    fig, ax = plt.subplots(figsize=cm_size(16.0, 10.0))
    fig.subplots_adjust(**adjust_fs(fig, left=4.5, bottom=2.0, top=1.5, right=2.0))
    # only show left, right, and bottom spine
    # (default is left and bottom spine as defined in __axes__init__()
    # via the default_spines string):
    ax.show_spines('lbr')
    ax.text(0.0, -0.2, "ax.show_spines('lbr')")
    # colors
    rectx = np.array([0, 1, 1, 0, 0])
    recty = np.array([0, 0, 1, 1, 0])
    for k, c in enumerate(colors):
        ax.fill(rectx + 1.5*k, recty, color=c)
        ax.text(0.5 + 1.5*k, -0.1, c, ha='center')
    ax.set_xlim(-0.5, len(colors) + 3.5)
    ax.set_ylim(-0.3, 1.1)
    plt.show()


# make functions available as member variables:
mpl.axes.Axes.show_spines = show_spines


if __name__ == "__main__":
    demo()
