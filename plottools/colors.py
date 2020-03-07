"""
# Colors

Some color palettes and tools for manipulating colors.

Dictionaries with colors:
- `colors`: the default colors, set to one of the following:
- `colors_bendalab`: muted colors used by the Benda-lab.
- `colors_vivid`: vivid colors used by the Benda-lab.
- `colors_plain`: plain rgb colors.
- `colors_henninger`: colors by Joerg Henninger.
- `colors_scicomp`: colors from the scientific computing script.
- `colors_unituebingen`: colors of the corporate design of the university of Tuebingen.

Converting colors:
- `rgb()`: integer RGB components of a hex string.
- `hexstr()`: hex string from integer RGB components.
- `latex_colors()`: print a \definecolor command for LaTeX.

Manipulating colors:
- `lighter()`: make a color lighter.
- `darker()`: make a color darker.

Displaying colors:
- `plot_colors()`: plot all colors of a palette and optionally some lighter and darker variants.
- `plot_complementary_colors()`: plot complementary colors of a palette on top of each other.
- `plot_color_comparison()`: plot matching colors of severals palettes on top of each other.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import OrderedDict


""" Muted colors used by the Benda-lab. """
colors_bendalab = OrderedDict()
colors_bendalab['red'] = '#C02717'
colors_bendalab['orange'] = '#F78017'
colors_bendalab['yellow'] = '#F0D730'
colors_bendalab['green'] = '#AAB71B'
colors_bendalab['darkgreen'] = '#007030'
colors_bendalab['cyan'] = '#40A787'
colors_bendalab['blue'] = '#2060A7'
colors_bendalab['purple'] = '#53379B'
colors_bendalab['magenta'] = '#873770'
colors_bendalab['pink'] = '#D03050'
colors_bendalab['white'] = '#FFFFFF'
colors_bendalab['gray'] = '#A0A0A0'
colors_bendalab['black'] = '#000000'


""" Vivid colors. """
colors_vivid = OrderedDict()
colors_vivid['red'] = '#D71000'
colors_vivid['orange'] = '#FF9000'
colors_vivid['yellow'] = '#FFF700'
colors_vivid['green'] = '#30D700'
colors_vivid['darkgreen'] = '#008020'
colors_vivid['cyan'] = '#00F0B0'
colors_vivid['blue'] = '#0020C0'
colors_vivid['purple'] = '#8000C0'
colors_vivid['magenta'] = '#B000B0'
colors_vivid['pink'] = '#F00080'
colors_vivid['white'] = '#FFFFFF'
colors_vivid['gray'] = '#A7A7A7'
colors_vivid['black'] = '#000000'

""" Plain rgb colors. """
colors_plain = OrderedDict()
colors_plain['red'] = '#FF0000'
colors_plain['orange'] = '#FFA500'
colors_plain['yellow'] = '#FFFF00'
colors_plain['green'] = '#00FF00'
colors_plain['darkgreen'] = '#008000'
colors_plain['cyan'] = '#00FFFF'
colors_plain['blue'] = '#0000FF'
colors_plain['purple'] = '#8000FF'
colors_plain['magenta'] = '#FF00FF'
colors_plain['pink'] = '#FF0080'
colors_plain['white'] = '#FFFFFF'
colors_plain['gray'] = '#808080'
colors_plain['black'] = '#000000'

""" Colors by Joerg Henninger. """
colors_henninger = OrderedDict()
colors_henninger['red'] = '#BA2D22'
colors_henninger['orange'] = '#F47F17'
colors_henninger['green'] = '#AAB71B'
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

""" Colors of the corporate design of the university of Tuebingen.
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
color_palettes = {'bendalab': colors_bendalab,
                  'vivid': colors_vivid,
                  'plain': colors_plain,
                  'henninger': colors_henninger,
                  'scicomp': colors_scicomp,
                  'unituebingen': colors_unituebingen }
    
