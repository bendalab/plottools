"""
## Layout settings and plot styles

- `screen_style()`: layout and plot styles optimized for display on a screen.
- `paper_style()`: layout and plot styles optimized for inclusion into a paper.
- `sketch_style()`: layout and plot styles with xkcd style activated.


## Duplicate and modify plotting styles

- `lighter_styles()`: duplicate style with a range of lighter colors.
- `darker_styles()`: duplicate style with a range of darker colors.
- `lighter_darker_styles()`: duplicate style with a range of lighter and darker colors.


## Generate plotting styles

- `make_linestyles()`: generate dictionaries for line styles.
- `make_pointstyles()`: generate dictionaries for point styles.
- `make_linepointstyles()`: generate line styles, point styles, and line point styles.
- `make_fillstyles()`: generate dictionaries for fill styles.
- `plot_styles()`: generate plot styles from names, dashes, colors, and markers.


## Settings

- `plot_params()`: set some default plot parameter via matplotlib's rc settings.


## Plot styles

- `plot_linestyles()`: plot names and lines of all available line styles.
- `plot_pointstyles()`: plot names and lines of all available point styles.
- `plot_linepointstyles()`: plot names and lines of all available linepoint styles.
- `plot_fillstyles()`: plot names and patches of all available fill styles.
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

import __main__
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .align import align_params, install_align, uninstall_align
from .arrows import arrow_style, plot_arrowstyles, install_arrows, uninstall_arrows
from .aspect import install_aspect, install_aspect, uninstall_aspect
from .axes import axes_params, install_axes, uninstall_axes
from .colors import colors_params, color_palettes, lighter, darker, gradient, colormap
from .figure import figure_params, latex_include_figures, install_figure, uninstall_figure
from .insets import install_insets, uninstall_insets
from .labels import labels_params, install_labels, uninstall_labels
from .legend import legend_params, install_legend, uninstall_legend
from .neurons import install_neurons, uninstall_neurons
from .scalebars import scalebar_params, install_scalebars, uninstall_scalebars
from .significance import install_significance, uninstall_significance
from .spines import spines_params, install_spines, uninstall_spines
from .subplots import install_subplots, uninstall_subplots
from .tag import tag_params, install_tag, uninstall_tag
from .text import text_params, install_text, uninstall_text
from .ticks import ticks_params, install_ticks, uninstall_ticks
from .version import __version__


def lighter_styles(style, n):
    """ Duplicate style with a range of lighter colors.

    Parameters
    ----------
    style: dict
        A dictionary holding plot style parameter like `linewidth` and `color` or `facecolor`.
    n: int
        Number of lighter colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with increasingly lighter `color` or `facecolor`.
        The first style is the original one.

    Example
    -------
    Suppose you have a style for blue lines in a plot like
    ```py
    lsBlue = dict(color=colors['blue'], lw=2)
    ```
    Now you need 5 variants of this plot style with increasingly lighter colors.
    Just call
    ```py
    lsBlues = lighter_styles(lsBlue, 5)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsBlues):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = lighter(c, 1.0-k/n)
                styles.append(sd)
            return styles
    return [style]*n


def darker_styles(style, n):
    """ Duplicate style with a range of darker colors.

    Parameters
    ----------
    style: dict
        A dictionary holding plot style parameter like `linewidth` and `color` or `facecolor`.
    n: int
        Number of darker colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with increasingly darker `color` or `facecolor`.
        The first style is the original one.

    Example
    -------
    Suppose you have a style for green lines in a plot like
    ```py
    lsGreen = dict(color=colors['lightgreen'], lw=2)
    ```
    Now you need 4 variants of this plot style with increasingly darker colors.
    Just call
    ```py
    lsGreens = darker_styles(lsGreen, 4)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsGreens):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = darker(c, 1.0-k/n)
                styles.append(sd)
            return styles
    return [style]*n


