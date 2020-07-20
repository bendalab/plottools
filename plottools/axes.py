"""
Mark axes with a label and simplify common axis labels.

The following functions are added as a member to mpl.figure.Figure:

- `label_axes()`: put a label on each axes.
- `common_xlabels()`: simplify common xlabels.
- `common_ylabels()`: simplify common ylabels.
- `common_xtick_labels()`: simplify common xtick labels.
- `common_ytick_labels()`: simplify common ytick labels.
- `labelaxes_params()`: set mpl.ptParams for labelaxes.

mpl.ptParams defined by the axes module:
```
figure.labelaxes.xoffs : 'auto',
figure.labelaxes.yoffs : 'auto',
figure.labelaxes.labels: 'A',
figure.labelaxes.font  : dict(fontsize='x-large',
                              fontstyle='sans-serif',
                              fontweight='normal')
```
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec


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
            ax.set_xlabel('')
        elif done:
            ax.set_xlabel('')
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
            ax.set_ylabel('')
        elif done:
            ax.set_ylabel('')
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def common_xtick_labels(fig, axes=None):
    """ Simplify common xtick labels.
    
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
            ax.set_xlabel('')
            ax.xaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.set_xlabel('')
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_ytick_labels(fig, axes=None):
    """ Simplify common ytick labels.
    
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
            ax.set_ylabel('')
            ax.yaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.set_ylabel('')
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True


def label_axes(fig=None, axes=None, xoffs=None, yoffs=None, labels=None, **kwargs):
    """ Put on each axes a label.

    Labels are left/top aligned.

    Parameters
    ----------
    fig: matplotlib figure
        If None take figure from first element in `axes`.
    axes: None or list of matplotlib axes or int
        If None label all axes of the figure.
        Integers in the list are indices to the axes of the figure.
    xoffs: float, 'auto', or None
        X-coordinate of label relative to origin of axis in multiples of the width
        of a character (simply 60% of the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the right-most axis to the left figure border,
        otherwise use the value computed by the first call.
        If None take value from mpl.ptParams 'figure.labelaxes.xoffs'.
    yoffs: float, 'auto', or None
        Y-coordinate of label relative to top end of left yaxis in multiples
        of the height of a character (the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the top-most axis to the top figure border,
        otherwise use the value computed by the first call.
        If None take value from mpl.ptParams 'figure.labelaxes.yoffs'.
    labels: string or list of strings
        If string, labels are increments of the first alphanumeric character in the string.
        Subsequent calls to label_axes() keep incrementing the label.
        With a list arbitary labels can be specified.
        If None, set to mpl.ptParams figure.labelaxes.labels.
    kwargs: keyword arguments
        Passed on to ax.text().
        Defaults to mpl.ptParams figure.labelaxes.font.
    """
    if fig is None:
        fig = axes[0].get_figure()
    if axes is None:
        axes = fig.get_axes()
    if labels is None:
        labels = mpl.ptParams['figure.labelaxes.labels']
    if not isinstance(labels, (list, tuple)):
        label = '%s'
        c = 'A'
        for i, c in enumerate(labels):
            if c.isalnum():
                label = labels[:i] + '%s' + labels[i+1:]
                break
        if hasattr(fig, 'labelaxes_counter'):
            c = fig.labelaxes_counter
        c = ord(c)
        labels = [label % chr(c + k) for k in range(len(axes))]
        fig.labelaxes_counter = chr(c + len(axes))
    # font settings:
    for k in mpl.ptParams['figure.labelaxes.font']:
        if not k in kwargs:
            kwargs[k] = mpl.ptParams['figure.labelaxes.font'][k]
    # get axes offsets:
    xo = -1.0
    yo = 1.0
    for ax, l in zip(axes, labels):
        if isinstance(ax, int):
            ax = fig.get_axes()[ax]
        x0, y0, width, height = ax.get_position().bounds
        if x0 <= -xo:
            xo = -x0
        if 1.0-y0-height < yo:
            yo = 1.0-y0-height
    # get figure size in pixel:
    w, h = fig.get_window_extent().bounds[2:]
    ppi = 72.0 # points per inch:
    fs = mpl.rcParams['font.size']*fig.dpi/ppi
    # set offsets:
    if xoffs is None:
        xoffs = mpl.ptParams['figure.labelaxes.xoffs']
    if yoffs is None:
        yoffs = mpl.ptParams['figure.labelaxes.yoffs']
    if xoffs == 'auto':
        if hasattr(fig, 'labelaxes_xoffs'):
            xoffs = fig.labelaxes_xoffs
        else:
            xoffs = xo
    else:
        xoffs *= 0.6*fs/w
    if yoffs == 'auto':
        if hasattr(fig, 'labelaxes_yoffs'):
            yoffs = fig.labelaxes_yoffs
        else:
            yoffs = yo
    else:
        yoffs *= fs/h
    fig.labelaxes_xoffs = xoffs
    fig.labelaxes_yoffs = yoffs
    # put labels onto axes:
    for ax, l in zip(axes, labels):
        if isinstance(ax, int):
            ax = fig.get_axes()[ax]
        x0, y0, width, height = ax.get_position().bounds
        x = x0+xoffs
        if x <= 0.0:
            x = 0.0
        y = y0+height+yoffs
        if y >= 1.0:
            y = 1.0
        ax.text(x, y, l, transform=fig.transFigure, ha='left', va='top', **kwargs)


# make the functions available as member variables:
mpl.figure.Figure.common_xlabels = common_xlabels
mpl.figure.Figure.common_ylabels = common_ylabels
mpl.figure.Figure.common_xtick_labels = common_xtick_labels
mpl.figure.Figure.common_ytick_labels = common_ytick_labels
mpl.figure.Figure.label_axes = label_axes


""" Add labelaxes parameter to rc configuration.
"""
if not hasattr(mpl, 'ptParams'):
    mpl.ptParams = {}
mpl.ptParams.update({'figure.labelaxes.xoffs': 'auto',
                     'figure.labelaxes.yoffs': 'auto',
                     'figure.labelaxes.labels': 'A',
                     'figure.labelaxes.font': dict(fontsize='x-large',
                                                   fontstyle='sans-serif',
                                                   fontweight='normal')})


def labelaxes_params(xoffs=None, yoffs=None, labels=None, font=None):
    """ Set rc settings for labelaxes.

    Only update those parameters that are not None.

    Parameters
    ----------
    xoffs: float or 'auto'
        X-coordinate of label relative to origin of axis in multiples of the width
        of a character (simply 60% of the current font size).
        If 'auto', set it to the distance of the right-most axis to the left figure border,
        or to a previously computed value from that figure.
    yoffs: float or 'auto'
        Y-coordinate of label relative to top end of left yaxis in multiples
        of the height of a character (the current font size).
        If 'auto', set it to the distance of the top-most axis to the top figure border,
        or to a previously computed value from that figure.
    labels: string
        Labels are increments of the first alphanumeric character in the string.
    font: dict
        Dictionary with font settings
        (e.g. fontsize, fontfamiliy, fontstyle, fontweight, bbox, ...).
    """
    if xoffs is not None:
        mpl.ptParams.update({'figure.labelaxes.xoffs': xoffs})
    if yoffs is not None:
        mpl.ptParams.update({'figure.labelaxes.yoffs': yoffs})
    if labels is not None:
        mpl.ptParams.update({'figure.labelaxes.labels': labels})
    if font is not None:
        mpl.ptParams.update({'figure.labelaxes.font': font})


def demo():
    """ Run a demonstration of the axes module.
    """

    def afigure():
        fig = plt.figure()
        gs = gridspec.GridSpec(2, 3, width_ratios=[5, 1.5, 2.4])
        gs.update(left=0.075, bottom=0.14, right=0.985, top=0.9, wspace=0.6, hspace=0.6)
        ax1 = fig.add_subplot(gs[:,0])
        ax2 = fig.add_subplot(gs[0,1:])
        ax3 = fig.add_subplot(gs[1,1])
        ax4 = fig.add_subplot(gs[1,2])
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlabel('xlabel')
            ax.set_ylabel('ylabel')
        return fig, (ax1, ax2, ax3, ax4)

    labelaxes_params(xoffs='auto', yoffs='auto', labels='A', font=dict(fontweight='bold'))
    
    fig, axs = afigure()
    axs[0].text(0.5, 0.5, 'fig.label_axes()', transform=axs[0].transAxes, ha='center')
    axs[0].text(0.0, 0.0, 'X', transform=fig.transFigure, ha='left', va='bottom')
    fig.label_axes()

    fig, axs = afigure()
    axs[0].text(0.5, 0.7, 'fig,label_axes([ax1])',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.5, 'fig,label_axes([ax2, ax4], \'auto\', 1, \'B\')',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.3, 'fig.common_xlabels()',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.1, 'fig.common_ylabels(axs[1:])',
                transform=axs[0].transAxes, ha='center')
    fig.common_xlabels() 
    fig.common_ylabels(axs[1:])
    fig.label_axes([axs[0]])
    fig.label_axes([axs[1], axs[3]], 'auto', 1)

    fig, axs = afigure()
    axs[0].text(0.05, 0.7, "fig.label_axes([0, 2, 3],\n labels='(a)',\n fontweight='normal',\n fontstyle='italic')",
                transform=axs[0].transAxes)
    axs[0].text(0.5, 0.5, 'fig.common_xtick_labels()',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.3, 'fig.common_ytick_labels(axs[1:])',
                transform=axs[0].transAxes, ha='center')
    fig.common_xtick_labels() 
    fig.common_ytick_labels(axs[1:])
    fig.label_axes([0, 1, 3], labels='(a)', fontweight='normal', fontstyle='italic')
    plt.show()
        

if __name__ == "__main__":
    demo()
