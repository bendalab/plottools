"""
# Label axes

Mark panels with a label.

- `label_axes()`: put on each axes a label.
"""

import numpy as np


def label_axes(fig=None, xoffs=-0.1, yoffs=0.0, axes=None, labels='A', **kwargs):
    """ Put on each axes a label.

    Labels are left/top aligned.

    Parameters
    ----------
    fig: matplotlib figure
        If None take figure from first element in `axes`.
    xoffs: float
        X-coordinate of label relative to origin of axis in figure coordinates.
    yoffs: float
        Y-coordinate of label relative to top end of left yaxis in figure coordinates.
    axes: None or list of matplotlib axes or int.
        If None label all axes of the figure.
        Integers in the list are indices to the axes of the figure.
    labels: string or list of strings
        If string labels are increments of the first alphanumeric character in the string.
        With a list arbitary labels can be specified.
    kwargs: keyword arguments
        Passed on to ax.text().
    """
    if fig is None:
        fig = axes[0].get_figure()
    if axes is None:
        axes = fig.get_axes()
    if not isinstance(labels, (list, tuple)):
        label = '%s'
        c = 'A'
        for i, c in enumerate(labels):
            if c.isalnum():
                c = ord(c)
                label = labels[:i] + '%s' + labels[i+1:]
                break
        labels = [label % chr(c + k) for k in range(len(axes))]
    pos = np.zeros((len(axes), 2))
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


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 3, width_ratios=[5, 1.5, 2.4])
    gs.update(left=0.075, bottom=0.14, right=0.985, top=0.9, wspace=0.6, hspace=0.6)
    ax1 = fig.add_subplot(gs[:,0])
    ax2 = fig.add_subplot(gs[0,1:])
    ax3 = fig.add_subplot(gs[1,1])
    ax4 = fig.add_subplot(gs[1,2])
    label_axes(fig, -0.05, 0.05, fontsize='large')
    #label_axes(None, -0.05, 0.05, [ax2, ax4], fontsize='large')
    #label_axes(fig, -0.05, 0.05, [0, 2, 3], '(a)', fontsize='large')
    plt.show()
    
