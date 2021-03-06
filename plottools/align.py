"""
Align axes labels.


Upon importing this module, x- and y-labels are aligned automatically.
Call `align_params()` turn off this behavior and to choose matplotlib's
original functions instead of the ones provided by this module.


## Figure member functions

- `align_xlabels()`: align xlabels of a figure.
- `align_ylabels()`: align ylabels of a figure.
- `align_labels()`: align x- and ylabels of a figure.


## Settings

- `align_params()`: set align parameters.

`mpl.ptParams` defined by the align module:
```py
axes.align.auto : True 
axes.align.overwrite : True 
```


## Install/uninstall align functions

You usually do not need to call the `install_align()` function. Upon
loading the align module, `install_align()` is called automatically.

- `install_align()`: install code for aligning axes labels into `show()` and `savefig()` functions.
- `uninstall_align()`: uninstall code for aligning axes labels in `show()` and `savefig()` functions.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def align_xlabels(fig, axs=None):
    """ Align xlabels of a figure.

    Labels with the same orientation and on axes with the same
    coordinate are aligned to the bottommost one. In contrast to the
    matplotlib function with the same name, this functions aligns all
    labels, independently of any grids.

    Parameter
    ---------
    fig: matplotlib figure
        The figure on which xlabels and ylabels of all axes are aligned.
    axs: list of matplotlib axes
        Axes of which labels should be aligned. If `None` align labels of all axes.
    """
    xdist = mpl.rcParams.get('axes.labelpad', 3)
    xtick_size = mpl.rcParams['xtick.major.size']
    if mpl.rcParams['xtick.direction'] == 'inout':
        xtick_size *= 0.5
    elif mpl.rcParams['xtick.direction'] == 'in':
        xtick_size = 0.0
    if xtick_size > 0:
        xdist += xtick_size
        xdist += mpl.rcParams['xtick.major.pad']
    if axs is None:
        axs = fig.get_axes()
    # get axes positions and ticklabel widths:
    renderer = fig.canvas.get_renderer()
    yap = np.zeros((len(fig.get_axes()), 3))
    yph = np.zeros(len(fig.get_axes()))
    ylh = np.zeros(len(fig.get_axes()))
    ylx = np.zeros(len(fig.get_axes()))
    for k, ax in enumerate(axs):
        xax = ax.xaxis
        if xax.get_label_text():
            ax_bbox = ax.get_window_extent().get_points()
            pixely = np.abs(np.diff(ax_bbox[:,1]))[0]
            pos = xax.get_label_position() == 'top'
            tlh = np.abs(np.diff(xax.get_ticklabel_extents(renderer)[pos].get_points()[:,1]))[0]
            tlh += xdist
            if pos:
                tlh += 0.5*xax.get_label().get_fontsize()
            else:
                tlh += 0.5*xax.get_label().get_fontsize()
            ylh[k] = tlh
            yph[k] = pixely
            ylx[k] = xax.get_label().get_position()[0]
            yap[k,:] = (ax_bbox[0,1], xax.get_label().get_rotation(), pos)
    # compute label position for axes with same position:
    for yp in set(zip(yap[:,0], yap[:,1], yap[:,2])):
        idx = np.all(yap == yp, 1)
        ylh[idx] = np.max(ylh[idx])
    # set label position:
    for k, ax in enumerate(fig.get_axes()):
        if yap[k, 0] > 0:
            if yap[k, 2]:
                ax.xaxis.set_label_coords(ylx[k], 1+ylh[k]/yph[k], None)
            else:
                ax.xaxis.set_label_coords(ylx[k], -ylh[k]/yph[k], None)


def align_ylabels(fig, axs=None):
    """ Align ylabels of a figure.

    Labels with the same orientation and on axes with the same
    coordinate are aligned to the outmost one. In contrast to the
    matplotlib function with the same name, this functions aligns all
    labels, independently of any grids.

    Parameter
    ---------
    fig: matplotlib figure
        The figure on which xlabels and ylabels of all axes are aligned.
    axs: list of matplotlib axes
        Axes of which labels should be aligned. If `None` align labels of all axes.
    """
    ydist = mpl.rcParams.get('axes.labelpad', 3)
    ytick_size = mpl.rcParams['ytick.major.size']
    if mpl.rcParams['ytick.direction'] == 'inout':
        ytick_size *= 0.5
    elif mpl.rcParams['ytick.direction'] == 'in':
        ytick_size = 0.0
    if ytick_size > 0:
        ydist += ytick_size
        ydist += mpl.rcParams['ytick.major.pad']
    if axs is None:
        axs = fig.get_axes()
    # get axes positions and ticklabel widths:
    renderer = fig.canvas.get_renderer()
    xap = np.zeros((len(fig.get_axes()), 3))
    xpw = np.zeros(len(fig.get_axes()))
    xlw = np.zeros(len(fig.get_axes()))
    xly = np.zeros(len(fig.get_axes()))
    for k, ax in enumerate(axs):
        yax = ax.yaxis
        if yax.get_label_text():
            ax_bbox = ax.get_window_extent().get_points()
            pixelx = np.abs(np.diff(ax_bbox[:,0]))[0]
            pos = yax.get_label_position() == 'right'
            tlw = np.abs(np.diff(yax.get_ticklabel_extents(renderer)[pos].get_points()[:,0]))[0]
            tlw += ydist
            if pos:
                tlw += 0.7*yax.get_label().get_fontsize()
            else:
                tlw += 0.5*yax.get_label().get_fontsize()
            xlw[k] = tlw
            xpw[k] = pixelx
            xly[k] = yax.get_label().get_position()[1]
            xap[k,:] = (ax_bbox[0,0], yax.get_label().get_rotation(), pos)
    # compute label position for axes with same position:
    for xp in set(zip(xap[:,0], xap[:,1], xap[:,2])):
        idx = np.all(xap == xp, 1)
        xlw[idx] = np.max(xlw[idx])
    # set label position:
    for k, ax in enumerate(fig.get_axes()):
        if xap[k, 0] > 0:
            if xap[k, 2]:
                ax.yaxis.set_label_coords(1+xlw[k]/xpw[k], xly[k], None)
            else:
                ax.yaxis.set_label_coords(-xlw[k]/xpw[k], xly[k], None)


def align_labels(fig, axs=None):
    """ Align x- and ylabels of a figure.

    Labels with the same orientation and on axes with the same
    coordinate are aligned to the outmost one. In contrast to the
    matplotlib function with the same name, this functions aligns all
    labels, independently of any grids.

    Parameter
    ---------
    fig: matplotlib figure
        The figure on which xlabels and ylabels of all axes are aligned.
    axs: list of matplotlib axes
        Axes of which labels should be aligned. If `None` align labels of all axes.
    """
    align_xlabels(fig, axs)
    align_ylabels(fig, axs)



def __align_xlabels(fig, axs=None):
    """ Select align_xlabels() function from matplotlib or plottools.
    """
    if mpl.ptParams['axes.align.overwrite']:
        fig.__align_xlabels(axs)
    else:
        fig.__align_xlabels_orig_align(axs)
    

def __align_ylabels(fig, axs=None):
    """ Select align_ylabels() function from matplotlib or plottools.
    """
    if mpl.ptParams['axes.align.overwrite']:
        fig.__align_ylabels(axs)
    else:
        fig.__align_ylabels_orig_align(axs)
    

def __align_labels(fig, axs=None):
    """ Select align_labels() function from matplotlib or plottools.
    """
    if mpl.ptParams['axes.align.overwrite']:
        fig.__align_labels(axs)
    else:
        fig.__align_labels_orig_align(axs)
    

        
def __fig_show_labels(fig, *args, **kwargs):
    """ Call `align_labels()` on the figure before showing it.
    """
    if mpl.ptParams['axes.align.auto']:
        fig.align_labels()
    fig.__show_orig_align(*args, **kwargs)

    
def __fig_savefig_labels(fig, *args, **kwargs):
    """ Call `align_labels()` on the figure before saving it.
    """
    if mpl.ptParams['axes.align.auto']:
        fig.align_labels()
    fig.__savefig_orig_align(*args, **kwargs)


def __plt_show_labels(*args, **kwargs):
    """ Call `align_labels()` on all figures before showing them.
    """
    for fig in map(plt.figure, plt.get_fignums()):
        if mpl.ptParams['axes.align.auto']:
            fig.align_labels()
    plt.__show_orig_align(*args, **kwargs)


def __plt_savefig_labels(*args, **kwargs):
    """ Call `align_labels()` on the current figure before saving it.
    """
    if mpl.ptParams['axes.align.auto']:
        plt.gcf().align_labels()
    plt.__savefig_orig_align(*args, **kwargs)

    
def align_params(auto=None, overwrite=None):
    """ Set align parameters.
                  
    Only parameters that are not `None` are updated.

    Parameters
    ----------
    auto: bool
        If `True` then `align_labels()` is called automatically before showing
        or saving the figure. Depending on ptParams[`axes.align.overwrite`] this is either this
        module's `align_labels()` function or matplotlib's `align_labels()` function.
        Sets ptParam `axes.align.auto`.
    overwrite: bool
        If `True`, this module's `align_xlabels()`,  `align_ylabels()`, and
        `align_labels()` function are used as member functions of `mpl.figure.Figure`
        instead of the respective functions provided by matplotlib.
        Sets ptParam `axes.align.overwrite`.
    """
    if auto is not None:
        mpl.ptParams['axes.align.auto'] = auto
    if overwrite is not None:
        mpl.ptParams['axes.align.overwrite'] = overwrite

        
def install_align():
    """ Install code for aligning axes labels into `show()` and `savefig()` functions.

    Adds mpl.ptParams:
    ```py
    axes.align.auto : True 
    axes.align.overwrite : True 
    ```

    This function is called automatically upon importing the module.

    See also
    --------
    - `uninstall_align()`
    """
    if hasattr(mpl.figure.Figure, 'align_xlabels'):
        if not hasattr(mpl.figure.Figure, '__installed_align_labels'):
            mpl.figure.Figure.__installed_align_labels = 'overwrote'
            mpl.figure.Figure.__align_xlabels_orig_align = mpl.figure.Figure.align_xlabels
            mpl.figure.Figure.__align_ylabels_orig_align = mpl.figure.Figure.align_ylabels
            mpl.figure.Figure.__align_labels_orig_align = mpl.figure.Figure.align_labels
            mpl.figure.Figure.__align_xlabels = align_xlabels
            mpl.figure.Figure.__align_ylabels = align_ylabels
            mpl.figure.Figure.__align_labels = align_labels
            mpl.figure.Figure.align_xlabels = __align_xlabels
            mpl.figure.Figure.align_ylabels = __align_ylabels
            mpl.figure.Figure.align_labels = __align_labels
    else:
        mpl.figure.Figure.__installed_align_labels = 'installed'
        mpl.figure.Figure.align_xlabels = align_xlabels
        mpl.figure.Figure.align_ylabels = align_ylabels
        mpl.figure.Figure.align_labels = align_labels
    if not hasattr(mpl.figure.Figure, '__savefig_orig_align'):
        mpl.figure.Figure.__savefig_orig_align = mpl.figure.Figure.savefig
        mpl.figure.Figure.savefig = __fig_savefig_labels
    if not hasattr(mpl.figure.Figure, '__show_orig_align'):
        mpl.figure.Figure.__show_orig_align = mpl.figure.Figure.show
        mpl.figure.Figure.show = __fig_show_labels
    if not hasattr(plt, '__savefig_orig_align'):
        plt.__savefig_orig_align = plt.savefig
        plt.savefig = __plt_savefig_labels
    if not hasattr(plt, '__show_orig_align'):
        plt.__show_orig_align = plt.show
        plt.show = __plt_show_labels
    # add align parameter to rc configuration:
    if not hasattr(mpl, 'ptParams'):
        mpl.ptParams = {}
    if 'axes.align.auto' not in mpl.ptParams:
        mpl.ptParams.update({'axes.align.auto': True,
                             'axes.align.overwrite': True})


def uninstall_align():
    """ Uninstall code for aligning axes labels in `show()` and `savefig()` functions.

    See also
    --------
    - `install_align_labels()`
    - `uninstall_labels()`
    """
    if hasattr(mpl.figure.Figure, '__installed_align_labels'):
        if mpl.figure.Figure.__installed_align_labels == 'installed':
            delattr(mpl.figure.Figure, 'align_xlabels')
            delattr(mpl.figure.Figure, 'align_ylabels')
            delattr(mpl.figure.Figure, 'align_labels')
        elif mpl.figure.Figure.__installed_align_labels == 'overwrote':
            mpl.figure.Figure.align_xlabels = mpl.figure.Figure.__align_xlabels_orig_align
            mpl.figure.Figure.align_ylabels = mpl.figure.Figure.__align_ylabels_orig_align
            mpl.figure.Figure.align_labels = mpl.figure.Figure.__align_labels_orig_align
            delattr(mpl.figure.Figure, '__align_xlabels')
            delattr(mpl.figure.Figure, '__align_ylabels')
            delattr(mpl.figure.Figure, '__align_labels')
            delattr(mpl.figure.Figure, '__align_xlabels_orig_align')
            delattr(mpl.figure.Figure, '__align_ylabels_orig_align')
            delattr(mpl.figure.Figure, '__align_labels_orig_align')
        delattr(mpl.figure.Figure, '__installed_align_labels')
    if hasattr(mpl.figure.Figure, '__savefig_orig_align'):
        mpl.figure.Figure.savefig = mpl.figure.Figure.__savefig_orig_align
        delattr(mpl.figure.Figure, '__savefig_orig_align')
    if hasattr(mpl.figure.Figure, '__show_orig_align'):
        mpl.figure.Figure.show = mpl.figure.Figure.__show_orig_align
        delattr(mpl.figure.Figure, '__show_orig_align')
    if hasattr(plt, '__savefig_orig_align'):
        plt.savefig = plt.__savefig_orig_align
        delattr(plt, '__savefig_orig_align')
    if hasattr(plt, '__show_orig_align'):
        plt.show = plt.__show_orig_align
        delattr(plt, '__show_orig_align')
    # remove align parameter from mpl.ptParams:
    if hasattr(mpl, 'ptParams') and 'axes.align.auto' in mpl.ptParams:
        mpl.ptParams.pop('axes.align.auto', None)
        mpl.ptParams.pop('axes.align.overwrite', None)


install_align()


def demo():
    """ Run a demonstration of the align module.
    """
    align_params(auto=True, overwrite=True)
    
    fig, axs = plt.subplots(3, 2, figsize=(9, 6))
    fig.subplots_adjust(wspace=0.2, left=0.15, right=0.85, bottom=0.15)

    fig.suptitle('plottools.align')
    x = np.linspace(0, 20, 200)
    y = np.sin(x)

    axs[0, 0].plot(x, 4000*y)
    axs[0, 0].set_ylim(-5000.0, 5000.0)
    axs[0, 0].set_ylabel('Velocity\nin water [m/s]')
    
    axs[0, 1].plot(x, y)
    axs[0, 1].set_ylim(-1.0, 1.7)
    axs[0, 1].set_ylabel('Accelaration [m/s^2]')
    axs[0, 1].yaxis.set_ticks_position('right')
    axs[0, 1].yaxis.set_label_position('right')
    
    axs[1, 0].plot(x, y)
    axs[1, 0].set_ylim(-1.0, 1.0)
    axs[1, 0].set_ylabel('Potential [mV]')
    
    axs[1, 1].plot(x, 5000*y)
    axs[1, 1].set_ylim(-10000.0, 10000.0)
    axs[1, 1].set_ylabel('Potential [mV]')
    axs[1, 1].yaxis.set_ticks_position('right')
    axs[1, 1].yaxis.set_label_position('right')
    
    axs[2, 0].plot(x, y)
    axs[2, 0].set_ylim(-1.0, 1.7)
    axs[2, 0].set_xlabel('time [ms]')
    axs[2, 0].set_ylabel('Amplitude [Pa]')
    
    axs[2, 1].plot(x, 1000*y)
    axs[2, 1].set_ylim(-1000, 1700)
    axs[2, 1].set_xlabel('Timepoints [ms]\nsince stimulus onset')
    axs[2, 1].set_ylabel('Amplitude [Pa]')
    axs[2, 1].yaxis.set_ticks_position('right')
    axs[2, 1].yaxis.set_label_position('right')

    plt.show()


if __name__ == "__main__":
    demo()