def lighter_darker_styles(style, n):
    """ Duplicate style with a range of lighter and darker colors.

    Parameters
    ----------
    style: dict
        A dictionary holding plot style parameter like `linewidth` and `color` or `facecolor`.
    n: int
        Number of modified colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with `color` or `facecolor` starting from a lighter color,
        traversing over the original color to darker colors.
        The central style has the original color if `n` is odd.

    Example
    -------
    Suppose you have a style for blue lines in a plot like
    ```py
    lsBlue = dict(color=colors['blue'], lw=2)
    ```
    Now you need 5 variants of this plot style with lighter and darker colors.
    Just call
    ```py
    lsBlues = lighter_darker_styles(lsBlue, 5)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsBlues):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = lighter(c, 1+(k-(n-1)/2)/((n+1)//2))
                styles.append(sd)
            return styles
    return [style]*n


def make_linestyles(prefix, names, suffix, colors, dashes='-', lws=1,
                    namespace=None, **kwargs):
    """ Generate dictionaries for line styles.

    The generated dictionaries can be passed as key-word arguments to `ax.plot()` commands.
    For each corresponding name, color, line style and line width a dictionary is generated
    holding these attributes. The generated dictionaries are named `prefix + name + suffix`,
    and are additionally added to the `prefix + suffix` dictionary in the given namespace.
    `name` is also added to the `style_names` list in the namespace.
    
    For example
    ```py
    make_linestyles('ls', 'Male', '', 'blue', '-', 2)
    ```
    generates a dictionary named `lsMale` defining a blue solid line,
    adds `Male` to the `style_names` list,
    and adds the `lsMale` dictionary to `ls` under the key `Male`.
    Simply throw the dictionary into a `plot()` command:
    ```py
    plt.plot(x, y, **lsMale)
    ```
    or
    ```py
    plt.plot(x, y, **ls['Male'])
    ```
    this is the same as:
    ```py
    plt.plot(x, y, '-', color='#0000FF', lw=2)
    ```
    but is more expressive and can be changed at a single central place.

    This
    ```py
    make_linestyles('ls', ['Red', 'Green'], 'm', ['r', 'g'], ['-', '--'], 0.5)
    ```
    adds two line styles 'lsRedm', 'lsGreenm' to the main module
    with the respective colors and a thin solid or dashed line, respectively.

    Parameters
    ----------
    prefix: string
        Prefix prepended to all line style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffix: string
        Sufffix appended to all line style names.
    colors: matplotlib color or list of matplotlib colors
        Colors of the line styles.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        Dash styles of the connecting lines.
    lws: float or list of floats
        Widths of the connecting lines.
    namespace: dict or None
        Namespace to which the generated line styles are added.
        If None add line styles to the __main__ module.
    kwargs: dict
        Key-word arguments with further line properties, e.g. alpha, zorder.
    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    ln = prefix + suffix 
    if not hasattr(namespace, ln):
        setattr(namespace, ln, {})
    # number of line styles to be generated:
    n = 1
    for x in (names, colors, dashes, lws):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        sn = prefix + name + suffix
        c = colors[k] if isinstance(colors, (tuple, list)) else colors
        ds = dashes[k] if isinstance(dashes, (tuple, list)) else dashes
        lw = lws[k] if isinstance(lws, (tuple, list)) else lws
        ld = dict(color=c, linestyle=ds, linewidth=lw, **kwargs)
        setattr(namespace, sn, ld)
        getattr(namespace, ln)[name] = ld


