"""
Size, margins and default filename of a figure.

Simply call
```
install_figure()
```
to patch a few matplotlib functions (`plt.figure()`, `plt.subplots()`,
`figure.add_gridspec()`, `gridspec.update()`, `fig.savefig()`, `plt.savefig()`)
and to add a `fig.set_size_cm()` function.

Then you can specify the figure size in centimeters:
```
fig = plt.figure(cmsize=(20.0, 16.0))         # in cm!
fig, ax = plt.subplots(cmsize=(16.0, 10.0))   # in cm!
```
and subplot positions can be adjusted by margins given in multiples of the current font size:
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

`plt.subplots()` can be called with `width_ratios` and `height_ratios`.

Further, `figure.add_gridspec()` is made available for older
matplotlib versions that do not have this function yet.

If no file name or only a file extension is specified in fig.savefig(),
then the file name of the main script is used.
If no file extension is specified, '.pdf' is appended.

Available functions:

- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.
- `latex_include_figures()`: print LaTeX `\includegraphics{}` commands for all saved files.
- `install_figure()`: install code for figsize in centimeters and margins in multiples of fontsize.
- `figure_params()`: set savefig options via matplotlib's rc settings.

Functions added to mpl.figure.Figure:

- `set_size_cm()`: set the figure size in centimeters.
- `merge()`: add axis that covers bounding box of some axis.
"""

import __main__
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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


def set_size_cm(fig, w, h=None, forward=True):
    """ Set the figure size in centimeters.

    Parameters
    ----------
    fig: matplotlib figure
        The figure of which to set the size.
    w: float or (float, float)
        If `h` is not specified, width and height of the figure in centimeters,
        otherwise the width of the figure.
    h: float or None
        Height of the figure in centimeters.
    forward : bool
        If ``True``, the canvas size is automatically updated, e.g.,
        you can resize the figure window from the shell.
    """
    if h is None:
        w, h = w
    winch, hinch = cm_size(w, h)
    fig.set_size_inches(winch, hinch, forward=forward)


