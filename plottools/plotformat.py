"""
# Plot format

Layout settings for a plot figure.

- `plot_format()`: set default plot format.
- `cm_size()`: convert dimensions from cm to inch.
- `show_spines()`: show spines and ticks of specified positions only.
"""

import matplotlib as mpl


def plot_format(fontsize=10.0):
    """ Set default plot format.

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


def cm_size(width, height):
    """ Convert dimensions from cm to inch.

    Parameters
    ----------
    width: float
        Width of the plot figure in centimeter.
    height: float
        Height of the plot figure in centimeter.

    Returns
    -------
    width: float
        Width of the plot figure in inch.
    height: float
        Height of the plot figure in inch.
    """
    inch_fac = 2.54
    return width/inch_fac, height/inch_fac


def show_spines(ax, spines):
    """ Show spines and ticks of specified positions only.

    Parameters
    ----------
    ax: matplotlib axis
        Axis whose spines and ticks ar emanipulated.
    spines: string
        Specify which spines and ticks should be shown. All other ones or hidden.
        'l' is the left spine, 'r' the right spine, 't' the top one and 'b' the bottom one.
        E.g. 'lb' shows the left and bottom spine, and hides the top and and right spines,
        as well as their tick marks and labels.
        '' shows not spine at all.
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
    # hide spines:
    if not 'top' in xspines:
        ax.spines['top'].set_visible(False)
    if not 'bottom' in xspines:
        ax.spines['bottom'].set_visible(False)
    if not 'left' in yspines:
        ax.spines['left'].set_visible(False)
    if not 'right' in yspines:
        ax.spines['right'].set_visible(False)
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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plot_format()
    fig, ax = plt.subplots(figsize=cm_size(16.0, 10.0))
    show_spines(ax, 'lb')
    plt.show()
