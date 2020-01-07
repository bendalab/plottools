"""
# Plot format

Layout settings for a plot figure.

- `plot_format()`: set default plot format.
- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.
- `colors`: list of nice colors

The following function is also added as a member to mpl.axes.Axes:
- `show_spines()`: show and hide spines and ticks.

Dictionaries with colors:
- `colors`: the default colors, set to one of the following:
- `colors_bendalab`: muted colors used by the Benda-lab.
- `colors_bendalab_vivid`: vivid colors used by the Benda-lab.
- `colors_henninger`: colors by Joerg Henninger.
- `colors_scicomp`: colors from the scientific computing script.
- `colors_uni_tuebingen`: colors of the corporate design of the university of Tuebingen.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import OrderedDict


""" Muted colors used by the Benda-lab. """
colors_bendalab = OrderedDict()
colors_bendalab['red'] = '#C02010'
colors_bendalab['orange'] = '#F78010'
colors_bendalab['yellow'] = '#F7E030'
colors_bendalab['green'] = '#97C010'
colors_bendalab['cyan'] = '#40A787'
colors_bendalab['blue'] = '#2050A0'
colors_bendalab['purple'] = '#7040A0'
colors_bendalab['pink'] = '#D72060'

""" Vivid colors used by the Benda-lab. """
colors_bendalab_vivid = OrderedDict()
colors_bendalab_vivid['red'] = '#D01000'
colors_bendalab_vivid['orange'] = '#FF9000'
colors_bendalab_vivid['yellow'] = '#FFF700'
colors_bendalab_vivid['green'] = '#30D700'
colors_bendalab_vivid['cyan'] = '#00F0B0'
colors_bendalab_vivid['blue'] = '#0020C0'
colors_bendalab_vivid['purple'] = '#B000B0'
colors_bendalab_vivid['pink'] = '#F00080'

""" Colors by Joerg Henninger. """
colors_henninger = OrderedDict()
colors_henninger['red'] = '#BA2D22'
colors_henninger['orange'] = '#F47F17'
colors_henninger['green'] = '#AAB71B'
colors_henninger['blue'] = '#3673A4'
colors_henninger['purple'] = '#53379B'

""" Colors from the scientific computing script. """
colors_scicomp = OrderedDict()
colors_scicomp['red'] = '#CC0000'
colors_scicomp['orange'] = '#FF9900'
colors_scicomp['lightorange'] = '#FFCC00'
colors_scicomp['yellow'] = '#FFFF66'
colors_scicomp['green'] = '#99FF00'
colors_scicomp['blue'] = '#0000CC'

""" Colors of the corporate design of the university of Tuebingen.
The first three are the primary colors, the remaining ones the secondary colors.
"""
colors_uni_tuebingen = OrderedDict()
colors_uni_tuebingen['darkred'] = '#A51E37'
colors_uni_tuebingen['gold'] = '#B4A069'
colors_uni_tuebingen['black'] = '#32414B'
colors_uni_tuebingen['darkblue'] = '#415A8C'
colors_uni_tuebingen['blue'] = '#0069AA'
colors_uni_tuebingen['lightblue'] = '#50AAC8'
colors_uni_tuebingen['cyan'] = '#82B9A0'
colors_uni_tuebingen['green'] = '#7DA54B'
colors_uni_tuebingen['darkgreen'] = '#326E1E'
colors_uni_tuebingen['red'] = '#C8503C'
colors_uni_tuebingen['purple'] = '#AF6E96'
colors_uni_tuebingen['gray'] = '#B4A096'
colors_uni_tuebingen['lightorange'] = '#D7B469'
colors_uni_tuebingen['orange'] = '#D29600'
colors_uni_tuebingen['brown'] = '#916946'

""" Default color palette. """
colors = colors_bendalab


""" Default spines to be shown (installed by plot_format()). """
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
    if 'axes.prop_cycle' in mpl.rcParams:
        from cycler import cycler
        mpl.rcParams['axes.prop_cycle'] = cycler(color=[colors['blue'], colors['red'],
                                                        colors['orange'], colors['green'],
                                                        colors['purple'], colors['yellow'],
                                                        colors['cyan'], colors['pink']])
    else:
        mpl.rcParams['axes.color_cycle'] = [colors['blue'], colors['red'],
                                            colors['orange'], colors['green'],
                                            colors['purple'], colors['yellow'],
                                            colors['cyan'], colors['pink']]
    
    # when using axislabels module, define the appearance of axis labels:
    #global axis_label_format
    #axis_label_format = '{label} [{unit}]'
    
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


def lighter(color, lightness):
    """ Make a color lighter.

    Parameters
    ----------
    color: string
        An RGB color as a hexadecimal string (e.g. '#rrggbb').
    lightness: float
        The smaller the lightness, the lighter the returned color.
        A lightness of 1 leaves the color untouched.
        A lightness of 0 returns white.

    Returns
    -------
    color: string
        The lighter color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rl = r + (1.0-lightness)*(0xff - r)
    gl = g + (1.0-lightness)*(0xff - g)
    bl = b + (1.0-lightness)*(0xff - b)
    return '#%02X%02X%02X' % (rl, gl, bl)


