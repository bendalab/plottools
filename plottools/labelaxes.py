"""
# Label axes

Mark panels with a label.

The following function is added as a member to mpl.figure.Figure:
- `label_axes()`: put a label on each axes.

- `labelaxes_params()`: set rc settings for labelsaxes.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def label_axes(fig=None, axes=None, xoffs=None, yoffs=None, labels=None, **kwargs):
    """ Put on each axes a label.

    Labels are left/top aligned.

    Parameters
    ----------
    fig: matplotlib figure
        If None take figure from first element in `axes`.
    axes: None or list of matplotlib axes or int.
        If None label all axes of the figure.
        Integers in the list are indices to the axes of the figure.
    xoffs: float or None
        X-coordinate of label relative to origin of axis in pixel coordinates.
        If None, set it to the distance of the right-most axis to the left figure border.
    yoffs: float
        Y-coordinate of label relative to top end of left yaxis in pixel coordinates.
        If None, set it to the distance of the top-most axis to the top figure border.
    labels: string or list of strings
        If string, labels are increments of the first alphanumeric character in the string.
        With a list arbitary labels can be specified.
        If None, set to figure.axeslabels.labels rc settings.
    kwargs: keyword arguments
        Passed on to ax.text().
        Defaults to figure.axeslabels.font rc settings.
    """
    if fig is None:
        fig = axes[0].get_figure()
    if axes is None:
        axes = fig.get_axes()
    if labels is None:
        labels = mpl.rcParams['figure.axeslabels.labels']
    if not isinstance(labels, (list, tuple)):
        label = '%s'
        c = 'A'
        for i, c in enumerate(labels):
            if c.isalnum():
                c = ord(c)
                label = labels[:i] + '%s' + labels[i+1:]
                break
        labels = [label % chr(c + k) for k in range(len(axes))]
    # font settings:
    for k in mpl.rcParams['figure.axeslabels.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['figure.axeslabels.font'][k]
    # get offsets:
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
    figwidth = fig.get_window_extent().width
    figheight = fig.get_window_extent().height
    # set offsets:
    if xoffs is None:
        xoffs = xo - 1.0/figwidth
    else:
        xoffs /= figwidth
    if yoffs is None:
        yoffs = yo - 1.0/figheight
    else:
        yoffs /= figheight
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
mpl.figure.Figure.label_axes = label_axes


""" Add labelaxes parameter to rc configuration.
"""
mpl.rcParams.update({'figure.axeslabels.labels': 'A',
                     'figure.axeslabels.font': dict(fontsize='x-large',
                                              fontstyle='sans-serif',
                                              fontweight='normal')})


def labelaxes_params(labels='A', font=None):
    """ Set rc settings for labelsaxes.

    Parameter
    ---------
    labels: string
        Labels are increments of the first alphanumeric character in the string.
    font: dict
        Dictionary with font settings
        (e.g. fontsize, fontfamiliy, fontstyle, fontweight, bbox, ...).
    """
    mpl.rcParams.update({'figure.axeslabels.labels': labels})
    if font is not None:
        mpl.rcParams.update({'figure.axeslabels.font': font})


def demo():
    """ Run a demonstration of the labelaxes module.
    """

    def afigure():
        fig = plt.figure()
        gs = gridspec.GridSpec(2, 3, width_ratios=[5, 1.5, 2.4])
        gs.update(left=0.075, bottom=0.14, right=0.985, top=0.9, wspace=0.6, hspace=0.6)
        ax1 = fig.add_subplot(gs[:,0])
        ax2 = fig.add_subplot(gs[0,1:])
        ax3 = fig.add_subplot(gs[1,1])
        ax4 = fig.add_subplot(gs[1,2])
        return fig, (ax1, ax2, ax3, ax4)

    labelaxes_params(labels='A', font=dict(fontweight='bold'))
    
    fig, axs = afigure()
    axs[0].text(0.5, 0.5, 'fig.label_axes()', transform=axs[0].transAxes, ha='center')
    fig.label_axes()

    fig, axs = afigure()
    axs[0].text(0.5, 0.5, 'label_axes(None, [ax2, ax4],\n -50.0, 20.0)',
                transform=axs[0].transAxes, ha='center')
    label_axes(None, [axs[1], axs[3]], -50.0, 20.0)

    fig, axs = afigure()
    axs[0].text(0.5, 0.5, "fig.label_axes([0, 2, 3],\n labels='(a)', fontsize='large')",
                transform=axs[0].transAxes, ha='center')
    fig.label_axes([0, 2, 3], labels='(a)', fontweight='normal', fontstyle='italic')
    plt.show()


if __name__ == "__main__":
    demo()
