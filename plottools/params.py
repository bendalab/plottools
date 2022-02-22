"""
Default rcParams settings for all modules.


You actually do not need to import this module. Rather use one of its
functions as a template. Copy it to your own module and adapt it to your
needs.


## Default plot styles and rc parameters

- `screen_style()`: layout and plot styles optimized for display on a screen.
- `paper_style()`: layout and plot styles optimized for inclusion into a paper.
- `sketch_style()`: layout and plot styles with xkcd style activated.
"""

import __main__
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .plottools import *


def screen_style(namespace=None):
    """ Layout and plot styles optimized for display on a screen.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:

    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit,
      e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.
    - a range of line, point, linepoint and fill styles defined in `namespace`,
      called A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:

    ```py
    ax.plot(x, y, **lsA1)   # major line only
    ax.plot(x, y, **lsB2m)  # minor line only
    ax.plot(x, y, **psA2)   # markers (points) only
    ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
    ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
    ```

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated line, point, linepoint and
        fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    ns = namespace
    if namespace is None:
        ns = __main__
    #ns.bar_fac = 0.9
    lwthick=2.5
    lwthin=1.5
    generic_styles(ns, colors='vivid', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=10.0, markersmall=6.5, mec=0.0, mew=1.5,
                   fillalpha=0.4)
    make_line_styles(ns, 'ls', 'Spine', '', ns.palette['black'], '-',
                     1.0, clip_on=False)
    make_line_styles(ns, 'ls', 'Grid', '', ns.palette['gray'], '--', 0.2)
    make_line_styles(ns, 'ls', 'Marker', '', ns.palette['black'], '-',
                     lwthick, clip_on=False)
    generic_arrow_styles(ns, ns.palette, 1.3)
    # rc settings:
    mpl.rcdefaults()
    axes_params(xmargin=0, ymargin=0, zmargin=0, color=ns.palette['white'])
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta',
                    'yellow', 'cyan', 'pink']
    colors_params(ns.palette, cycle_colors, cmap='RdYlBu')
    figure_params(color=ns.palette['gray'], format='png',
                  compression=6, fonttype=3, stripfonts=False)
    grid_params(grid=True, axis='both', which='major', **ns.lsGrid)
    labels_params(labelformat='{label} [{unit}]', labelsize='medium',
                  labelweight='normal', labelcolor='axes', labelpad=4,
                  xlabellocation='center', ylabellocation='center')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=ns.palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0},
                  spines_bounds={'lrtb': 'full'},
                  color=ns.lsSpine['color'],
                  linewidth=ns.lsSpine['linewidth'])
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=11.0, font_family='sans-serif', color='axes')
    ticks_params(xtick_minor=False, xtick_dir='out', xtick_size=4.0, minor_tick_frac=0.6,
                 xtick_major_width=None, xtick_minor_width=None, xtick_major_pad=None,
                 xtick_alignment='center', ytick_alignment='center_baseline',
                 xtick_color='axes', xtick_labelcolor='ticks', xtick_labelsize='medium')

    
def paper_style(namespace=None):
    """ Layout and plot styles optimized for inclusion into a paper.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:

    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit,
      e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.
    - a range of line, point, linepoint and fill styles defined in `namespace`,
      called A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:

    ```py
    ax.plot(x, y, **lsA1)   # major line only
    ax.plot(x, y, **lsB2m)  # minor line only
    ax.plot(x, y, **psA2)   # markers (points) only
    ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
    ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
    ```

    Parameters
    ----------
    namespace: clas or None
        Namespace to which the generated line, point, linepoint and
        fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    ns = namespace
    if namespace is None:
        ns = __main__
    #ns.bar_fac = 0.9
    lwthick=1.7
    lwthin=0.8
    generic_styles(ns, colors='muted', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4)
    make_line_styles(ns, 'ls', 'Spine', '', ns.palette['black'], '-',
                     0.8, clipon=False)
    make_line_styles(ns, 'ls', 'Grid', '', ns.palette['gray'], '--', 0.5)
    make_line_styles(ns, 'ls', 'Marker', '', ns.palette['black'], '-',
                     lwthick, clipon=False)
    generic_arrow_styles(ns, ns.palette, 1.0)
    # rc settings:
    mpl.rcdefaults()
    axes_params(xmargin=0, ymargin=0, zmargin=0, color='none')
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta',
                    'yellow', 'cyan', 'pink']
    colors_params(ns.palette, cycle_colors, cmap='RdYlBu')
    figure_params(color='none', format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    grid_params(grid=False, axis='both', which='major', **ns.lsGrid)
    labels_params(labelformat='{label} [{unit}]', labelsize='small',
                  labelweight='normal', labelcolor='axes', labelpad=4,
                  xlabellocation='center', ylabellocation='center')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5, numpoints=1,
                  scatterpoints=1, labelspacing=0.5,
                  columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f', lw=2,
                    color=ns.palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0},
                  spines_bounds={'lrtb': 'full'},
                  color=ns.lsSpine['color'],
                  linewidth=ns.lsSpine['linewidth'])
    tag_params(xoffs='auto', yoffs='auto', label='%A',
               minor_label='%A%mi',
               font=dict(fontsize='x-large',
                         fontstyle='normal',
                         fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif', color='axes')
    ticks_params(xtick_minor=False, xtick_dir='out', xtick_size=2.5,
                 minor_tick_frac=0.6, xtick_major_width=None,
                 xtick_minor_width=None, xtick_major_pad=None,
                 xtick_alignment='center',
                 ytick_alignment='center_baseline',
                 xtick_color='axes', xtick_labelcolor='ticks',
                 xtick_labelsize='medium')
    
   
def sketch_style(namespace=None):
    """ Layout and plot styles with xkcd style activated.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:

    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit,
      e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.
    - a range of line, point, linepoint and fill styles defined in `namespace`,
      called A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:

    ```py
    ax.plot(x, y, **lsA1)   # major line only
    ax.plot(x, y, **lsB2m)  # minor line only
    ax.plot(x, y, **psA2)   # markers (points) only
    ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
    ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
    ```

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated line, point, linepoint and
        fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    ns = namespace
    if namespace is None:
        ns = __main__
    #ns.bar_fac = 0.9
    lwthick=3.0
    lwthin=1.8
    generic_styles(ns, colors='vivid', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4)
    make_line_styles(ns, 'ls', 'Spine', '', ns.palette['black'], '-',
                     1.8, clipon=False)
    make_line_styles(ns, 'ls', 'Grid', '', ns.palette['gray'], '--', 0.5)
    make_line_styles(ns, 'ls', 'Marker', '', ns.palette['black'], '-',
                     lwthick, clipon=False)
    generic_arrow_styles(ns, ns.palette, 1.3)
    # rc settings:
    mpl.rcdefaults()
    plt.xkcd()
    axes_params(xmargin=0, ymargin=0, zmargin=0, color='none')
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta',
                    'yellow', 'cyan', 'pink']
    colors_params(ns.palette, cycle_colors, cmap='RdYlBu')
    figure_params(color=ns.palette['white'], format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    grid_params(grid=False, axis='both', which='major', **ns.lsGrid)
    labels_params(labelformat='{label} ({unit})', labelsize='medium',
                  labelweight='normal', labelcolor='axes', labelpad=4,
                  xlabellocation='center', ylabellocation='center')
    legend_params(fontsize='medium', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5, numpoints=1,
                  scatterpoints=1, labelspacing=0.5,
                  columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f', lw=2,
                    color=ns.palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lb', spines_offsets={'lrtb': 0},
                  spines_bounds={'lrtb': 'full'},
                  color=ns.lsSpine['color'],
                  linewidth=ns.lsSpine['linewidth'])
    tag_params(xoffs='auto', yoffs='auto', label='%A',
               minor_label='%A%mi',
               font=dict(fontsize='x-large',
                         fontstyle='normal',
                         fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif',
                color='axes')
    ticks_params(xtick_minor=False, xtick_dir='out', xtick_size=6,
                 minor_tick_frac=0.6, xtick_major_width=None,
                 xtick_minor_width=None, xtick_major_pad=None,
                 xtick_alignment='center',
                 ytick_alignment='center_baseline',
                 xtick_color='axes', xtick_labelcolor='ticks',
                 xtick_labelsize='medium')
        

def demo(style='screen'):
    """ Run a demonstration of the params module.

    Parameters
    ----------
    style: string
        'screen', 'print', or 'sketch': style to use.
    """
    class s: pass
    if style == 'sketch':
        sketch_style(s)
    elif style == 'paper':
        paper_style(s)
    else:
        style = 'screen'
        screen_style(s)
    fig, ax = plt.subplots()
    fig.suptitle('plottools.params')
    x = np.linspace(0, 20, 200)
    y = np.sin(x)
    ax.plot(x, y, **s.lsA1)
    ax.text(0.1, 0.9, '%s_style()' % style, transform=ax.transAxes)
    ax.text(0.1, 0.8, 'ax.plot(x, y, **s.lsA1)', transform=ax.transAxes)
    ax.set_ylim(-1.2, 2.0)
    ax.set_xlabel('Time', 'ms')
    ax.set_ylabel('Amplitude')
    plt.show()
    mpl.rcdefaults()


if __name__ == "__main__":
    style = 'screen'
    if len(sys.argv) > 1:
        style = sys.argv[1]
    demo(style)
