"""
# Colors

Some color palettes and tools for manipulating colors.

Dictionaries with colors:
- `colors`: the default colors, set to one of the following:
- `colors_plain`: plain rgb colors.
- `colors_vivid`: vivid colors.
- `colors_muted`: muted colors.
- `colors_henninger`: colors by Joerg Henninger upond which the muted colors are build.
- `colors_scicomp`: colors from the scientific computing script.
- `colors_unituebingen`: colors of the corporate design of the University of Tuebingen.

Converting colors:
- `rgb()`: integer RGB components of a hex string.
- `hexstr()`: hex string from integer RGB components.
- `latex_colors()`: print a \definecolor command for LaTeX.

Manipulating colors:
- `lighter()`: make a color lighter.
- `darker()`: make a color darker.
- `gradient()`: interpolate between two colors.

Displaying colors:
- `plot_colors()`: plot all colors of a palette and optionally some lighter and darker variants.
- `plot_complementary_colors()`: plot complementary colors of a palette on top of each other.
- `plot_color_comparison()`: plot matching colors of severals palettes on top of each other.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import OrderedDict

""" Plain rgb colors. """
colors_plain = OrderedDict()
colors_plain['red'] = '#FF0000'
colors_plain['orange'] = '#FF8000'
colors_plain['yellow'] = '#FFFF00'
colors_plain['lightgreen'] = '#80FF00' # Chartreuse
colors_plain['green'] = '#00FF00'      # Lime
#colors_plain['darkgreen'] = '#008000'  # Green
colors_plain['greenblue'] = '#00FF80' # SpringGreen
colors_plain['cyan'] = '#00FFFF'
colors_plain['lightblue'] = '#0080FF'
colors_plain['blue'] = '#0000FF'
colors_plain['purple'] = '#8000FF'
colors_plain['magenta'] = '#FF00FF'
colors_plain['pink'] = '#FF0080'
colors_plain['white'] = '#FFFFFF'
colors_plain['gray'] = '#808080'
colors_plain['black'] = '#000000'

""" Vivid colors. """
colors_vivid = OrderedDict()
colors_vivid['red'] = '#D71000'
colors_vivid['orange'] = '#FF9000'
colors_vivid['yellow'] = '#FFF700'
colors_vivid['lightgreen'] = '#B0FF00'
colors_vivid['green'] = '#30D700'
colors_vivid['darkgreen'] = '#008020'
colors_vivid['cyan'] = '#00F0B0'
colors_vivid['lightblue'] = '#00B0C7'
colors_vivid['blue'] = '#0020C0'
colors_vivid['purple'] = '#8000C0'
colors_vivid['magenta'] = '#B000B0'
colors_vivid['pink'] = '#F00080'
colors_vivid['white'] = '#FFFFFF'
colors_vivid['gray'] = '#A7A7A7'
colors_vivid['black'] = '#000000'

""" Muted colors. """
colors_muted = OrderedDict()
colors_muted['red'] = '#C02717'
colors_muted['orange'] = '#F78017'
colors_muted['yellow'] = '#F0D730'
colors_muted['lightgreen'] = '#AAB71B'
colors_muted['green'] = '#408020'
colors_muted['darkgreen'] = '#007030'
colors_muted['cyan'] = '#40A787'
colors_muted['lightblue'] = '#008797'
colors_muted['blue'] = '#2060A7'
colors_muted['purple'] = '#53379B'
colors_muted['magenta'] = '#873770'
colors_muted['pink'] = '#D03050'
colors_muted['white'] = '#FFFFFF'
colors_muted['gray'] = '#A0A0A0'
colors_muted['black'] = '#000000'

""" Colors by Joerg Henninger. """
colors_henninger = OrderedDict()
colors_henninger['red'] = '#BA2D22'
colors_henninger['orange'] = '#F47F17'
colors_henninger['lightgreen'] = '#AAB71B'
colors_henninger['blue'] = '#3673A4'
colors_henninger['purple'] = '#53379B'

""" Colors from the scientific computing script. """
colors_scicomp = OrderedDict()
colors_scicomp['red'] = '#CC0000'
colors_scicomp['orange'] = '#FF9900'
colors_scicomp['lightorange'] = '#FFCC00'
colors_scicomp['yellow'] = '#FFFF66'
colors_scicomp['green'] = '#99FF00'
colors_scicomp['blue'] = '#0000CC'

""" Colors of the corporate design of the University of Tuebingen.
The first three are the primary colors, the remaining ones the secondary colors.
"""
colors_unituebingen = OrderedDict()
colors_unituebingen['red'] = '#A51E37'
colors_unituebingen['gold'] = '#B4A069'
colors_unituebingen['black'] = '#32414B'
colors_unituebingen['darkblue'] = '#415A8C'
colors_unituebingen['blue'] = '#0069AA'
colors_unituebingen['lightblue'] = '#50AAC8'
colors_unituebingen['cyan'] = '#82B9A0'
colors_unituebingen['green'] = '#7DA54B'
colors_unituebingen['darkgreen'] = '#326E1E'
colors_unituebingen['lightred'] = '#C8503C'
colors_unituebingen['magenta'] = '#AF6E96'
colors_unituebingen['gray'] = '#B4A096'
colors_unituebingen['lightorange'] = '#D7B469'
colors_unituebingen['orange'] = '#D29600'
colors_unituebingen['brown'] = '#916946'

""" All color palettes. """
color_palettes = OrderedDict()
color_palettes['plain'] = colors_plain
color_palettes['vivid'] = colors_vivid
color_palettes['muted'] = colors_muted
color_palettes['henninger'] = colors_henninger
color_palettes['scicomp'] = colors_scicomp
color_palettes['unituebingen'] = colors_unituebingen
    
""" Default color palette. """
colors = colors_muted


def rgb(hexcolor):
    """ Integer RGB components of a hex string.

    Parameters
    ----------
    hexcolor: string
        A rgb hex-string, e.g. '#FF0000'.
    """
    r = int(hexcolor[1:3], 16)
    g = int(hexcolor[3:5], 16)
    b = int(hexcolor[5:7], 16)
    return r, g, b
    

def hexstr(r, g, b):
    """ Hex string from integer RGB components.

    Parameters
    ----------
    r: int
        Red component.
    g: int
        Green component.
    b: int
        Blue component.
        
    Returns
    -------
    color: string.
        The color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    return '#%02X%02X%02X' % (r, g, b)

    
