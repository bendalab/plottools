"""
# Ticks

Setting tick locations and formats.

The following functions are available as members of mpl.axes.Axes:
- `set_xticks_delta()`: set interval between xticks.
- `set_yticks_delta()`: set interval between yticks.
- `set_xticks_fixed()`: set custom xticks at fixed positions.
- `set_yticks_fixed()`: set custom yticks at fixed positions.
- `set_xticks_prefix()`: format xticks with SI prefixes.
- `set_yticks_prefix()`: format yticks with SI prefixes.
- `set_xticks_fracs()`: format and place xticks as fractions.
- `set_yticks_fracs()`: format and place xticks as fractions.
- `set_xticks_pifracs()`: format and place xticks as mutiples of pi.
- `set_yticks_pifracs()`: format and place yticks as mutiples of pi.
- `set_xticks_off()`: do not draw and label any xticks.
- `set_yticks_off()`: do not draw and label any yticks.
- `set_xticks_format()`: format xticks according to formatter string.
- `set_yticks_format()`: format yticks according to formatter string.
- `set_xticks_blank()`: draw xticks without labeling them.
- `set_yticks_blank()`: draw yticks without labeling them.

- `set_minor_xticks_off()`: do not draw any minor xticks.
- `set_minor_yticks_off()`: do not draw any minor yticks.

The following functions are available as members of mpl.figure.Figure:
- `common_xtick_labels()`: simplify common xtick labels.
- `common_ytick_labels()`: simplify common ytick labels.

"""

import numpy as np
from fractions import Fraction
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def set_xticks_delta(ax, delta):
    """ Set interval between xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    delta: float
        Interval between xticks.
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_yticks_delta(ax, delta):
    """ Set interval between yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    delta: float
        Interval between yticks.
    """
    ax.yaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_xticks_fixed(ax, locs, labels='%g'):
    """ Set custom xticks at fixed positions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    locs: list of floats
        Locations of xticks.
    labels: string or list of strings
        Either a format string (e.g. '%.1f') or a list of labels
        for each tick position in `locs`.
    """
    ax.xaxis.set_major_locator(ticker.FixedLocator(locs))
    if isinstance(labels, (tuple, list)):
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))
    else:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labels))


def set_yticks_fixed(ax, locs, labels='%g'):
    """ Set custom yticks at fixed positions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    locs: list of floats
        Locations of yticks.
    labels: string or list of strings
        Either a format string (e.g. '%.1f') or a list of labels
        for each tick position in `locs`.
    """
    ax.yaxis.set_major_locator(ticker.FixedLocator(locs))
    if isinstance(labels, (tuple, list)):
        ax.yaxis.set_major_formatter(ticker.FixedFormatter(labels))
    else:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labels))


def prefix_formatter(x, pos):
    """ Function formatter used by set_xticks_prefix() and set_yticks_prefix().
    """
    if x <= 0:
        return '%g' % x
    prefixes = {-4: 'p', -3: 'n', -2: u'\u00B5', -1: 'm', 0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
    if plt.rcParams['text.usetex']:
        prefixes[-2] = r'\micro'
    e = int(np.log10(x)//3)
    prefix = prefixes[e]
    if prefix:
        if plt.rcParams['text.usetex']:
            return u'%g\,%s' % (x/10**(3*e), prefix)
        else:
            return u'%g\u2009%s' % (x/10**(3*e), prefix)
    else:
        return '%g' % x

        
def set_xticks_prefix(ax):
    """ Format xticks with SI prefixes.

    Ensures ticks to be numbers between 1 and 999 by appending necessary
    SI prefixes. That is, numbers between 1 and 999 are not modified and
    are formatted with '%g'. Numbers between 1000 and 999999 are
    divdided by 1000 and get an 'k' appended, e.g. 10000 ->
    '10k'. Numbers between 0.001 and 0.999 are multiplied with 1000 and
    get an 'm' appended, e.g. 0.02 -> '20m'. And so on.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(prefix_formatter))

        
