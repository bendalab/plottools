"""
# Spines

Modify the appearance of spines.

The following functions are added as a members to mpl.axes.Axes and mpl.figure.Figure:
- `show_spines()`: show and hide spines and corresponding tick marks.
- `set_spines_outward()`: set the specified spines outward.
- `set_spines_bounds()`: set bounds for the specified spines.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def show_spines(ax, spines):
    """ Show and hide spines.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axis on which spine and ticks visibility is manipulated.
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
    if isinstance(ax, (list, tuple, np.ndarray)):
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


def set_spines_outward(ax, spines, offset=0):
    """ Set the specified spines outward.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axis on which spines are set outwards.
        If figure, then apply manipulations on all axes of the figure.
        If list of axes, apply manipulations on each of the given axes.
    spines: string or dictionary 
        - string: specify to which spines the offset given by the `offset` argument
          should be applied.
          'l' is the left spine, 'r' the right spine, 't' the top one and 'b' the bottom one.
          E.g. 'lb' applies the offset to the left and bottom spine.
        - dictionary: apply offsets for several sets of spines individually.
          Dictionary keys are strings spcifying the spines as described above.
          The corresponding values specify the offset by which the spines are move outwards.
    offset: float
        Move the specified spines outward by that many pixels.

    Examples
    --------
    ```
    # set left and right spine outwards by 10 pixels:
    ax.set_spines_outward('lr', 10)

    # set the left and right spines outwards by 10 pixels and the top and bottom ones by 5:
    ax.set_spines_outward({'lr': 10, 'bt': 5})

    # set the bottom spine of all axis of the figure outward by 5 pixels:
    fig.set_spines_outward('b', 5)
    ```
    """
    if isinstance(spines, dict):
        for sp in spines:
            set_spines_outward(ax, sp, spines[sp])
    else:
        # collect axes:
        if isinstance(ax, (list, tuple, np.ndarray)):
            axs = ax
        else:
            axs = ax.get_axes()
        if not isinstance(axs, (list, tuple)):
            axs = [axs]
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


def set_spines_bounds(ax, spines, bounds='full'):
    """ Set bounds for the specified spines.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axis on which spine bounds are set.
        If figure, then apply manipulations on all axes of the figure.
        If list of axes, apply manipulations on each of the given axes.
    spines: string or dictionary 
        - string: specify to which spines the bound setttings given by
          the `bounds` argument should be applied.
          'l' is the left spine, 'r' the right spine, 't' the top one and 'b' the bottom one.
          E.g. 'lb' applies the bounds settings to the left and bottom spine.
        - dictionary: apply bound settings for several sets of spines.
          Dictionary keys are strings spcifying the spines as described above.
          The corresponding values specify the bound settings
          (see `bounds` below for possible values and their effects).
    bounds: 'full', 'data', 'ticks' or tuple
        - 'full': draw the spine in its full length (default)
        - 'data': do not draw the spine beyond the data range, uses matplotlib's smart_bounds
        - 'ticks': draw the spine only within the first and last major tick mark.
        - tuple: two values of 'full', 'data', or 'ticks' specifying the lower
          and upper bound separately.

    Raises
    ------
    ValueError:
        If an invalid `bounds` argument was specified.
    """
    if isinstance(spines, dict):
        for sp in spines:
            set_spines_bounds(ax, sp, spines[sp])
    else:
        # collect axes:
        if isinstance(ax, (list, tuple, np.ndarray)):
            axs = ax
        else:
            axs = ax.get_axes()
        if not isinstance(axs, (list, tuple)):
            axs = [axs]
        if isinstance(bounds, (tuple, list)):
            if len(bounds) != 2:
                raise ValueError('Invalid number of elements for bounds. Should be one or two.')
            if bounds[0] not in ['full', 'data', 'ticks']:
                raise ValueError('Invalid value for lower bound: %s. Should be one of "full", "data", "ticks")' % bounds[0])
            if bounds[1] not in ['full', 'data', 'ticks']:
                raise ValueError('Invalid value for upper bound: %s. Should be one of "full", "data", "ticks")' % bounds[1])
            lower_bound = bounds[0]
            upper_bound = bounds[1]
        else:
            if bounds not in ['full', 'data', 'ticks']:
                raise ValueError('Invalid value for bounds: %s. Should be one of "full", "data", "ticks")' % bounds)
            lower_bound = bounds
            upper_bound = bounds
        if lower_bound == 'data' and lower_bound != upper_bound:
            raise ValueError('Invalid value for smart bounds: both upper and lower bound need to be set to "data".' )
        # collect spine ids:
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
                ax.spines[sp].bounds_style = (lower_bound, upper_bound)


