"""
# Arrows

The following functions are also provided as mpl.axes.Axes member functions:
- `harrow()`: 
- `varrow()`: 
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def harrow(ax, x, y, dx, heads='right', text=None, va='bottom', dist=3.0,
           style='>', shrink=0, lw=1, color='k', scale=20.0, **kwargs):
    """
    heads: string
        left, right, both, none
    """
    if style == '|':
        scale /= 4.0
    bstyle = style[::-1]
    if bstyle[0] == '>':
        bstyle = '<' + bstyle[1:]
    arrowstyle = '-'
    if heads == 'right':
        arrowstyle = '-' + style
    elif heads == 'left':
        arrowstyle = bstyle + '-'
    elif heads == 'both':
        arrowstyle = bstyle + '-' + style
    ax.annotate('', (x+dx, y), (x, y),
                arrowprops=dict(arrowstyle=arrowstyle, edgecolor=color, facecolor=color,
                                linewidth=lw, shrinkA=shrink, shrinkB=shrink,
                                mutation_scale=scale, clip_on=False))
    if text:
        # ax dimensions:
        ax.autoscale(False)
        pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))
        ymin, ymax = ax.get_ylim()
        dyu = np.abs(ymax - ymin)/pixely
        dy = 0.5*lw + dist
        if va == 'top':
            ax.text(x+0.5*dx, y+dy*dyu, text, ha='center', va='bottom',
                    clip_on=False, **kwargs)
        else:
            ax.text(x+0.5*dx, y-dy*dyu, text, ha='center', va='top',
                    clip_on=False, **kwargs)


def varrow(ax, x, y, dy, heads='right', text=None, ha='right', dist=3.0,
           style='>', shrink=0, lw=1, color='k', scale=20.0, **kwargs):
    """
    """
    if style == '|':
        scale /= 4.0
    bstyle = style[::-1]
    if bstyle[0] == '>':
        bstyle = '<' + bstyle[1:]
    arrowstyle = '-'
    if heads == 'right':
        arrowstyle = '-' + style
    elif heads == 'left':
        arrowstyle = bstyle + '-'
    elif heads == 'both':
        arrowstyle = bstyle + '-' + style
    ax.annotate('', (x, y+dy), (x, y),
                arrowprops=dict(arrowstyle=arrowstyle, edgecolor=color, facecolor=color,
                                linewidth=lw, shrinkA=shrink, shrinkB=shrink,
                                mutation_scale=scale, clip_on=False))
    if text:
        # ax dimensions:
        ax.autoscale(False)
        pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))
        xmin, xmax = ax.get_xlim()
        dxu = np.abs(xmax - xmin)/pixelx
        dx = 0.5*lw + dist
        if ha == 'right':
            ax.text(x+dx*dxu, y+0.5*dy, text, ha='left', va='center',
                    clip_on=False, **kwargs)
        else:
            ax.text(x-dx*dxu, y+0.5*dy, text, ha='right', va='center',
                    clip_on=False, **kwargs)



# make functions available as member variables:
mpl.axes.Axes.harrow = harrow
mpl.axes.Axes.varrow = varrow


def demo():
    """ Run a demonstration of the arrow module.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0.0, 2.0)
    ax.harrow(0.2, 1.9, 1.6, 'right', 'these', lw=4)
    ax.harrow(0.2, 1.6, 1.6, 'both', 'are', lw=2)
    ax.harrow(0.2, 1.3, 1.6, 'left', 'all', style='|>', lw=1)
    ax.harrow(0.2, 1.0, 1.6, 'both', 'arrows', style='|', va='top', lw=2)
    ax.varrow(0.2, 0.1, 0.7, 'right', 'these', lw=4)
    ax.varrow(0.5, 0.1, 0.7, 'both', 'are', lw=2)
    ax.varrow(0.8, 0.1, 0.7, 'left', 'all', ha='left', style='|>', lw=1)
    ax.varrow(1.1, 0.1, 0.7, 'both', 'arrows', lw=2, style='|', rotation=90)
    plt.show()


if __name__ == "__main__":
    demo()


