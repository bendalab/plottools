"""
# Ticks

Convience functions for setting tick locations and formats.

The following functions are also added as members to mpl.axes.Axes:
- `set_xticks_delta()`: set distance between xticks.
- `set_yticks_delta()`: set distance between yticks.
- `set_xticks_fixed()`: set custom xticks at fixed positions.
- `set_yticks_fixed()`: set custom yticks at fixed positions.
- `set_xticks_off()`: do not draw any xticks.
- `set_yticks_off()`: do not draw any yticks.
- `set_xticks_format()`: format xticks according to formatter string.
- `set_yticks_format()`: format yticks according to formatter string.
- `set_xticks_blank()`: draw xticks without labeling them.
- `set_yticks_blank()`: draw yticks without labeling them.

- `set_minor_xticks_off()`: do not draw any minor xticks.
- `set_minor_yticks_off()`: do not draw any minor yticks.

"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def set_xticks_delta(ax, delta):
    """ Set distance between xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    delta: float
        Distance between xticks.
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_yticks_delta(ax, delta):
    """ Set distance between yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    delta: float
        Distance between yticks.
    """
    ax.yaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_xticks_fixed(ax, locs, labels='%g'):
    """ Set custom xticks at fixed positions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    locs: list of floats
        Locations of xticks.
    labels: string or list of strings
        Either a format string (e.g. '%.1f') or a list of labels
        for each tick position in `locs`.
    """
    ax.xaxis.set_major_locator(ticker.FixedLocator(locs))
    if isinstance(labels, (tuple, list)):
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))
    else:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labels))


def set_yticks_fixed(ax, locs, labels='%g'):
    """ Set custom yticks at fixed positions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    locs: list of floats
        Locations of yticks.
    labels: string or list of strings
        Either a format string (e.g. '%.1f') or a list of labels
        for each tick position in `locs`.
    """
    ax.yaxis.set_major_locator(ticker.FixedLocator(locs))
    if isinstance(labels, (tuple, list)):
        ax.yaxis.set_major_formatter(ticker.FixedFormatter(labels))
    else:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labels))


def set_xticks_off(ax):
    """ Do not draw any xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_locator(ticker.NullLocator())


def set_yticks_off(ax):
    """ Do not draw any yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    """
    ax.yaxis.set_major_locator(ticker.NullLocator())


def set_xticks_format(ax, fs):
    """ Format xticks according to formatter string.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    fs: string
        Format string used to format xticks.
    """
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(fs))


def set_yticks_format(ax, fs):
    """ Format yticks according to formatter string.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    fs: string
        Format string used to format xticks.
    """
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(fs))


def set_xticks_blank(ax):
    """ Draw xticks without labeling them.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_formatter(ticker.NullFormatter())


def set_yticks_blank(ax):
    """ Draw yticks without labeling them.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    """
    ax.yaxis.set_major_formatter(ticker.NullFormatter())


def set_minor_xticks_off(ax):
    """ Do not draw any minor xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the minor xticks are set.
    """
    ax.xaxis.set_minor_locator(ticker.NullLocator())


def set_minor_yticks_off(ax):
    """ Do not draw any minor yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the minor yticks are set.
    """
    ax.yaxis.set_minor_locator(ticker.NullLocator())


# make functions available as member variables:
mpl.axes.Axes.set_xticks_delta = set_xticks_delta
mpl.axes.Axes.set_yticks_delta = set_yticks_delta
mpl.axes.Axes.set_xticks_fixed = set_xticks_fixed
mpl.axes.Axes.set_yticks_fixed = set_yticks_fixed
mpl.axes.Axes.set_xticks_off = set_xticks_off
mpl.axes.Axes.set_yticks_off = set_yticks_off
mpl.axes.Axes.set_xticks_format = set_xticks_format
mpl.axes.Axes.set_yticks_format = set_yticks_format
mpl.axes.Axes.set_xticks_blank = set_xticks_blank
mpl.axes.Axes.set_yticks_blank = set_yticks_blank
mpl.axes.Axes.set_minor_xticks_off = set_minor_xticks_off
mpl.axes.Axes.set_minor_yticks_off = set_minor_yticks_off

    
def demo():
    """ Run a demonstration of the ticks module.
    """
    fig, axs = plt.subplots(2, 2)

    fig.suptitle('plottools.ticks')

    axs[0,0].text(0.1, 0.8, 'ax.set_xticks_delta(1.0)')
    axs[0,0].text(0.1, 0.6, 'ax.set_yticks_delta(0.5)')
    axs[0,0].set_xticks_delta(1.0)
    axs[0,0].set_yticks_delta(0.5)

    axs[0,1].text(0.1, 0.8, 'ax.set_xticks_off()')
    axs[0,1].text(0.1, 0.6, 'ax.set_yticks_off()')
    axs[0,1].set_xticks_off()
    axs[0,1].set_yticks_off()

    axs[1,0].text(0.1, 0.8, "ax.set_xticks_format('%04.1f')")
    axs[1,0].text(0.1, 0.6, "ax.set_yticks_format('%.2f')")
    axs[1,0].set_xticks_format('%04.1f')
    axs[1,0].set_yticks_format('%.2f')

    axs[1,1].text(0.1, 0.8, 'ax.set_xticks_blank()')
    axs[1,1].text(0.1, 0.6, 'ax.set_yticks_blank()')
    axs[1,1].set_xticks_blank()
    axs[1,1].set_yticks_blank()
    
    plt.show()


if __name__ == "__main__":
    demo()
