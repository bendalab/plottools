"""
# Ticks

Convience functions for setting tick locations and formats.

The following functions are also added as members to mpl.axes.Axes:
- `set_xticks_delta()`: set distance between xticks.
- `set_yticks_delta()`: set distance between yticks.
- `set_xticks_none()`: do not draw any xticks.
- `set_yticks_none()`: do not draw any yticks.
- `set_xticks_format()`: format xticks according to formatter string.
- `set_yticks_format()`: format yticks according to formatter string.
- `set_xticks_blank()`: draw xticks without labeling them.
- `set_yticks_blank()`: draw yticks without labeling them.
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


def set_xticks_none(ax):
    """ Do not draw any xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_locator(ticker.NullLocator())


def set_yticks_none(ax):
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

    
def demo():
    """ Run a demonstration of the ticks module.
    """
    pass


# make functions available as member variables:
mpl.axes.Axes.set_xticks_delta = set_xticks_delta
mpl.axes.Axes.set_yticks_delta = set_yticks_delta
mpl.axes.Axes.set_xticks_none = set_xticks_none
mpl.axes.Axes.set_yticks_none = set_yticks_none
mpl.axes.Axes.set_xticks_format = set_xticks_format
mpl.axes.Axes.set_yticks_format = set_yticks_format
mpl.axes.Axes.set_xticks_blank = set_xticks_blank
mpl.axes.Axes.set_yticks_blank = set_yticks_blank


if __name__ == "__main__":
    demo()
