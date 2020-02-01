"""
# Plot format

Layout settings for a plot figure.

- `plot_format()`: set default plot format.
- `cm_size()`: convert dimensions from cm to inch.
- `adjust_fs()`: compute plot margins from multiples of the current font size.

Dictionaries with colors:
- `colors`: the default colors, set to one of the following:
- `colors_bendalab`: muted colors used by the Benda-lab.
- `colors_bendalab_vivid`: vivid colors used by the Benda-lab.
- `colors_plain`: plain rgb colors.
- `colors_henninger`: colors by Joerg Henninger.
- `colors_scicomp`: colors from the scientific computing script.
- `colors_uni_tuebingen`: colors of the corporate design of the university of Tuebingen.

Line and marker styles.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import OrderedDict
from .spines import show_spines, set_spines_outward, set_spines_bounds
from .ticks import set_xticks_delta, set_yticks_delta, set_xticks_none, set_yticks_none
from .ticks import set_xticks_format, set_yticks_format, set_xticks_blank, set_yticks_blank
from .labels import set_xlabel, set_ylabel, set_zlabel
from .insets import inset, zoomed_inset
from .labelaxes import label_axes
from .scalebars import xscalebar, yscalebar, scalebars
from .significance import significance_bar


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


""" Vivid colors used by the Benda-lab. """
colors_bendalab_vivid = OrderedDict()
colors_bendalab_vivid['red'] = '#D71000'
colors_bendalab_vivid['orange'] = '#FF9000'
colors_bendalab_vivid['yellow'] = '#FFF700'
colors_bendalab_vivid['green'] = '#30D700'
colors_bendalab_vivid['darkgreen'] = '#008020'
colors_bendalab_vivid['cyan'] = '#00F0B0'
colors_bendalab_vivid['blue'] = '#0020C0'
colors_bendalab_vivid['purple'] = '#8000C0'
colors_bendalab_vivid['magenta'] = '#B000B0'
colors_bendalab_vivid['pink'] = '#F00080'
colors_bendalab_vivid['white'] = '#FFFFFF'
colors_bendalab_vivid['gray'] = '#A7A7A7'
colors_bendalab_vivid['black'] = '#000000'

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
colors_uni_tuebingen = OrderedDict()
colors_uni_tuebingen['red'] = '#A51E37'
colors_uni_tuebingen['gold'] = '#B4A069'
colors_uni_tuebingen['black'] = '#32414B'
colors_uni_tuebingen['darkblue'] = '#415A8C'
colors_uni_tuebingen['blue'] = '#0069AA'
colors_uni_tuebingen['lightblue'] = '#50AAC8'
colors_uni_tuebingen['cyan'] = '#82B9A0'
colors_uni_tuebingen['green'] = '#7DA54B'
colors_uni_tuebingen['darkgreen'] = '#326E1E'
colors_uni_tuebingen['lightred'] = '#C8503C'
colors_uni_tuebingen['magenta'] = '#AF6E96'
colors_uni_tuebingen['gray'] = '#B4A096'
colors_uni_tuebingen['lightorange'] = '#D7B469'
colors_uni_tuebingen['orange'] = '#D29600'
colors_uni_tuebingen['brown'] = '#916946'

""" Default color palette. """
colors = colors_bendalab


""" line styles for plot(). """
lwthick = 2.0
lwthin = 1.0
mainline = {'linestyle': '-', 'linewidth': lwthick}
minorline = {'linestyle': '-', 'linewidth': lwthin}
largemarker = {'markersize': 7.5, 'markeredgecolor': colors['white'], 'markeredgewidth': 1, 'linestyle': 'none'}
smallmarker = {'markersize': 5.5, 'markeredgecolor': colors['white'], 'markeredgewidth': 1, 'linestyle': 'none'}
largecirclemarker = dict({'marker': 'o'}, **largemarker)
smallcirclemarker = dict({'marker': 'o'}, **smallmarker)
largelinepoints = {'linestyle': '-', 'linewidth': lwthick, 'markersize': 7.5, 'markeredgecolor': colors['white'], 'markeredgewidth': 1}
smalllinepoints = {'linestyle': '-', 'linewidth': lwthin, 'markersize': 5.5, 'markeredgecolor': colors['white'], 'markeredgewidth': 1}
largecirclelinepoints = dict({'marker': 'o'}, **largelinepoints)
smallcirclelinepoints = dict({'marker': 'o'}, **smalllinepoints)
filllw = 1.0
fillec = colors['white']
fillalpha = 0.4

# helper lines:
lsSpine = {'c': colors['black'], 'linestyle': '-', 'linewidth': 1, 'clip_on': False}
lsGrid = {'c': colors['gray'], 'linestyle': '--', 'linewidth': 1}
lsMarker = {'c': colors['black'], 'linestyle': '-', 'linewidth': 2}

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

lsA1 = dict({'color': colors['red']}, **mainline)
lsA2 = dict({'color': colors['orange']}, **mainline)
lsA3 = dict({'color': colors['yellow']}, **mainline)
lsA1m = dict({'color': colors['red']}, **minorline)
lsA2m = dict({'color': colors['orange']}, **minorline)
lsA3m = dict({'color': colors['yellow']}, **minorline)
psA1 = dict({'color': colors['red'], 'marker': 'o'}, **largemarker)
psA2 = dict({'color': colors['orange'], 'marker': 'p'}, **largemarker)
psA2.update({'markersize': 1.3*psA2['markersize']})
psA3 = dict({'color': colors['yellow'], 'marker': 'h'}, **largemarker)
psA3.update({'markersize': 1.2*psA3['markersize']})
psA1c = dict({'color': colors['red']}, **largecirclemarker)
psA2c = dict({'color': colors['orange']}, **largecirclemarker)
psA3c = dict({'color': colors['yellow']}, **largecirclemarker)
psA1m = dict({'color': colors['red']}, **smallcirclemarker)
psA2m = dict({'color': colors['orange']}, **smallcirclemarker)
psA3m = dict({'color': colors['yellow']}, **smallcirclemarker)
lpsA1 = dict({'color': colors['red'], 'marker': 'o'}, **largelinepoints)
lpsA2 = dict({'color': colors['orange'], 'marker': 'p'}, **largelinepoints)
lpsA2.update({'markersize': 1.3*lpsA2['markersize']})
lpsA3 = dict({'color': colors['yellow'], 'marker': 'h'}, **largelinepoints)
lpsA3.update({'markersize': 1.2*lpsA3['markersize']})
lpsA1c = dict({'color': colors['red']}, **largecirclelinepoints)
lpsA2c = dict({'color': colors['orange']}, **largecirclelinepoints)
lpsA3c = dict({'color': colors['yellow']}, **largecirclelinepoints)
lpsA1m = dict({'color': colors['red']}, **smallcirclelinepoints)
lpsA2m = dict({'color': colors['orange']}, **smallcirclelinepoints)
lpsA3m = dict({'color': colors['yellow']}, **smallcirclelinepoints)
fsA1 = {'facecolor': colors['red'], 'edgecolor': fillec, 'linewidth': filllw}
fsA2 = {'facecolor': colors['orange'], 'edgecolor': fillec, 'linewidth': filllw}
fsA3 = {'facecolor': colors['yellow'], 'edgecolor': fillec, 'linewidth': filllw}
fsA1s = {'facecolor': colors['red'], 'edgecolor': 'none'}
fsA2s = {'facecolor': colors['orange'], 'edgecolor': 'none'}
fsA3s = {'facecolor': colors['yellow'], 'edgecolor': 'none'}
fsA1a = {'facecolor': colors['red'], 'edgecolor': 'none', 'alpha': fillalpha}
fsA2a = {'facecolor': colors['orange'], 'edgecolor': 'none', 'alpha': fillalpha}
fsA3a = {'facecolor': colors['yellow'], 'edgecolor': 'none', 'alpha': fillalpha}

lsB1 = dict({'color': colors['blue']}, **mainline)
lsB2 = dict({'color': colors['purple']}, **mainline)
lsB3 = dict({'color': colors['magenta']}, **mainline)
lsB4 = dict({'color': colors['pink']}, **mainline)
lsB1m = dict({'color': colors['blue']}, **minorline)
lsB2m = dict({'color': colors['purple']}, **minorline)
lsB3m = dict({'color': colors['magenta']}, **minorline)
lsB4m = dict({'color': colors['pink']}, **minorline)
psB1 = dict({'color': colors['blue'], 'marker': 'v'}, **largemarker)
psB1.update({'markersize': 1.3*psB1['markersize']})
psB2 = dict({'color': colors['purple'], 'marker': '^'}, **largemarker)
psB2.update({'markersize': 1.3*psB2['markersize']})
psB3 = dict({'color': colors['magenta'], 'marker': '<'}, **largemarker)
psB3.update({'markersize': 1.3*psB3['markersize']})
psB4 = dict({'color': colors['pink'], 'marker': '>'}, **largemarker)
psB4.update({'markersize': 1.3*psB4['markersize']})
psB1c = dict({'color': colors['blue']}, **largecirclemarker)
psB2c = dict({'color': colors['purple']}, **largecirclemarker)
psB3c = dict({'color': colors['magenta']}, **largecirclemarker)
psB4c = dict({'color': colors['pink']}, **largecirclemarker)
psB1m = dict({'color': colors['blue']}, **smallcirclemarker)
psB2m = dict({'color': colors['purple']}, **smallcirclemarker)
psB3m = dict({'color': colors['magenta']}, **smallcirclemarker)
psB4m = dict({'color': colors['pink']}, **smallcirclemarker)
lpsB1 = dict({'color': colors['blue'], 'marker': 'v'}, **largelinepoints)
lpsB1.update({'markersize': 1.3*lpsB1['markersize']})
lpsB2 = dict({'color': colors['purple'], 'marker': '^'}, **largelinepoints)
lpsB2.update({'markersize': 1.3*lpsB2['markersize']})
lpsB3 = dict({'color': colors['magenta'], 'marker': '<'}, **largelinepoints)
lpsB3.update({'markersize': 1.3*lpsB3['markersize']})
lpsB4 = dict({'color': colors['pink'], 'marker': '>'}, **largelinepoints)
lpsB4.update({'markersize': 1.3*lpsB4['markersize']})
lpsB1c = dict({'color': colors['blue']}, **largecirclelinepoints)
lpsB2c = dict({'color': colors['purple']}, **largecirclelinepoints)
lpsB3c = dict({'color': colors['magenta']}, **largecirclelinepoints)
lpsB4c = dict({'color': colors['pink']}, **largecirclelinepoints)
lpsB1m = dict({'color': colors['blue']}, **smallcirclelinepoints)
lpsB2m = dict({'color': colors['purple']}, **smallcirclelinepoints)
lpsB3m = dict({'color': colors['magenta']}, **smallcirclelinepoints)
lpsB4m = dict({'color': colors['pink']}, **smallcirclelinepoints)
fsB1 = {'facecolor': colors['blue'], 'edgecolor': fillec, 'linewidth': filllw}
fsB2 = {'facecolor': colors['purple'], 'edgecolor': fillec, 'linewidth': filllw}
fsB3 = {'facecolor': colors['magenta'], 'edgecolor': fillec, 'linewidth': filllw}
fsB4 = {'facecolor': colors['pink'], 'edgecolor': fillec, 'linewidth': filllw}
fsB1s = {'facecolor': colors['blue'], 'edgecolor': 'none'}
fsB2s = {'facecolor': colors['purple'], 'edgecolor': 'none'}
fsB3s = {'facecolor': colors['magenta'], 'edgecolor': 'none'}
fsB4s = {'facecolor': colors['pink'], 'edgecolor': 'none'}
fsB1a = {'facecolor': colors['blue'], 'edgecolor': 'none', 'alpha': fillalpha}
fsB2a = {'facecolor': colors['purple'], 'edgecolor': 'none', 'alpha': fillalpha}
fsB3a = {'facecolor': colors['magenta'], 'edgecolor': 'none', 'alpha': fillalpha}
fsB4a = {'facecolor': colors['pink'], 'edgecolor': 'none', 'alpha': fillalpha}

lsC1 = dict({'color': colors['green']}, **mainline)
lsC2 = dict({'color': colors['darkgreen']}, **mainline)
lsC3 = dict({'color': colors['cyan']}, **mainline)
lsC1m = dict({'color': colors['green']}, **minorline)
lsC2m = dict({'color': colors['darkgreen']}, **minorline)
lsC3m = dict({'color': colors['cyan']}, **minorline)
psC1 = dict({'color': colors['green'], 'marker': 's'}, **largemarker)
psC2 = dict({'color': colors['darkgreen'], 'marker': 'D'}, **largemarker)
psC2.update({'markersize': 0.95*psC2['markersize']})
psC3 = dict({'color': colors['cyan'], 'marker': '*'}, **largemarker)
psC3.update({'markersize': 1.7*psC3['markersize']})
psC1c = dict({'color': colors['green']}, **largecirclemarker)
psC2c = dict({'color': colors['darkgreen']}, **largecirclemarker)
psC3c = dict({'color': colors['cyan']}, **largecirclemarker)
psC1m = dict({'color': colors['green']}, **smallcirclemarker)
psC2m = dict({'color': colors['darkgreen']}, **smallcirclemarker)
psC3m = dict({'color': colors['cyan']}, **smallcirclemarker)
lpsC1 = dict({'color': colors['green'], 'marker': 's'}, **largelinepoints)
lpsC2 = dict({'color': colors['darkgreen'], 'marker': 'D'}, **largelinepoints)
lpsC2.update({'markersize': 0.95*lpsC2['markersize']})
lpsC3 = dict({'color': colors['cyan'], 'marker': '*'}, **largelinepoints)
lpsC3.update({'markersize': 1.7*lpsC3['markersize']})
lpsC1c = dict({'color': colors['green']}, **largecirclelinepoints)
lpsC2c = dict({'color': colors['darkgreen']}, **largecirclelinepoints)
lpsC3c = dict({'color': colors['cyan']}, **largecirclelinepoints)
lpsC1m = dict({'color': colors['green']}, **smallcirclelinepoints)
lpsC2m = dict({'color': colors['darkgreen']}, **smallcirclelinepoints)
lpsC3m = dict({'color': colors['cyan']}, **smallcirclelinepoints)
fsC1 = {'facecolor': colors['green'], 'edgecolor': fillec, 'linewidth': filllw}
fsC2 = {'facecolor': colors['darkgreen'], 'edgecolor': fillec, 'linewidth': filllw}
fsC3 = {'facecolor': colors['cyan'], 'edgecolor': fillec, 'linewidth': filllw}
fsC1s = {'facecolor': colors['green'], 'edgecolor': 'none'}
fsC2s = {'facecolor': colors['darkgreen'], 'edgecolor': 'none'}
fsC3s = {'facecolor': colors['cyan'], 'edgecolor': 'none'}
fsC1a = {'facecolor': colors['green'], 'edgecolor': 'none', 'alpha': fillalpha}
fsC2a = {'facecolor': colors['darkgreen'], 'edgecolor': 'none', 'alpha': fillalpha}
fsC3a = {'facecolor': colors['cyan'], 'edgecolor': 'none', 'alpha': fillalpha}

# lines for male female colors:
lsMale = dict({'color': colors['blue']}, **mainline)
lsFemale = dict({'color': colors['pink']}, **mainline)
lsMalem = dict({'color': colors['blue']}, **minorline)
lsFemalem = dict({'color': colors['pink']}, **minorline)
psMale = dict({'color': colors['blue'], 'marker': 'o'}, **largemarker)
psFemale = dict({'color': colors['pink'], 'marker': 'o'}, **largemarker)
psMalec = dict({'color': colors['blue']}, **largecirclemarker)
psFemalec = dict({'color': colors['pink']}, **largecirclemarker)
psMalem = dict({'color': colors['blue']}, **smallcirclemarker)
psFemalem = dict({'color': colors['pink']}, **smallcirclemarker)
lpsMale = dict({'color': colors['blue'], 'marker': 'o'}, **largelinepoints)
lpsFemale = dict({'color': colors['pink'], 'marker': 'o'}, **largelinepoints)
lpsMalec = dict({'color': colors['blue']}, **largecirclelinepoints)
lpsFemalec = dict({'color': colors['pink']}, **largecirclelinepoints)
lpsMalem = dict({'color': colors['blue']}, **smallcirclelinepoints)
lpsFemalem = dict({'color': colors['pink']}, **smallcirclelinepoints)
fsMale = {'facecolor': colors['blue'], 'edgecolor': fillec, 'linewidth': filllw}
fsFemale = {'facecolor': colors['pink'], 'edgecolor': fillec, 'linewidth': filllw}
fsMales = {'facecolor': colors['blue'], 'edgecolor': 'none'}
fsFemales = {'facecolor': colors['pink'], 'edgecolor': 'none'}
fsMalea = {'facecolor': colors['blue'], 'edgecolor': 'none', 'alpha': fillalpha}
fsFemalea = {'facecolor': colors['pink'], 'edgecolor': 'none', 'alpha': fillalpha}

# dictionaries for line, point, linepoint and fill styles:
style_names = ('A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'Male', 'Female')
ls = {'A1': lsA1, 'A2': lsA2, 'A3': lsA3,
      'B1': lsB1, 'B2': lsB2, 'B3': lsB3, 'B4': lsB4,
      'C1': lsC1, 'C2': lsC2, 'C3': lsC3,
      'Male': lsMale, 'Female': lsFemale}
lsm = {'A1': lsA1m, 'A2': lsA2m, 'A3': lsA3m,
       'B1': lsB1m, 'B2': lsB2m, 'B3': lsB3m, 'B4': lsB4m,
       'C1': lsC1m, 'C2': lsC2m, 'C3': lsC3m,
       'Male': lsMalem, 'Female': lsFemalem}
ps = {'A1': psA1, 'A2': psA2, 'A3': psA3,
      'B1': psB1, 'B2': psB2, 'B3': psB3, 'B4': psB4,
      'C1': psC1, 'C2': psC2, 'C3': psC3,
      'Male': psMale, 'Female': psFemale}
psc = {'A1': psA1c, 'A2': psA2c, 'A3': psA3c,
       'B1': psB1c, 'B2': psB2c, 'B3': psB3c, 'B4': psB4c,
       'C1': psC1c, 'C2': psC2c, 'C3': psC3c,
       'Male': psMalec, 'Female': psFemalec}
psm = {'A1': psA1m, 'A2': psA2m, 'A3': psA3m,
       'B1': psB1m, 'B2': psB2m, 'B3': psB3m, 'B4': psB4m,
       'C1': psC1m, 'C2': psC2m, 'C3': psC3m,
       'Male': psMalem, 'Female': psFemalem}
lps = {'A1': lpsA1, 'A2': lpsA2, 'A3': lpsA3,
       'B1': lpsB1, 'B2': lpsB2, 'B3': lpsB3, 'B4': lpsB4,
       'C1': lpsC1, 'C2': lpsC2, 'C3': lpsC3,
       'Male': lpsMale, 'Female': lpsFemale}
lpsc = {'A1': lpsA1c, 'A2': lpsA2c, 'A3': lpsA3c,
        'B1': lpsB1c, 'B2': lpsB2c, 'B3': lpsB3c, 'B4': lpsB4c,
        'C1': lpsC1c, 'C2': lpsC2c, 'C3': lpsC3c,
        'Male': lpsMalec, 'Female': lpsFemalec}
lpsm = {'A1': lpsA1m, 'A2': lpsA2m, 'A3': lpsA3m,
        'B1': lpsB1m, 'B2': lpsB2m, 'B3': lpsB3m, 'B4': lpsB4m,
        'C1': lpsC1m, 'C2': lpsC2m, 'C3': lpsC3m,
        'Male': lpsMalem, 'Female': lpsFemalem}
fs = {'A1': fsA1, 'A2': fsA2, 'A3': fsA3,
      'B1': fsB1, 'B2': fsB2, 'B3': fsB3, 'B4': fsB4,
      'C1': fsC1, 'C2': fsC2, 'C3': fsC3,
      'Male': fsMale, 'Female': fsFemale}
fss = {'A1': fsA1s, 'A2': fsA2s, 'A3': fsA3s,
       'B1': fsB1s, 'B2': fsB2s, 'B3': fsB3s, 'B4': fsB4s,
       'C1': fsC1s, 'C2': fsC2s, 'C3': fsC3s,
       'Male': fsMales, 'Female': fsFemales}
fsa = {'A1': fsA1a, 'A2': fsA2a, 'A3': fsA3a,
       'B1': fsB1a, 'B2': fsB2a, 'B3': fsB3a, 'B4': fsB4a,
       'C1': fsC1a, 'C2': fsC2a, 'C3': fsC3a,
       'Male': fsMalea, 'Female': fsFemalea}


""" Default spines to be shown and their appearance (installed by plot_format()). """
__default_spines = 'lb'
__default_spines_offsets = {'lrtb': 3}
__default_spines_bounds = {'lrtb': 'full'}


def __axes__init__(ax, *args, **kwargs):
    """ Set some default formatting for a new Axes instance.

    Used by plot_format().
    """
    ax.__init__orig(*args, **kwargs)
    ax.show_spines(__default_spines)
    ax.set_spines_outward(__default_spines_offsets)
    ax.set_spines_bounds(__default_spines_bounds)


def plot_format(fontsize=10.0, label_format=None,
                spines=None, spines_offsets=None, spines_bounds=None):
    """ Set default plot format.

    Call this function *before* you create a matplotlib figure.

    You most likely want to copy it and adjust it according to your needs.

    Parameters
    ----------
    fontsize: float
        Fontsize for text in points.
    label_format: string
        Defines how an axis label is formatted from a label and an unit.
    spines: string
        Spines to be shown. See spines.show_spines() for details.
    spines_offsets: dict
        Offsets for moving spines outward. See spines.set_spines_outward() for details.
    spines_bounds: dict
        Bounds for the spines. See spines.set_spines_bounds() for details.
    """
    mpl.rcParams['figure.facecolor'] = 'white'
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.size'] = fontsize
    mpl.rcParams['xtick.labelsize'] = 'small'
    mpl.rcParams['ytick.labelsize'] = 'small'
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    mpl.rcParams['xtick.major.size'] = 2.5
    mpl.rcParams['ytick.major.size'] = 2.5
    mpl.rcParams['legend.fontsize'] = 'x-small'
    mpl.rcParams['grid.color'] = lsGrid['c']
    mpl.rcParams['grid.linestyle'] = lsGrid['linestyle']
    mpl.rcParams['grid.linewidth'] = lsGrid['linewidth']
    mpl.rcParams['axes.facecolor'] = 'none'
    mpl.rcParams['axes.edgecolor'] = lsSpine['c']
    mpl.rcParams['axes.linewidth'] = lsSpine['linewidth']
    color_cycle = [colors[c] for c in ['blue', 'red', 'orange', 'green', 'magenta',
                                       'yellow', 'cyan', 'pink'] if c in colors]
    if 'axes.prop_cycle' in mpl.rcParams:
        from cycler import cycler
        mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle)
    else:
        mpl.rcParams['axes.color_cycle'] = color_cycle
    
    # define the appearance of axis labels:
    if label_format:
        global axis_label_format
        axis_label_format = label_format
    
    # extend Axes constructor (for modifying spine appearence):
    mpl.axes.Subplot.__init__orig = mpl.axes.Subplot.__init__
    mpl.axes.Subplot.__init__ = __axes__init__
    if spines is not None:
        global __default_spines
        __default_spines = spines
    if spines_offsets is not None:
        global __default_spines_offsets
        __default_spines_offsets = spines_offsets
    if spines_bounds is not None:
        global __default_spines_bounds
        __default_spines_bounds = spines_bounds


def cm_size(*args):
    """ Convert dimensions from cm to inch.

    Use this function to set the size of a figure in centimeter:
    ```
    fig = plt.figure(figsize=cm_size(16.0, 10.0))
    ```

    Parameters
    ----------
    args: one or many float
        Size in centimeter.

    Returns
    -------
    inches: float or list of floats
        Input arguments converted to inch.
    """
    cm_per_inch = 2.54
    if len(args) == 1:
        return args[0]/cm_per_inch
    else:
        return [v/cm_per_inch for v in args]


def adjust_fs(fig=None, left=5.5, right=0.5, bottom=2.8, top=0.5):
    """ Compute plot margins from multiples of the current font size.

    Parameters
    ----------
    fig: matplotlib.figure or None
        The figure from which the figure size is taken. If None use the current figure.
    left: float
        the left margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
    right: float
        the right margin of the plots given in multiples of the width of a character
        (in fact, simply 60% of the current font size).
        *Note:* in contrast to the matplotlib `right` parameters, this specifies the
        width of the right margin, not its position relative to the origin.
    bottom: float
        the bottom margin of the plots given in multiples of the height of a character
        (the current font size).
    top: float
        the right margin of the plots given in multiples of the height of a character
        (the current font size).
        *Note:* in contrast to the matplotlib `top` parameters, this specifies the
        width of the top margin, not its position relative to the origin.

    Example
    -------
    ```
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    fig.subplots_adjust(**adjust_fs(fig, left=4.5))   # no matter what the figsize is!
    ```
    """
    if fig is None:
        fig = plt.gcf()
    ppi = 72.0 # points per inch:
    w, h = fig.get_size_inches()*ppi
    fs = plt.rcParams['font.size']
    return { 'left': left*0.6*fs/w,
             'right': 1.0 - right*0.6*fs/w,
             'bottom': bottom*fs/h,
             'top': 1.0 - top*fs/h }


def lighter(color, lightness):
    """ Make a color lighter.

    Parameters
    ----------
    color: string
        An RGB color as a hexadecimal string (e.g. '#rrggbb').
    lightness: float
        The smaller the lightness, the lighter the returned color.
        A lightness of 1 leaves the color untouched.
        A lightness of 0 returns white.

    Returns
    -------
    color: string
        The lighter color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rl = r + (1.0-lightness)*(0xff - r)
    gl = g + (1.0-lightness)*(0xff - g)
    bl = b + (1.0-lightness)*(0xff - b)
    return '#%02X%02X%02X' % (rl, gl, bl)