def set_yticks_prefix(ax):
    """ Format yticks with SI prefixes.

    Ensures ticks to be numbers between 1 and 999 by appending necessary
    SI prefixes. That is, numbers between 1 and 999 are not modified and
    are formatted with '%g'. Numbers between 1000 and 999999 are
    divdided by 1000 and get an 'k' appended, e.g. 10000 ->
    '10k'. Numbers between 0.001 and 0.999 are multiplied with 1000 and
    get an 'm' appended, e.g. 0.02 -> '20m'. And so on.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    """
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(prefix_formatter))


def fraction_formatter(denominator, factor=1, fstring='', ontop=False):
    """ Function formatter used by set_xticks_fracs() and set_yticks_fracs().

    Parameters
    ----------
    denominator: int
        Ticks are located at multiples of factor/denominator.
    factor: float
        Tick values are interpreted as multiples of factor, i.e.
        they are divided by factor, before turning them into fractions.
    fstring: string
        Textual representation of factor that is appended to the fractions.
    ontop: boolean
        Place fstring into the numerator instead of after the fraction.

    Returns
    -------
    Function formatter.
    """
    def _fraction_formatter(x, pos):
        denom = int(np.round(denominator))
        num = int(np.round(x*denominator/factor))
        f = Fraction(num, denom)
        denom = f.denominator
        num = f.numerator
        sign = ''
        if num < 0:
            num = -num
            sign = '-'
        if denom == 1:
            if num == 0:
                return '$0$'
            elif num == 1 and fstring:
                return '$%s%s$' % (sign, fstring)
            else:
                return '$%s%d%s$' % (sign, num, fstring)
        else:
            if ontop:
                if num == 1 and fstring:
                    return r'$%s\frac{%s}{%d}$' % (sign, fstring, denom)
                else:
                    return r'$%s\frac{%d%s}{%d}$' % (sign, num, fstring, denom)
            else:
                return r'$%s\frac{%d}{%d}%s$' % (sign, num, denom, fstring)
    return _fraction_formatter


def set_xticks_fracs(ax, denominator, factor=1, fstring='', ontop=False):
    """ Format and place xticks as fractions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    denominator: int
        XTicks are located at multiples of factor/denominator.
    factor: float
        Tick values are interpreted as multiples of factor, i.e.
        they are divided by factor, before turning them into fractions.
    fstring: string
        Textual representation of factor that is appended to the fractions.
    ontop: boolean
        Place fstring into the numerator instead of after the fraction.
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(factor/denominator))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fraction_formatter(denominator, factor, fstring, ontop)))

    
def set_yticks_fracs(ax, denominator, factor=1, fstring='', ontop=False):
    """ Format and place xticks as fractions.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    denominator: int
        YTicks are located at multiples of factor/denominator.
    factor: float
        Tick values are interpreted as multiples of factor, i.e.
        they are divided by factor, before turning them into fractions.
    fstring: string
        Textual representation of factor that is appended to the fractions.
    ontop: boolean
        Place fstring into the numerator instead of after the fraction.
    """
    ax.yaxis.set_major_locator(ticker.MultipleLocator(factor/denominator))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(fraction_formatter(denominator, factor, fstring, ontop)))


def set_xticks_pifracs(ax, denominator, ontop=False):
    """ Format and place xticks as mutiples of pi.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    denominator: int
        XTicks are located at multiples of pi/denominator.
    ontop: boolean
        Place fstring into the numerator instead of after the fraction.
    """
    ax.set_xticks_fracs(denominator, np.pi, '\pi', ontop)


def set_yticks_pifracs(ax, denominator, ontop=False):
    """ Format and place yticks as mutiples of pi.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    denominator: int
        YTicks are located at multiples of pi/denominator.
    ontop: boolean
        Place fstring into the numerator instead of after the fraction.
    """
    ax.set_yticks_fracs(denominator, np.pi, '\pi', ontop)


def set_xticks_off(ax):
    """ Do not draw and label any xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_locator(ticker.NullLocator())


def set_yticks_off(ax):
    """ Do not draw and label any yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    """
    ax.yaxis.set_major_locator(ticker.NullLocator())