def __update_spines(fig):
    """ Update bounds of spines.

    This is needed for applying the 'ticks' setting of set_spines_bounds().
    The spines module patches the plt.show(), fig.show(), and fig.savefig()
    functions to first call __update_spines(). This way this function is
    called automatically right before the figure is drawn.

    Parameters
    ----------
    fig: matplotlib figure
    """
    for ax in fig.get_axes():
        for sp in ['left', 'right', 'top', 'bottom']:
            if hasattr(ax.spines[sp], 'bounds_style'):
                if ax.spines[sp].bounds_style[0] == 'data':
                    ax.spines[sp].set_smart_bounds(True)
                else:
                    ax.spines[sp].set_smart_bounds(False)
                    if sp in ['top', 'bottom']:
                        view = sorted(ax.xaxis.get_view_interval())
                        ticks = np.asarray(ax.xaxis.get_majorticklocs())
                    else:
                        view = sorted(ax.yaxis.get_view_interval())
                        ticks = np.asarray(ax.yaxis.get_majorticklocs())
                    # limit ticks to view:
                    ticks = ticks[(ticks>=np.min(view))&(ticks<=np.max(view))]
                    if len(ticks) < 2:
                        ticks = view
                    else:
                        ticks = (np.min(ticks), np.max(ticks))
                    lower = view[0]
                    upper = view[1]
                    if ax.spines[sp].bounds_style[0] == 'ticks':
                        lower = ticks[0]
                    if ax.spines[sp].bounds_style[1] == 'ticks':
                        upper = ticks[1]
                    ax.spines[sp].set_bounds(lower, upper)

    
def __fig_show_spines(fig, *args, **kwargs):
    """ Call __update_spines() on the figures before showing it.
    """
    fig.update_spines()
    fig.show_orig_spines(*args, **kwargs)

    
def __fig_savefig_spines(fig, *args, **kwargs):
    """ Call __update_spines() on the figures before saving it.
    """
    fig.update_spines()
    fig.savefig_orig_spines(*args, **kwargs)


def __plt_show_spines(*args, **kwargs):
    """ Call __update_spines() on all figures before showing them.
    """
    for fig in map(plt.figure, plt.get_fignums()):
        fig.update_spines()
    plt.show_orig_spines(*args, **kwargs)


def __plt_savefig_spines(*args, **kwargs):
    """ Call __update_spines() on the curren figure before saving it.
    """
    plt.gcf().update_spines()
    plt.savefig_orig_spines(*args, **kwargs)


# make functions available as member variables:
mpl.axes.Axes.show_spines = show_spines
mpl.axes.Axes.set_spines_outward = set_spines_outward
mpl.axes.Axes.set_spines_bounds = set_spines_bounds
mpl.figure.Figure.show_spines = show_spines
mpl.figure.Figure.set_spines_outward = set_spines_outward
mpl.figure.Figure.set_spines_bounds = set_spines_bounds
mpl.figure.Figure.update_spines = __update_spines

# install __update_spines():
mpl.figure.Figure.savefig_orig_spines = mpl.figure.Figure.savefig
mpl.figure.Figure.savefig = __fig_savefig_spines
mpl.figure.Figure.show_orig_spines = mpl.figure.Figure.show
mpl.figure.Figure.show = __fig_show_spines
plt.savefig_orig_spines = plt.savefig
plt.savefig = __plt_savefig_spines
plt.show_orig_spines = plt.show
plt.show = __plt_show_spines

            
def demo():
    """ Run a demonstration of the spine module.
    """
    fig, axs = plt.subplots(3, 2, figsize=(10, 8))
    # spine visibility:
    axs[0, 0].show_spines('lt')
    axs[0, 0].text(0.05, 1.7, "ax.show_spines('lt')")
    axs[0, 1].show_spines('rt')
    axs[0, 1].text(0.05, 1.7, "ax.show_spines('rt')")
    axs[1, 0].show_spines('l')
    axs[1, 0].text(0.05, 1.7, "ax.show_spines('l')")
    axs[1, 1].show_spines('r')
    axs[1, 1 ].text(0.05, 1.7, "ax.show_spines('r')")
    axs[2, 0].show_spines('lb')
    axs[2, 0].text(0.05, 1.7, "ax.show_spines('lb')")
    axs[2, 1].show_spines('rb')
    axs[2, 1 ].text(0.05, 1.7, "ax.show_spines('rb')")
    # set spines outward:
    fig.set_spines_outward('lrtb', 10)
    # set spine bounds:
    axs[0, 1].set_spines_bounds('lr', 'full')
    axs[0, 1].text(0.05, 1.1, "ax.set_spines_bounds('lr', 'full')")
    axs[1, 0].set_spines_bounds('lr', 'data')
    axs[1, 0].text(0.05, 1.1, "ax.set_spines_bounds('lr', 'data')")
    axs[1, 1].set_spines_bounds('lr', 'ticks')
    axs[1, 1].text(0.05, 1.1, "ax.set_spines_bounds('lr', 'ticks')")
    axs[2, 0].set_spines_bounds('lr', ('full', 'ticks'))
    axs[2, 0].text(0.05, 1.1, "ax.set_spines_bounds('lr', ('full', 'ticks'))")
    axs[2, 1].set_spines_bounds('lr', ('ticks', 'full'))
    axs[2, 1].text(0.05, 1.1, "ax.set_spines_bounds('lr', ('ticks', 'full'))")
    # plot and annotate:
    x = np.linspace(0.0, 1.0, 100)
    y = 0.5*np.sin(2.0*np.pi*x) + 0.5
    for axx in axs:
        for ax in axx:
            ax.plot(x, y)
            ax.set_ylim(-1.0, 2.0)
            ax.set_yticks([-0.5, 0, 0.5, 1])
            ax.text(0.05, 1.4, "fig.set_spines_outward('lrtb', 10)")
    #fig.savefig('spines.pdf')
    plt.show()


if __name__ == "__main__":
    demo()