def adjust_fs(fig=None, left=None, bottom=None, right=None, top=None,
              leftm=6.0, bottomm=3.0, rightm=1.5, topm=0.5,
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
    fig.subplots_adjust(**adjust_fs(fig, leftm=4.5))   # no matter what the figsize is!
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

    
def __figure_figure(num=None, cmsize=None, **kwargs):
    """ plt.figure() with `cmsize` argument to specify figure size in centimeters.
    """
    if cmsize:
        kwargs.update(figsize=cm_size(*cmsize))
    fig = plt.__figure_orig_figure(num, **kwargs)
    fig.canvas.mpl_connect('resize_event', __resize)
    return fig


def __fig_subplots_adjust_figure(fig, *args, **kwargs):
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
        fig.__subplots_adjust_orig_figure(**adjust_fs(fig, *args, **kwargs))

    
def __gridspec_update_figure(gridspec, **kwargs):
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
    gridspec.__update_orig_figure(**adjust_fs(figure, **kwargs))


def __fig_add_gridspec_figure(fig, nrows=1, ncols=1, **kwargs):
    """ This emulates more current versions of matplotlib.
    """
    if fig.__add_gridspec_orig_figure:
        gs = fig.__add_gridspec_orig_figure(nrows=nrows, ncols=ncols,
                                            **adjust_fs(fig, **kwargs))
    else:
        _ = kwargs.pop('figure', None)  # pop in case user has added this...
        gs = gridspec.GridSpec(nrows=nrows, ncols=ncols, **adjust_fs(fig, **kwargs))
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


def __plt_subplots_figure(nrows=1, ncols=1, *args, **kwargs):
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
        return plt.__subplots_orig_figure(nrows, ncols, *args, **kwargs)


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
    """ Add axis that covers bounding box of some axis.

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


plot_saved_files = []

    
def __fig_savefig_figure(fig, fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script.
    
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if hasattr(fname, '__len__'):
        if len(fname) == 0:
            fname = '.' + mpl.rcParams['savefig.format']
        if fname[0] == '.':
            fname = os.path.splitext(os.path.basename(__main__.__file__))[0] + fname
        if len(os.path.splitext(fname)[1]) <= 1:
            fname = os.path.splitext(fname)[0] + '.' + mpl.rcParams['savefig.format']
        fig.__savefig_orig_figure(fname, *args, **kwargs)
        if not hasattr(fig, '__saved_files_counter'):
            fig.__saved_files_counter = 0
        fig.__saved_files_counter += 1
        global plot_saved_files
        plot_saved_files.append([fname, fig.__saved_files_counter])
        if stripfonts is None:
            if 'pdf.stripfonts' in mpl.ptParams:
                stripfonts = mpl.ptParams['pdf.stripfonts']
            else:
                stripfonts = False
        if os.path.splitext(fname)[1] == '.pdf' and stripfonts:
            subprocess.call(['ps2pdf', '-dAutoRotatePages=/None', fname, 'tmp-'+fname])
            os.rename('tmp-'+fname, fname)
    else:
        fig.__savefig_orig_figure(fname, *args, **kwargs)


def __plt_savefig_figure(fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script.
    
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if hasattr(fname, '__len__'):
        if len(fname) == 0:
            fname = '.' + mpl.rcParams['savefig.format']
        if fname[0] == '.':
            fname = os.path.splitext(os.path.basename(__main__.__file__))[0] + fname
        if len(os.path.splitext(fname)[1]) <= 1:
            fname = os.path.splitext(fname)[0] + '.' + mpl.rcParams['savefig.format']
        plt.__savefig_orig_figure(fname, *args, **kwargs)
        global plot_saved_files
        plot_saved_files.append([fname, 1])
        if stripfonts is None:
            if 'pdf.stripfonts' in mpl.ptParams:
                stripfonts = mpl.ptParams['pdf.stripfonts']
            else:
                stripfonts = False
        if os.path.splitext(fname)[1] == '.pdf' and stripfonts:
            subprocess.call(['ps2pdf', '-dAutoRotatePages=/None', fname, 'tmp-'+fname])
            os.rename('tmp-'+fname, fname)
    else:
        fig.__savefig_orig_figure(fname, *args, **kwargs)


def latex_include_figures():
    """ Print LaTeX `\includegraphics{}` commands for all saved files.

    This can then be copied directly into you LaTeX document to include
    the generated figures.  For multiple files from the same figure,
    beamer overlay specification are printed as well.

    Examples
    --------
    ```py
    fig1.savefig('introA')
    fig1.savefig('introB')
    fig2.savefig('data')
    latex_include_figures()
    ```
    writes to console
    ```txt
    \includegraphics<1>{introA}
    \includegraphics<2>{introB}
    \includegraphics{data}
    ```
    """
    global plot_saved_files
    for k in range(len(plot_saved_files)):
        if plot_saved_files[k][1] <= 1 and \
           (k+1 >= len(plot_saved_files) or plot_saved_files[k+1][1] <= 1):
            plot_saved_files[k][1] = None
    for fname, counter in plot_saved_files:
        fname = os.path.splitext(fname)[0]
        if counter is not None:
            print(r'\includegraphics<%d>{%s}' % (counter, fname))
        else:
            print(r'\includegraphics{%s}' % fname)
    plot_saved_files = []
    

def install_figure():
    """ Install code for figure size in centimeters, margins in multiples of fontsize, and default filename for savefig().

    In addition, each new figure gets an resize event handler installed, that applies
    the supplied margins whenever a figure is resized.

    See also
    --------
    uninstall_figure()
    """
    mpl.figure.Figure.set_size_cm = set_size_cm
    mpl.figure.Figure.merge = merge
    mpl.axes.Axes.__set_merged_position = __set_merged_position
    if not hasattr(plt, '__figure_orig_figure'):
        plt.__figure_orig_figure = plt.figure
        plt.figure = __figure_figure
    if not hasattr(mpl.figure.Figure, '__subplots_adjust_orig_figure'):
        mpl.figure.Figure.__subplots_adjust_orig_figure = mpl.figure.Figure.subplots_adjust
        mpl.figure.Figure.subplots_adjust = __fig_subplots_adjust_figure
    if not hasattr(mpl.figure.Figure, 'add_gridspec'):
        mpl.figure.Figure.add_gridspec = __fig_add_gridspec_figure
        mpl.figure.Figure.__add_gridspec_orig_figure = None
    if not hasattr(mpl.figure.Figure, '__add_gridspec_orig_figure'):
        mpl.figure.Figure.__add_gridspec_orig_figure = mpl.figure.Figure.add_gridspec
        mpl.figure.Figure.add_gridspec = __fig_add_gridspec_figure
    if not hasattr(mpl.gridspec.GridSpec, '__update_orig_figure'):
        mpl.gridspec.GridSpec.__update_orig_figure = mpl.gridspec.GridSpec.update
        mpl.gridspec.GridSpec.update = __gridspec_update_figure
    if not hasattr(mpl.figure.Figure, '__savefig_orig_figure'):
        mpl.figure.Figure.__savefig_orig_figure = mpl.figure.Figure.savefig
        mpl.figure.Figure.savefig = __fig_savefig_figure
    if not hasattr(plt, '__subplots_orig_figure'):
        plt.__subplots_orig_figure = plt.subplots
        plt.subplots = __plt_subplots_figure
    if not hasattr(plt, '__savefig_orig_figure'):
        plt.__savefig_orig_figure = plt.savefig
        plt.savefig = __plt_savefig_figure


def uninstall_figure():
    """ Uninstall all code that has been installed by install_figure().
    """
    if hasattr(mpl.figure.Figure, 'set_size_cm'):
        delattr(mpl.figure.Figure, 'set_size_cm')
    if hasattr(mpl.figure.Figure, 'merge'):
        delattr(mpl.figure.Figure, 'merge')
    if hasattr(mpl.axes.Axes, '__set_merged_position'):
        delattr(mpl.axes.Axes, '__set_merged_position')
    if hasattr(plt, '__figure_orig_figure'):
        plt.figure = plt.__figure_orig_figure
        delattr(plt, '__figure_orig_figure')
    if hasattr(mpl.figure.Figure, '__subplots_adjust_orig_figure'):
        mpl.figure.Figure.subplots_adjust = mpl.figure.Figure.__subplots_adjust_orig_figure
        delattr(mpl.figure.Figure, '__subplots_adjust_orig_figure')
    if hasattr(mpl.figure.Figure, '__add_gridspec_orig_figure'):
        if mpl.figure.Figure.__add_gridspec_orig_figure is None:
            delattr(mpl.figure.Figure, 'add_gridspec')
        else:
            mpl.figure.Figure.add_gridspec = mpl.figure.Figure.__add_gridspec_orig_figure
            delattr(mpl.figure.Figure, '__add_gridspec_orig_figure')
    if hasattr(mpl.gridspec.GridSpec, '__update_orig_figure'):
        mpl.gridspec.GridSpec.update = mpl.gridspec.GridSpec.__update_orig_figure
        delattr(mpl.gridspec.GridSpec, '__update_orig_figure')
    if hasattr(mpl.figure.Figure, '__savefig_orig_figure'):
        mpl.figure.Figure.savefig = mpl.figure.Figure.__savefig_orig_figure
        delattr(mpl.figure.Figure, '__savefig_orig_figure')
    if hasattr(plt, '__subplots_orig_figure'):
        plt.subplots = plt.__subplots_orig_figure
        delattr(plt, '__subplots_orig_figure')
    if hasattr(plt, '__savefig_orig_figure'):
        plt.savefig = plt.__savefig_orig_figure
        delattr(plt, '__savefig_orig_figure')


""" Add figure parameter to rc configuration.
"""
if not hasattr(mpl, 'ptParams'):
    mpl.ptParams = {}
mpl.ptParams.update({'pdf.stripfonts': False})


def figure_params(format='pdf', compression=6, fonttype=3, stripfonts=False):
    """ Set savefig options via matplotlib's rc settings.

    Parameters
    ----------
    format: 'png', 'ps', 'pdf', 'svg'
        File format of the saved figure.
    compression: int
        Compression level of pdf file from 0 to 9
    fonttype: 3 or 42
        Type 3 (Type3) or Type 42 (TrueType) fonts.
        Type3 use less disk space but are less well editable,
        Type42 use more disk space but are better editable in vector graphics software
        (says the internet).
    stripfonts: boolean
        If output file format is pdf, then run ps2pdf on the generated pdf file to
        strip it from embedded fonts. This might then look ugly as a standalone figure,
        but results in nice plots within a latex documents at a fraction of the file size.
    """
    mpl.ptParams.update({'pdf.stripfonts': stripfonts})
    mpl.rcParams['savefig.format'] = format
    # these all have only minor effects on file size:
    mpl.rcParams['pdf.compression'] = compression
    mpl.rcParams['pdf.fonttype'] = fonttype
    mpl.rcParams['pdf.use14corefonts'] = False
    mpl.rcParams['pdf.inheritcolor'] = False
    mpl.rcParams['ps.fonttype'] = fonttype

        
def demo():
    """ Run a demonstration of the figure module.
    """
    install_figure()
    
    fig, axs = plt.subplots(2, 1, cmsize=(16.0, 10.0), height_ratios=[5, 1])  # figsize in cm!
    fig.subplots_adjust(leftm=5.0, bottomm=2.0, rightm=2.0, topm=1.0)  # in fontsize margins!
    axs[0].text(0.1, 1.7, 'fig, ax = plt.subplots(cmsize=(16.0, 10.0), height_ratios=[5, 1])  # in cm!')
    axs[0].text(0.1, 1.4, 'fig.subplots_adjust(leftm=5.0, bottomm=2.0, topm=1.0, rightm=2.0)  # in fontsize margins!')
    x = np.linspace(0.0, 2.0, 200)
    axs[0].plot(x, np.sin(2.0*np.pi*x))
    axs[0].set_ylim(-1.0, 2.0)
    fig.savefig('.pdf', stripfonts=False)

    fig, axs = plt.subplots(3, 3)
    fig.set_size_cm(30.0, 16.0)
    # in fontsize margins and even with old matplotlib versions:
    fig.subplots_adjust(wspace=0.3, hspace=0.3, leftm=5.0, bottomm=2.0, rightm=2.0, topm=4)
    fig.suptitle('axs = plt.subplots(3, 3)\nfig.subplots_adjust(wspace=0.3, hspace=0.3, leftm=5.0, bottomm=2.0, rightm=2.0, topm=4)')
    ax = fig.merge(axs[1:3,0:2])
    ax.plot(x, np.sin(2.0*np.pi*x))
    ax.text(0.05, 0.1, 'ax = fig.merge(axs[1:3,0:2])', transform=ax.transAxes)
    for k in range(3):
        axs[0,k].plot(x, np.sin(2.0*np.pi*x+k))
        axs[0,k].text(0.1, 0.8, '0,%d' % k, transform=axs[0,k].transAxes)
    for k in range(1, 3):
        axs[k,-1].plot(x, np.sin(2.0*np.pi*x-k))
        axs[k,-1].text(0.1, 0.8, '%d,-1' % k, transform=axs[k,-1].transAxes)

    latex_include_figures()
            
    plt.show()
    uninstall_figure()


if __name__ == "__main__":
    demo()