def latex_colors(colors):
    """ Print a \definecolor command for LaTeX.

    Parameters
    ----------
    colors: dict or string
        A dictionary with names and rgb hex-strings of colors
        or an rgb hex-string.
    """
    if isinstance(colors, dict):
        for cn in colors:
            r, g, b = rgb(colors[cn])
            print('\\definecolor{darkblue}{RGB}{%3d,%3d,%3d}  %% %s' % (r, g, b, cn))
    else:
        r, g, b = rgb(colors)
        print('\\definecolor{darkblue}{RGB}{%3d,%3d,%3d}' % (r, g, b))
        

def lighter(color, lightness):
    """ Make a color lighter.

    Parameters
    ----------
    color: string or dict
        An RGB color as a hexadecimal string (e.g. '#rrggbb')
        or a dictionary with an 'color' or 'facecolor' key.
    lightness: float
        The smaller the lightness, the lighter the returned color.
        A lightness of 0 returns white.
        A lightness of 1 leaves the color untouched.
        A lightness of 2 returns black.

    Returns
    -------
    color: string or dict
        The lighter color as a hexadecimal RGB string (e.g. '#rrggbb').
        If `color` is a dictionary, a copy of the dictionary is returned
        with the value of 'color' or 'facecolor' set to the lighter color.
    """
    try:
        c = color['color']
        cd = {k: v for k, v in color.items()}
        cd['color'] = lighter(c, lightness)
        return cd
    except (KeyError, TypeError):
        try:
            c = color['facecolor']
            cd = {k: v for k, v in color.items()}
            cd['facecolor'] = lighter(c, lightness)
            return cd
        except (KeyError, TypeError):
            if lightness > 2:
                lightness = 2
            if lightness > 1:
                return darker(color, 2.0-lightness)
            if lightness < 0:
                lightness = 0
            r, g, b = rgb(color)
            rl = r + (1.0-lightness)*(0xff - r)
            gl = g + (1.0-lightness)*(0xff - g)
            bl = b + (1.0-lightness)*(0xff - b)
            return hexstr(rl, gl, bl)


def darker(color, saturation):
    """ Make a color darker.

    Parameters
    ----------
    color: string or dict
        An RGB color as a hexadecimal string (e.g. '#rrggbb')
        or a dictionary with an 'color' key.
    saturation: float
        The smaller the saturation, the darker the returned color.
        A saturation of 0 returns black.
        A saturation of 1 leaves the color untouched.
        A saturation of 2 returns white.

    Returns
    -------
    color: string or dictionary
        The darker color as a hexadecimal RGB string (e.g. '#rrggbb').
        If `color` is a dictionary, a copy of the dictionary is returned
        with the value of 'color' or 'facecolor' set to the darker color.
    """
    try:
        c = color['color']
        cd = {k: v for k, v in color.items()}
        cd['color'] = darker(c, saturation)
        return cd
    except (KeyError, TypeError):
        try:
            c = color['facecolor']
            cd = {k: v for k, v in color.items()}
            cd['facecolor'] = darker(c, saturation)
            return cd
        except (KeyError, TypeError):
            if saturation > 2:
                sauration = 2
            if saturation > 1:
                return lighter(color, 2.0-saturation)
            if saturation < 0:
                saturation = 0
            r, g, b = rgb(color)
            rd = r*saturation
            gd = g*saturation
            bd = b*saturation
            return hexstr(rd, gd, bd)


