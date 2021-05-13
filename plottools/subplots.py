"""
Enhanced subplots with margins.


Patches matplotlib to provide the following features:


## Figure margins

Subplot positions can be adjusted by margins given in multiples of the current font size:
```
fig.subplots_adjust(leftm=5.0, bottomm=2.0, rightm=2.0, topm=1.0)  # in fontsize margins!
gs = fig.add_gridspec(3, 3, leftm=5.0, bottomm=2.0, rightm=2.0, topm=2.5)
gs.update(leftm=5.0, bottomm=2.0, rightm=2.0, topm=2.5)
```
That is, `leftm` specifies the distance of the leftmost axes from the left margin of the figure,
`bottomm` specifies the distance of the bottom axes from the bottom margin of the figure,
`rightm` specifies the distance of the rightmost axes from the right margin of the figure, and
`topm` specifies the distance of the top axes from the top margin of the figure,
all as multiples of the font size.

This way, margins do not need to be adjusted when changing the size of a figure!

For figures without any margins you can use the `nomargins` keyword:
```
fig.subplots_adjust(nomargins=True)
```
This sets all margins to zero.


## Grid specs

`plt.subplots()` can be called with `width_ratios` and `height_ratios`.

Further, `figure.add_gridspec()` is made available for older
matplotlib versions that do not have this function yet.

To merge several subplots into a single axes, call `fig.merge()`.


## Figure member functions

- `merge()`: add axis that covers bounding box of several axes.


## Install/uninstall subplots functions

You usually do not need to call these functions. Upon loading the subplots
module, `install_subplots()` is called automatically.

- `install_subplots()`: install functions of the subplots module in matplotlib.
- `uninstall_subplots()`: uninstall all code of the subplots module from matplotlib.


## Todo

- default figure margins
"""

import __main__
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def __adjust_fs(fig=None, left=None, bottom=None, right=None, top=None,
                leftm=None, bottomm=None, rightm=None, topm=None,
                nomargins=False, **kwargs):
    """ Compute plot margins from multiples of the current font size.

    Subplots margins can be either specified by the usual parameters
    `left`, `right`, `top`, and `bottom` as fractions of the figure size,
    or alternatively via `leftm`, `rightm`, `topm`, and `bottomm`.
    The latter specify margins measured from the figure borders in multiples
    of the current font size.

    Parameters
    ----------
    fig: matplotlib.figure or None
        The figure from which the figure size is taken. If None use the current figure.
    left: float
        The usual position of the left side of the axes as a fraction of the full figure.
    bottom: float
        The usual position of the bottom side of the axes as a fraction of the full figure.
    right: float
        The usual position of the right side of the axes as a fraction of the full figure.
    top: float
        The usual position of the top side of the axes as a fraction of the full figure.
    leftm: float
        The left margin of the plots given in multiples of the width of a character
        (simply 60% of the current font size).
    bottomm: float
        The bottom margin of the plots given in multiples of the height of a character
        (the current font size).
    rightm: float
        The right margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
        *Note:* in contrast to the matplotlib `right` parameters, this specifies the
        width of the right margin, not its position relative to the origin.
    topm: float
        The right margin of the plots given in multiples of the height of a character
        (the current font size).
        *Note:* in contrast to the matplotlib `top` parameters, this specifies the
        width of the top margin, not its position relative to the origin.
    nomargins: bool
        If `True` set all margins to zero.
    kwargs: dict
        Any further key-word arguments that are simply passed on.

    Returns
    -------
    kwargs: dict
        The margins and the kwargs combined.

    Example
    -------
    ```
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    fig.subplots_adjust(**__adjust_fs(fig, leftm=4.5))   # no matter what the figsize is!
    ```
    """
    if fig is None:
        fig = plt.gcf()
    w, h = fig.get_window_extent().bounds[2:]
    ppi = 72.0 # points per inch:
    fs = plt.rcParams['font.size']*fig.dpi/ppi
    if nomargins:
        left = 0.0
        bottom = 0.0
        right = 1.0
        top = 1.0
    margins = {}
    if left is not None or leftm is not None:
        margins['left'] = left if left is not None else leftm*0.6*fs/w
    if bottom is not None or bottomm is not None:
        margins['bottom'] = bottom if bottom is not None else bottomm*fs/h
    if right is not None or rightm is not None:
        margins['right'] = right if right is not None else 1.0 - rightm*0.6*fs/w
    if top is not None or topm is not None:
        margins['top'] = top if top is not None else 1.0 - topm*fs/h
    margins.update(kwargs)
    return margins


