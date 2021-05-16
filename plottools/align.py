"""
Align axes labels.


## Figure member functions

- `align_labels()`: align x- and ylabels of a figure.


## Settings

- `align_params()`: set align parameters.

`mpl.ptParams` defined by the align module:
```py
axes.label.xdist: 5
axes.label.ydist: 10
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
        Axes of which labels should be aligned. If None align labels of all axes.

    TODO
    ----
    The size of the ticks should be included as well in computing the position of the labels.
    """
    xdist = 5
    ydist = 10
    if hasattr(mpl, 'ptParams'):
        xdist = mpl.ptParams.get('axes.label.xdist', 5)
        ydist = mpl.ptParams.get('axes.label.ydist', 10)
    if axs is None:
        axs = fig.get_axes()
    # get axes positions and ticklabel widths:
    renderer = fig.canvas.get_renderer()
    yap = np.zeros((len(fig.get_axes()), 2))
    yph = np.zeros(len(fig.get_axes()))
    ylh = np.zeros(len(fig.get_axes()))
    ylx = np.zeros(len(fig.get_axes()))
    xap = np.zeros((len(fig.get_axes()), 2))
    xpw = np.zeros(len(fig.get_axes()))
    xlw = np.zeros(len(fig.get_axes()))
    xly = np.zeros(len(fig.get_axes()))
    for k, ax in enumerate(axs):
        xax = ax.xaxis
        if xax.get_label_text():
            ax_bbox = ax.get_window_extent().get_points()
            pixely = np.abs(np.diff(ax_bbox[:,1]))[0]
            th = xax.get_text_heights(renderer)[1]
            th -= np.abs(np.diff(xax.get_label().get_window_extent(renderer).get_points()[:,1]))[0]
            th += xdist
            ylh[k] = th
            yph[k] = pixely
            ylx[k] = xax.get_label().get_position()[0]
            yap[k,:] = (ax_bbox[0,1], xax.get_label().get_rotation())
        yax = ax.yaxis
        if yax.get_label_text():
            ax_bbox = ax.get_window_extent().get_points()
            pixelx = np.abs(np.diff(ax_bbox[:,0]))[0]
            tw = yax.get_text_widths(renderer)[0]
            tw -= np.abs(np.diff(yax.get_label().get_window_extent(renderer).get_points()[:,0]))[0]
            tw += ydist
            xlw[k] = tw
            xpw[k] = pixelx
            xly[k] = yax.get_label().get_position()[1]
            xap[k,:] = (ax_bbox[0,0], yax.get_label().get_rotation())
    # compute label position for axes with same position:
    for yp in set(zip(yap[:,0], yap[:,1])):
        idx = np.all(yap == yp, 1)
        ylh[idx] = np.max(ylh[idx])
    for xp in set(zip(xap[:,0], xap[:,1])):
        idx = np.all(xap == xp, 1)
        xlw[idx] = np.max(xlw[idx])
    # set label position:
    for k, ax in enumerate(fig.get_axes()):
        if yap[k, 0] > 0:
            ax.xaxis.set_label_coords(ylx[k], -ylh[k]/yph[k], None)
        if xap[k, 0] > 0:
            ax.yaxis.set_label_coords(-xlw[k]/xpw[k], xly[k], None)

    
def __fig_show_labels(fig, *args, **kwargs):
    """ Call `align_labels()` on the figure before showing it.
    """
    fig.align_labels()
    fig.__show_orig_align(*args, **kwargs)

    
def __fig_savefig_labels(fig, *args, **kwargs):
    """ Call `align_labels()` on the figure before saving it.
    """
    fig.align_labels()
    fig.__savefig_orig_align(*args, **kwargs)


def __plt_show_labels(*args, **kwargs):
    """ Call `align_labels()` on all figures before showing them.
    """
    for fig in map(plt.figure, plt.get_fignums()):
        fig.align_labels()
    plt.__show_orig_align(*args, **kwargs)


def __plt_savefig_labels(*args, **kwargs):
    """ Call `align_labels()` on the current figure before saving it.
    """
    plt.gcf().align_labels()
    plt.__savefig_orig_align(*args, **kwargs)


