"""
Enhanced subplots with margins.


Patches matplotlib to provide the following features:


## Figure margins

Subplot positions can be adjusted by margins given in multiples of the current font size:
```
fig.subplots_adjust(leftm=5.0, bottomm=2.0, rightm=2.0, topm=1.0)  # in fontsize units!
gs = fig.add_gridspec(3, 3, leftm=5.0, bottomm=2.0, rightm=2.0, topm=2.5)
gs.update(leftm=5.0, bottomm=2.0, rightm=2.0, topm=2.5)
```
That is,
- `leftm` specifies the distance of the leftmost axes from the left margin of the figure,
- `bottomm` specifies the distance of the bottom axes from the bottom margin of the figure,
- `rightm` specifies the distance of the rightmost axes from the right margin of the figure, and
- `topm` specifies the distance of the top axes from the top margin of the figure,
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

To replace an axes by subplots, call `ax.subplots()`.

`fig.merge()` and `ax.subplots()` can be arbitrarily combined.


## Axes member functions

- `subplots()`: replace axes by subplots.
- `make_polar()`: turn an axes into one with polar projection.


## Figure member functions

- `merge()`: merge several axes into a single one.


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
        axs = np.zeros((nrows, ncols), object)
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

    
def __fig_figure(*args, **kwargs):
    """ Install resize event handler to keep margins.
    """
    fig = plt.__figure_orig_subplots(*args, **kwargs)
    fig.canvas.mpl_connect('resize_event', __resize)
    return fig


def merge(fig, axs, remove=True):
    """ Merge several axes into a single one.

    Add new axes to the figure at the position and size of the common
    bounding box of all axes in `axs`. All axes in `axs` are then
    removed. This way you do not need to use `gridspec` explicitly.

    Parameters
    ----------
    fig: matplotlib.figure
        The figure that contains the axes.
    axs: array of axis objects
        The axes that should be combined.
    remove: bool
        If `True` remove the orignal axes `axs`.

    Returns
    -------
    ax: axes object
        A single axes covering the area of all the axes objects in `axs`.

    See also
    --------
    subplots()
    
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
    ```
    with merge() this simplifies to
    ```
    fig, axs = plt.subplots(3, 3)     # axs contains 3x3 axes objects
    ax1 = fig.merge(axs[1:3,0:2])     # merge 2x2 bottom left subplots into a single one.
    ax2 = axs[0,0]                    # first in top row
    ax3 = axs[0,1]                    # second in top row
    # ...
    ```
    """
    axs = np.asarray(axs).ravel()
    rows = []
    cols = []
    for ax in axs:
        sps = ax.get_subplotspec()
        gs = sps.get_gridspec()
        nrows, ncols, idx0, idx1 = sps.get_geometry()
        if idx1 is None:
            idx1 = idx0
        rows.extend((idx0//ncols, idx1//ncols))
        cols.extend((idx0%ncols, idx1%ncols))
        if remove:
            try:
                ax.remove()
            except NotImplementedError:
                ax.set_visible(False)
    ax = fig.add_subplot(gs[np.min(rows):np.max(rows)+1, np.min(cols):np.max(cols)+1])
    sps = ax.get_subplotspec()
    return ax


def subplots(ax, nrows, ncols, **kwargs):
    """ Replace axes by subplots.
    
    Replace axes by all plots of a subgridspec at that axes. This way
    you do not need to use `subgridspec()` explicitly.

    Parameters
    ----------
    ax: matplotlib.axes
        Axes that should be replaced by subplots.
    nrows: int
        Number of rows of the new subgrid.
    ncols: int
        Number of columns of the new subgrid.
    kwargs: dict
        Further arguments for matplotlib.gridspec.GridSpecFromSubplotSpec,
        e.g. `wspace`, `hspace`, `height_ratios`, `width_ratios`.

    Returns
    -------
    axs: array of matplotlib axes
        Axes of the new subgrid.

    See also
    --------
    merge()

    Example
    -------
    With gridspec you would do
    ```
    fig = plt.figure()
    gs = fig.add_gridspec(3, 3)
    sgs = gs[0,2].subgridspec(2, 1)
    ax1 = fig.add_subplot(gs[0,0])
    # ... 8 more for all the subplots on gs
    subax1 = fig.add_subplot(sgs[0])
    subax2 = fig.add_subplot(sgs[1])
    ```
    As usual, this requires a lot of calls to `fig.add_subplot()`.
    With subplots() this simplifies to
    ```py
    fig, axs = plt.subplots(3, 3)     # axs contains 3x3 axes objects
    subaxs = axs[0,2].subplots(2, 1)  # replace axs[0,2] by two new subplots
    ```
    and you can use the axes in `axs` and `subaxs` right away.
    """
    sps = ax.get_subplotspec()
    gs = sps.get_gridspec()
    nr, nc, idx0, idx1 = sps.get_geometry()
    if idx1 is None:
        idx1 = idx0
    rows = (idx0//nc, idx1//nc)
    cols = (idx0%nc, idx1%nc)
    gsi = gs[np.min(rows):np.max(rows)+1, np.min(cols):np.max(cols)+1]
    try:
        sgs = gsi.subgridspec(nrows, ncols, **kwargs)
    except AttributeError:
        sgs = gridspec.GridSpecFromSubplotSpec(nrows, ncols, subplot_spec=gsi, **kwargs)
    axs = np.array([ax.get_figure().add_subplot(sgs[r,c])
                    for r in range(nrows) for c in range(ncols)])
    try:
        ax.remove()
    except NotImplementedError:
        ax.set_visible(False)
    return axs.squeeze()


def make_polar(ax):
    """ Turn an axes into one with polar projection.

    Creates a new axes with polar projection at the position 
    of the given axes.

    Parameters
    ----------
    ax: Axes object
        The axes to be turned into polar projection .

    Returns
    -------
    ax: axes object
        An axes with polar projection at the position of the given axes.
    
    Example
    -------
    ```
    fig, axs = plt.subplots(2, 3)
    axp = axs[1, 2].make_polar()
    axp.plot(theta, r)   # this is a polar plot!
    ```
    """
    fig = ax.get_figure()
    pos = ax.get_position()
    ax.remove()
    ax = fig.add_axes(pos, projection='polar')
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
    if not hasattr(mpl.axes.Axes, 'subplots'):
        mpl.axes.Axes.subplots = subplots
    if not hasattr(mpl.figure.Figure, 'merge'):
        mpl.figure.Figure.merge = merge
    if not hasattr(mpl.axes.Axes, 'make_polar'):
        mpl.axes.Axes.make_polar = make_polar
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
    if hasattr(mpl.axes.Axes, 'subplots'):
        delattr(mpl.axes.Axes, 'subplots')
    if hasattr(mpl.figure.Figure, 'merge'):
        delattr(mpl.figure.Figure, 'merge')
    if hasattr(mpl.axes.Axes, 'make_polar'):
        delattr(mpl.axes.Axes, 'make_polar')
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
    fig, axs = plt.subplots(3, 3, width_ratios=[1, 1, 2], height_ratios=[3, 2, 2])
    fig.subplots_adjust(leftm=5, bottomm=2, rightm=2, topm=4)
    fig.suptitle('axs = plt.subplots(3, 3, width_ratios=[1, 1, 2], height_ratios=[3, 2, 2])\nfig.subplots_adjust(leftm=5, bottomm=2, rightm=2, topm=4)')
    x = np.linspace(0.0, 2.0, 200)
    ax = fig.merge(axs[1:3,0:2])
    ax.plot(x, np.sin(2.0*np.pi*x))
    ax.text(0.05, 0.1, 'ax = fig.merge(axs[1:3,0:2])', transform=ax.transAxes)
    subaxs = axs[0,2].subplots(2, 1)
    subaxs[0].text(0.05, 0.7, 'subaxs = axs[0,2].subplots(2, 1)', transform=subaxs[0].transAxes)
    subaxs[0].text(0.05, 0.3, 'subaxs[0]', transform=subaxs[0].transAxes)
    subaxs[1].text(0.05, 0.3, 'subaxs[1]', transform=subaxs[1].transAxes)
    axs[0,0].plot(x, np.sin(2.0*np.pi*x))
    axs[0,0].text(0.1, 0.8, 'axs[0,0]', transform=axs[0,0].transAxes)
    axp = axs[0,1].make_polar()
    axp.plot(np.pi*x, 1+np.sin(2.0*np.pi*x))
    axp.text(-0.2, 1, 'axp = axs[0,1].make_polar()', transform=axp.transAxes)
    for k in range(1, 3):
        axs[k,2].plot(x, np.sin(2.0*np.pi*x-k))
        axs[k,2].text(0.1, 0.8, 'axs[%d,2]' % k, transform=axs[k,-1].transAxes)
            
    plt.show()


if __name__ == "__main__":
    demo()
