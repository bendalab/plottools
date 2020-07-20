"""
Modify the appearance of spines.

The following functions are added as a members to mpl.axes.Axes and mpl.figure.Figure:

- `show_spines()`: show and hide spines and corresponding tick marks.
- `set_spines_outward()`: set the specified spines outward.
- `set_spines_bounds()`: set bounds for the specified spines.

The following functions enable and disable spine control:

- `spines_params()`: set default spine appearance.
- `install_spines()`: install code for controlling spines.
- `uninstall_spines()`: uninstall code for controlling spines.
- `install_default_spines()`: install code and rc settings for formatting spines.
- `uninstall_default_spines()`: uninstall code for default spine settings.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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
            ax.xaxis.label.set_visible(False)
            ax.xaxis._orig_major_locator = ax.xaxis.get_major_locator()
            ax.xaxis.set_major_locator(ticker.NullLocator())
        else:
            if hasattr(ax.xaxis, '_orig_major_locator'):
                ax.xaxis.set_major_locator(ax.xaxis._orig_major_locator)
                delattr(ax.xaxis, '_orig_major_locator')
            elif isinstance(ax.xaxis.get_major_locator(), ticker.NullLocator):
                ax.xaxis.set_major_locator(ticker.AutoLocator())
            if len(xspines) == 1:
                ax.xaxis.set_ticks_position(xspines[0])
                ax.xaxis.set_label_position(xspines[0])
            else:
                ax.xaxis.set_ticks_position('both')
                ax.xaxis.set_label_position('bottom')
        if len(yspines) == 0:
            ax.yaxis.set_ticks_position('none')
            ax.yaxis.label.set_visible(False)
            ax.yaxis._orig_major_locator = ax.yaxis.get_major_locator()
            ax.yaxis.set_major_locator(ticker.NullLocator())
        else:
            if hasattr(ax.yaxis, '_orig_major_locator'):
                ax.yaxis.set_major_locator(ax.yaxis._orig_major_locator)
                delattr(ax.yaxis, '_orig_major_locator')
            elif isinstance(ax.yaxis.get_major_locator(), ticker.NullLocator):
                ax.yaxis.set_major_locator(ticker.AutoLocator())
            if len(yspines) == 1:
                ax.yaxis.set_ticks_position(yspines[0])
                ax.yaxis.set_label_position(yspines[0])
            else:
                ax.yaxis.set_ticks_position('both')
                ax.yaxis.set_label_position('left')


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
          Dictionary keys are strings specifying the spines as described above.
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
                if ax.spines[sp].get_visible():
                    loc = ax.yaxis.get_major_locator()
                    ax.spines[sp].set_position(('outward', offset))
                    ax.yaxis.set_major_locator(loc)


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
          Dictionary keys are strings specifying the spines as described above.
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

    This is needed for applying the 'ticks' setting of `set_spines_bounds()`.
    The spines module patches the `plt.show()`, `fig.show()`, and `fig.savefig()`
    functions to first call `__update_spines()`. This way this function is
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
    """ Call `__update_spines()` on the figure before showing it.
    """
    fig.update_spines()
    fig.__show_orig_spines(*args, **kwargs)

    
def __fig_savefig_spines(fig, *args, **kwargs):
    """ Call `__update_spines()` on the figure before saving it.
    """
    fig.update_spines()
    fig.__savefig_orig_spines(*args, **kwargs)


def __plt_show_spines(*args, **kwargs):
    """ Call `__update_spines()` on all figures before showing them.
    """
    for fig in map(plt.figure, plt.get_fignums()):
        fig.update_spines()
    plt.__show_orig_spines(*args, **kwargs)


def __plt_savefig_spines(*args, **kwargs):
    """ Call `__update_spines()` on the current figure before saving it.
    """
    plt.gcf().update_spines()
    plt.__savefig_orig_spines(*args, **kwargs)


def install_spines():
    """ Install code for controlling spines.

    This makes `show_spines()`, `set_spines_outward()` and
    `set_spines_bounds()` available as member functions for matplib axes
    and figures. In addition, the matplotlib functions `show()` and
    `savefig()` are patched for fixing spine bounds before finishing the
    figure.

    Call this function before creating any figure to make `show_spines()`,
    `set_spines_outwards()` and `set_spines_bounds()` available and working.

    This function is also called by `install_default_spines()` or `spines_params()`,
    so usually you do not need to explicitly call this function.

    See also
    --------
    `uninstall_spines()`
    """
    # make functions available as members:
    mpl.axes.Axes.show_spines = show_spines
    mpl.axes.Axes.set_spines_outward = set_spines_outward
    mpl.axes.Axes.set_spines_bounds = set_spines_bounds
    mpl.figure.Figure.show_spines = show_spines
    mpl.figure.Figure.set_spines_outward = set_spines_outward
    mpl.figure.Figure.set_spines_bounds = set_spines_bounds
    mpl.figure.Figure.update_spines = __update_spines
    # install __update_spines():
    if not hasattr(mpl.figure.Figure, '__savefig_orig_spines'):
        mpl.figure.Figure.__savefig_orig_spines = mpl.figure.Figure.savefig
        mpl.figure.Figure.savefig = __fig_savefig_spines
    if not hasattr(mpl.figure.Figure, '__show_orig_spines'):
        mpl.figure.Figure.__show_orig_spines = mpl.figure.Figure.show
        mpl.figure.Figure.show = __fig_show_spines
    if not hasattr(plt, '__savefig_orig_spines'):
        plt.__savefig_orig_spines = plt.savefig
        plt.savefig = __plt_savefig_spines
    if not hasattr(plt, '__show_orig_spines'):
        plt.__show_orig_spines = plt.show
        plt.show = __plt_show_spines


def uninstall_spines():
    """ Uninstall code for controlling spines.

    Call this code to disable anything that was installed by `install_spines()`.
    """
    uninstall_default_spines()
    # remove installed members:
    if hasattr(mpl.axes.Axes, 'show_spines'):
        delattr(mpl.axes.Axes, 'show_spines')
    if hasattr(mpl.axes.Axes, 'set_spines_outward'):
        delattr(mpl.axes.Axes, 'set_spines_outward')
    if hasattr(mpl.axes.Axes, 'set_spines_bounds'):
        delattr(mpl.axes.Axes, 'set_spines_bounds')
    if hasattr(mpl.figure.Figure, 'show_spines'):
        delattr(mpl.figure.Figure, 'show_spines')
    if hasattr(mpl.figure.Figure, 'set_spines_outward'):
        delattr(mpl.figure.Figure, 'set_spines_outward')
    if hasattr(mpl.figure.Figure, 'set_spines_bounds'):
        delattr(mpl.figure.Figure, 'set_spines_bounds')
    if hasattr(mpl.figure.Figure, 'update_spines'):
        delattr(mpl.figure.Figure, 'update_spines')
    # uninstall __update_spines():
    if hasattr(mpl.figure.Figure, '__savefig_orig_spines'):
        mpl.figure.Figure.savefig = mpl.figure.Figure.__savefig_orig_spines
        delattr(mpl.figure.Figure, '__savefig_orig_spines')
    if hasattr(mpl.figure.Figure, '__show_orig_spines'):
        mpl.figure.Figure.show = mpl.figure.Figure.__show_orig_spines
        delattr(mpl.figure.Figure, '__show_orig_spines')
    if hasattr(plt, '__savefig_orig_spines'):
        plt.savefig = plt.__savefig_orig_spines
        delattr(plt, '__savefig_orig_spines')
    if hasattr(plt, '__show_orig_spines'):
        plt.show = plt.__show_orig_spines
        delattr(plt, '__show_orig_spines')
        

def __axes_init_spines__(ax, *args, **kwargs):
    """ Apply default spine settings to a new Axes instance.

    Installed by `install_default_spines()`.
    """
    ax.__init__orig_spines(*args, **kwargs)
    ax.show_spines(mpl.ptParams['axes.spines.show'])
    ax.set_spines_outward(mpl.ptParams['axes.spines.offsets'])
    ax.set_spines_bounds(mpl.ptParams['axes.spines.bounds'])


def __twinx_spines(ax, *args, **kwargs):
    """ Mark a twinx axes such that the corresponding spine properties can be set. """
    ax_spines = mpl.ptParams['axes.spines.show']
    if 'l' in mpl.ptParams['axes.spines.twinx'] and 'l' not in ax_spines:
        ax_spines += 'l'
    if 'r' in mpl.ptParams['axes.spines.twinx'] and 'r' not in ax_spines:
        ax_spines += 'r'
    axt_spines = mpl.ptParams['axes.spines.twinx']
    if 'b' in mpl.ptParams['axes.spines.show'] and 'b' not in axt_spines:
        axt_spines += 'b'
    if 't' in mpl.ptParams['axes.spines.show'] and 't' not in axt_spines:
        axt_spines += 'b'
    ax.show_spines(ax_spines)
    ax.set_spines_outward(mpl.ptParams['axes.spines.offsets'])
    orig_default_spines = mpl.ptParams['axes.spines.show']
    mpl.ptParams.update({'axes.spines.show': axt_spines})
    axt = ax.__twinx_orig_spines(*args, **kwargs)
    mpl.ptParams.update({'axes.spines.show': orig_default_spines})
    return axt


def __twiny_spines(ax, *args, **kwargs):
    """ Mark a twiny axes such that the corresponding spine properties can be set. """
    ax_spines = mpl.ptParams['axes.spines.show']
    if 't' in mpl.ptParams['axes.spines.twiny'] and 't' not in ax_spines:
        ax_spines += 't'
    if 'b' in mpl.ptParams['axes.spines.twiny'] and 'b' not in ax_spines:
        ax_spines += 'b'
    axt_spines = mpl.ptParams['axes.spines.twiny']
    if 'l' in mpl.ptParams['axes.spines.show'] and 'l' not in axt_spines:
        axt_spines += 'l'
    if 'r' in mpl.ptParams['axes.spines.show'] and 'r' not in axt_spines:
        axt_spines += 'r'
    ax.show_spines(ax_spines)
    ax.set_spines_outward(mpl.ptParams['axes.spines.offsets'])
    orig_default_spines = mpl.ptParams['axes.spines.show']
    mpl.ptParams.update({'axes.spines.show': axt_spines})
    axt = ax.__twiny_orig_spines(*args, **kwargs)
    mpl.ptParams.update({'axes.spines.show': orig_default_spines})
    return axt


def __inset_spines(ax, *args, **kwargs):
    """ Mark an inset axes such that the corresponding spine properties can be set. """
    # save default settings for normal axes:
    orig_default_spines = mpl.ptParams['axes.spines.show']
    orig_default_spines_offsets = mpl.ptParams['axes.spines.offsets']
    orig_default_spines_bounds = mpl.ptParams['axes.spines.bounds']
    # override settings with values for insets:
    mpl.ptParams.update({'axes.spines.show': mpl.ptParams['axes.spines.inset.show']})
    mpl.ptParams.update({'axes.spines.offsets': mpl.ptParams['axes.spines.inset.offsets']})
    mpl.ptParams.update({'axes.spines.bounds': mpl.ptParams['axes.spines.inset.bounds']})
    # create inset axes:
    axi = ax.__inset_orig_spines(*args, **kwargs)
    # restore default settings for normal axes:
    mpl.ptParams.update({'axes.spines.show': orig_default_spines})
    mpl.ptParams.update({'axes.spines.offsets': orig_default_spines_offsets})
    mpl.ptParams.update({'axes.spines.bounds': orig_default_spines_bounds})
    return axi


def install_default_spines():
    """ Install code and `mpl.ptParams` for formatting spines.

    Adds mpl.ptParams:
    ```
    axes.spines.show   : 'lrtb'
    axes.spines.offsets: {'lrtb': 0}
    axes.spines.bounds : {'lrtb': 'full'}
    axes.spines.twinx: 'r'
    axes.spines.twiny: 'l'
    axes.spines.inset.show   : 'lrtb'
    axes.spines.inset.offsets: {'lrtb': 0}
    axes.spines.inset.bounds : {'lrtb': 'full'}
    ```

    Patches the matplotlib axes constructor, the `twinx()`, `twiny()`,
    and the `plottools.insets` functions.    

    This function is also called by `spines_params()`, so usually you
    do not need to explicitly call this function.

    See also
    --------
    `uninstall_default_spines()`
    """
    install_spines()
    # add spine parameter to rc configuration:
    if not hasattr(mpl, 'ptParams'):
        mpl.ptParams = {}
    if 'axes.spines.show' not in mpl.ptParams:
        mpl.ptParams.update({'axes.spines.show': 'lrtb',
                             'axes.spines.offsets': {'lrtb': 0},
                             'axes.spines.bounds': {'lrtb': 'full'},
                             'axes.spines.twinx': 'r',
                             'axes.spines.twiny': 'l',
                             'axes.spines.inset.show': 'lrtb',
                             'axes.spines.inset.offsets': {'lrtb': 0},
                             'axes.spines.inset.bounds': {'lrtb': 'full'}})
    # extend Axes constructor for modifying spine appearance:
    if not hasattr(mpl.axes.Axes, '__init__orig_spines'):
        mpl.axes.Axes.__init__orig_spines = mpl.axes.Axes.__init__
        mpl.axes.Axes.__init__ = __axes_init_spines__
    if not hasattr(mpl.axes.Axes, '__twinx_orig_spines'):
        mpl.axes.Axes.__twinx_orig_spines = mpl.axes.Axes.twinx
        mpl.axes.Axes.twinx = __twinx_spines
    if not hasattr(mpl.axes.Axes, '__twiny_orig_spines'):
        mpl.axes.Axes.__twiny_orig_spines = mpl.axes.Axes.twiny
        mpl.axes.Axes.twiny = __twiny_spines
    if not hasattr(mpl.axes.Axes, '__inset_orig_spines') and hasattr(mpl.axes.Axes, 'inset'):
        mpl.axes.Axes.__inset_orig_spines = mpl.axes.Axes.inset
        mpl.axes.Axes.inset = __inset_spines


def uninstall_default_spines():
    """ Uninstall code for default spine settings.
    
    Call this code to disable anything that was installed by `install_default_spines()`.
    """
    # remove spine parameter from mpl.ptParams:
    if hasattr(mpl, 'ptParams') and 'axes.spines.show' in mpl.ptParams:
        mpl.ptParams.pop('axes.spines.show', None)
        mpl.ptParams.pop('axes.spines.offsets', None)
        mpl.ptParams.pop('axes.spines.bounds', None)
        mpl.ptParams.pop('axes.spines.twinx', None)
        mpl.ptParams.pop('axes.spines.twiny', None)
        mpl.ptParams.pop('axes.spines.inset.show', None)
        mpl.ptParams.pop('axes.spines.inset.offsets', None)
        mpl.ptParams.pop('axes.spines.inset.bounds', None)
        mpl.ptParams = {}
    # reinstall original Axes constructors:
    if hasattr(mpl.axes.Axes, '__init__orig_spines'):
        mpl.axes.Axes.__init__ = mpl.axes.Axes.__init__orig_spines
        delattr(mpl.axes.Axes, '__init__orig_spines')
    if hasattr(mpl.axes.Axes, '__twinx_orig_spines'):
        mpl.axes.Axes.twinx = mpl.axes.Axes.__twinx_orig_spines
        delattr(mpl.axes.Axes, '__twinx_orig_spines')
    if hasattr(mpl.axes.Axes, '__twiny_orig_spines'):
        mpl.axes.Axes.twiny = mpl.axes.Axes.__twiny_orig_spines
        delattr(mpl.axes.Axes, '__twiny_orig_spines')
    if hasattr(mpl.axes.Axes, '__inset_orig_spines'):
        mpl.axes.Axes.inset = mpl.axes.Axes.__inset_orig_spines
        delattr(mpl.axes.Axes, '__inset_orig_spines')


def spines_params(spines=None, spines_offsets=None, spines_bounds=None,
                  twinx_spines=None, twiny_spines=None,
                  inset_spines=None, inset_spines_offsets=None, inset_spines_bounds=None):
    """ Set default spine appearance.

    Call this function *before* you create a matplotlib figure.

    Parameters
    ----------
    spines: string
        Spines to be shown. See `spines.show_spines()` for details.
    spines_offsets: dict
        Offsets for moving spines outward. See `spines.set_spines_outward()` for details.
    spines_bounds: dict
        Bounds for the spines. See `spines.set_spines_bounds()` for details.
    twinx_spines: string
        Spines to be shown for `twinx()` axes. See `spines.show_spines()` for details.
        Twinned axes get the same default offsets and bounds as the defaults for normal axes.
    twiny_spines: string
        Spines to be shown for `twiny()` axes. See `spines.show_spines()` for details.
        Twinned axes get the same default offsets and bounds as the defaults for normal axes.
    inset_spines: string
        Spines to be shown for an inset. See `spines.show_spines()` for details.
    inset_spines_offsets: dict
        Offsets for moving spines outward for an inset.
        See `spines.set_spines_outward()` for details.
    inset_spines_bounds: dict
        Bounds for the spines of an inset. See `spines.set_spines_bounds()` for details.
    """
    install_default_spines()
    if spines is not None:
        mpl.ptParams.update({'axes.spines.show': spines})
    if spines_offsets is not None:
        mpl.ptParams.update({'axes.spines.offsets': spines_offsets})
    if spines_bounds is not None:
        mpl.ptParams.update({'axes.spines.bounds': spines_bounds})
    if twinx_spines is not None:
        mpl.ptParams.update({'axes.spines.twinx': twinx_spines})
    if twiny_spines is not None:
        mpl.ptParams.update({'axes.spines.twiny': twiny_spines})
    if inset_spines is not None:
        mpl.ptParams.update({'axes.spines.inset.show': inset_spines})
    if inset_spines_offsets is not None:
        mpl.ptParams.update({'axes.spines.inset.offsets': inset_spines_offsets})
    if inset_spines_bounds is not None:
        mpl.ptParams.update({'axes.spines.inset.bounds': inset_spines_bounds})


def demo_basic():
    """ Run a basic demonstration of the spine module.
    """
    install_spines()
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
    #fig.savefig('spinesbasic.pdf')
    plt.show()
    uninstall_spines()

            
def demo_twin_inset():
    """ Run a demonstration of the spine module showing twin behavior.
    """
    from .insets import inset
    spines_params('lb', {'lrtb': 10}, {'lrtb': 'ticks'}, 'r', 't', 'lrb', {'tr': 5})
    fig, axs = plt.subplots(1, 3, figsize=(14, 4))
    fig.subplots_adjust(wspace=0.5)
    axs[0].text(0.05, 1.85, "spines='lb'")
    axt = axs[1].twinx()
    axt.set_ylim(0.5, 5.5)
    axs[1].text(0.05, 1.85, "ax.twinx()")
    axs[1].text(0.05, 1.7, "twinx_spines='r'")
    axi = axs[2].inset((0.5, 0.5, 0.9, 0.75))
    axs[2].text(0.05, 1.85, "ax.inset((0.5, 0.5, 0.9, 0.75))")
    axs[2].text(0.05, 1.7, "inset_spines='lrb'")
    # plot and annotate:
    x = np.linspace(0.0, 1.0, 100)
    y = 0.5*np.sin(2.0*np.pi*x) + 0.5
    for ax in axs:
        ax.plot(x, y)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 2.0)
    #fig.savefig('spinestwin.pdf')
    plt.show()
    uninstall_spines()


def demo():
    demo_basic()
    demo_twin_inset()


if __name__ == "__main__":
    demo()
