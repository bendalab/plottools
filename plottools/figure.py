"""
# Figure

Size, margins and default filename of a figure.

Simply call
```
install_figure()
```
to patch a few matplotlib functions (`plt.figure()`, `plt.subplots()`,
`figure.add_gridspec()`, `gridspec.update()`, `fig.savefig()`, `plt.savefig()`).

Then `figsize` is in centimeters:
```
fig = plt.figure(figsize=(20.0, 16.0))         # in cm!
fig, ax = plt.subplots(figsize=(16.0, 10.0))   # in cm!
```
and subplot positions can be adjusted by margins given in multiples of the current font size:
```
fig.subplots_adjust(left=5.0, bottom=2.0, right=2.0, top=1.0)  # in fontsize margins!
gs = fig.add_gridspec(3, 3, wspace=0.3, hspace=0.3, left=5.0, bottom=2.0, right=2.0, top=2.5)
gs.update(wspace=0.3, hspace=0.3, left=5.0, bottom=2.0, right=2.0, top=2.5)
```
That is, `left` specifies the distance of the leftmost axes from the left margin of the figure,
`bottom` specifies the distance of the bottom axes from the bottom margin of the figure,
`right` specifies the distance of the rightmost axes from the right margin of the figure, and
`top` specifies the distance of the top axes from the top margin of the figure,
all as multiples of the font size.
This way, margins do not need to be adjusted when changing the `figsize`!

`plt.subplots()` can be called with `width_ratios` and `height_ratios`.

Further, `figure.add_gridspec()` is made available for older
matplotlib versions that do not have this function yet.

If no file name or only a file extension is specified in fig.savefig(),
then the file name of the main script is used.
If no file extension is specified, '.pdf' is appended.

Available functions:
- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.
- `install_figure()`: install code for figsize in centimeters and margins in multiples of fontsize.
- `figure_params()`: set savefig options via matplotlib's rc settings.
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


def adjust_fs(fig=None, left=6.0, bottom=3.0, right=1.5, top=0.5, **kwargs):
    """ Compute plot margins from multiples of the current font size.

    Parameters
    ----------
    fig: matplotlib.figure or None
        The figure from which the figure size is taken. If None use the current figure.
    left: float
        the left margin of the plots given in multiples of the width of a character
        (simply 60% of the current font size).
    bottom: float
        the bottom margin of the plots given in multiples of the height of a character
        (the current font size).
    right: float
        the right margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
        *Note:* in contrast to the matplotlib `right` parameters, this specifies the
        width of the right margin, not its position relative to the origin.
    top: float
        the right margin of the plots given in multiples of the height of a character
        (the current font size).
        *Note:* in contrast to the matplotlib `top` parameters, this specifies the
        width of the top margin, not its position relative to the origin.
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
    fig.subplots_adjust(**adjust_fs(fig, left=4.5))   # no matter what the figsize is!
    ```
    """
    if fig is None:
        fig = plt.gcf()
    w, h = fig.get_window_extent().bounds[2:]
    ppi = 72.0 # points per inch:
    fs = plt.rcParams['font.size']*fig.dpi/ppi
    margins = { 'left': left*0.6*fs/w,
                'bottom': bottom*fs/h,
                'right': 1.0 - right*0.6*fs/w,
                'top': 1.0 - top*fs/h }
    margins.update(kwargs)
    return margins

    
def __figure_figure(num=None, figsize=None, **kwargs):
    """ plt.figure() with figsize in centimeters.
    """
    if figsize:
        figsize = cm_size(*figsize)
    fig = plt.__figure_orig_figure(num, figsize, **kwargs)
    fig.canvas.mpl_connect('resize_event', __resize)
    return fig


def __fig_subplots_adjust_figure(fig, left=6.0, bottom=3.0, right=1.5, top=0.5, **kwargs):
    """ figure.subplots_adjust() with margins in multiples of the current font size.
    """
    if hasattr(fig, '__gridspecs'):
        for gs in fig.__gridspecs:
            gs.update(left, bottom, right, top, **kwargs)
    else:
        fig.__subplots_margins = {'left': left, 'bottom': bottom, 'right': right, 'top': top}
        fig.__subplots_adjust_orig_figure(**adjust_fs(fig, left, bottom, right, top, **kwargs))

    
def __gridspec_update_figure(gridspec, left=6.0, bottom=3.0, right=1.5, top=0.5, **kwargs):
    """ gridspec.update() with margins in multiples of the current font size.
    """
    figure = None
    if hasattr(gridspec, 'figure'):
        figure = gridspec.figure
    gridspec.__subplots_margins = {'left': left, 'bottom': bottom, 'right': right, 'top': top}
    gridspec.__update_orig_figure(**adjust_fs(figure, left, bottom, right, top, **kwargs))


def __fig_add_gridspec_figure(fig, nrows=1, ncols=1, left=6.0, bottom=3.0, right=1.5, top=0.5,
                              **kwargs):
    """ This emulates more current versions of matplotlib.
    """
    if fig.__add_gridspec_orig_figure:
        gs = fig.__add_gridspec_orig_figure(nrows=nrows, ncols=ncols,
                                            **adjust_fs(fig, left, bottom,
                                                        right, top,**kwargs))
    else:
        _ = kwargs.pop('figure', None)  # pop in case user has added this...
        gs = gridspec.GridSpec(nrows=nrows, ncols=ncols, **adjust_fs(fig, left, bottom,
                                                                     right, top, **kwargs))
    if not hasattr(fig, '__gridspecs'):
        fig.__gridspecs = []
    fig.__gridspecs.append(gs)    
    gs.__subplots_margins = {'left': left, 'bottom': bottom, 'right': right, 'top': top}
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
        for k in ['num', 'figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon', 'clear']:
            if k in kwargs:
                figkwargs[k] = kwargs.pop(k)
        upkwargs = {}
        for k in ['left', 'right', 'top', 'bottom', 'hspace', 'wspace']:
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

    
def __fig_savefig_figure(fig, fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script.
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if len(fname) == 0:
        fname = '.' + mpl.rcParams['savefig.format']
    if fname[0] == '.':
        fname = os.path.splitext(os.path.basename(__main__.__file__))[0] + fname
    if len(os.path.splitext(fname)[1]) <= 1:
        fname = os.path.splitext(fname)[0] + '.' + mpl.rcParams['savefig.format']
    fig.__savefig_orig_figure(fname, *args, **kwargs)
    if stripfonts is None:
        if 'pdf.stripfonts' in mpl.rcParams:
            stripfonts = mpl.rcParams['pdf.stripfonts']
        else:
            stripfonts = False
    if os.path.splitext(fname)[1] == '.pdf' and stripfonts:
       subprocess.call(['ps2pdf', '-dAutoRotatePages=/None', fname, 'tmp-'+fname])
       os.rename('tmp-'+fname, fname)


def __plt_savefig_figure(fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script. 
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if len(fname) == 0:
        fname = '.' + mpl.rcParams['savefig.format']
    if fname[0] == '.':
        fname = os.path.splitext(os.path.basename(__main__.__file__))[0] + fname
    if len(os.path.splitext(fname)[1]) <= 1:
        fname = os.path.splitext(fname)[0] + '.' + mpl.rcParams['savefig.format']
    plt.__savefig_orig_figure(fname, *args, **kwargs)
    if stripfonts is None:
        if 'pdf.stripfonts' in mpl.rcParams:
            stripfonts = mpl.rcParams['pdf.stripfonts']
        else:
            stripfonts = False
    if os.path.splitext(fname)[1] == '.pdf' and stripfonts:
       subprocess.call(['ps2pdf', '-dAutoRotatePages=/None', fname, 'tmp-'+fname])
       os.rename('tmp-'+fname, fname)


def install_figure():
    """ Install code for figsize in centimeters, margins in multiples of fontsize, and default filename for savefig().

    In addition, each new figure gets an resize event handler installed, that applies
    the supplied margins whenever a figure is resized.
    """
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


""" Add figure parameter to rc configuration.
"""
mpl.rcParams.update({'pdf.stripfonts': False})


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
    mpl.rcParams['savefig.format'] = format
    mpl.rcParams.update({'pdf.stripfonts': stripfonts})
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
    
    #fig, axs = plt.subplots(2, 1, figsize=(16.0, 10.0))  # figsize in cm!
    fig, axs = plt.subplots(2, 1, figsize=(16.0, 10.0), height_ratios=[5, 1])  # figsize in cm!
    fig.subplots_adjust(left=5.0, bottom=2.0, right=2.0, top=1.0)  # in fontsize margins!
    axs[0].text(0.1, 1.7, 'fig, ax = plt.subplots(figsize=(16.0, 10.0), height_ratios=[5, 1])  # in cm!')
    axs[0].text(0.1, 1.4, 'fig.subplots_adjust(left=5.0, bottom=2.0, top=1.0, right=2.0)  # in fontsize margins!')
    x = np.linspace(0.0, 2.0, 200)
    axs[0].plot(x, np.sin(2.0*np.pi*x))
    axs[0].set_ylim(-1.0, 2.0)
    fig.savefig('.pdf', stripfonts=False)

    fig = plt.figure(figsize=(20.0, 16.0))   # in cm!
    # in fontsize margins and even with old matplotlib versions:
    gs = fig.add_gridspec(3, 3, wspace=0.3, hspace=0.3, left=5.0, bottom=2.0, right=2.0, top=2.5)
    fig.suptitle('gs = fig.add_gridspec(3, 3, left=5.0, bottom=2.0, right=2.0, top=2.5)')
    for k in range(3):
        for j in range(3):
            ax = fig.add_subplot(gs[k,j])
            ax.plot(x, np.sin(2.0*np.pi*x+k*j))
    
    plt.show()


if __name__ == "__main__":
    demo()
