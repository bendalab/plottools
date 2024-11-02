"""
Reduce common axis labels.


## Figure member functions

- `common_xlabels()`: reduce common xlabels.
- `common_ylabels()`: reduce common ylabels.
- `common_xticks()`: reduce common xtick labels and xlabels.
- `common_yticks()`: reduce common ytick labels and ylabels.
- `common_xspines()`: reduce common x-spines, xtick labels, and xlabels.
- `common_yspines()`: reduce common y-spines, ytick labels, and ylabels.


## Install/uninstall common functions

You usually do not need to call these functions. Upon loading the common
module, `install_common()` is called automatically.

- `install_common()`: install functions of the common module in matplotlib.
- `uninstall_common()`: uninstall all code of the common module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def common_xlabels(fig, *axes):
    """ Reduce common xlabels.

    Remove all xlabels except for one that is centered at the bottommost axes.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: Sequence of matplotlib axes
        Axes whose xlabels should be merged.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.min(coords[:,3])
    xl = 0.5*(minx+maxx)
    if axes[0].xaxis.get_label().get_position()[0] == 1:
        xl = maxx
    pos = axes[0].xaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().y0 < miny + 1e-6 if pos == 'bottom' else \
            ax.get_position().y1 > maxy - 1e-6
        if not first:
            ax.xaxis.label.set_visible(False)
        elif done:
            ax.xaxis.label.set_visible(False)
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_ylabels(fig, *axes):
    """ Reduce common ylabels.

    Remove all ylabels except for one that is centered at the leftmost axes.
    
    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose ylabels should be merged.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    # center common ylabel:
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    pos = axes[0].yaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().x0 < minx + 1e-6 if pos == 'left' else \
            ax.get_position().x1 > maxx - 1e-6
        if not first:
            ax.yaxis.label.set_visible(False)
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def common_xticks(fig, *axes):
    """ Reduce common xtick labels and xlabels.
    
    Keep xtick labels only at the lowest axes and center the common xlabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xticks should be combined.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.min(coords[:,3])
    xl = 0.5*(minx+maxx)
    if axes[0].xaxis.get_label().get_position()[0] == 1:
        xl = maxx
    pos = axes[0].xaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().y0 < miny + 1e-6 if pos == 'bottom' else \
            ax.get_position().y1 > maxy - 1e-6
        if not first:
            ax.xaxis.label.set_visible(False)
            ax.xaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.xaxis.label.set_visible(False)
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_yticks(fig, *axes):
    """ Reduce common ytick labels and ylabels.
    
    Keep ytick labels only at the leftmost axes and center the common ylabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose yticks should be combined.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    pos = axes[0].yaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().x0 < minx + 1e-6 if pos == 'left' else \
            ax.get_position().x1 > maxx - 1e-6
        if not first:
            ax.yaxis.label.set_visible(False)
            ax.yaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def common_xspines(fig, *axes):
    """ Reduce common x-spines, xtick labels, and xlabels.
    
    Keep spine and xtick labels only at the lowest axes and center the common xlabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xticks should be combined.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.min(coords[:,3])
    xl = 0.5*(minx+maxx)
    if axes[0].xaxis.get_label().get_position()[0] == 1:
        xl = maxx
    pos = axes[0].xaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().y0 < miny + 1e-6 if pos == 'bottom' else \
            ax.get_position().y1 > maxy - 1e-6
        if not first:
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


def common_yspines(fig, *axes):
    """ Reduce common y-spines, ytick labels, and ylabels.
    
    Keep spine and ytick labels only at the lowest axes and center the common ylabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose yticks should be combined.
        If not specified, take all axes of the figure.
    """
    if len(axes) == 0:
        axes = fig.get_axes()
    if len(axes) == 0:
        return
    axs = []
    for ax in axes:
        if isinstance(ax, np.ndarray):
            axs.extend(ax.ravel())
        elif isinstance(ax, (tuple, list)):
            axs.extend(ax)
        else:
            axs.append(ax)
    axes = axs
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    pos = axes[0].yaxis.get_label_position()
    done = False
    for ax in axes:
        first = ax.get_position().x0 < minx + 1e-6 if pos == 'left' else \
            ax.get_position().x1 > maxx - 1e-6
        if not first:
            ax.yaxis.label.set_visible(False)
            ax.yaxis.set_major_locator(ticker.NullLocator())
            ax.spines[pos].set_visible(False)
        elif done:
            ax.yaxis.label.set_visible(False)
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def install_common():
    """ Install functions of the common module in matplotlib.

    See also
    --------
    uninstall_common()
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


def uninstall_common():
    """ Uninstall all code of the common module from matplotlib.

    See also
    --------
    install_common()
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


install_common()


def demo():
    """ Run a demonstration of the common module.
    """
    fig, axs = plt.subplots(4, 4, figsize=(13,7))
    fig.subplots_adjust(left=0.05, right=0.98, bottom=0.08, wspace=0.3, hspace=0.5)
    fig.suptitle('plottools.common')
    for ax in axs.ravel():
        ax.set_xlabel('xlabel')
        ax.set_ylabel('ylabel')
    
    axs[0,2].text(0.5, 0.7, 'fig.common_xlabels(axs[0:2,2:4])',
                  transform=axs[0,2].transAxes, ha='center')
    axs[0,2].text(0.5, 0.5, 'fig.common_ylabels(axs[0:2,2:4])',
                  transform=axs[0,2].transAxes, ha='center')
    fig.common_xlabels(axs[0:2,2:4]) 
    fig.common_ylabels(axs[0:2,2:4])

    axs[2,0].text(0.5, 0.7, 'fig.common_xticks(axs[2:4,0:2])',
                  transform=axs[2,0].transAxes, ha='center')
    axs[2,0].text(0.5, 0.5, 'fig.common_yticks(axs[2:4,0:2])',
                  transform=axs[2,0].transAxes, ha='center')
    fig.common_xticks(axs[2:4,0:2]) 
    fig.common_yticks(axs[2:4,0:2])

    axs[2,2].text(0.5, 0.7, 'fig.common_xspines(axs[2:4,2:4])',
                  transform=axs[2,2].transAxes, ha='center')
    axs[2,2].text(0.5, 0.5, 'fig.common_yspines(axs[2:4,2:4])',
                  transform=axs[2,2].transAxes, ha='center')
    fig.common_xspines(axs[2:4,2:4]) 
    fig.common_yspines(axs[2:4,2:4])
    
    plt.show()
        

if __name__ == "__main__":
    demo()