def __fig_subplots_adjust(fig, *args, **kwargs):
    """ figure.subplots_adjust() with margins in multiples of the current font size.
    """
    if hasattr(fig, '__gridspecs'):
        for gs in fig.__gridspecs:
            gs.update(**kwargs)
    else:
        fig.__subplots_margins = {}
        if kwargs.get('nomargins', False):
            fig.__subplots_margins['leftm'] = 0.0
            fig.__subplots_margins['rightm'] = 0.0
            fig.__subplots_margins['topm'] = 0.0
            fig.__subplots_margins['bottomm'] = 0.0
        else:
            if 'leftm' in kwargs:
                fig.__subplots_margins['leftm'] = kwargs['leftm']
            if 'bottomm' in kwargs:
                fig.__subplots_margins['bottomm'] = kwargs['bottomm']
            if 'rightm' in kwargs:
                fig.__subplots_margins['rightm'] = kwargs['rightm']
            if 'topm' in kwargs:
                fig.__subplots_margins['topm'] = kwargs['topm']
        fig.__subplots_adjust_orig_subplots(**__adjust_fs(fig, *args, **kwargs))

    
def __gridspec_update(gridspec, **kwargs):
    """ gridspec.update() with margins in multiples of the current font size.
    """
    figure = None
    if hasattr(gridspec, 'figure'):
        figure = gridspec.figure
        gridspec.__subplots_margins = {}
        if kwargs.get('nomargins', False):
            gridspec.__subplots_margins['leftm'] = 0.0
            gridspec.__subplots_margins['rightm'] = 0.0
            gridspec.__subplots_margins['topm'] = 0.0
            gridspec.__subplots_margins['bottomm'] = 0.0
        else:
            if 'leftm' in kwargs:
                gridspec.__subplots_margins['leftm'] = kwargs['leftm']
            if 'bottomm' in kwargs:
                gridspec.__subplots_margins['bottomm'] = kwargs['bottomm']
            if 'rightm' in kwargs:
                gridspec.__subplots_margins['rightm'] = kwargs['rightm']
            if 'topm' in kwargs:
                gridspec.__subplots_margins['topm'] = kwargs['topm']
    gridspec.__update_orig_subplots(**__adjust_fs(figure, **kwargs))


def __fig_add_gridspec(fig, nrows=1, ncols=1, **kwargs):
    """ This emulates more current versions of matplotlib.
    """
    if fig.__add_gridspec_orig_subplots:
        gs = fig.__add_gridspec_orig_subplots(nrows=nrows, ncols=ncols,
                                              **__adjust_fs(fig, **kwargs))
    else:
        _ = kwargs.pop('figure', None)  # pop in case user has added this...
        gs = gridspec.GridSpec(nrows=nrows, ncols=ncols, **__adjust_fs(fig, **kwargs))
    if not hasattr(fig, '__gridspecs'):
        fig.__gridspecs = []
    fig.__gridspecs.append(gs)    
    gs.__subplots_margins = {}
    if kwargs.get('nomargins', False):
        gs.__subplots_margins['leftm'] = 0.0
        gs.__subplots_margins['rightm'] = 0.0
        gs.__subplots_margins['topm'] = 0.0
        gs.__subplots_margins['bottomm'] = 0.0
    else:
        if 'leftm' in kwargs:
            gs.__subplots_margins['leftm'] = kwargs['leftm']
        if 'bottomm' in kwargs:
            gs.__subplots_margins['bottomm'] = kwargs['bottomm']
        if 'rightm' in kwargs:
            gs.__subplots_margins['rightm'] = kwargs['rightm']
        if 'topm' in kwargs:
            gs.__subplots_margins['topm'] = kwargs['topm']
    gs.figure = fig
    return gs


def __plt_subplots(nrows=1, ncols=1, *args, **kwargs):
    """ plt.subplots() with width_ratios and height_ratios.
    
    Missing: sharex, sharey support together with width_ratios, height_ratios!
    """
    gskwargs = {}
    for k in ['width_ratios', 'height_ratios']:
        if k in kwargs:
            gskwargs[k] = kwargs.pop(k)
    if len(gskwargs) > 0:
        figkwargs = {}
        for k in ['num', 'cmsize', 'figsize', 'dpi', 'facecolor', 'edgecolor',
                  'frameon', 'clear']:
            if k in kwargs:
                figkwargs[k] = kwargs.pop(k)
        upkwargs = {}
        for k in ['leftm', 'rightm', 'topm', 'bottomm', 'nomargins',
                  'left', 'right', 'top', 'bottom', 'hspace', 'wspace']:
            if k in kwargs:
                upkwargs[k] = kwargs.pop(k)
        squeeze = True
        if 'squeeze' in kwargs:
            squeeze = kwargs.pop('squeeze')
        fig = plt.figure(**figkwargs)
        gs = fig.add_gridspec(nrows, ncols, **gskwargs)
        gs.update(**upkwargs)
        axs = np.zeros((nrows, ncols), np.object)
        for r in range(nrows):
            for c in range(ncols):
                axs[r,c] = fig.add_subplot(gs[r,c], **kwargs)
        return fig, np.squeeze(axs) if squeeze else axs
    else:
        return plt.__subplots_orig_subplots(nrows, ncols, *args, **kwargs)


