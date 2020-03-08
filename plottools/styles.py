"""
# Styles

Layout settings and plot styles.

- `screen_style()`: 
- `paper_style()`: 

Displaying line and marker styles:
- `plot_linestyles()`: plot names and lines of all available line styles.
- `plot_pointstyles()`: plot names and lines of all available point styles.
- `plot_linepointstyles()`: plot names and lines of all available linepoint styles.

Line and marker styles.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .colors import colors_vivid, colors_muted, lighter, darker, gradient
from .figure import install_figure
from .spines import show_spines, set_spines_outward, set_spines_bounds, set_default_spines
from .ticks import set_xticks_delta, set_yticks_delta, set_xticks_none, set_yticks_none
from .ticks import set_xticks_format, set_yticks_format, set_xticks_blank, set_yticks_blank
from .labels import set_label_format, install_align_labels
from .insets import inset, zoomed_inset
from .labelaxes import label_axes
from .scalebars import xscalebar, yscalebar, scalebars
from .significance import significance_bar


def make_linestyles(prefix, name, suffix, colors, linedict, namespace):
    if 'style_names' not in namespace:
        namespace['style_names'] = []
    ln = prefix + suffix 
    if ln not in namespace:
        namespace[ln] = {}
    for k, c in enumerate(colors):
        n = name[k] if isinstance(name, list) else name % (k+1)
        if n not in namespace['style_names']:
            namespace['style_names'].append(n)
        sn = prefix + n + suffix
        namespace[sn] = dict({'color': c}, **linedict)
        namespace[ln].update({n: namespace[sn]})


def make_pointstyles(prefix, name, suffix, colors, markers, mec, pointdict, namespace):
    if 'style_names' not in namespace:
        namespace['style_names'] = []
    ln = prefix + suffix 
    if ln not in namespace:
        namespace[ln] = {}
    if not isinstance(markers, list):
        markers = len(colors)*[markers]
    for k, (c, m) in enumerate(zip(colors, markers)):
        n = name[k] if isinstance(name, list) else name % (k+1)
        if n not in namespace['style_names']:
            namespace['style_names'].append(n)
        sn = prefix + n + suffix
        namespace[sn] = dict({'color': c, 'marker': m[0], 'markeredgecolor': lighter(c, mec)},
                             **pointdict)
        namespace[sn].update({'markersize': m[1]*namespace[sn]['markersize']})
        namespace[ln].update({n: namespace[sn]})


def make_fillstyles(prefix, name, suffix, colors, ec, filldict, namespace):
    if 'style_names' not in namespace:
        namespace['style_names'] = []
    ln = prefix + suffix 
    if ln not in namespace:
        namespace[ln] = {}
    for k, c in enumerate(colors):
        n = name[k] if isinstance(name, list) else name % (k+1)
        if n not in namespace['style_names']:
            namespace['style_names'].append(n)
        sn = prefix + n + suffix
        namespace[sn] = dict({'facecolor': c, 'edgecolor': lighter(c, ec)}, **filldict)
        namespace[ln].update({n: namespace[sn]})


def plot_styles(colors, lwthick=2.0, lwthin=1.0, lwspines=1.0,
                markerlarge=7.5, markersmall=5.5, mec=0.5, mew=1.0,
                fillalpha=0.4, namespace=globals()):
    """
    Parameters
    ----------
    mec: float
        Edge color for markers and fill. A factor between 0 and 2 passed together
        with the facecolor to lighter(). I.e. 0 results in a white edge,
        1 in an edge of the color of the face color, and 2 in a black edge color.
    """
    # line (ls), point (ps), and fill styles (fs).

    # Each style is derived from a main color as indicated by the capital letter.
    # Substyles, indicated by the number following the capital letter, have
    # the same style and similar hues.

    # Line styles come in two variants:
    # - plain style with a thick/solid line (e.g. lsA1), and
    # - minor style with a thinner or dashed line (e.g. lsA1m).

    # Point (marker) styles come in four variants:
    # - plain style with large solid markers (e.g. psB1),
    # - plain style with large circular markers (e.g. psB1c), and
    # - minor style with smaller (circular) markers (e.g. psB1m).

    # Linepoint styles (markers connected by lines) come in two variants:
    # - plain style with large solid markers (e.g. lpsA2),
    # - plain style with large circular markers (e.g. lpsA2c),
    # - minor style with smaller (circular) markers (e.g. lpsA2m).

    # Fill styles come in three variants:
    # - plain (e.g. fsA3) for a solid fill color and an edge color,
    # - solid (e.g. fsA3s) for a solid fill color without edge color, and
    # - alpha (e.g. fsA3a) for a transparent fill color.
    mainline = {'linestyle': '-', 'linewidth': lwthick}
    minorline = {'linestyle': '-', 'linewidth': lwthin}
    largemarker = {'markersize': markerlarge, 'markeredgewidth': mew, 'linestyle': 'none'}
    smallmarker = {'markersize': markersmall, 'markeredgewidth': mew, 'linestyle': 'none'}
    largelinepoints = {'linestyle': '-', 'linewidth': lwthick, 'markersize': markerlarge,
                       'markeredgewidth': mew}
    smalllinepoints = {'linestyle': '-', 'linewidth': lwthin, 'markersize': markersmall,
                       'markeredgewidth': mew}
    mainfill = {'linewidth': mew}
    solidfill = {'edgecolor': 'none'}
    alphafill = {'edgecolor': 'none', 'alpha': fillalpha}

    # color groups:
    colorsA = [colors['red'], colors['orange'], colors['yellow']]
    colorsB = [colors['blue'], colors['purple'], colors['magenta'], colors['lightblue']]
    colorsC = [colors['lightgreen'], colors['green'], colors['darkgreen'], colors['cyan']]
    colorsS = [colors['blue'], colors['pink']]

    # marker groups:
    markersA = [('o', 1.0), ('p', 1.1), ('h', 1.1)]
    markersB = [((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25)]
    markersC = [('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4)]
    markersS = [('o', 1.0), ('o', 1.0)]

    # helper lines:
    namespace['lsSpine'] = {'color': colors['black'], 'linestyle': '-', 'linewidth': lwspines, 'clip_on': False}
    namespace['lsGrid'] = {'color': colors['gray'], 'linestyle': '--', 'linewidth': lwthin}
    namespace['lsMarker'] = {'color': colors['black'], 'linestyle': '-', 'linewidth': lwthick}

    # line styles:
    make_linestyles('ls', 'A%d', '', colorsA, mainline, namespace)
    make_linestyles('ls', 'B%d', '', colorsB, mainline, namespace)
    make_linestyles('ls', 'C%d', '', colorsC, mainline, namespace)
    make_linestyles('ls', ['Male', 'Female'], '', colorsS, mainline, namespace)

    # minor line styles:
    make_linestyles('ls', 'A%d', 'm', colorsA, minorline, namespace)
    make_linestyles('ls', 'B%d', 'm', colorsB, minorline, namespace)
    make_linestyles('ls', 'C%d', 'm', colorsC, minorline, namespace)
    make_linestyles('ls', ['Male', 'Female'], 'm', colorsS, minorline, namespace)

    # point styles:
    make_pointstyles('ps', 'A%d', '', colorsA, markersA, mec, largemarker, namespace)
    make_pointstyles('ps', 'B%d', '', colorsB, markersB, mec, largemarker, namespace)
    make_pointstyles('ps', 'C%d', '', colorsC, markersC, mec, largemarker, namespace)
    make_pointstyles('ps', ['Male', 'Female'], '', colorsS, markersS, mec, largemarker, namespace)

    # circular point styles:
    make_pointstyles('ps', 'A%d', 'c', colorsA, ('o', 1.0), mec, largemarker, namespace)
    make_pointstyles('ps', 'B%d', 'c', colorsB, ('o', 1.0), mec, largemarker, namespace)
    make_pointstyles('ps', 'C%d', 'c', colorsC, ('o', 1.0), mec, largemarker, namespace)
    make_pointstyles('ps', ['Male', 'Female'], 'c', colorsS, ('o', 1.0), mec, largemarker, namespace)

    # minor point styles:
    make_pointstyles('ps', 'A%d', 'm', colorsA, ('o', 1.0), mec, smallmarker, namespace)
    make_pointstyles('ps', 'B%d', 'm', colorsB, ('o', 1.0), mec, smallmarker, namespace)
    make_pointstyles('ps', 'C%d', 'm', colorsC, ('o', 1.0), mec, smallmarker, namespace)
    make_pointstyles('ps', ['Male', 'Female'], 'm', colorsS, ('o', 1.0), mec, smallmarker, namespace)

    # line point styles:
    make_pointstyles('lps', 'A%d', '', colorsA, markersA, mec, largelinepoints, namespace)
    make_pointstyles('lps', 'B%d', '', colorsB, markersB, mec, largelinepoints, namespace)
    make_pointstyles('lps', 'C%d', '', colorsC, markersC, mec, largelinepoints, namespace)
    make_pointstyles('lps', ['Male', 'Female'], '', colorsS, markersS, mec, largelinepoints, namespace)

    # circular line point styles:
    make_pointstyles('lps', 'A%d', 'c', colorsA, ('o', 1.0), mec, largelinepoints, namespace)
    make_pointstyles('lps', 'B%d', 'c', colorsB, ('o', 1.0), mec, largelinepoints, namespace)
    make_pointstyles('lps', 'C%d', 'c', colorsC, ('o', 1.0), mec, largelinepoints, namespace)
    make_pointstyles('lps', ['Male', 'Female'], 'c', colorsS, ('o', 1.0), mec, largelinepoints, namespace)

    # minor line point styles:
    make_pointstyles('lps', 'A%d', 'm', colorsA, ('o', 1.0), mec, smalllinepoints, namespace)
    make_pointstyles('lps', 'B%d', 'm', colorsB, ('o', 1.0), mec, smalllinepoints, namespace)
    make_pointstyles('lps', 'C%d', 'm', colorsC, ('o', 1.0), mec, smalllinepoints, namespace)
    make_pointstyles('lps', ['Male', 'Female'], 'm', colorsS, ('o', 1.0), mec, smalllinepoints, namespace)

    # fill styles:
    make_fillstyles('fs', 'A%d', '', colorsA, mec, mainfill, namespace)
    make_fillstyles('fs', 'B%d', '', colorsB, mec, mainfill, namespace)
    make_fillstyles('fs', 'C%d', '', colorsC, mec, mainfill, namespace)
    make_fillstyles('fs', ['Male', 'Female'], '', colorsS, mec, mainfill, namespace)

    # solid fill styles:
    make_fillstyles('fs', 'A%d', 's', colorsA, 0.0, solidfill, namespace)
    make_fillstyles('fs', 'B%d', 's', colorsB, 0.0, solidfill, namespace)
    make_fillstyles('fs', 'C%d', 's', colorsC, 0.0, solidfill, namespace)
    make_fillstyles('fs', ['Male', 'Female'], 's', colorsS, 0.0, solidfill, namespace)

    # transparent fill styles:
    make_fillstyles('fs', 'A%d', 'a', colorsA, 0.0, alphafill, namespace)
    make_fillstyles('fs', 'B%d', 'a', colorsB, 0.0, alphafill, namespace)
    make_fillstyles('fs', 'C%d', 'a', colorsC, 0.0, alphafill, namespace)
    make_fillstyles('fs', ['Male', 'Female'], 'a', colorsS, 0.0, alphafill, namespace)

    # color cycler:
    color_cycle = [colors[c] for c in ['blue', 'red', 'orange', 'lightgreen', 'magenta',
                                       'yellow', 'cyan', 'pink'] if c in colors]
    if 'axes.prop_cycle' in mpl.rcParams:
        from cycler import cycler
        mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle)
    else:
        mpl.rcParams['axes.color_cycle'] = color_cycle


def plot_params(font_size=10.0, font_family='sans-serif',
                label_size='small', label_format='{label} [{unit}]',
                label_xdist=5, label_ydist=10,
                tick_dir='out', tick_size=2.5,
                legend_size='x-small', fig_color='none', axes_color='none',
                spines='lb', spines_offsets={'lrtb': 3}, spines_bounds={'lrtb': 'full'},
                namespace=globals()):
    """ Set default plot parameter.

    Call this function *before* you create any matplotlib figure.

    You most likely want to copy it and adjust it according to your needs.

    Parameters
    ----------
    fontsize: float
        Fontsize for text in points.
    label_format: string
        Defines how an axis label is formatted from a label and an unit.
        See labels.set_label_format() for details.
    spines: string
        Spines to be shown. See spines.show_spines() for details.
    spines_offsets: dict
        Offsets for moving spines outward. See spines.set_spines_outward() for details.
    spines_bounds: dict
        Bounds for the spines. See spines.set_spines_bounds() for details.
    """
    mpl.rcParams['figure.facecolor'] = fig_color
    mpl.rcParams['font.family'] = font_family
    mpl.rcParams['font.size'] = font_size
    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size
    mpl.rcParams['xtick.direction'] = tick_dir
    mpl.rcParams['ytick.direction'] = tick_dir
    mpl.rcParams['xtick.major.size'] = tick_size
    mpl.rcParams['ytick.major.size'] = tick_size
    mpl.rcParams['legend.fontsize'] = legend_size
    mpl.rcParams['grid.color'] = namespace['lsGrid']['color']
    mpl.rcParams['grid.linestyle'] = namespace['lsGrid']['linestyle']
    mpl.rcParams['grid.linewidth'] = namespace['lsGrid']['linewidth']
    mpl.rcParams['axes.facecolor'] = axes_color
    mpl.rcParams['axes.edgecolor'] = namespace['lsSpine']['color']
    mpl.rcParams['axes.linewidth'] = namespace['lsSpine']['linewidth']
    # figsize in centimeter:
    install_figure()
    # define the appearance of axis labels:
    set_label_format(label_format)
    install_align_labels(label_xdist, label_ydist)
    # spines:
    set_default_spines(spines, spines_offsets, spines_bounds)

    
def screen_style(namespace=globals()):
    plot_styles(colors_vivid, lwthick=2.5, lwthin=1.5, lwspines=1.0,
                markerlarge=10.0, markersmall=6.5, mec=0.0, mew=1.5,
                fillalpha=0.4, namespace=namespace)
    plot_params(font_size=10.0, font_family='sans-serif',
                label_size='small', label_format='{label} [{unit}]',
                label_xdist=5, label_ydist=10,
                tick_dir='out', tick_size=4.0, legend_size='x-small',
                fig_color=colors_muted['white'], axes_color='none',
                spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'},
                namespace=namespace)

    
def paper_style(namespace=globals()):
    plot_styles(colors_muted, lwthick=1.7, lwthin=0.8, lwspines=0.8,
                markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                fillalpha=0.4, namespace=namespace)
    plot_params(font_size=10.0, font_family='sans-serif',
                label_size='small', label_format='{label} [{unit}]',
                label_xdist=5, label_ydist=10,
                tick_dir='out', tick_size=2.5, legend_size='x-small',
                fig_color=colors_muted['white'], axes_color='none',
                spines='lb', spines_offsets={'lrtb': 3}, spines_bounds={'lrtb': 'full'},
                namespace=namespace)


def plot_linestyles(ax):
    """ Plot names and lines of all available line styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the line styles.
    """
    for k, name in enumerate(style_names):
        ax.text(k, 0.9, 'ls'+name)
        ax.plot([k, k+3.5], [1.0, 1.8], **ls[name])
        ax.text(k, -0.1, 'ls'+name+'m')
        ax.plot([k, k+3.5], [0.0, 0.8], **lsm[name])
    ax.set_xlim(-0.2, len(style_names)+2.8)
    ax.set_ylim(-0.15, 1.9)
    ax.set_title('line styles')
        

def plot_pointstyles(ax):
    """ Plot names and lines of all available point styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the point styles.
    """
    dy = 0.2
    for k, name in enumerate(reversed(style_names)):
        ax.text(0.1, k, 'ps'+name)
        ax.plot([0.6], [k+dy], **ps[name])
        ax.text(1.1, k, 'ps'+name+'c')
        ax.plot([1.6], [k+dy], **psc[name])
        ax.text(2.1, k, 'ps'+name+'m')
        ax.plot([2.6], [k+dy], **psm[name])
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(-1.0, len(style_names))
    ax.set_title('point styles')
        

def plot_linepointstyles(ax):
    """ Plot names and lines of all available linepoint styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the linepoint styles.
    """
    dy = 0.2
    for k, name in enumerate(reversed(style_names)):
        ax.text(0.1, k-dy, 'lps'+name)
        ax.plot([0.8, 1.1, 1.4], [k, k, k], **lps[name])
        ax.text(2.1, k-dy, 'lps'+name+'c')
        ax.plot([2.8, 3.1, 3.4], [k, k, k], **lpsc[name])
        ax.text(4.1, k-dy, 'lps'+name+'m')
        ax.plot([4.8, 5.1, 5.4], [k, k, k], **lpsm[name])
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(-1.0, len(style_names))
    ax.set_title('linepoint styles')
        

def plot_fillstyles(ax):
    """ Plot names and patches of all available fill styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the fill styles.
    """
    x = np.linspace(0.0, 0.8, 50)
    y0 = np.zeros(len(x))
    y1 = -x*(x-0.6)*0.6/0.3/0.3
    y1[y1<0.0] = 0.0
    y2 = np.zeros(len(x))
    y2[x>0.3] = 0.7
    ax.text(0.0, 2.75, 'plain')
    ax.text(0.0, 1.75, 'solid')
    ax.text(0.0, 0.75, 'alpha')
    for k, name in enumerate(style_names):
        ax.text(k, 1.9, 'fs'+name)
        ax.fill_between(x+k, y0+2, y2+2, **fs[name])
        ax.fill_between(x+k, y0+2, y1+2, **fs[name])
        ax.text(k, 0.9, 'fs'+name+'s')
        ax.fill_between(x+k, y0+1, y2+1, **fss[name])
        ax.fill_between(x+k, y0+1, y1+1, **fss[name])
        ax.text(k, -0.1, 'fs'+name+'a')
        ax.fill_between(x+k, y0+0, y2+0, **fsa[name])
        ax.fill_between(x+k, y0+0, y1+0, **fsa[name])
    ax.set_xlim(-0.2, len(style_names))
    ax.set_ylim(-0.15, 2.9)
    ax.set_title('fill styles')
        

def demo(mode='line'):
    """ Run a demonstration of the plotformat module.

    Parameters
    ----------
    mode: string
        'linestyles': plot the names and lines of all available line styles
        'pointstyles': plot the names and points (markers) of all available point styles
        'linepointstyles': plot the names and lines of all available linepoint styles
        'fillstyles': plot the names and patches of all available fill styles
    """
    fig, ax = plt.subplots()
    if 'linep' in mode:
        plot_linepointstyles(ax)
    elif 'line' in mode:
        plot_linestyles(ax)
    elif 'point' in mode:
        plot_pointstyles(ax)
    elif 'fill' in mode:
        plot_fillstyles(ax)
    else:
        print('unknown option %s!' % mode)
        print('possible options are: line, point, linep(oints), fill')
        return
    plt.show()


if __name__ == "__main__":
    import sys
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    screen_style()
    demo(mode)