def gradient(color0, color1, r):
    """ Interpolate between two colors.

    Parameters
    ----------
    color0: string or dict
        An RGB color as a hexadecimal string (e.g. '#rrggbb')
        or a dictionary with an 'color' or 'facecolor' key.
    color1: string or dict
        An RGB color as a hexadecimal string (e.g. '#rrggbb')
        or a dictionary with an 'color' or 'facecolor' key.
    r: float
        Value between 0 and for interpolating between the two colors.
        r=0 returns color0, r=1 returns color1.

    Returns
    -------
    color: string or dict
        The interpolated color as a hexadecimal RGB string (e.g. '#rrggbb').
        If at least one of the colors is a dictionary, then return a copy of the
        first dictionary with the value of 'color' or 'facecolor'
        set to the interpolated color.

    Raises
    ------
    KeyError:
        If a `color0` or `color1` is a dictionary, but does not contain a
        'color' or 'facecolor' key.
    """
    try:
        cd0 = {k: v for k, v in color0.items()}
        if 'color' in cd0:
            key0 = 'color'
            color0 = cd0[key0]
        elif 'facecolor' in cd0:
            key0 = 'facecolor'
            color0 = cd0[key0]
        else:
            raise KeyError('no color in color0 dictionary')
    except AttributeError:
        cd0 = None
    try:
        cd1 = {k: v for k, v in color1.items()}
        if 'color' in cd1:
            key1 = 'color'
            color1 = cd1[key1]
        elif 'facecolor' in cd1:
            key1 = 'facecolor'
            color1 = cd1[key1]
        else:
            raise KeyError('no color in color1 dictionary')
    except AttributeError:
        cd1 = None
    r0, g0, b0 = rgb(color0)
    r1, g1, b1 = rgb(color1)
    if r < 0:
        r = 0
    if r > 1:
        r = 1
    rg = r0 + r*(r1 - r0)
    gg = g0 + r*(g1 - g0)
    bg = b0 + r*(b1 - b0)
    cs = hexstr(rg, gg, bg)
    if cd0:
        cd0[key0] = cs
        return cd0
    elif cd1:
        cd1[key1] = cs
        return cd1
    else:
        return cs


def plot_colors(ax, colors, n=1):
    """ Plot all colors of a palette and optionally some lighter and darker variants.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colors: dict
        A dictionary with names and rgb hex-strings of colors.
    n: int
        If one, plot the colors of the palette only.
        If larger than one, plot in addition that many
        lighter and darker versions of the colors.
    """
    if n < 1:
        n = 1
    nn = 1 + 2*(n-1)
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    if n > 1:
        recty *= 0.9
    for k, c in enumerate(colors):
        for i in range(-n+1, n):
            if i < 0:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=darker(colors[c], (n+i)/float(n)))
            elif i > 0:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=lighter(colors[c], (n-i)/float(n)))
            else:
                ax.fill(rectx + 1.5*k, (i+n-1+recty)/nn, color=colors[c])
        ax.text(0.5 + 1.5*k, -0.09, c, ha='center')
        ax.text(0.5 + 1.5*k, -0.16, colors[c], ha='center')
    if n > 1:
        for i in range(-n+1, n):
            if i < 0:
                ax.text(-0.1, (i+n-0.6)/nn, '%.0f%%' % (100.0*(n+i)/float(n)), ha='right')
            elif i > 0:
                ax.text(-0.1, (i+n-0.6)/nn, '%.0f%%' % (100.0*(n-i)/float(n)), ha='right')
            else:
                ax.text(-0.1, (i+n-0.6)/nn, '100%', ha='right')
        ax.text(-1.1, 0.75, 'lighter', ha='center', va='center', rotation='vertical')
        ax.text(-1.1, 0.25, 'darker', ha='center', va='center', rotation='vertical')
        ax.set_xlim(-1.5, len(colors)*1.5)
    else:
        ax.set_xlim(-0.5, len(colors)*1.5)
    ax.set_ylim(-0.2, 1.05)


