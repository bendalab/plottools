"""
# Arrows

The following functions are provided as mpl.axes.Axes member functions:
- `harrow()`: draw a horizontal arrow with annotation on the arrow. 
- `varrow()`: draw a vertical arrow with annotation on the arrow. 
- `point_to()`: text with arrow pointing to a point.

Setting and plotting arrow styles:
- `arrow_style()`: generate an arrow style.
- `plot_arrowstyles()`: plot names and arrows of all available arrow styles.
"""

import __main__
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle


def harrow(ax, x, y, dx, heads='right', text=None, va='bottom', dist=3.0,
           style='>', shrink=0, lw=1, color='k',
           head_width=15, head_length=15, **kwargs):
    """ Draw a horizontal arrow with annotation on the arrow.
           
    Parameters
    ----------
    ax: matplotlib axes
        Axes on which to draw the arrow.
    x: float
        X-coordinate of starting point of arrow in data coordinates.
    y: float
        Y-coordinate of starting point of arrow in data coordinates.
    dx: float
        Length of arrow in data x-coordinates.
    heads: string
        One of 'left', '<', 'right', '>', 'both', '<>', 'none', or '',
        Specifies whether to draw the arrow head at the starting point ('left', '<'),
        at the end ('right', '>'), on both ends ('both', '<>'), or none ('none', '').
    text: string
        Text for annotating the arrow. A formatting instruction within text (e.g. 'd=%.1fm')
        is replaced by `dx`.
    va: string
        Place text annotation above ('top') or below ('bottom') the arrow.
    dist: float
        Distance of text annotation from arrow in points.
    style: string
        Appearance of the arrow head:
        '>': line arrow, '|>': filled arrow, '>>': fancy arrow, '|': bar
    shrink: float
        Shrink arrow away from endpoints.
    lw: float
        Linewidth of line in points.
    color: matplotlib color
        Color of line and arrow.
    head_width: float
        Width of arrow head in points.
    head_length: float
        Length of arrow head in points.
    **kwargs: key-word arguments
        Formatting of the annotation text, passed on to text().
    """
    heads_d = {'leftx': 'left', '<x': 'left', 'rightx': 'right', '>x': 'right',
               'bothx': 'both', '<>x': 'both', 'nonex': 'none', 'x': 'none'}
    heads = heads_d[heads+'x']
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
                                        clip_on=False), annotation_clip=False)
        if heads in ['left', 'both']:
            ax.annotate('', (x, y), (x+dx, y),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=lw, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False), annotation_clip=False)
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
                                    mutation_scale=scale, clip_on=False), annotation_clip=False)
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
        ax.plot([x+ddxl, x+dx-ddxr], [y, y], '-', lw=lw, color=color,
                solid_capstyle='butt', clip_on=False)
    if text:
        if '%' in text and text[-1] != '%':
            text = text % dx
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
    """ Draw a vertical arrow with annotation on the arrow.
           
    Parameters
    ----------
    ax: matplotlib axes
        Axes on which to draw the arrow.
    x: float
        X-coordinate of starting point of arrow in data coordinates.
    y: float
        Y-coordinate of starting point of arrow in data coordinates.
    dx: float
        Length of arrow in data x-coordinates.
    heads: string
        One of 'left', '<', 'right', '>', 'both', '<>', 'none', or '',
        Specifies whether to draw the arrow head at the starting point ('left', '<'),
        at the end ('right', '>'), on both ends ('both', '<>'), or none ('none', '').
    text: string
        Text for annotating the arrow. A formatting instruction within text (e.g. 'd=%.1fm')
        is replaced by `dy`.
    ha: string
        Place text annotation to the left ('left') or right ('right') of the arrow.
    dist: float
        Distance of text annotation from arrow in points.
    style: string
        Appearance of the arrow head:
        '>': line arrow, '|>': filled arrow, '>>': fancy arrow, '|': bar
    shrink: float
        Shrink arrow away from endpoints.
    lw: float
        Linewidth of line in points.
    color: matplotlib color
        Color of line and arrow.
    head_width: float
        Width of arrow head in points.
    head_length: float
        Length of arrow head in points.
    **kwargs: key-word arguments
        Formatting of the annotation text, passed on to text().
    """
    heads_d = {'leftx': 'left', '<x': 'left', 'rightx': 'right', '>x': 'right',
               'bothx': 'both', '<>x': 'both', 'nonex': 'none', 'x': 'none'}
    heads = heads_d[heads+'x']
    if heads == 'none':
        style = '>'
    if style == '>>':
        arrowstyle = ArrowStyle.Fancy(head_length=0.07*head_length,
                                      head_width=0.07*head_width, tail_width=0.01)
        if heads in ['right', 'both']:
            ax.annotate('', (x, y+dy), (x, y),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=0, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False), annotation_clip=False)
        if heads in ['left', 'both']:
            ax.annotate('', (x, y), (x, y+dy),
                        arrowprops=dict(arrowstyle=arrowstyle,
                                        edgecolor='none', facecolor=color,
                                        linewidth=0, shrinkA=shrink, shrinkB=shrink,
                                        clip_on=False), annotation_clip=False)
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
                                    mutation_scale=scale, clip_on=False), annotation_clip=False)
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
        ax.plot([x, x], [y+ddyl, y+dy-ddyr], '-', lw=lw, color=color,
                solid_capstyle='butt', clip_on=False)
    if text:
        if '%' in text and text[-1] != '%':
            text = text % dy
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