def make_pointstyles(prefix, names, suffix, colors, dashes='none', lws=0,
                     markers=('o', 1.0), markersizes=5.0, markeredgecolors=0.0,
                     markeredgewidths=1.0, namespace=None, **kwargs):
    """ Generate dictionaries for point styles.

    The generated dictionaries can be passed as key-word arguments to `ax.plot()` commands.
    For each corresponding name, color, line style, line width, marker, marker size,
    marker edge color and marker edge width a dictionary is generated holding these attributes.
    The generated dictionaries are named `prefix + name + suffix`,
    and are additionally added to the `prefix + suffix` dictionary in the given namespace.
    `name` is also added to the `style_names` list in the namespace.
    
    For example
    ```py
    make_pointstyles('ps', 'Female', '', 'red', '-', 1, ('o', 1.0), 8, 0.5, 1, alpha=0.5)
    ```
    generates a dictionary named `psFemale` defining transparent red filled markers
    with a lighter edge, adds `Female` to `style_names`,
    and adds the dictionary to `ps` under the key `Female`.
    Simply throw the dictionary into a `plot()` command:
    ```py
    plt.plot(x, y, **psFemale)
    ```
    this is the same as:
    ```py
    plt.plot(x, y, **ps['Female'])
    ```
    This
    ```py
    make_pointstyles('ps', 'Reds%d', 'c', ['red', 'orange', 'yellow'], 'none', 0, ('o', 1.0), 8, 1, 0)
    ```
    generates 'psReds1',  'psReds2',  'psReds3' for plotting
    filled circels with colors red, orange, and yellow, respectively.

    Parameters
    ----------
    prefix: string
        Prefix prepended to all point style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffix: string
        Sufffix appended to all point style names.
    colors: matplotlib color or list of matplotlib colors
        For each color in the list a point style is generated.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        Dash styles of the connecting lines. If points are not to be connected, set to 'none'.
    lws: float or list of floats
        Widths of the connecting lines.
    markers: 2-tuple or list of 2-tuples
        For each point style a marker. The first element of the inner tuple is
        the marker symbol, the second one is a factor that is used to scale
        the marker's size.
    markersizes: float or list of floats
        For each point style a marker size. The marker size is multiplied with a factor
        of the corresponding marker.
    medgecolors: float or list of floats
        Defines the edge color for each point style.
        It is passed as the lightness argument to `lighter()`
        using the face color form `colors`. That is, 0 results in a white edge color,
        1 in an edge with the same color as the face color, and 2 in a black edge color.
    markersizes: float, list of floats
        For each point style a marker edge width.
    namespace: dict or None
        Namespace to which the generated point styles are added.
        If None add point styles to the __main__ module.
    kwargs: dict
        Key-word arguments with further marker properties, e.g. alpha, zorder.
    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    ln = prefix + suffix 
    if not hasattr(namespace, ln):
        setattr(namespace, ln, {})
    # number of markers:
    n_markers = 1
    if len(markers) >= 2 and isinstance(markers[1], (tuple, list)):
        n_markers = len(markers)
    # number of line styles to be generated:
    n = 1
    for x in (names, colors, dashes, lws, markersizes,
              markeredgecolors, markeredgewidths):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    if n < n_markers:
        n = n_markers
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        sn = prefix + name + suffix
        c = colors[k] if isinstance(colors, (tuple, list)) else colors
        ds = dashes[k] if isinstance(dashes, (tuple, list)) else dashes
        lw = lws[k] if isinstance(lws, (tuple, list)) else lws
        mk = markers[k] if n_markers > 1 else markers
        ms = markersizes[k] if isinstance(markersizes, (tuple, list)) else markersizes
        mc = markeredgecolors[k] if isinstance(markeredgecolors, (tuple, list)) else markeredgecolors
        mw = markeredgewidths[k] if isinstance(markeredgewidths, (tuple, list)) else markeredgewidths
        pd = dict(color=c, linestyle=ds, linewidth=lw, marker=mk[0], markersize=mk[1]*ms,
                  markeredgecolor=lighter(c, mc), markeredgewidth=mw, **kwargs)
        setattr(namespace, sn, pd)
        getattr(namespace, ln)[name] = pd


def make_linepointstyles(prefixes, names, suffix, colors, dashes, lws,
                         markers, markersizes, markeredgecolors,
                         markeredgewidths=1.0, namespace=None, **kwargs):
    """ Generate line styles, point styles, and line point styles.

    Passes the arguments on to `make_linestyles()` and twice to `make_pointstyles()`,
    once with `dashes='none'` for non-connected markers, and once
    with dashes and line widths for connecting lines.
    See those functions for a detailed description.

    Parameters
    ----------
    prefixes: list of strings
        If the first string is not None, generate line styles using `make_linestyles()`.
        If the second string is not None, generate point styles using `make_pointstyles()`.
        If the third string is not None, generate linepoint styles using `make_pointstyles()`
        with `pointdict` and `linedict` merged.
    namespace: dict or None
        Namespace to which the generated styles are added.
        If None add line styles to the __main__ module.
    *args:
        All remaining arguments are explained in the `make_linestyles()` and `make_pointstyles()`
        functions.
    """
    if namespace is None:
        namespace = __main__
    if prefixes[0]:
        make_linestyles(prefixes[0], names, suffix, colors, dashes, lws,
                        namespace, **kwargs)
    if prefixes[1]:
        make_pointstyles(prefixes[1], names, suffix, colors, 'none', 0,
                         markers, markersizes, markeredgecolors, markeredgewidths,
                         namespace, **kwargs)
    if prefixes[2]:
        make_pointstyles(prefixes[2], names, suffix, colors, dashes, lws,
                         markers, markersizes, markeredgecolors, markeredgewidths,
                         namespace, **kwargs)


def make_fillstyles(prefix, names, suffixes, colors, edgecolors, edgewidths, fillalphas,
                    namespace=None, **kwargs):
    """ Generate dictionaries for fill styles.

    The generated dictionaries can be passed as key-word arguments
    to `ax.fill_between()` commands.
    For each corresponding name, color, edge color, edge width and alpha
    a dictionary is generated holding these attributes.
    The generated dictionaries are named `prefix + name + suffix`,
    and are additionally added to the `prefix + suffix` dictionary in the given namespace.
    `name` is also added to the `style_names` list in the namespace.
    
    For example
    ```py
    make_fillstyles('fs', 'PSD', ['', 's', 'a'], [#00FF00], 2.0, 0.5, 0.4)
    ```
    generates the dictionaries named `fsPSD`, `fsPSDs`, `fsPSDa` defining a green fill color.
    The first, `fsPSD` gets a black edge color with edge width set to 0.5.
    The second, `fsPSDs` is without edge.
    The third, `fsPSDa` is without edge and has alpha set to 0.4.
    Further, `PSD` is added to `style_names`, and the three dictionaries are added
    to the `fs`, `fss` and `fsa` dictionaries under the key `PSD`.
    Simply throw the dictionaries into a `fill_between()` command:
    ```py
    plt.fill_between(x, y0, y1, **fsPSD)
    ```
    or like this (here for a transparent fill style):
    ```py
    plt.plot(x, y, **fsa['PSD'])
    ```

    Parameters
    ----------
    prefix: string
        Prefix prepended to all fill style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffixes: list of strings or None
        Sufffixes appended to all fill style names.  The first is for a
        fill style with edge color, the second for a solid fill style
        without edge, and the third for a transparent fill style without
        edge. If None the corresponding style is not generated.
    colors: matplotlib color or list of matplotlib colors
        Fill colors.
    edgecolors: float or list of floats
        Defines edge colors for the first fill style.
        It is passed as the lightness argument to `lighter()`
        using the face color from `colors`. That is, 0 results in a white edge color,
        1 in an edge with the same color as the face color, and 2 in a black edge color.
    edgewidth: float or list of floats
        Widths for the edge color of the first fill style.
    fillalphas: float or list of floats
        Alpha values for the transparent (third) fill style.
    namespace: dict or None
        Namespace to which the generated fill styles are added.
        If None add fill styles to the __main__ module.
    kwargs: dict
        Key-word arguments with further fill properties, e.g. zorder.
    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    for suffix in suffixes:
        if suffix is not None:
            ln = prefix + suffix 
            if not hasattr(namespace, ln):
                setattr(namespace, ln, {})
    # number of line styles to be generated:
    n = 1
    for x in (names, colors, edgecolors, edgewidths, fillalphas):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        for j, suffix in enumerate(suffixes):
            if suffix is not None:
                sn = prefix + name + suffix
                c = colors[k] if isinstance(colors, (tuple, list)) else colors
                ec = edgecolors[k] if isinstance(edgecolors, (tuple, list)) else edgecolors
                ew = edgewidths[k] if isinstance(edgewidths, (tuple, list)) else edgewidths
                fa = fillalphas[k] if isinstance(fillalphas, (tuple, list)) else fillalphas
                filldict = dict(facecolor=c, **kwargs)
                if j == 0:   # fill with edge:
                    filldict.update(dict(edgecolor=lighter(c, ec), linewidth=ew))
                elif j == 1: # fill without edge:
                    filldict.update(dict(edgecolor='none'))
                elif j == 2: # fill without edge, with alpha:
                    filldict.update(dict(edgecolor='none', alpha=fa))
                setattr(namespace, sn, filldict)
                getattr(namespace, prefix + suffix)[name] = filldict

    