def plot_complementary_colors(ax, colors, n=0):
    """ Plot complementary colors of a palette on top of each other.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colors: dict
        A dictionary with names and rgb hex-strings of colors.
    n: int
        Number of additional gradient values to be plotted inbetween the complementary colors.
    """
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    if n > 0:
        recty *= 0.9
    n += 2
    dx = 1.0/(n-1)
    m = 0
    if 'red' in colors and 'green' in colors:
        for k, x in enumerate(np.linspace(0.0, 1.0, n)):
            ax.fill(rectx + 1.5*m, recty + k, color=gradient(colors['red'], colors['green'], x))
        m += 1
    if 'orange' in colors and 'blue' in colors:
        for k, x in enumerate(np.linspace(0.0, 1.0, n)):
            ax.fill(rectx + 1.5*m, recty + k, color=gradient(colors['orange'], colors['blue'], x))
        m += 1
    if 'yellow' in colors and 'magenta' in colors:
        for k, x in enumerate(np.linspace(0.0, 1.0, n)):
            ax.fill(rectx + 1.5*m, recty + k, color=gradient(colors['yellow'], colors['magenta'], x))
        m += 1
    if 'pink' in colors and 'cyan' in colors:
        for k, x in enumerate(np.linspace(0.0, 1.0, n)):
            ax.fill(rectx + 1.5*m, recty + k, color=gradient(colors['pink'], colors['cyan'], x))
        m += 1
    if 'pink' in colors and 'blue' in colors:
        for k, x in enumerate(np.linspace(0.0, 1.0, n)):
            ax.fill(rectx + 1.5*m, recty + k, color=gradient(colors['blue'], colors['pink'], x))
        m += 1
    ax.set_xlim(-0.5, m*1.5)
    ax.set_ylim(-0.1, n + 0.1)


def plot_color_comparison(ax, colorsa, *args):
    """ Plot matching colors of severals palettes on top of each other.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colorsa: dict or tuple (dict, string)
        A dictionary with names and rgb hex-strings of colors.
        This is the reference palette which is plotted completely at the bottom.
        The optional second name is used as a string to annotated the colors.
    args: list of dicts or tuples (dict, string)
        Further dictionaries with names and rgb hex-strings of colors.
        Colors with names matching the ones from `colorsa` are plotted on top.
        The optional second element is used as a string to annotated the colors.
    """
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    if isinstance(colorsa, (list, tuple)):
        ax.text(-0.1, 0.5, colorsa[1], rotation='vertical', ha='right', va='center')
        colorsa = colorsa[0]
    for k, c in enumerate(colorsa):
        ax.fill(rectx + 1.5*k, recty + 0.0, color=colorsa[c])
        for i, cbn in enumerate(args):
            cb = cbn
            if isinstance(cbn, (list, tuple)):
                cb = cbn[0]
                if k == 0:
                    ax.text(-0.1, 1.5+i, cbn[1], rotation='vertical', ha='right', va='center')
            if c in cb:
                ax.fill(rectx + 1.5*k, recty + 1 + i, color=cb[c])
        ax.text(0.5 + 1.5*k, -0.1, c, ha='center')
    ax.set_xlim(-0.5, len(colorsa)*1.5)
    ax.set_ylim(-0.2, 1.1 + len(args))

    
def demo(mode='default', n=1):
    """ Run a demonstration of the colors module.

    Parameters
    ----------
    mode: string
        - 'default': plot the default color palette
        - 'complementary': plot complementary colors of the default color palette
        - 'comparison': plot the default color palette in comparison to all other palettes
        - name of a color palette: plot the specified color palette (see `color_palettes`)
    n: int
        - 1: plot the selected color palette
        - n>1: plot the selected color palette with n-1 lighter and darker colors or
          n gradient values for 'complementary'
    """
    fig, ax = plt.subplots()
    if 'default' in mode:
        plot_colors(ax, colors, n)
    elif 'compl' in mode:
        plot_complementary_colors(ax, colors, n-1)
    elif 'compa' in mode:
        palettes = [(color_palettes[c], c) for c in color_palettes]
        plot_color_comparison(ax, *palettes)
    elif 'blabhenn' in mode:
        plot_color_comparison(ax, (colors_muted, 'muted'),
                              (colors_henninger, 'henninger'))
    elif mode in color_palettes:
        plot_colors(ax, color_palettes[mode], n)
        ax.set_title('colors_' + mode)
    else:
        print('unknown option %s!' % mode)
        print('possible options are: an integer number, compa(rison), compl(ementary), or one of the color palettes ' + ', '.join(color_palettes.keys()) + '.')
        return
    plt.show()


if __name__ == "__main__":
    import sys
    mode = 'default'
    n = 1
    if len(sys.argv) > 2:
        mode = sys.argv[1]
        n = int(sys.argv[2])
    elif len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            n = int(sys.argv[1])
        else:
            mode = sys.argv[1]
    demo(mode, n)