def point_to(ax, text, xyfrom, xyto, radius=0.2, relpos=(1, 0.5),
             style='>', shrink=0, lw=1, color='k',
             head_width=15, head_length=15, **kwargs):
    """ Text with arrow pointing to a point.
           
    Parameters
    ----------
    ax: matplotlib axes
        Axes on which to draw the text and arrow.
    text: string
        Text placed at `xyfrom`.
    xyfrom: tuple of floats
        X- and y-coordinates of text position in data coordinates.
    xyto: tuple of floats
        X- and y-coordinates of arrow point in data coordinates.
    radius: float
        Radius of arrow line. Negative curves to the right. Relative to arrow length.
    relpos: tuple of floats
        X- and y-coordinate of starting point of arrow on text box. Between 0 and 1.
    style: string
        Appearance of the arrow head:
        '>': line arrow, '|>': filled arrow, '>>': fancy arrow
    shrink: float
        Shrink arrow away from endpoints.
    lw: float
        Linewidth of line in points.
    color: matplotlib color
        Color of line and arrow.
    head_width: float
        Width of arrow head in points.
    head_length: float
        Length of arrow head in points.
    **kwargs: key-word arguments
        Formatting of the text, passed on to annotate().
    """
    if style == '>>':
        arrowstyle = ArrowStyle.Fancy(head_length=0.09*head_length,
                                      head_width=0.09*head_width, tail_width=0.14*lw)
        arrowprops = dict(arrowstyle=arrowstyle, edgecolor='none', linewidth=0)
    else:
        scale = head_width*2.0
        if style == '|':
            scale /= 4.0
        arrowprops = dict(arrowstyle='-' + style, edgecolor=color,
                          mutation_scale=scale, linewidth=lw)
    arrowprops.update(dict(facecolor=color, relpos=relpos,
                           shrinkA=shrink, shrinkB=shrink, clip_on=False))
    arrowprops.update(dict(connectionstyle='arc3,rad=%g' % radius))
    if 'dist' in kwargs:
        kwargs.pop('dist')
    ax.annotate(text, xy=xyto, xytext=xyfrom, arrowprops=arrowprops,
                annotation_clip=False, **kwargs)


def arrow_style(name, dist=3.0, style='>', shrink=0, lw=1, color='k',
                head_width=15, head_length=15, namespace=None, **kwargs):
    """ Generate an arrow style.

    Add dictionary with name 'as'+name to namespace and to ars

    Parameters
    ----------
    name: string
        The name of the arrow style, the prefix 'as' is prepended.
    dist: float
        Distance of text annotation from arrow in points (for harrow() and varrow()).
    style: string
        Appearance of the arrow head:
        '>': line arrow, '|>': filled arrow, '>>': fancy arrow, '|': bar
    shrink: float
        Shrink arrow away from endpoints.
    lw: float
        Linewidth of line in points.
    color: matplotlib color
        Color of line and arrow.
    head_width: float
        Width of arrow head in points.
    head_length: float
        Length of arrow head in points.
    **kwargs: key-word arguments
        Formatting of the annotation text, passed on to text().
    namespace: dict or None
        Namespace to which the generated arrow style is added.
        If None add arrow style to the __main__ module.
    """
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'ars'):
        setattr(namespace, 'ars', {})
    ad = dict(dist=dist, style=style, shrink=shrink, lw=lw, color=color,
              head_width=head_width, head_length=head_length, **kwargs)
    setattr(namespace, 'as' + name, ad)
    getattr(namespace, 'ars')[name] = ad


def plot_arrowstyles(ax):
    """ Plot names and arrows of all available arrow styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the arrow styles.
    """
    namespace = __main__
    for k, name in enumerate(namespace.ars):
        ax.harrow(0.5, 0.5*k+0.5, 1.0, 'both', 'as'+name, **namespace.ars[name])
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0.0, 0.5*k+1)
    ax.set_title('arrow styles')
        

# make functions available as member variables:
mpl.axes.Axes.harrow = harrow
mpl.axes.Axes.varrow = varrow
mpl.axes.Axes.point_to = point_to


def demo():
    """ Run a demonstration of the arrow module.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0.0, 3.0)
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
    ax.varrow(0.2, 0.1, 0.7, '>', 'these', lw=4)
    ax.varrow(0.5, 0.1, 0.7, '<>', 'are', style='|>', lw=4)
    ax.varrow(0.8, 0.1, 0.7, '<', 'all', ha='left', style='>>', lw=2)
    ax.varrow(1.1, 0.1, 0.7, 'both', 'arrows', style='|', lw=4, rotation=90)
    ax.varrow(1.4, 0.1, 0.7, 'both', 'fancy', style='>>', lw=2, rotation='vertical')
    x = 1.7
    ax.plot([x, x], [0.1, 0.8], '-c', lw=25, solid_capstyle='butt')
    ax.varrow(x, 0.1, 0.7, 'both', 'big fancy', style='>>', lw=5, rotation=90,
              head_width=25, head_length=35)
    ax.point_to('point_to', (2.0, 1.9), (2.8, 1.7), -0.3, (1, 0.5))
    ax.point_to('point_to', (2.0, 1.6), (2.8, 1.4), -0.3, (1, 0.5), style='|>')
    ax.point_to('point_to', (2.0, 1.3), (2.8, 1.1), -0.3, (1, 0.5), style='>>')
    ax.point_to('point_to', (2.0, 1.0), (2.8, 0.8), -0.3, (1, 0.5), style='>', lw=4)
    ax.point_to('point_to', (2.0, 0.7), (2.8, 0.5), -0.3, (1, 0.5), style='|>', lw=4)
    ax.point_to('point_to', (2.0, 0.4), (2.8, 0.2), -0.3, (1, 0.5), style='>>', lw=4)
    plt.show()


if __name__ == "__main__":
    demo()