def __resize(event):
    """ Resize event updating subplot margins.
    """
    fig = event.canvas.figure
    if hasattr(fig, '__subplots_margins'):
        fig.subplots_adjust(**fig.__subplots_margins)
    if hasattr(fig, '__gridspecs'):
        for gs in fig.__gridspecs:
            if hasattr(gs, '__subplots_margins'):
                gs.update(**gs.__subplots_margins)
    for ax in fig.get_axes():
        if hasattr(ax, '__merged_axis'):
            ax.__set_merged_position(ax.__merged_axis)

    
def __fig_figure(*args, **kwargs):
    """ Install resize event handler to keep margins.
    """
    fig = plt.__figure_orig_subplots(*args, **kwargs)
    fig.canvas.mpl_connect('resize_event', __resize)
    return fig


def __set_merged_position(self, axs):
    """ Set position of axis to bounding box of other axis.

    Parameters
    ----------
    self: axis object
        Axis whose position is set.
    axs: flat array of axis objects
        The axis from which the bounding box is taken.
    """
    bboxes = np.array([ax.get_position().get_points().ravel() for ax in axs])
    x0 = np.min(bboxes[:,0])
    y0 = np.min(bboxes[:,1])
    x1 = np.max(bboxes[:,2])
    y1 = np.max(bboxes[:,3])
    pos = [x0, y0, x1-x0, y1-y0]
    self.set_position(pos)


def merge(fig, axs):
    """ Add axis that covers bounding box of several axes.

    Add a new axis to the figure at the position and size of the common
    bounding box of all axis in `axs`. All axis in `axs` are then made
    invisible. This way you do not need to use `gridspec` explicitly.

    Parameters
    ----------
    fig: matplotlib.figure
        The figure that contains the axes.
    axs: array of axis objects
        The axis that should be combined.

    Returns
    -------
    ax: axis object
        A single axis covering the area of all the axis objects in `axs`.

    Example
    -------
    With gridspec you would do
    ```
    fig = plt.figure()
    gs = fig.add_gridspec(3, 3)
    ax1 = fig.add_subplot(gs[1:,:2])  # merge 2x2 bottom left subplots
    ax2 = fig.add_subplot(gs[0,0])    # first in top row
    ax3 = fig.add_subplot(gs[0,1])    # second in top row
    ax4 = fig.add_subplot(gs[0,2])    # third in top row
    ax5 = fig.add_subplot(gs[1,2])    # last in second row
    ax6 = fig.add_subplot(gs[2,2])    # last in bottom row
    ``
    with merge() this simplifies to
    ```
    fig, axs = plt.subplots(3, 3)     # axs contains 3x3 axis objects
    ax1 = fig.merge(axs[1:3,0:2])     # merge 2x2 bottom left subplots into a single one.
    ax2 = axs[0,0]                    # first in top row
    ax3 = axs[0,1]                    # second in top row
    # ...
    ```
    """
    axs = np.asarray(axs).ravel()
    for ax in axs:
        ax.set_visible(False)
    count = 0
    if hasattr(fig, '__merged_axis_counter'):
        count = fig.__merged_axis_counter
    count += 1
    fig.__merged_axis_counter = count
    ax = fig.add_axes([0, 0, 1, 1], label='merged%d' % count)
    ax.__set_merged_position(axs)
    ax.__merged_axis = axs
    return ax