""" Default color palette. """
colors = colors_bendalab


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
        or a dictionary with an 'color' key.
    lightness: float
        The smaller the lightness, the lighter the returned color.
        A lightness of 1 leaves the color untouched.
        A lightness of 0 returns white.

    Returns
    -------
    color: string
        The lighter color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    try:
        c = color['color']
        color['color'] = lighter(c, lightness)
        return color
    except TypeError:
        r, g, b = rgb(color)
        if lightness < 0:
            lightness = 0
        if lightness > 1:
            lightness = 1
        rl = r + (1.0-lightness)*(0xff - r)
        gl = g + (1.0-lightness)*(0xff - g)
        bl = b + (1.0-lightness)*(0xff - b)
        return hexstr(rl, gl, bl)


def darker(color, saturation):
    """ Make a color darker.

    Parameters
    ----------
    color: string
        An RGB color as a hexadecimal string (e.g. '#rrggbb')
        or a dictionary with an 'color' key.
    saturation: float
        The smaller the saturation, the darker the returned color.
        A saturation of 1 leaves the color untouched.
        A saturation of 0 returns black.

    Returns
    -------
    color: string
        The darker color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    try:
        c = color['color']
        color['color'] = darker(c, saturation)
        return color
    except TypeError:
        r, g, b = rgb(color)
        if saturation < 0:
            saturation = 0
        if saturation > 1:
            saturation = 1
        rd = r * saturation
        gd = g * saturation
        bd = b * saturation
        return hexstr(rd, gd, bd)


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


def plot_complementary_colors(ax, colors):
    """ Plot complementary colors of a palette on top of each other.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the colors.
    colors: dict
        A dictionary with names and rgb hex-strings of colors.
    """
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    n = 0
    if 'red' in colors and 'green' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['red'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['green'])
        n += 1
    if 'orange' in colors and 'blue' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['orange'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['blue'])
        n += 1
    if 'yellow' in colors and 'magenta' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['yellow'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['magenta'])
        n += 1
    if 'pink' in colors and 'cyan' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['pink'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['cyan'])
        n += 1
    if 'pink' in colors and 'blue' in colors:
        ax.fill(rectx + 1.5*n, recty + 1.0, color=colors['blue'])
        ax.fill(rectx + 1.5*n, recty + 0.0, color=colors['pink'])
        n += 1
    ax.set_xlim(-0.5, n*1.5)
    ax.set_ylim(-0.1, 2.1)


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

    
def demo(mode=1):
    """ Run a demonstration of the colors module.

    Parameters
    ----------
    mode: int or string
        - 1: plot the default color palette
        - n>1: plot the default color palette with n-1 lighter and darker colors
        - 'complementary': plot complementary colors of the default color palette
        - 'comparison': plot the default color palette in comparison to all other palettes
        - name of a color palette: plot the specified color palette (see `color_palettes`)
    """
    fig, ax = plt.subplots()
    if isinstance(mode, int):
        plot_colors(ax, colors, mode)
    else:
        if 'compl' in mode:
            plot_complementary_colors(ax, colors)
        elif 'compa' in mode:
            plot_color_comparison(ax, (colors_bendalab, 'benda_lab'),
                                  (colors_vivid, 'vivid'),
                                  (colors_plain, 'plain'),
                                  (colors_henninger, 'henninger'),
                                  (colors_scicomp, 'scicomp'),
                                  (colors_unituebingen, 'unituebingen'))
        elif 'blabhenn' in mode:
            plot_color_comparison(ax, (colors_bendalab, 'benda_lab'),
                                  (colors_henninger, 'henninger'))
        elif mode in color_palettes:
            plot_colors(ax, color_palettes[mode], 1)
            ax.set_title('colors_' + mode)
        else:
            print('unknown option %s!' % mode)
            print('possible options are: an integer number, compa(rison), compl(ementary), or one of the color palettes ' + ', '.join(color_palettes.keys()) + '.')
            return
    plt.show()


if __name__ == "__main__":
    import sys
    mode = 1
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode.isdigit():
            mode = int(mode)
    demo(mode)
