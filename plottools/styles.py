"""
# Styles

Layout settings and plot styles.

- `screen_style()`: 
- `paper_style()`: 

Display line, point and fill styles:
- `plot_linestyles()`: plot names and lines of all available line styles.
- `plot_pointstyles()`: plot names and lines of all available point styles.
- `plot_linepointstyles()`: plot names and lines of all available linepoint styles.
- `plot_fillstyles()`: plot names and patches of all available fill styles.
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


def make_linestyles(prefix, name, suffix, colors, dashes, linedict, namespace):
    """ Generate dictionaries for line styles.

    Add for each color a line style dictionary, add this to the
    dictionary for the styles specified by their suffix and prefix, and
    add its name to the `style_names` list to a namespace.
    
    For example
    ```
    make_linestyles('ls', 'Male', '', [#0000FF], '-', {'linestyle': '-', 'linewidth': 2'}, globals())
    ```
    generates a dictionary named `lsMale` defining a blue solid line,
    adds `Male` to `style_names`, and adds the dictionary to `ls` under the key `Male`.
    Throw the dictionary into a plot() command:
    ```
    plt.plot(x, y, **lsMale)
    ```
    this is the same as:
    ```
    plt.plot(x, y, **ls['Male'])
    ```

    Parameters
    ----------
    prefix: string
        Prefix appended to all line style names.
    name: string or list of strings
        For each color the name of the line style.
        If string, then '%d' is replaced by the index of the color plus one.
    suffix: string
        Sufffix prepended to all line style names.
    colors: list of RGB hex-strings
        For each color in the list a line style is generated.
    dashes: matplot linestyle or list of matplotlib linestyles
        For each color a descriptor of a matplotlib linestyle.
    linedict: dict
        Dictionary with 'linestyle' and 'linewidth' items.
    namespace: dict
        Namespace to which the generated line styles are added.
    """
    if 'style_names' not in namespace:
        namespace['style_names'] = []
    ln = prefix + suffix 
    if ln not in namespace:
        namespace[ln] = {}
    for k, c in enumerate(colors):
        n = name[k] if isinstance(name, list) else name % (k+1)
        if n not in namespace['style_names']:
            namespace['style_names'].append(n)
        ds = dashes[k] if isinstance(dashes, list) else dashes
        sn = prefix + n + suffix
        namespace[sn] = dict({'color': c}, **linedict)
        if ds:
            namespace[sn].update({'linestyle': ds})
        namespace[ln].update({n: namespace[sn]})


def make_pointstyles(prefix, name, suffix, colors, dashes, markers, mec, pointdict, namespace):
    """ Generate dictionaries for point styles.

    Add for each color a point style dictionary, add this to the
    dictionary for the styles specified by their suffix and prefix, and
    add its name to the `style_names` list to a namespace.
    
    For example
    ```
    make_pointstyles('ps', 'Female', '', [#FF0000], '-', ('o', 1.0), 0.5, {'markersize': 8, 'markeredgewidth': 1.0, 'linestyle': 'none'}, globals())
    ```
    generates a dictionary named `psFemale` defining red filled markers with a lighter edge,
    adds `Female` to `style_names`, and adds the dictionary to `ps` under the key `Female`.
    Throw the dictionary into a plot() command:
    ```
    plt.plot(x, y, **psFemale)
    ```
    this is the same as:
    ```
    plt.plot(x, y, **ps['Female'])
    ```

    Parameters
    ----------
    prefix: string
        Prefix appended to all point style names.
    name: string or list of strings
        For each color the name of the point style.
        If string, then '%d' is replaced by the index of the color plus one.
    suffix: string
        Sufffix prepended to all point style names.
    colors: list of RGB hex-strings
        For each color in the list a point style is generated.
    dashes: matplot linestyle or list of matplotlib linestyles
        For each color a descriptor of a matplotlib linestyle.
        Set to 'none' if the points should not be connected.
    markers: tuple or list of tuples
        For each color a marker. The first element of the tuple is the marker symbol,
        the second on is a factor that is used to scale the markeredgewidth in `pointdict`.
    mec: float
        Defines the edge color. It is passed as the lightness argument to lighter()
        using the face color form `colors`. That is 0 results in a white edge color,
        1 in an edge with the same color as the face color, and 2 in a black edge color.
    pointdict: dict
        Dictionary with 'markersize', markeredgewidth', 'linestyle' and 'linewidth' items.
    namespace: dict
        Namespace to which the generated point styles are added.
    """
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
        ds = dashes[k] if isinstance(dashes, list) else dashes
        mk = markers[k] if isinstance(markers, list) else markers
        namespace[sn] = dict({'color': c, 'marker': mk[0], 'markeredgecolor': lighter(c, mec)},
                             **pointdict)
        if ds:
            namespace[sn].update({'linestyle': ds})
        namespace[sn].update({'markersize': mk[1]*namespace[sn]['markersize']})
        namespace[ln].update({n: namespace[sn]})


def make_linepointstyles(prefixes, name, suffix, colors, dashes, markers, mec,
                         linedict, pointdict, namespace):
    """ Generate line styles, point styles, and line point styles.

    Passes the arguments on to make_linestyles() and make_pointstyles(),
    and again to make_pointstyles() with `pointdict` and `linedict` merged.
    See those functions for a detailed description.

    Parameters
    ----------
    prefixes: list of strings
        If the first string is not None, generate line styles using make_linestyles().
        If the second string is not None, generate point styles using make_pointstyles().
        If the third string is not None, generate linepoint styles using make_pointstyles()
        with `pointdict` and `linedict` merged.
    *args:
        All remaining arguments are explained in the make_linestyles() and make_pointstyles()
        functions.
    """
    if prefixes[0]:
        make_linestyles(prefixes[0], name, suffix, colors, dashes, linedict, namespace)
    if prefixes[1]:
        make_pointstyles(prefixes[1], name, suffix, colors, 'none', markers, mec,
                         pointdict, namespace)
    if prefixes[2]:
        linepointdict = {k: v for k, v in pointdict.items()}
        linepointdict.update(linedict)
        make_pointstyles(prefixes[2], name, suffix, colors, dashes, markers, mec,
                         linepointdict, namespace)


def make_fillstyles(prefix, name, suffixes, colors, ec, ew, fillalpha, namespace):
    """ Generate dictionaries for fill styles.

    Add for each color three fill style dictionaries, add these to the
    dictionary for the styles specified by their suffix and prefix, and
    add their names to the `style_names` list to a namespace.
    
    For example
    ```
    make_fillstyles('fs', 'PSD', ['', 's', 'a'], [#00FF00], 2.0, 0.5, 0.4, globals())
    ```
    generates the dictionaries named `fsPSD`, `fsPSDs`, `fsPSDa` defining a green fill color.
    The first, `fsPSD` gets a black edge color with linewidth set to 0.5.
    The second, `fsPSDs` is without edge.
    The third, `fsPSDa` is without edge and has an alpha set to 0.4.
    Further, `PSD` is added to `style_names`, and the three dictionaries are added
    to the `fs`, `fss` and `fsa` dictionaries under the key `PSD`.
    Throw the dictionaries into a fill_between() command:
    ```
    plt.fill_between(x, y0, y1, **fsPSD)
    ```
    or like this for a transparent fill style:
    ```
    plt.plot(x, y, **fsa['PSD'])
    ```

    Parameters
    ----------
    prefix: string
        Prefix appended to all fill style names.
    name: string or list of strings
        For each color the name of the fill style.
        If string, then '%d' is replaced by the index of the color plus one.
    suffixes: list of strings or None
        Sufffixes prepended to all fill style names.  The first is for a
        fill style with edge color, the second for a solid fill style
        without edge, and the third for a transparent fill style without
        edge. If None the corresponding style is not generated.
    colors: list of RGB hex-strings
        For each color in the list a fill style is generated.
    ec: float
        Defines the edge color for the first fill style.
        It is passed as the lightness argument to lighter()
        using the face color form `colors`. That is 0 results in a white edge color,
        1 in an edge with the same color as the face color, and 2 in a black edge color.
    ew: float
        Line width for the edge color of the first fill style.
    fillalpha: float
        Alpha value for the transparent fill style.
    namespace: dict
        Namespace to which the generated fill styles are added.
    """
    if 'style_names' not in namespace:
        namespace['style_names'] = []
    for suffix in suffixes:
        if suffix is not None:
            ln = prefix + suffix 
            if ln not in namespace:
                namespace[ln] = {}
    for k, c in enumerate(colors):
        n = name[k] if isinstance(name, list) else name % (k+1)
        if n not in namespace['style_names']:
            namespace['style_names'].append(n)
        for k, suffix in enumerate(suffixes):
            if suffix is not None:
                sn = prefix + n + suffix
                filldict = {'facecolor': c}
                if k == 0:   # fill with edge:
                    filldict.update({'edgecolor': lighter(c, ec), 'linewidth': ew})
                elif k == 1: # fill without edge:
                    filldict.update({'edgecolor': 'none'})
                elif k == 2: # fill without edge, with alpha:
                    filldict.update({'edgecolor': 'none', 'alpha': fillalpha})
                namespace[sn] = filldict
                namespace[prefix + suffix].update({n: namespace[sn]})

    
def plot_styles(names, colors, dashes, markers, lwthick=2.0, lwthin=1.0,
                markerlarge=7.5, markersmall=5.5, mec=0.5, mew=1.0,
                fillalpha=0.4, namespace=globals()):
    """ Generate plot styles from names, dashes, colors, and markers.
                
    Parameters
    ----------
    mec: float
        Edge color for markers and fill. A factor between 0 and 2 passed together
        with the facecolor to lighter(). I.e. 0 results in a white edge,
        1 in an edge of the color of the face color, and 2 in a black edge.
    """    
    mainline = {'linestyle': '-', 'linewidth': lwthick}
    minorline = {'linestyle': '-', 'linewidth': lwthin}
    largemarker = {'markersize': markerlarge, 'markeredgewidth': mew, 'linestyle': 'none'}
    smallmarker = {'markersize': markersmall, 'markeredgewidth': mew, 'linestyle': 'none'}

    # line, point and linepoint styles:
    make_linepointstyles(['ls', 'ps', 'lps'], names, '', colors, dashes, markers, mec,
                         mainline, largemarker, namespace)
    # circular point and linepoint styles:
    make_linepointstyles(['', 'ps', 'lps'], names, 'c', colors, dashes, ('o', 1.0), mec,
                         mainline, largemarker, namespace)
    # minor line, point and linepoint styles:
    make_linepointstyles(['ls', 'ps', 'lps'], names, 'm', colors, dashes, ('o', 1.0), mec,
                         minorline, smallmarker, namespace)
    # fill styles:
    make_fillstyles('fs', names, ['', 's', 'a'], colors, mec, mew, fillalpha, namespace)


def line_style(name, color, dash, lw, clip_on=None, namespace=globals()):
    linedict = {'linestyle': '-', 'linewidth': lw}
    if clip_on is not None:
        linedict.update({'clip_on': clip_on})
    make_linestyles('ls', [name], '', [color], dash, linedict, namespace)

    
def color_cycler(palette, colors):
    color_cycle = [palette[c] for c in colors if c in palette]
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
    palette = colors_vivid
    lwthick=2.5
    lwthin=1.5
    lwspines=1.0    
    names = ['A1', 'A2', 'A3',
             'B1', 'B2', 'B3', 'B4',
             'C1', 'C2', 'C3', 'C4',
             'Male', 'Female']
    colors = [palette['red'], palette['orange'], palette['yellow'],
              palette['blue'], palette['purple'], palette['magenta'], palette['lightblue'],
              palette['lightgreen'], palette['green'], palette['darkgreen'], palette['cyan'],
              palette['blue'], palette['pink']]
    dashes = ['-', '-', '-',
              '-', '-', '-', '-.',
              '-', '-', '-', '-',
              '-', '-']
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4),
               ('o', 1.0), ('o', 1.0)]
    plot_styles(names, colors, dashes, markers, lwthick=lwthick, lwthin=lwthin,
                markerlarge=10.0, markersmall=6.5, mec=0.0, mew=1.5,
                fillalpha=0.4, namespace=namespace)
    line_style('Spine', palette['black'], '-', lwspines, False, namespace)
    line_style('Grid', palette['gray'], '--', lwthin, None, namespace)
    line_style('Marker', palette['black'], '-', lwthick, False, namespace)
    plot_params(font_size=10.0, font_family='sans-serif',
                label_size='small', label_format='{label} [{unit}]',
                label_xdist=5, label_ydist=10,
                tick_dir='out', tick_size=4.0, legend_size='x-small',
                fig_color=palette['white'], axes_color='none',
                spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'},
                namespace=namespace)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    color_cycler(palette, cycle_colors)

    
def paper_style(namespace=globals()):
    palette = colors_muted
    lwthick=1.7
    lwthin=0.8
    lwspines=0.8    
    names = ['A1', 'A2', 'A3',
             'B1', 'B2', 'B3', 'B4',
             'C1', 'C2', 'C3', 'C4',
             'Male', 'Female']
    colors = [palette['red'], palette['orange'], palette['yellow'],
              palette['blue'], palette['purple'], palette['magenta'], palette['lightblue'],
              palette['lightgreen'], palette['green'], palette['darkgreen'], palette['cyan'],
              palette['blue'], palette['pink']]
    dashes = ['-', '-', '-',
              '-', '-', '-', '-.',
              '-', '-', '-', '-',
              '-', '-']
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4),
               ('o', 1.0), ('o', 1.0)]
    plot_styles(names, colors, dashes, markers, lwthick=lwthick, lwthin=lwthin,
                markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                fillalpha=0.4, namespace=namespace)
    line_style('Spine', palette['black'], '-', lwspines, False, namespace)
    line_style('Grid', palette['gray'], '--', lwthin, None, namespace)
    line_style('Marker', palette['black'], '-', lwthick, False, namespace)
    plot_params(font_size=10.0, font_family='sans-serif',
                label_size='small', label_format='{label} [{unit}]',
                label_xdist=5, label_ydist=10,
                tick_dir='out', tick_size=2.5, legend_size='x-small',
                fig_color=palette['white'], axes_color='none',
                spines='lb', spines_offsets={'lrtb': 3}, spines_bounds={'lrtb': 'full'},
                namespace=namespace)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    color_cycler(palette, cycle_colors)


def plot_linestyles(ax):
    """ Plot names and lines of all available line styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the line styles.
    """
    k = 0
    for j, name in enumerate(style_names):
        gotit = False
        if name in ls:
            ax.text(k, 0.9, 'ls'+name)
            ax.plot([k, k+3.5], [1.0, 1.8], **ls[name])
            gotit = True
        if name in lsm:
            ax.text(k, -0.1, 'ls'+name+'m')
            ax.plot([k, k+3.5], [0.0, 0.8], **lsm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(-0.2, k+2.8)
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
    k = 0
    for j, name in enumerate(reversed(style_names)):
        gotit = False
        if name in ps:
            ax.text(0.1, k, 'ps'+name)
            ax.plot([0.6], [k+dy], **ps[name])
            gotit = True
        if name in psc:
            ax.text(1.1, k, 'ps'+name+'c')
            ax.plot([1.6], [k+dy], **psc[name])
            gotit = True
        if name in psm:
            ax.text(2.1, k, 'ps'+name+'m')
            ax.plot([2.6], [k+dy], **psm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(-1.0, k)
    ax.set_title('point styles')
        

def plot_linepointstyles(ax):
    """ Plot names and lines of all available linepoint styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the linepoint styles.
    """
    dy = 0.2
    k = 0
    for j, name in enumerate(reversed(style_names)):
        gotit = False
        if name in lps:
            ax.text(0.1, k-dy, 'lps'+name)
            ax.plot([0.8, 1.1, 1.4], [k, k, k], **lps[name])
            gotit = True
        if name in lpsc:
            ax.text(2.1, k-dy, 'lps'+name+'c')
            ax.plot([2.8, 3.1, 3.4], [k, k, k], **lpsc[name])
            gotit = True
        if name in lpsm:
            ax.text(4.1, k-dy, 'lps'+name+'m')
            ax.plot([4.8, 5.1, 5.4], [k, k, k], **lpsm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(-1.0, k)
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
    k = 0
    for j, name in enumerate(style_names):
        gotit = False
        if name in fs:
            ax.text(k, 1.9, 'fs'+name)
            ax.fill_between(x+k, y0+2, y2+2, **fs[name])
            ax.fill_between(x+k, y0+2, y1+2, **fs[name])
            gotit = True
        if name in fss:
            ax.text(k, 0.9, 'fs'+name+'s')
            ax.fill_between(x+k, y0+1, y2+1, **fss[name])
            ax.fill_between(x+k, y0+1, y1+1, **fss[name])
            gotit = True
        if name in fsa:
            ax.text(k, -0.1, 'fs'+name+'a')
            ax.fill_between(x+k, y0+0, y2+0, **fsa[name])
            ax.fill_between(x+k, y0+0, y1+0, **fsa[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(-0.2, k)
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