def install_subplots():
    """ Install functions of the subplots module in matplotlib.

    Patches a few matplotlib functions (`plt.figure()`,
    `plt.subplots()`, `figure.add_gridspec()`, `gridspec.update()`).
    Each figure gets an resize event handler installed, that applies the
    supplied margins whenever a figure is resized.
    
    See also
    --------
    uninstall_subplots()
    """
    if not hasattr(mpl.figure.Figure, 'merge'):
        mpl.figure.Figure.merge = merge
        mpl.axes.Axes.__set_merged_position = __set_merged_position
    if not hasattr(mpl.figure.Figure, '__subplots_adjust_orig_subplots'):
        mpl.figure.Figure.__subplots_adjust_orig_subplots = mpl.figure.Figure.subplots_adjust
        mpl.figure.Figure.subplots_adjust = __fig_subplots_adjust
    if not hasattr(mpl.gridspec.GridSpec, '__update_orig_subplots'):
        mpl.gridspec.GridSpec.__update_orig_subplots = mpl.gridspec.GridSpec.update
        mpl.gridspec.GridSpec.update = __gridspec_update
    if not hasattr(mpl.figure.Figure, 'add_gridspec'):
        mpl.figure.Figure.add_gridspec = __fig_add_gridspec
        mpl.figure.Figure.__add_gridspec_orig_subplots = None
    if not hasattr(mpl.figure.Figure, '__add_gridspec_orig_subplots'):
        mpl.figure.Figure.__add_gridspec_orig_subplots = mpl.figure.Figure.add_gridspec
        mpl.figure.Figure.add_gridspec = __fig_add_gridspec
    if not hasattr(plt, '__subplots_orig_subplots'):
        plt.__subplots_orig_subplots = plt.subplots
        plt.subplots = __plt_subplots
    if not hasattr(plt, '__figure_orig_subplots'):
        plt.__figure_orig_subplots = plt.figure
        plt.figure = __fig_figure


def uninstall_subplots():
    """ Uninstall all code of the subplots module from matplotlib.

    See also
    --------
    install_subplots()
    """
    if hasattr(mpl.figure.Figure, 'merge'):
        delattr(mpl.figure.Figure, 'merge')
        delattr(mpl.axes.Axes, '__set_merged_position')
    if hasattr(mpl.figure.Figure, '__subplots_adjust_orig_subplots'):
        mpl.figure.Figure.subplots_adjust = mpl.figure.Figure.__subplots_adjust_orig_subplots
        delattr(mpl.figure.Figure, '__subplots_adjust_orig_subplots')
    if hasattr(mpl.gridspec.GridSpec, '__update_orig_subplots'):
        mpl.gridspec.GridSpec.update = mpl.gridspec.GridSpec.__update_orig_subplots
        delattr(mpl.gridspec.GridSpec, '__update_orig_subplots')
    if hasattr(mpl.figure.Figure, '__add_gridspec_orig_subplots'):
        if mpl.figure.Figure.__add_gridspec_orig_subplots is None:
            delattr(mpl.figure.Figure, 'add_gridspec')
        else:
            mpl.figure.Figure.add_gridspec = mpl.figure.Figure.__add_gridspec_orig_subplots
            delattr(mpl.figure.Figure, '__add_gridspec_orig_subplots')
    if hasattr(plt, '__subplots_orig_subplots'):
        plt.subplots = plt.__subplots_orig_subplots
        delattr(plt, '__subplots_orig_subplots')
    if hasattr(plt, '__figure_orig_subplots'):
        plt.figure = plt.__figure_orig_subplots
        delattr(plt, '__figure_orig_subplots')


install_subplots()

        
def demo():
    """ Run a demonstration of the subplots module.
    """
    fig, axs = plt.subplots(3, 3, height_ratios=[3, 2, 2])
    # in fontsize margins and even with old matplotlib versions:
    fig.subplots_adjust(leftm=5, bottomm=2, rightm=2, topm=4)
    fig.suptitle('axs = plt.subplots(3, 3, height_ratios=[3, 2, 2])\nfig.subplots_adjust(leftm=5, bottomm=2, rightm=2, topm=4)')
    x = np.linspace(0.0, 2.0, 200)
    ax = fig.merge(axs[1:3,0:2])
    ax.plot(x, np.sin(2.0*np.pi*x))
    ax.text(0.05, 0.1, 'ax = fig.merge(axs[1:3,0:2])', transform=ax.transAxes)
    for k in range(3):
        axs[0,k].plot(x, np.sin(2.0*np.pi*x+k))
        axs[0,k].text(0.1, 0.8, '0,%d' % k, transform=axs[0,k].transAxes)
    for k in range(1, 3):
        axs[k,2].plot(x, np.sin(2.0*np.pi*x-k))
        axs[k,2].text(0.1, 0.8, '%d,2' % k, transform=axs[k,-1].transAxes)
            
    plt.show()


if __name__ == "__main__":
    demo()
