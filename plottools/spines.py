"""
# Spines

Modify the appearance of spines.

The following functions are added as a members to mpl.axes.Axes:
- `show_spines()`: show and hide spines and corresponding tick marks.
- `set_spines_outward()`: set the specified spines outward.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


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


def set_spines_outward(ax, spines, offset=0, smart_bounds=None):
    """ Set the specified spines outward.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axis whose spines are manipulated.
        If figure, then apply manipulations on all axes of the figure.
        If list of axes, apply manipulations on each of the given axes.
    spines: dictionary or string
        If dictionary then apply offsets and smart bounds as specified
        in the dictionary for each spine individually. Valid dictionary
        keys are "left', 'right', 'top', 'bottom'. If the corresponding
        values are tuples, then the first value specifies the offset by
        which the spines are moved outwards in pixels and the second one
        the smart bound (True, False, or None). Single numbers as values
        specify the offsets, smart bounds are set according to the
        `smart_bound` parameter.
        If string, specify to which spines the offset given by the `offset` argument
        should be applied.
        'l' is the left spine, 'r' the right spine, 't' the top one and 'b' the bottom one.
        E.g. 'lb' applies the offset to the left and bottom spine.
    offset: float
        Move the specified spines outward by that many pixels.
    smart_bounds: boolean or None
        If True do not draw the spine beyond the data range.
        If None do not set the smart bounds behavior.
    """
    # collect axes:
    if isinstance(ax, (list, tuple)):
        axs = ax
    else:
        axs = ax.get_axes()
        if not isinstance(axs, (list, tuple)):
            axs = [axs]
    if isinstance(spines, dict):
        for ax in axs:
            for sp in spines:
                val = spines[sp]
                if isinstance(val, (tuple, list)):
                    offset = val[0]
                    sb = val[1]
                else:
                    offset = val
                    sb = smart_bounds
                ax.spines[sp].set_position(('outward', offset))
                if sb is not None:
                    ax.spines[sp].set_smart_bounds(sb)
    else:
        # collect spine visibility:
        spines_list = []
        if 't' in spines:
            spines_list.append('top')
        if 'b' in spines:
            spines_list.append('bottom')
        if 'l' in spines:
            spines_list.append('left')
        if 'r' in spines:
            spines_list.append('right')
        for ax in axs:
            for sp in spines_list:
                ax.spines[sp].set_position(('outward', offset))
                if smart_bounds is not None:
                    ax.spines[sp].set_smart_bounds(smart_bounds)


def demo():
    """ Run a demonstration of the spine module.
    """
    fig, axs = plt.subplots(2, 2)
    x = np.linspace(0.0, 1.0, 100)
    y = np.sin(2.0*np.pi*x)
    for axx in axs:
        for ax in axx:
            ax.plot(x, y)
            ax.set_ylim(-1.1, 2.0)
            ax.set_spines_outward('lrtb', 10)
            ax.text(0.05, 1.4, "ax.set_spines_outward('lrtb', 10)")
    axs[0, 0].show_spines('lt')
    axs[0, 0].text(0.05, 1.7, "ax.show_spines('lt')")
    axs[0, 1].show_spines('rt')
    axs[0, 1].text(0.05, 1.7, "ax.show_spines('rt')")
    axs[1, 0].show_spines('lb')
    axs[1, 0].text(0.05, 1.7, "ax.show_spines('lb')")
    axs[1, 1].show_spines('rb')
    axs[1, 1 ].text(0.05, 1.7, "ax.show_spines('rb')")
    plt.show()


# make functions available as member variables:
mpl.axes.Axes.show_spines = show_spines
mpl.axes.Axes.set_spines_outward = set_spines_outward


if __name__ == "__main__":
    demo()