def plot_styles(names, colors, dashes, markers, lwthick=2.0, lwthin=1.0,
                markerlarge=7.5, markersmall=5.5, mec=0.5, mew=1.0,
                fillalpha=0.4, namespace=None):
    """ Generate plot styles from names, dashes, colors, and markers.

    For each color and name a variety of plot styles are generated
    (for the example, names is 'Female'):
    - Major line styles (prefix 'ls', no suffix, e.g. 'lsFemale')
      for normal lines without markers.
    - Minor line styles (prefix 'ls', suffix 'm', e.g. 'lsFemalem')
      for thinner lines without markers.
    - Major point styles (prefix 'ps', no suffix, e.g. 'psFemale')
      for large markers without connecting lines.
    - Major circular point styles (prefix 'ps', suffix 'c', e.g. 'psFemalec')
      for large circular markers without connecting lines.
    - Minor point styles (prefix 'ps', suffix 'm', e.g. 'psFemalem')
      for small circular markers without connecting lines.
    - Major linepoint styles (prefix 'lps', no suffix, e.g. 'lpsFemale')
      for large markers with connecting lines.
    - Major circular linepoint styles (prefix 'lps', suffix 'c', e.g. 'lpsFemalec')
      for large circular markers with connecting lines.
    - Minor linepoint styles (prefix 'lps', suffix 'm', e.g. 'lpsFemalem')
      for small circular markers with connecting lines.
    - Fill styles with edge color (prefix 'fs', no suffix, e.g. 'fsFemale')
    - Fill styles with solid fill color and no edge color (prefix 'fs', suffix 's', e.g. 'fsFemals')
    - Fill styles with transparent fill color and no edge color (prefix 'fs', suffix 'a', e.g. 'fsFemala')
                
    Parameters
    ----------
    names: list of strings
        For each color in `colors` a name.
    colors: list of RGB hex-strings
        For each color in the list line, point, linepoint, and fill styles are generated.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        For each color a descriptor of a matplotlib linestyle
        that is used for line and linepoint styles.
    markers: tuple or list of tuples
        For each color a marker that is used for point and linepoint styles.
        The first element of the tuple is the marker symbol,
        the second on is a factor that is used to scale the markeredgewidth in `pointdict`.
    lwthick: float
        Line width for major line styles.
    lwthin: float
        Line width for minor line styles.
    markerlarge: float
        Marker size for major point styles.
    markersmall: float
        Marker size for minor point styles.
    mec: float
        Edge color for markers and fill styles. A factor between 0 and 2 passed together
        with the facecolor to `lighter()`. I.e. 0 results in a white edge,
        1 in an edge of the color of the face color, and 2 in a black edge.
    mew: float
        Line width for marker edges and fill styles.
    fillalpha: float
        Alpha value for transparent fill styles.
    namespace: dict or None
        Namespace to which the generated styles are added.
        If None add styles to the __main__ module.
    """    
    if namespace is None:
        namespace = __main__

    # line, point and linepoint styles:
    make_linepointstyles(['ls', 'ps', 'lps'], names, '', colors, dashes, lwthick,
                         markers, markerlarge, mec, mew, namespace)
    # circular point and linepoint styles:
    make_linepointstyles(['', 'ps', 'lps'], names, 'c', colors, dashes, lwthick,
                         ('o', 1.0), markerlarge, mec, mew, namespace)
    # minor line, point and linepoint styles:
    make_linepointstyles(['ls', 'ps', 'lps'], names, 'm', colors, dashes, lwthin,
                         ('o', 1.0), markersmall, mec, mew, namespace)
    # fill styles:
    make_fillstyles('fs', names, ['', 's', 'a'], colors, mec, mew, fillalpha, namespace)


