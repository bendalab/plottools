"""
# Label axes

Mark panels with a label.

The following function is added as a member to mpl.figure.Figure:
- `label_axes()`: put a label on each axes.

- `labelaxes_params()`: set rc settings for labelaxes.
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
    xoffs: float, 'auto', or None
        X-coordinate of label relative to origin of axis in multiples of the width
        of a character (simply 60% of the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the right-most axis to the left figure border,
        otherwise use the value computed by the first call.
        If None take value from rc settings 'figure.labelaxes.xoffs'.
    yoffs: float, 'auto', or None
        Y-coordinate of label relative to top end of left yaxis in multiples
        of the height of a character (the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the top-most axis to the top figure border,
        otherwise use the value computed by the first call.
        If None take value from rc settings 'figure.labelaxes.yoffs'.
    labels: string or list of strings
        If string, labels are increments of the first alphanumeric character in the string.
        Subsequent calls to label_axes() keep incrementing the label.
        With a list arbitary labels can be specified.
        If None, set to figure.labelaxes.labels rc settings.
    kwargs: keyword arguments
        Passed on to ax.text().
        Defaults to figure.labelaxes.font rc settings.
    """
    if fig is None:
        fig = axes[0].get_figure()
    if axes is None:
        axes = fig.get_axes()
    if labels is None:
        labels = mpl.rcParams['figure.labelaxes.labels']
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
    for k in mpl.rcParams['figure.labelaxes.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['figure.labelaxes.font'][k]
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
        xoffs = mpl.rcParams['figure.labelaxes.xoffs']
    if yoffs is None:
        yoffs = mpl.rcParams['figure.labelaxes.yoffs']
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
mpl.figure.Figure.label_axes = label_axes


""" Add labelaxes parameter to rc configuration.
"""
mpl.rcParams.update({'figure.labelaxes.xoffs': 'auto',
                     'figure.labelaxes.yoffs': 'auto',
                     'figure.labelaxes.labels': 'A',
                     'figure.labelaxes.font': dict(fontsize='x-large',
                                                   fontstyle='sans-serif',
                                                   fontweight='normal')})


def labelaxes_params(xoffs='auto', yoffs='auto', labels=None, font=None):
    """ Set rc settings for labelaxes.

    Parameter
    ---------
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
    mpl.rcParams.update({'figure.labelaxes.xoffs': xoffs,
                         'figure.labelaxes.yoffs': yoffs,
                         'figure.labelaxes.labels': labels})
    if font is not None:
        mpl.rcParams.update({'figure.labelaxes.font': font})


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

    labelaxes_params(xoffs='auto', yoffs='auto', labels='A', font=dict(fontweight='bold'))
    
    fig, axs = afigure()
    axs[0].text(0.5, 0.5, 'fig.label_axes()', transform=axs[0].transAxes, ha='center')
    axs[0].text(0.0, 0.0, 'X', transform=fig.transFigure, ha='left', va='bottom')
    fig.label_axes()

    fig, axs = afigure()
    axs[0].text(0.5, 0.6, 'fig,label_axes([ax1])',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.4, 'fig,label_axes([ax2, ax4], \'auto\', 1, \'B\')',
                transform=axs[0].transAxes, ha='center')
    fig.label_axes([axs[0]])
    fig.label_axes([axs[1], axs[3]], 'auto', 1)

    fig, axs = afigure()
    axs[0].text(0.05, 0.7, "fig.label_axes([0, 2, 3],\n labels='(a)',\n fontweight='normal',\n fontstyle='italic')",
                transform=axs[0].transAxes)
    fig.label_axes([0, 2, 3], labels='(a)', fontweight='normal', fontstyle='italic')
    plt.show()


if __name__ == "__main__":
    demo()