def darker(color, saturation):
    """ Make a color darker.

    Parameters
    ----------
    color: string
        An RGB color as a hexadecimal string (e.g. '#rrggbb').
    saturation: float
        The smaller the saturation, the darker the returned color.
        A saturation of 1 leaves the color untouched.
        A saturation of 0 returns black.

    Returns
    -------
    color: string
        The darker color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rd = r * saturation
    gd = g * saturation
    bd = b * saturation
    return '#%02X%02X%02X' % (rd, gd, bd)


def plot_colors(ax, colors, n=1):
    """ Plot all colors of a palette and optionally some lighter and darker variants.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colors: dict
        A dictionary with names and rgb hex-strings of colors.
    n: int
        If one, plot the colors of the palette only.
        If larger than one, plot in addition that many
        lighter and darker versions of the colors.
    """
    if n < 1:
        n = 1
    nn = 1 + 2*(n-1)
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    if n > 1:
        recty *= 0.9
    for k, c in enumerate(colors):
        for i in range(-n+1, n):
            if i < 0:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=darker(colors[c], (n+i)/float(n)))
            elif i > 0:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=lighter(colors[c], (n-i)/float(n)))
            else:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=colors[c])
        ax.text(0.5 + 1.5*k, -0.09, c, ha='center')
        ax.text(0.5 + 1.5*k, -0.16, colors[c], ha='center')
    if n > 1:
        for i in range(-n+1, n):
            if i < 0:
                ax.text(-0.1, (i+n-0.6)/nn, '%.0f%%' % (100.0*(n+i)/float(n)), ha='right')
            elif i > 0:
                ax.text(-0.1, (i+n-0.6)/nn, '%.0f%%' % (100.0*(n-i)/float(n)), ha='right')
            else:
                ax.text(-0.1, (i+n-0.6)/nn, '100%', ha='right')
        ax.text(-1.1, 0.75, 'lighter', ha='center', va='center', rotation='vertical')
        ax.text(-1.1, 0.25, 'darker', ha='center', va='center', rotation='vertical')
        ax.set_xlim(-1.5, len(colors)*1.5)
    else:
        ax.set_xlim(-0.5, len(colors)*1.5)
    ax.set_ylim(-0.2, 1.05)


def plot_complementary_colors(ax, colors):
    """ Plot complementary colors of a palette on top of each other.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colors: dict
        A dictionary with names and rgb hex-strings of colors.
    """
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    n = 0
    if 'red' in colors and 'green' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['red'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['green'])
        n += 1
    if 'orange' in colors and 'blue' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['orange'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['blue'])
        n += 1
    if 'yellow' in colors and 'purple' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['yellow'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['purple'])
        n += 1
    if 'pink' in colors and 'cyan' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['pink'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['cyan'])
        n += 1
    if 'pink' in colors and 'blue' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['pink'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['blue'])
        n += 1
    ax.set_xlim(-0.5, n*1.5)
    ax.set_ylim(-0.1, 2.1)


def plot_color_comparison(ax, colorsa, colorsb):
    """ Plot matching colors of two palettes on top of each other.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colorsa: dict
        A dictionary with names and rgb hex-strings of colors.
        This is the reference palette which is plotted completely at the bottom.
    colorsb: dict
        A dictionary with names and rgb hex-strings of colors.
        Colors with names matching the ones from `colorsa` are plotted on top.
    """
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    for k, c in enumerate(colorsa):
        ax.fill(rectx + 1.5*k, recty + 0.0, color=colorsa[c])
        if c in colorsb:
            ax.fill(rectx + 1.5*k, recty + 1.0, color=colorsb[c])
        ax.text(0.5 + 1.5*k, -0.1, c, ha='center')
    ax.set_xlim(-0.5, len(colorsa)*1.5)
    ax.set_ylim(-0.2, 2.1)


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
    ax.text(0.0, -0.23, "ax.show_spines('lbr')")
    # colors
    #plot_complementary_colors(ax, colors)
    #plot_color_comparison(ax, colors, colors_bendalab_vivid)
    #plot_color_comparison(ax, colors, colors_henninger)
    plot_colors(ax, colors, 1)
    #plot_colors(ax, colors, 4)
    ax.set_ylim(-0.27, 1.05)
    plt.show()


# make functions available as member variables:
mpl.axes.Axes.show_spines = show_spines


if __name__ == "__main__":
    demo()