def plot_params(axes_color='none', namespace=None):
    """ Set some default plot parameter via matplotlib's rc settings.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    axes_color: matplotlib color specification or 'none'
        Background color for each subplot.
    namespace: dict
        Namespace to which generated line, point, linepoint and fill styles were added.
        If None use the global namespace of the __main__ module.
        `lsSpine` and `lsGrid` of the namespace are used to set spine and grid properties.
    """
    if namespace is None:
        namespace = __main__
    # axes, label, ticks and text color:
    mpl.rcParams['axes.facecolor'] = axes_color
    if hasattr(namespace, 'lsSpine'):
        mpl.rcParams['axes.linewidth'] = getattr(namespace, 'lsSpine')['linewidth']
        mpl.rcParams['axes.edgecolor'] = getattr(namespace, 'lsSpine')['color']
        mpl.rcParams['axes.labelcolor'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['xtick.color'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['ytick.color'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['text.color'] = mpl.rcParams['axes.edgecolor']
    # grid style:
    if hasattr(namespace, 'lsGrid'):
        mpl.rcParams['grid.color'] = getattr(namespace, 'lsGrid')['color']
        mpl.rcParams['grid.linestyle'] = getattr(namespace, 'lsGrid')['linestyle']
        mpl.rcParams['grid.linewidth'] = getattr(namespace, 'lsGrid')['linewidth']


def screen_style(namespace=None):
    """ Layout and plot styles optimized for display on a screen.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    palette = color_palettes['vivid']
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
              '-', '-', '-', '-',
              '-', '-', '-', '-',
              '-', '-']
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4),
               ('o', 1.0), ('o', 1.0)]
    if namespace is None:
        namespace = __main__
    plot_styles(names, colors, dashes, markers, lwthick=lwthick, lwthin=lwthin,
                markerlarge=10.0, markersmall=6.5, mec=0.0, mew=1.5,
                fillalpha=0.4, namespace=namespace)
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines,
                    namespace, clip_on=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick,
                    namespace, clip_on=False)
    arrow_style('Line', dist=3.0, style='>', shrink=0, lw=0.8,
                color=palette['black'], head_length=5, head_width=5, namespace=namespace)
    arrow_style('Filled', dist=3.0, style='>>', shrink=0, lw=1,
                color=palette['black'], head_length=10, head_width=6, namespace=namespace)
    # rc settings:
    mpl.rcdefaults()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color=palette['gray'], format='png',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} [{unit}]', label_size='medium')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=4.0)
    plot_params(axes_color=palette['white'], namespace=namespace)

    
def paper_style(namespace=None):
    """ Layout and plot styles optimized for inclusion into a paper.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    palette = color_palettes['muted']
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
              '-', '-', '-', '-',
              '-', '-', '-', '-',
              '-', '-']
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4),
               ('o', 1.0), ('o', 1.0)]
    if namespace is None:
        namespace = __main__
    plot_styles(names, colors, dashes, markers, lwthick=lwthick, lwthin=lwthin,
                markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                fillalpha=0.4, namespace=namespace)
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines, namespace, clipon=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick, namespace, clipon=False)
    arrow_style('Line', dist=3.0, style='>', shrink=0, lw=0.8,
                color=palette['black'], head_length=5, head_width=5, namespace=namespace)
    arrow_style('Filled', dist=3.0, style='>>', shrink=0, lw=1,
                color=palette['black'], head_length=10, head_width=6, namespace=namespace)
    # rc settings:
    mpl.rcdefaults()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color='none', format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} [{unit}]', label_size='small')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=2.5)
    plot_params(axes_color='none', namespace=namespace)
    
   
