"""
# Arrows

The following functions are also provided as mpl.axes.Axes member functions:
- `harrow()`: 
- `varrow()`: 
"""

import inspect
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle


def harrow(ax, x, y, dx, heads='right', text=None, va='bottom', dist=3.0,
           style='>', shrink=0, lw=1, color='k',
           head_width=15, head_length=15, **kwargs):
    """
    heads: string
        left, right, both, none
    head_width: float
        In points, same unit as linewidth
    """
    if heads == 'none':
        style = '>'
    if style == '>>':
        arrowstyle = ArrowStyle.Fancy(head_length=0.07*head_length,
                                      head_width=0.07*head_width, tail_width=0.01)
        if heads in ['right', 'both']:
            ax.annotate('', (x+dx, y), (x, y),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=lw, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False))
        if heads in ['left', 'both']:
            ax.annotate('', (x, y), (x+dx, y),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=lw, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False))
    else:
        scale = head_width*2.0
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
        ec = color
        lww = lw
        if style == '|>':
            ec = 'none'
            lww = 0
        ax.annotate('', (x+dx, y), (x, y),
                    arrowprops=dict(arrowstyle=arrowstyle, edgecolor=ec, facecolor=color,
                                    linewidth=lww, shrinkA=shrink, shrinkB=shrink,
                                    mutation_scale=scale, clip_on=False))
    if style in ['|>', '>>']:
        pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))
        xmin, xmax = ax.get_xlim()
        dxu = np.abs(xmax - xmin)/pixelx
        ddx = 0.5*head_length*dxu
        ddxr = ddx if heads in ['right', 'both'] else 0
        ddxl = ddx if heads in ['left', 'both'] else 0
        if dx < 0:
            ddxl = -ddxl
            ddxr = -ddxr
        ax.plot([x+ddxl, x+dx-ddxr], [y, y], '-', lw=lw, color=color, solid_capstyle='butt')
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
           style='>', shrink=0, lw=1, color='k',
           head_width=15, head_length=15, **kwargs):
    """
    """
    if style == '>>':
        arrowstyle = ArrowStyle.Fancy(head_length=0.07*head_length,
                                      head_width=0.07*head_width, tail_width=0.01)
        if heads in ['right', 'both']:
            ax.annotate('', (x, y+dy), (x, y),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=0, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False))
        if heads in ['left', 'both']:
            ax.annotate('', (x, y), (x, y+dy),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=0, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False))
    else:
        scale = head_width*2.0
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
        ec = color
        lww = lw
        if style == '|>':
            ec = 'none'
            lww = 0
        ax.annotate('', (x, y+dy), (x, y),
                    arrowprops=dict(arrowstyle=arrowstyle, edgecolor=ec, facecolor=color,
                                    linewidth=lww, shrinkA=shrink, shrinkB=shrink,
                                    mutation_scale=scale, clip_on=False))
    if style in ['|>', '>>']:
        pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))
        ymin, ymax = ax.get_ylim()
        dyu = np.abs(ymax - ymin)/pixely
        ddy = 0.5*head_length*dyu
        ddyr = ddy if heads in ['right', 'both'] else 0
        ddyl = ddy if heads in ['left', 'both'] else 0
        if dy < 0:
            ddyl = -ddyl
            ddyr = -ddyr
        ax.plot([x, x], [y+ddyl, y+dy-ddyr], '-', lw=lw, color=color, solid_capstyle='butt')
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


def arrow_style(name, dist=3.0, style='>', shrink=0, lw=1, color='k',
                head_width=15, head_length=15, namespace=None):
    """ Generate a single arrow style.

    Parameters
    ----------
    name: string
        The name of the arrow style, the prefix 'as' is prepended.
    color: any matplotlib color
        The color of the arrow. 
    namespace: dict
        Namespace to which the generated line style is added.
        If None add line styles to the global namespace of the caller.
    """
    if namespace is None:
        frame = inspect.currentframe()
        namespace = frame.f_back.f_globals
    if 'ahvs' not in namespace:
        namespace['ahvs'] = {}
    an = 'as' + name 
    namespace[an] = dict(dist=dist, style=style, shrink=shrink, lw=lw, color=color,
                         head_width=head_width, head_length=head_length)
    namespace['ahvs'].update({name: namespace[an]})


# make functions available as member variables:
mpl.axes.Axes.harrow = harrow
mpl.axes.Axes.varrow = varrow


def demo():
    """ Run a demonstration of the arrow module.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0.0, 2.0)
    for y in [1.1, 1.3, 1.5, 1.7, 1.9]:
        ax.plot([0.2, 1.8], [y, y], '-c', lw=15, solid_capstyle='butt')
    ax.harrow(0.2, 1.9, 1.6, 'right', 'these', lw=1)
    ax.harrow(0.2, 1.7, 1.6, 'both', 'are', style='|>', lw=1)
    ax.harrow(0.2, 1.5, 1.6, 'left', 'all', style='>>', lw=2)
    ax.harrow(0.2, 1.3, 1.6, 'both', 'arrows', style='|', va='top', lw=2)
    ax.harrow(0.2, 1.1, 1.6, 'both', 'fancy', style='>>', va='top', lw=2)
    for x in [0.2, 0.5, 0.8, 1.1, 1.4]:
        ax.plot([x, x], [0.1, 0.8], '-c', lw=15, solid_capstyle='butt')
    ax.varrow(0.2, 0.1, 0.7, 'right', 'these', lw=4)
    ax.varrow(0.5, 0.1, 0.7, 'both', 'are', style='|>', lw=4)
    ax.varrow(0.8, 0.1, 0.7, 'left', 'all', ha='left', style='>>', lw=2)
    ax.varrow(1.1, 0.1, 0.7, 'both', 'arrows', style='|', lw=4, rotation=90)
    ax.varrow(1.4, 0.1, 0.7, 'both', 'fancy', style='>>', lw=2, rotation=90)
    x = 1.7
    ax.plot([x, x], [0.1, 0.8], '-c', lw=25, solid_capstyle='butt')
    ax.varrow(x, 0.1, 0.7, 'both', 'big fancy', style='>>', lw=5, rotation=90,
              head_width=25, head_length=35)
    plt.show()


if __name__ == "__main__":
    demo()


