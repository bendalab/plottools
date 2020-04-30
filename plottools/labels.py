"""
# Labels

Annotate axis with label and unit and align axes labels.

- `set_label_format()`: set the string for formatting the axes labels.
- `install_align_labels()`: install code for aligning axes labels into show() and savefig() functions.
- `uninstall_align_labels()`: uninstall code for aligning axes labels in show() and savefig() functions.

The following functions are avilable as members of mpl.axes.Axes:
- `set_xlabel()`: format the xlabel from a label and an unit.
- `set_ylabel()`: format the ylabel from a label and an unit.
- `set_zlabel()`: format the zlabel from a label and an unit.

The following functions are available as members of mpl.figure.Figure:
- `align_labels()`: align x- and ylabels of a figure.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


""" This string defines how an axis label is formatted from a label and an unit. """
label_format = '{label} [{unit}]'


def set_label_format(labelf):
    """ Set the string for formatting the axes labels.
    
    Parameters
    ----------
    labelf: string
        A string for formatting the axes labels.
        In this string '{label}' is replaced by the axes' label,
        and '{unit}' is replaced by the axes' unit.
        The default format string is '{label} [{unit}]'.
    """
    global label_format
    label_format = labelf


def __axis_label(label, unit=None):
    """ Format an axis label from a label and a unit
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.

    Returns
    -------
    label: string
        An axis label formatted from `label` and `unit` according to
        the `label_format` string.
    """
    if not unit:
        return label
    else:
        return label_format.format(label=label, unit=unit)


def set_xlabel(ax, label, unit=None, **kwargs):
    """ Format the xlabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_xlabel() function.
    """
    ax.set_xlabel_labels(__axis_label(label, unit), **kwargs)

        
def set_ylabel(ax, label, unit=None, **kwargs):
    """ Format the ylabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_ylabel() function.
    """
    ax.set_ylabel_labels(__axis_label(label, unit), **kwargs)

        
def set_zlabel(ax, label, unit=None, **kwargs):
    """ Format the zlabel from a label and an unit.

    Uses the __axis_label() function to format the axis label.
    
    Parameters
    ----------
    label: string
        The name of the axis.
    unit: string
        The unit of the axis values.
    kwargs: key-word arguments
        Further arguments passed on to the set_zlabel() function.
    """
    ax.set_zlabel_labels(__axis_label(label, unit), **kwargs)


def align_labels(fig, xdist=5, ydist=10):
    """ Align x- and ylabels of a figure.

    Labels with the same orientation and on axes with the same coordinate
    are aligned to the outmost one.

    Parameter
    ---------
    fig: matplotlib figure
        The figure on which xlabels and ylabels of all axes are aligned.
    xdist: float
        Minimum vertical distance between xtick labels and label of x-axis.
    ydist: float
        Minimum horizontal distance between ytick labels and label of y-axis.
    """
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
    for k, ax in enumerate(fig.get_axes()):
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


""" Default distances between axis labels and tick labels. """
__default_xdist = 5
__default_ydist = 10

    
def __fig_show_labels(fig, *args, **kwargs):
    """ Call align_labels() on the figure before showing it.
    """
    fig.align_labels(__default_xdist, __default_ydist)
    fig.__show_orig_labels(*args, **kwargs)

    
def __fig_savefig_labels(fig, *args, **kwargs):
    """ Call align_labels() on the figure before saving it.
    """
    fig.align_labels(__default_xdist, __default_ydist)
    fig.__savefig_orig_labels(*args, **kwargs)


def __plt_show_labels(*args, **kwargs):
    """ Call align_labels() on all figures before showing them.
    """
    for fig in map(plt.figure, plt.get_fignums()):
        fig.align_labels(__default_xdist, __default_ydist)
    plt.__show_orig_labels(*args, **kwargs)


def __plt_savefig_labels(*args, **kwargs):
    """ Call align_labels() on the current figure before saving it.
    """
    plt.gcf().align_labels(__default_xdist, __default_ydist)
    plt.__savefig_orig_labels(*args, **kwargs)


def install_align_labels(xdist=5, ydist=10):
    """ Install code for aligning axes labels into show() and savefig() functions.

    Parameter
    ---------
    xdist: float
        Minimum vertical distance between xtick labels and label of x-axis.
    ydist: float
        Minimum horizontal distance between ytick labels and label of y-axis.
    """
    global __default_xdist
    __default_xdist = xdist
    global __default_ydist
    __default_ydist = ydist
    
    if not hasattr(mpl.figure.Figure, '__savefig_orig_labels'):
        mpl.figure.Figure.__savefig_orig_labels = mpl.figure.Figure.savefig
        mpl.figure.Figure.savefig = __fig_savefig_labels
    if not hasattr(mpl.figure.Figure, '__show_orig_labels'):
        mpl.figure.Figure.__show_orig_labels = mpl.figure.Figure.show
        mpl.figure.Figure.show = __fig_show_labels
    if not hasattr(plt, '__savefig_orig_labels'):
        plt.__savefig_orig_labels = plt.savefig
        plt.savefig = __plt_savefig_labels
    if not hasattr(plt, '__show_orig_labels'):
        plt.__show_orig_labels = plt.show
        plt.show = __plt_show_labels


def uninstall_align_labels():
    """ Uninstall code for aligning axes labels in show() and savefig() functions.
    """
    if hasattr(mpl.figure.Figure, '__savefig_orig_labels'):
        mpl.figure.Figure.savefig = mpl.figure.Figure.__savefig_orig_labels
        delattr(mpl.figure.Figure, '__savefig_orig_labels')
    if hasattr(mpl.figure.Figure, '__show_orig_labels'):
        mpl.figure.Figure.show = mpl.figure.Figure.__show_orig_labels
        delattr(mpl.figure.Figure, '__show_orig_labels')
    if hasattr(plt, '__savefig_orig_labels'):
        plt.savefig = plt.__savefig_orig_labels
        delattr(plt, '__savefig_orig_labels')
    if hasattr(plt, '__show_orig_labels'):
        plt.show = plt.__show_orig_labels
        delattr(plt, '__show_orig_labels')


# make functions available as member variables:
mpl.axes.Axes.set_xlabel_labels = mpl.axes.Axes.set_xlabel
mpl.axes.Axes.set_xlabel = set_xlabel
mpl.axes.Axes.set_ylabel_labels = mpl.axes.Axes.set_ylabel
mpl.axes.Axes.set_ylabel = set_ylabel
Axes3D.set_zlabel_labels = Axes3D.set_zlabel
Axes3D.set_zlabel = set_zlabel
mpl.figure.Figure.align_labels = align_labels


def demo():
    """ Run a demonstration of the labels module.
    """
    install_align_labels()
    
    fig, axs = plt.subplots(3, 2, figsize=(11, 8))
    fig.subplots_adjust(wspace=0.5)

    fig.suptitle('fig.align_labels(): aligns x- and ylabels')
    x = np.linspace(0.0, 4.0*np.pi, 200)
    y = np.sin(x)

    axs[0, 0].text(0.1, 7000, "ax.set_ylabel('Velocity', 'm/s')")
    axs[0, 0].set_ylim(-10000.0, 10000.0)
    axs[0, 0].set_ylabel('Velocity', 'm/s')
    
    axs[0, 1].text(0.1, 1.3, "ax.set_ylabel('Acceleration', 'm/s^2')")
    axs[0, 1].set_ylim(-1.0, 1.7)
    axs[0, 1].set_ylabel('Accelaration', 'm/s^2')
    
    axs[1, 0].set_ylim(-1.0, 1.0)
    
    axs[1, 1].text(0.1, 7000, "ax.set_ylabel('Voltage', 'mV')")
    axs[1, 1].set_ylim(-10000.0, 10000.0)
    axs[1, 1].set_ylabel('Voltage', 'mV')
    
    axs[2, 0].plot(x, y)
    axs[2, 0].set_ylim(-1.0, 1.7)
    axs[2, 0].text(1.0, 1.3, "ax.set_xlabel('Time', 'ms')")
    axs[2, 0].text(1.0, 1.1, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[2, 0].set_xlabel('Time', 'ms')
    axs[2, 0].set_ylabel('Amplitude', 'Pa')
    
    set_label_format('{label} / {unit}')   # usually you would do this before any plotting!
    axs[2, 1].plot(x, 1000*y)
    axs[2, 1].set_ylim(-1000, 1700)
    axs[2, 1].text(1.0, 1500, "set_label_format('{label} / {unit}')")
    axs[2, 1].text(1.0, 1300, "ax.set_xlabel('Time', 'ms')")
    axs[2, 1].text(1.0, 1100, "ax.set_ylabel('Amplitude', 'Pa')")
    axs[2, 1].set_xlabel('Time', 'ms')
    axs[2, 1].set_ylabel('Amplitude', 'Pa')
    
    plt.show()


if __name__ == "__main__":
    demo()
