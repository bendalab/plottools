"""
Tag axes with a label.


## Figure member functions

- `tag()`: tag each axes with a label.


## Settings

- `tag_params()`: set default tag appearance.

`mpl.ptParams` defined by the tag module:
```py
figure.tags.xoffs : 'auto',
figure.tags.yoffs : 'auto',
figure.tags.label : '%A',
figure.tags.minorlabel : '%A%mi',
figure.tags.font  : dict(fontsize='x-large', fontstyle='sans-serif', fonttweight='normal')
```

## Install/uninstall tag functions

You usually do not need to call these functions. Upon loading the tag
module, `install_tag()` is called automatically.

- `install_tag()`: install functions of the tag module in matplotlib.
- `uninstall_tag()`: uninstall all code of the tag module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def tag(fig=None, axes=None, xoffs=None, yoffs=None,
        labels=None, minor_label=None, major_index=None,
        minor_index=None, **kwargs):
    """Tag each axes with a label.

    Labels are left/top aligned.

    Parameters
    ----------
    fig: matplotlib figure
        If None take figure from first element in `axes`.
    axes: None or matplotlib axes or int or list of matplotlib axes or int
        If None label all axes of the figure.
        Integers in the list are indices to the axes of the figure.
        For axes in the out list, `labels` is used for tagging,
        for axes in (optional) inner lists, `minor_label` is used.
    xoffs: float, 'auto', or None
        X-coordinate of label relative to origin of axis in multiples of the width
        of a character (simply 60% of the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the right-most axis to the left figure border,
        otherwise use the value computed by the first call.
        If None take value from `mpl.ptParams['figure.tags.xoffs']`.
    yoffs: float, 'auto', or None
        Y-coordinate of label relative to top end of left yaxis in multiples
        of the height of a character (the current font size).
        If 'auto' and this is the first call of this function on the figure,
        set it to the distance of the top-most axis to the top figure border,
        otherwise use the value computed by the first call.
        If None take value from `mpl.ptParams['figure.tags.yoffs']`.
    labels: string or list of strings
        If string, then replace formatting substrings 
        '%A', '%a', '%1', '%i', and '%I' to generate labels for each axes in the outer list.
        
        - '%A': A B C ...
        - '%a': a b c ...
        - '%1': 1 2 3 ...
        - '%i': i ii iii iv ...
        - '%I': I II III IV ...
        
        Subsequent calls to `tag()` keep incrementing the label.
        With a list arbitary labels can be specified.
        If None, set to `mpl.ptParams['figure.tags.label']`.
    minor_label: string
        If `axes` is a nested list of axes, then for the inner lists
        `minor_label` is used for formatting the axes label.
        Formatting substrings '%A', '%a', '%1', '%i', and '%I' are replaced
        by the corresponding tags for the outer list, '%mA', '%ma', '%m1', '%mi',
        and '%mI' are replaced by the equivalently formatted tags for the inner list.
        See `labels` for meaning of the formatting substrings.
        If None, set to `mpl.ptParams['figure.tags.minorlabel']`.
    major_index: int or None
        Start labeling major axes with this index (0 = 'A').
        If None, use last index from previous call to `tag()`.
    minor_index: int or None
        Start labeling minor axes with this index (0 = 'A').
        If None, start with 0.
    kwargs: dict
        Key-word arguments are passed on to ax.text() for formatting the tag label.
        Overrides settings in `mpl.ptParams['figure.tags.font']`.
    """
    if fig is None:
        fig = axes[0].get_figure()
    if axes is None:
        axes = fig.get_axes()
    if not isinstance(axes, (list, tuple, np.ndarray)):
        axes = [axes]
    if labels is None:
        labels = mpl.ptParams['figure.tags.label']
    if minor_label is None:
        minor_label = mpl.ptParams['figure.tags.minorlabel']
    if not isinstance(labels, (list, tuple, np.ndarray)):
        # generate labels:
        romans_lower = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
                        'xi', 'xii', 'xiii']
        romans_upper = [r.upper() for r in romans_lower]
        if major_index is None:
            if hasattr(fig, 'tags_major_index'):
                major_index = fig.tags_major_index
            else:
                major_index = 0
        if minor_index is None:
            minor_index = 0
        label_list = []
        for k, axs in enumerate(axes):
            if isinstance(axs, (list, tuple, np.ndarray)):
                for j in range(len(axs)):
                    mlabel = str(minor_label) if minor_label else str(lables)
                    mlabel = mlabel.replace('%a', chr(ord('a') + major_index + k))
                    mlabel = mlabel.replace('%A', chr(ord('A') + major_index + k))
                    mlabel = mlabel.replace('%1', chr(ord('1') + major_index + k))
                    mlabel = mlabel.replace('%i', romans_lower[major_index + k])
                    mlabel = mlabel.replace('%I', romans_upper[major_index + k]) 
                    mlabel = mlabel.replace('%ma', chr(ord('a') + minor_index + j))
                    mlabel = mlabel.replace('%mA', chr(ord('A') + minor_index + j))
                    mlabel = mlabel.replace('%m1', chr(ord('1') + minor_index + j))
                    mlabel = mlabel.replace('%mi', romans_lower[minor_index + j])
                    mlabel = mlabel.replace('%mI', romans_upper[minor_index + j]) 
                    label_list.append(mlabel)
                minor_index = 0
            else:
                label = labels.replace('%a', chr(ord('a') + major_index + k))
                label = label.replace('%A', chr(ord('A') + major_index + k))
                label = label.replace('%1', chr(ord('1') + major_index + k))
                label = label.replace('%i', romans_lower[major_index + k])
                label = label.replace('%I', romans_upper[major_index + k]) 
                label_list.append(label)
        fig.tags_major_index = major_index + len(axes)
    else:
        label_list = labels
    # flatten axes:
    axes_list = []
    for axs in axes:
        if isinstance(axs, (list, tuple, np.ndarray)):
            axes_list.extend(axs)
        else:
            axes_list.append(axs)
    # font settings:
    fkwargs = dict(**mpl.ptParams['figure.tags.font'])
    fkwargs.update(**kwargs)
    # get axes offsets:
    xo = -1.0
    yo = 1.0
    for ax, l in zip(axes_list, label_list):
        if isinstance(ax, int):
            ax = fig.get_axes()[ax]
        x0, y0, width, height = ax.get_position(original=True).bounds
        if x0 <= -xo:
            xo = -x0
        if 1.0-y0-height < yo:
            yo = 1.0-y0-height
    # get figure size in pixel:
    w, h = fig.get_window_extent().bounds[2:]
    ppi = 72.0 # points per inch:
    fs = mpl.rcParams['font.size']*fig.dpi/ppi
    # compute offsets:
    if xoffs is None:
        xoffs = mpl.ptParams['figure.tags.xoffs']
    if yoffs is None:
        yoffs = mpl.ptParams['figure.tags.yoffs']
    if xoffs == 'auto':
        if hasattr(fig, 'tags_xoffs'):
            xoffs = fig.tags_xoffs
        else:
            xoffs = xo
    else:
        xoffs *= 0.6*fs/w
    if yoffs == 'auto':
        if hasattr(fig, 'tags_yoffs'):
            yoffs = fig.tags_yoffs
        else:
            yoffs = yo - 1.0/h   # minus one pixel
    else:
        yoffs *= fs/h
    fig.tags_xoffs = xoffs
    fig.tags_yoffs = yoffs
    # put labels onto axes:
    for ax, l in zip(axes_list, label_list):
        if isinstance(ax, int):
            ax = fig.get_axes()[ax]
        x0, y0, width, height = ax.get_position(original=True).bounds
        x = x0 + xoffs
        if x <= 0.0:
            x = 0.0
        y = y0 + height + yoffs
        if y >= 1.0:
            y = 1.0
        ax.text(x, y, l, transform=fig.transFigure, ha='left', va='top', **fkwargs)


def tag_params(xoffs=None, yoffs=None, label=None, minor_label=None, font=None):
    """ Set default tag appearance.

    Only parameters that are not `None` are updated.

    Parameters
    ----------
    xoffs: float or 'auto'
        X-coordinate of tag relative to origin of axis in multiples of the width
        of a character (simply 60% of the current font size).
        If 'auto', set it to the distance of the right-most axis to the left figure border,
        or to a previously computed value from that figure.
        Sets ptParam `figure.tags.xoffs`.
    yoffs: float or 'auto'
        Y-coordinate of tag relative to top end of left yaxis in multiples
        of the height of a character (the current font size).
        If 'auto', set it to the distance of the top-most axis to the top figure border,
        or to a previously computed value from that figure.
        Sets ptParam `figure.tags.yoffs`.
    label: string
        Label used to tag axes. Sets ptParam `figure.tags.label`.
        See `tag()` for details.
    minor_label: string
        Label used to tag minor axes. Sets ptParam `figure.tags.minorlabel`.
        See `tag()` for details.
    font: dict
        Dictionary with font settings for tags
        (e.g. fontsize, fontfamiliy, fontstyle, fontweight, bbox, ...).
        Updates ptParam `figure.tags.font`.
    """
    if hasattr(mpl, 'ptParams'):
        if xoffs is not None:
            mpl.ptParams['figure.tags.xoffs'] = xoffs
        if yoffs is not None:
            mpl.ptParams['figure.tags.yoffs'] = yoffs
        if label is not None:
            mpl.ptParams['figure.tags.label'] = label
        if minor_label is not None:
            mpl.ptParams['figure.tags.minorlabel'] = minor_label
        if font is not None:
            mpl.ptParams['figure.tags.font'].update(**font)


def install_tag():
    """ Install functions of the tag module in matplotlib.

    See also
    --------
    uninstall_tag()
    """
    if not hasattr(mpl.figure.Figure, 'tag'):
        mpl.figure.Figure.tag = tag
    # add tag parameter to rc configuration:
    if not hasattr(mpl, 'ptParams'):
        mpl.ptParams = {}
    if 'figure.tags.xoffs' not in mpl.ptParams:
        mpl.ptParams.update({'figure.tags.xoffs': 'auto',
                             'figure.tags.yoffs': 'auto',
                             'figure.tags.label': '%A',
                             'figure.tags.minorlabel': '%A%mi',
                             'figure.tags.font': dict(fontsize='x-large')})


def uninstall_tag():
    """ Uninstall all code of the tag module from matplotlib.

    See also
    --------
    install_tag()
    """
    if hasattr(mpl.figure.Figure, 'tag'):
        delattr(mpl.figure.Figure, 'tag')
    if hasattr(mpl, 'ptParams'):
        del mpl.ptParams['figure.tags.xoffs']
        del mpl.ptParams['figure.tags.yoffs']
        del mpl.ptParams['figure.tags.label']
        del mpl.ptParams['figure.tags.minorlabel']
        del mpl.ptParams['figure.tags.font']


install_tag()


def demo():
    """ Run a demonstration of the tag module.
    """

    def afigure():
        fig = plt.figure()
        fig.suptitle('plottools.tag')
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

    tag_params(xoffs='auto', yoffs='auto', label='%A', font=dict(fontweight='bold'))
    
    fig, axs = afigure()
    axs[0].text(0.5, 0.5, 'fig.tag()', transform=axs[0].transAxes, ha='center')
    axs[0].text(0.0, 0.0, 'X', transform=fig.transFigure, ha='left', va='bottom')
    fig.tag(xoffs=-5, yoffs=3)

    fig, axs = afigure()
    axs[0].text(0.5, 0.7, 'fig,tag([ax1])',
                transform=axs[0].transAxes, ha='center')
    axs[0].text(0.5, 0.5, "fig,tag([ax2, ax4], 'auto', 2, '%a:', major_index=0,\n fontweight='normal', fontstyle='italic')", transform=axs[0].transAxes, ha='center')
    fig.tag([axs[0]], xoffs=-5, yoffs=3)
    fig.tag([axs[1], axs[3]], 'auto', 2, '%a:', major_index=0,
            fontweight='normal', fontstyle='italic')

    fig, axs = afigure()
    axs[0].text(0.05, 0.7, "fig.tag([0, [1, 2, 3]],\n labels='Panel %A)',\n minor_label='%A.%mi)')",
                transform=axs[0].transAxes)
    fig.tag([0, [1, 2, 3]], xoffs=0, yoffs=3, labels='Panel %A)', minor_label='%A.%mi)')
    plt.show()
        

if __name__ == "__main__":
    demo()