def set_xticks_format(ax, fs):
    """ Format xticks according to formatter string.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    fs: string
        Format string used to format xticks.
    """
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(fs))


def set_yticks_format(ax, fs):
    """ Format yticks according to formatter string.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    fs: string
        Format string used to format xticks.
    """
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(fs))


def set_xticks_blank(ax):
    """ Draw xticks without labeling them.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    """
    ax.xaxis.set_major_formatter(ticker.NullFormatter())


def set_yticks_blank(ax):
    """ Draw yticks without labeling them.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    """
    ax.yaxis.set_major_formatter(ticker.NullFormatter())


def set_minor_xticks_off(ax):
    """ Do not draw any minor xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the minor xticks are set.
    """
    ax.xaxis.set_minor_locator(ticker.NullLocator())


def set_minor_yticks_off(ax):
    """ Do not draw any minor yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the minor yticks are set.
    """
    ax.yaxis.set_minor_locator(ticker.NullLocator())


def common_xtick_labels(fig, axes=None):
    """ Simplify common xtick labels.
    
    Keep xtick labels only at the lowest axes and center the common xlabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose xticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    miny = np.min(coords[:,1])
    minx = np.min(coords[:,0])
    maxx = np.max(coords[:,2])
    xl = 0.5*(minx+maxx)
    done = False
    for ax in axes:
        if ax.get_position().p0[1] > miny + 1e-6:
            ax.set_xlabel('')
            ax.xaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.set_xlabel('')
        else:
            x, y = ax.xaxis.get_label().get_position()
            x = ax.transAxes.inverted().transform(fig.transFigure.transform((xl, 0)))[0]
            ax.xaxis.get_label().set_position((x, y))
            done = True


def common_ytick_labels(fig, axes=None):
    """ Simplify common ytick labels.
    
    Keep ytick labels only at the leftmost axes and center the common ylabel.

    Parameters
    ----------
    fig: matplotlib figure
        The figure containing the axes.
    axes: None or sequence of matplotlib axes
        Axes whose yticks should be combined.
        If None take all axes of the figure.
    """
    if axes is None:
        axes = fig.get_axes()
    coords = np.array([ax.get_position().get_points().ravel() for ax in axes])
    minx = np.min(coords[:,0])
    miny = np.min(coords[:,1])
    maxy = np.max(coords[:,3])
    yl = 0.5*(miny+maxy)
    done = False
    for ax in axes:
        if ax.get_position().p0[0] > minx + 1e-6:
            ax.set_ylabel('')
            ax.yaxis.set_major_formatter(ticker.NullFormatter())
        elif done:
            ax.set_ylabel('')
        else:
            x, y = ax.yaxis.get_label().get_position()
            y = ax.transAxes.inverted().transform(fig.transFigure.transform((0, yl)))[1]
            ax.yaxis.get_label().set_position((x, y))
            done = True

            
# make functions available as member variables:
mpl.axes.Axes.set_xticks_delta = set_xticks_delta
mpl.axes.Axes.set_yticks_delta = set_yticks_delta
mpl.axes.Axes.set_xticks_fixed = set_xticks_fixed
mpl.axes.Axes.set_yticks_fixed = set_yticks_fixed
mpl.axes.Axes.set_xticks_prefix = set_xticks_prefix
mpl.axes.Axes.set_yticks_prefix = set_yticks_prefix
mpl.axes.Axes.set_xticks_fracs = set_xticks_fracs
mpl.axes.Axes.set_yticks_fracs = set_yticks_fracs
mpl.axes.Axes.set_xticks_pifracs = set_xticks_pifracs
mpl.axes.Axes.set_yticks_pifracs = set_yticks_pifracs
mpl.axes.Axes.set_xticks_off = set_xticks_off
mpl.axes.Axes.set_yticks_off = set_yticks_off
mpl.axes.Axes.set_xticks_format = set_xticks_format
mpl.axes.Axes.set_yticks_format = set_yticks_format
mpl.axes.Axes.set_xticks_blank = set_xticks_blank
mpl.axes.Axes.set_yticks_blank = set_yticks_blank
mpl.axes.Axes.set_minor_xticks_off = set_minor_xticks_off
mpl.axes.Axes.set_minor_yticks_off = set_minor_yticks_off
mpl.figure.Figure.common_xtick_labels = common_xtick_labels
mpl.figure.Figure.common_ytick_labels = common_ytick_labels

    
def demo():
    """ Run a demonstration of the ticks module.
    """
    fig, axs = plt.subplots(4, 2)

    fig.suptitle('plottools.ticks')

    axs[0,0].text(0.1, 0.8, 'ax.set_xticks_delta(1.0)')
    axs[0,0].text(0.1, 0.6, 'ax.set_yticks_delta(0.5)')
    axs[0,0].set_xticks_delta(1.0)
    axs[0,0].set_yticks_delta(0.5)

    axs[0,1].text(0.1, 0.8, 'ax.set_xticks_off()')
    axs[0,1].text(0.1, 0.6, 'ax.set_yticks_off()')
    axs[0,1].set_xticks_off()
    axs[0,1].set_yticks_off()

    axs[1,0].text(0.1, 0.8, "ax.set_xticks_format('%04.1f')")
    axs[1,0].text(0.1, 0.6, "ax.set_yticks_format('%.2f')")
    axs[1,0].set_xticks_format('%04.1f')
    axs[1,0].set_yticks_format('%.2f')

    axs[1,1].text(0.1, 0.8, 'ax.set_xticks_blank()')
    axs[1,1].text(0.1, 0.6, 'ax.set_yticks_blank()')
    axs[1,1].set_xticks_blank()
    axs[1,1].set_yticks_blank()

    axs[2,0].text(0.1, 0.8, 'ax.set_xticks_fixed((0, 0.3, 1))')
    axs[2,0].text(0.1, 0.6, "ax.set_yticks_fixed((0, 0.5, 1), ('a', 'b', 'c'))")
    axs[2,0].set_xticks_fixed((0, 0.3, 1))
    axs[2,0].set_yticks_fixed((0, 0.5, 1), ('a', 'b', 'c'))

    axs[2,1].text(0.1, 0.8, 'ax.set_xticks_prefix()', transform=axs[2,1].transAxes)
    axs[2,1].text(0.1, 0.6, 'ax.set_yticks_prefix()', transform=axs[2,1].transAxes)
    axs[2,1].set_xscale('log')
    axs[2,1].set_xlim(1e-6, 1e0)
    axs[2,1].set_xticks_prefix()
    axs[2,1].set_yscale('log')
    axs[2,1].set_ylim(1e0, 1e6)
    axs[2,1].set_yticks_prefix()

    axs[3,0].text(0.1, 0.8, 'ax.set_xticks_fracs(4)', transform=axs[3,0].transAxes)
    axs[3,0].text(0.1, 0.6, "ax.set_yticks_fracs(3)", transform=axs[3,0].transAxes)
    axs[3,0].set_xlim(-1, 1)
    axs[3,0].set_ylim(-1, 1)
    axs[3,0].set_xticks_fracs(4)
    axs[3,0].set_yticks_fracs(3)

    axs[3,1].text(0.1, 0.8, 'ax.set_xticks_pifracs(2)', transform=axs[3,1].transAxes)
    axs[3,1].text(0.1, 0.6, "ax.set_yticks_pifracs(3, True)", transform=axs[3,1].transAxes)
    axs[3,1].set_xlim(-np.pi, 2*np.pi)
    axs[3,1].set_ylim(0, 4*np.pi/3)
    axs[3,1].set_xticks_pifracs(2)
    axs[3,1].set_yticks_pifracs(3, True)

    fig, axs = plt.subplots(2, 2)
    for ax in axs.ravel():
        ax.set_xlabel('xlabel')
        ax.set_ylabel('ylabel')
    axs[0,0].text(0.1, 0.8, 'fig.common_xtick_labels()')
    axs[0,0].text(0.1, 0.6, 'fig.common_ytick_labels()')
    fig.common_xtick_labels() 
    fig.common_ytick_labels()
    
    plt.show()


if __name__ == "__main__":
    demo()
