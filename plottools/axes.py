"""
Simplify common axis labels.


## Figure member functions

- `common_xlabels()`: simplify common xlabels.
- `common_ylabels()`: simplify common ylabels.
- `common_xticks()`: simplify common xtick labels and xlabels.
- `common_yticks()`: simplify common ytick labels and ylabels.
- `common_xspines()`: simplify common x-spines, xtick labels, and xlabels.
- `common_yspines()`: simplify common y-spines, ytick labels, and ylabels.


## Settings

- `axes_params()`: set `mpl.ptParams` for axes module.

## Install/uninstall axes functions

You usually do not need to call these functions. Upon loading the axes
module, `install_axes()` is called automatically.

- `install_axes()`: install functions of the axes module in matplotlib.
- `uninstall_axes()`: uninstall all code of the axes module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def common_xlabels(fig, axes=None):
    """ Simplify common xlabels.

    Remove all xlabels except for one that is centered at the bottommost axes.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xlabels should be merged.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    miny = np.min(coords[:,1])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    xl = 0.5*(minx+maxx)
    done = False
    for ax in axes:
        if ax.get_position().p0[1] > miny + 1e-6:
            ax.xaxis.label.set_visible(False)
        elif done:
            ax.xaxis.label.set_visible(False)
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_ylabels(fig, axes=None):
    """ Simplify common ylabels.

    Remove all ylabels except for one that is centered at the leftmost axes.
    
    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose ylabels should be merged.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    # center common ylabel:
    minx = np.min(coords[:,0])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    done = False
    for ax in axes:
        if ax.get_position().p0[0] > minx + 1e-6:
            ax.yaxis.label.set_visible(False)
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def common_xticks(fig, axes=None):
    """ Simplify common xtick labels and xlabels.
    
    Keep xtick labels only at the lowest axes and center the common xlabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    miny = np.min(coords[:,1])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    xl = 0.5*(minx+maxx)
    done = False
    for ax in axes:
        if ax.get_position().p0[1] > miny + 1e-6:
            ax.xaxis.label.set_visible(False)
            ax.xaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.xaxis.label.set_visible(False)
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_yticks(fig, axes=None):
    """ Simplify common ytick labels and ylabels.
    
    Keep ytick labels only at the leftmost axes and center the common ylabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose yticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    done = False
    for ax in axes:
        if ax.get_position().p0[0] > minx + 1e-6:
            ax.yaxis.label.set_visible(False)
            ax.yaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def common_xspines(fig, axes=None):
    """ Simplify common x-spines, xtick labels, and xlabels.
    
    Keep spine and xtick labels only at the lowest axes and center the common xlabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    miny = np.min(coords[:,1])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    xl = 0.5*(minx+maxx)
    done = False
    for ax in axes:
        if ax.get_position().p0[1] > miny + 1e-6:
            ax.xaxis.label.set_visible(False)
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.spines['bottom'].set_visible(False)
        elif done:
            ax.xaxis.label.set_visible(False)
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_yspines(fig, axes=None):
    """ Simplify common y-spines, ytick labels, and ylabels.
    
    Keep spine and ytick labels only at the lowest axes and center the common ylabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose yticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    done = False
    for ax in axes:
        if ax.get_position().p0[0] > minx + 1e-6:
            ax.yaxis.label.set_visible(False)
            ax.yaxis.set_major_locator(ticker.NullLocator())
            ax.spines['left'].set_visible(False)
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def axes_params(xmargin=None, ymargin=None):
    """ Set rc settings for axes.

    Only parameters that are not `None` are updated.

    Parameters
    ----------
    xmargin: float
        Padding added to x-axis limits in fractions of the data interval.
        Sets rcParam `axes.xmargin`.
    ymargin: float
        Padding added to y-axis limits in fractions of the data interval.
        Sets rcParam `axes.ymargin`.
    """
    if xmargin is not None:
        mpl.rcParams['axes.xmargin'] = xmargin
    if ymargin is not None:
        mpl.rcParams['axes.ymargin'] = ymargin


def install_axes():
    """ Install functions of the axes module in matplotlib.

    See also
    --------
    uninstall_axes()
    """
    if not hasattr(mpl.figure.Figure, 'common_xlabels'):
        mpl.figure.Figure.common_xlabels = common_xlabels
    if not hasattr(mpl.figure.Figure, 'common_ylabels'):
        mpl.figure.Figure.common_ylabels = common_ylabels
    if not hasattr(mpl.figure.Figure, 'common_xticks'):
        mpl.figure.Figure.common_xticks = common_xticks
    if not hasattr(mpl.figure.Figure, 'common_yticks'):
        mpl.figure.Figure.common_yticks = common_yticks
    if not hasattr(mpl.figure.Figure, 'common_xspines'):
        mpl.figure.Figure.common_xspines = common_xspines
    if not hasattr(mpl.figure.Figure, 'common_yspines'):
        mpl.figure.Figure.common_yspines = common_yspines


def uninstall_axes():
    """ Uninstall all code of the axes module from matplotlib.

    See also
    --------
    install_axes()
    """
    if hasattr(mpl.figure.Figure, 'common_xlabels'):
        delattr(mpl.figure.Figure, 'common_xlabels')
    if hasattr(mpl.figure.Figure, 'common_ylabels'):
        delattr(mpl.figure.Figure, 'common_ylabels')
    if hasattr(mpl.figure.Figure, 'common_xticks'):
        delattr(mpl.figure.Figure, 'common_xticks')
    if hasattr(mpl.figure.Figure, 'common_yticks'):
        delattr(mpl.figure.Figure, 'common_yticks')
    if hasattr(mpl.figure.Figure, 'common_xspines'):
        delattr(mpl.figure.Figure, 'common_xspines')
    if hasattr(mpl.figure.Figure, 'common_yspines'):
        delattr(mpl.figure.Figure, 'common_yspines')


install_axes()


def demo():
    """ Run a demonstration of the axes module.
    """

    def afigure():
        fig, axs = plt.subplots(2, 2)
        for ax in axs.ravel():
            ax.set_xlabel('xlabel')
            ax.set_ylabel('ylabel')
        return fig, axs.ravel()

    axes_params(xmargin=0, ymargin=0)
    
    fig, axs = afigure()
    axs[0].text(0.5, 0.7, 'fig.common_xlabels()',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.5, 'fig.common_ylabels()',
                transform=axs[0].transAxes, ha='center')
    fig.common_xlabels() 
    fig.common_ylabels()

    fig, axs = afigure()
    axs[0].text(0.5, 0.7, 'fig.common_xticks()',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.5, 'fig.common_yticks()',
                transform=axs[0].transAxes, ha='center')
    fig.common_xticks() 
    fig.common_yticks()

    fig, axs = afigure()
    axs[0].text(0.5, 0.7, 'fig.common_xspines()',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.5, 'fig.common_yspines()',
                transform=axs[0].transAxes, ha='center')
    fig.common_xspines() 
    fig.common_yspines()
    
    plt.show()
        

if __name__ == "__main__":
    demo()