def align_params(xdist=None, ydist=None):
    """ Set align parameters.
                  
    Only parameters that are not `None` are updated.
    
    Parameters
    ----------
    xdist: float
        Minimum vertical distance between xtick labels and label of x-axis.
        Used by `align_labels()`. Set ptParam `axes.label.xdist`.
    ydist: float
        Minimum horizontal distance between ytick labels and label of y-axis.
        Used by `align_labels()`. Set ptParam `axes.label.ydist`.
    """
    if hasattr(mpl, 'ptParams'):
        if xdist is not None:
            mpl.ptParams['axes.label.xdist'] = xdist
        if ydist is not None:
            mpl.ptParams['axes.label.ydist'] = ydist


def install_align():
    """ Install code for aligning axes labels into `show()` and `savefig()` functions.

    This function is also called automatically upon importing the module.

    See also
    --------
    - `uninstall_align()`
    """
    if not hasattr(mpl.figure.Figure, '__installed_align_labels'):
        if hasattr(mpl.figure.Figure, 'align_labels'):
            mpl.figure.Figure.__align_labels_orig_align = mpl.figure.Figure.align_labels
        mpl.figure.Figure.align_labels = align_labels
        mpl.figure.Figure.__installed_align_labels = True
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
    # add labels parameter to rc configuration:
    if not hasattr(mpl, 'ptParams'):
        mpl.ptParams = {}
    if 'axes.label.xdist' not in mpl.ptParams:
        mpl.ptParams['axes.label.xdist'] = 5
    if 'axes.label.ydist' not in mpl.ptParams:
        mpl.ptParams['axes.label.ydist'] = 10


def uninstall_align():
    """ Uninstall code for aligning axes labels in `show()` and `savefig()` functions.

    See also
    --------
    - `install_align_labels()`
    - `uninstall_labels()`
    """
    if hasattr(mpl.figure.Figure, '__installed_align_labels'):
        delattr(mpl.figure.Figure, 'align_labels')
        delattr(mpl.figure.Figure, '__installed_align_labels')
        if hasattr(mpl.figure.Figure, '__align_labels_orig_align'):
            mpl.figure.Figure.align_labels = mpl.figure.Figure.__align_labels_orig_align
            delattr(mpl.figure.Figure, '__align_labels_orig_align')
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
    # remove labels parameter from mpl.ptParams:
    if hasattr(mpl, 'ptParams') and 'axess.label.xdist' in mpl.ptParams:
        mpl.ptParams.pop('axes.label.xdist', None)
    if hasattr(mpl, 'ptParams') and 'axess.label.ydist' in mpl.ptParams:
        mpl.ptParams.pop('axes.label.ydist', None)


install_align()


def demo():
    """ Run a demonstration of the align module.
    """
    fig, axs = plt.subplots(3, 2, figsize=(11, 8))
    fig.subplots_adjust(wspace=0.5)

    fig.suptitle('plottools.align')
    x = np.linspace(0, 20, 200)
    y = np.sin(x)

    axs[0, 0].plot(x, 5000*y)
    axs[0, 0].set_ylim(-10000.0, 10000.0)
    axs[0, 0].set_ylabel('Velocity [m/s]')
    
    axs[0, 1].plot(x, y)
    axs[0, 1].set_ylim(-1.0, 1.7)
    axs[0, 1].set_ylabel('Accelaration [m/s^2]')
    
    axs[1, 0].plot(x, y)
    axs[1, 0].set_ylim(-1.0, 1.0)
    axs[1, 0].set_ylabel('Voltage [mV]')
    
    axs[1, 1].plot(x, 5000*y)
    axs[1, 1].set_ylim(-10000.0, 10000.0)
    axs[1, 1].set_ylabel('Voltage [mV]')
    
    axs[2, 0].plot(x, y)
    axs[2, 0].set_ylim(-1.0, 1.7)
    axs[2, 0].set_xlabel('Time [ms]')
    axs[2, 0].set_ylabel('Amplitude [Pa]')
    
    axs[2, 1].plot(x, 1000*y)
    axs[2, 1].set_ylim(-1000, 1700)
    axs[2, 1].set_xlabel('Timepoints [ms]')
    axs[2, 1].set_ylabel('Amplitude [Pa]')
    
    plt.show()


if __name__ == "__main__":
    demo()