def darker(color, saturation):
    """ Make a color darker.

    Parameters
    ----------
    color: string
        An RGB color as a hexadecimal string (e.g. '#rrggbb').
    saturation: float
        The smaller the saturation, the darker the returned color.
        A saturation of 1 leaves the color untouched.
        A saturation of 0 returns black.

    Returns
    -------
    color: string
        The darker color as a hexadecimal RGB string (e.g. '#rrggbb').
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rd = r * saturation
    gd = g * saturation
    bd = b * saturation
    return '#%02X%02X%02X' % (rd, gd, bd)


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


def plot_linestyles(ax):
    """ Plot names and lines of all available line styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the line styles.
    """
    for k, name in enumerate(style_names):
        ax.text(k, 1.9, 'fs'+name+'a')
        ax.fill_between([k, k+3.5], [1.9, 2.7], [2.1, 2.9], **fsa[name])
        ax.plot([k, k+3.5], [2.0, 2.8], **ls[name])
        ax.text(k, 0.9, 'ls'+name)
        ax.plot([k, k+3.5], [1.0, 1.8], **ls[name])
        ax.text(k, -0.1, 'ls'+name+'m')
        ax.plot([k, k+3.5], [0.0, 0.8], **lsm[name])
    ax.set_ylim(-0.15, 3.1)
    ax.set_title('line styles')
        

def plot_pointstyles(ax):
    """ Plot names and lines of all available point styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the point styles.
    """
    for k, name in enumerate(reversed(style_names)):
        ax.text(0.1, k, 'ps'+name)
        ax.plot([0.6], [k], **ps[name])
        ax.text(1.1, k, 'ps'+name+'c')
        ax.plot([1.6], [k], **psc[name])
        ax.text(2.1, k, 'ps'+name+'m')
        ax.plot([2.6], [k], **psm[name])
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
    for k, name in enumerate(reversed(style_names)):
        ax.text(0.1, k, 'lps'+name)
        ax.plot([0.8, 1.1, 1.4], [k, k, k], **lps[name])
        ax.text(2.1, k, 'lps'+name+'c')
        ax.plot([2.8, 3.1, 3.4], [k, k, k], **lpsc[name])
        ax.text(4.1, k, 'lps'+name+'m')
        ax.plot([4.8, 5.1, 5.4], [k, k, k], **lpsm[name])
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(-1.0, len(style_names))
    ax.set_title('linepoint styles')
        

def demo(mode=1):
    """ Run a demonstration of the plotformat module.

    Parameters
    ----------
    mode: int or string
        1: plot the default color palette
        n>1: plot the default color palette with n-1 lighter and darker colors
        'linestyles': plot the names and lines of all available line styles
        'pointstyles': plot the names and points (markers) of all available point styles
        'linepointstyles': plot the names and lines of all available linepoint styles
        'complementary': plot complementary colors of the default color palette
        'comparison': plot the default color palette in comparison with colors_bendalab_vivid
    """
    # set default plot parameter:
    plot_format()
    # figsize in centimeter:
    fig, ax = plt.subplots(figsize=cm_size(16.0, 10.0))
    fig.subplots_adjust(**adjust_fs(fig, left=4.5, bottom=2.5, top=2.0, right=2.0))
    # colors and linestyles:
    if isinstance(mode, int):
        plot_colors(ax, colors, mode)
        ax.set_ylim(-0.27, 1.05)
    else:
        if 'linep' in mode:
            plot_linepointstyles(ax)
        elif 'line' in mode:
            plot_linestyles(ax)
        elif 'point' in mode:
            plot_pointstyles(ax)
        elif 'compl' in mode:
            plot_complementary_colors(ax, colors)
        elif 'compa' in mode:
            plot_color_comparison(ax, (colors_bendalab, 'benda_lab'),
                                  (colors_bendalab_vivid, 'bendalab_vivid'),
                                  (colors_plain, 'plain'),
                                  (colors_henninger, 'henninger'),
                                  (colors_scicomp, 'scicomp'),
                                  (colors_uni_tuebingen, 'uni_tuebingen'))
        elif 'henn' in mode:
            plot_color_comparison(ax, (colors_bendalab, 'benda_lab'),
                                  (colors_henninger, 'henninger'))
        else:
            print('unknown option %s!' % mode)
    plt.show()


if __name__ == "__main__":
    import sys
    mode = 1
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode.isdigit():
            mode = int(mode)
    demo(mode)