def sketch_style(namespace=None):
    """ Layout and plot styles with xkcd style activated.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    #global bar_fac
    #bar_fac = 0.9
    palette = color_palettes['vivid']
    lwthick=3.0
    lwthin=1.8
    lwspines=1.8    
    names = ['A1', 'A2', 'A3',
             'B1', 'B2', 'B3', 'B4',
             'C1', 'C2', 'C3', 'C4',
             'Male', 'Female']
    colors = [palette['red'], palette['orange'], palette['yellow'],
              palette['blue'], palette['purple'], palette['magenta'], palette['lightblue'],
              palette['lightgreen'], palette['green'], palette['darkgreen'], palette['cyan'],
              palette['blue'], palette['pink']]
    dashes = ['-', '-', '-',
              '-', '-', '-', '-',
              '-', '-', '-', '-',
              '-', '-']
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4),
               ('o', 1.0), ('o', 1.0)]
    if namespace is None:
        namespace = __main__
    plot_styles(names, colors, dashes, markers, lwthick=lwthick, lwthin=lwthin,
                markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                fillalpha=0.4, namespace=namespace)
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines, namespace, clipon=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick, namespace, clipon=False)
    arrow_style('Line', dist=3.0, style='>', shrink=0, lw=0.8,
                color=palette['black'], head_length=5, head_width=5, namespace=namespace)
    arrow_style('Filled', dist=3.0, style='>>', shrink=0, lw=1,
                color=palette['black'], head_length=10, head_width=6, namespace=namespace)
    # rc settings:
    mpl.rcdefaults()
    plt.xkcd()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color='none', format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} ({unit})', label_size='medium')
    legend_params(fontsize='medium', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lb', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=6)
    plot_params(axes_color='none', namespace=namespace)
        

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
        

def demo(style='screen', mode='line'):
    """ Run a demonstration of the plotformat module.

    Parameters
    ----------
    style: string
        'screen', 'print', or 'sketch': style to use.
    mode: string
        'line': plot the names and lines of all available line styles
        'point': plot the names and points (markers) of all available point styles
        'linepoint': plot the names and lines of all available linepoint styles
        'fill': plot the names and patches of all available fill styles
        'arrow': plot the names and arrows of all available arrow styles
    """
    if style == 'sketch':
        sketch_style(sys.modules[__name__])
    elif style == 'paper':
        paper_style(sys.modules[__name__])
    else:
        screen_style(sys.modules[__name__])
    fig, ax = plt.subplots()
    if 'linep' in mode:
        plot_linepointstyles(ax)
    elif 'line' in mode:
        plot_linestyles(ax)
    elif 'point' in mode:
        plot_pointstyles(ax)
    elif 'fill' in mode:
        plot_fillstyles(ax)
    elif 'arrow' in mode:
        plot_arrowstyles(ax)
    else:
        print('unknown option %s!' % mode)
        print('possible options are: line, point, linep(oint), fill, arrow')
        return
    plt.show()


if __name__ == "__main__":
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    demo(mode=mode)
