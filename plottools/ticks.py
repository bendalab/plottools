"""
Setting tick locations and formats.


## Axes member functions

- `set_xticks_delta()`: set interval between major xticks.
- `set_yticks_delta()`: set interval between major yticks.
- `set_xticks_log()`: set major ticks on a logarithmic x-axis.
- `set_yticks_log()`: set major ticks on a logarithmic y-axis.
- `set_xticks_fixed()`: set custom xticks at fixed positions.
- `set_yticks_fixed()`: set custom yticks at fixed positions.
- `set_xticks_prefix()`: format xticks with SI prefixes.
- `set_yticks_prefix()`: format yticks with SI prefixes.
- `set_xticks_fracs()`: format and place xticks as fractions.
- `set_yticks_fracs()`: format and place xticks as fractions.
- `set_xticks_pifracs()`: format and place xticks as mutiples of pi.
- `set_yticks_pifracs()`: format and place yticks as mutiples of pi.
- `set_xticks_format()`: format xticks according to formatter string.
- `set_yticks_format()`: format yticks according to formatter string.
- `set_xticks_blank()`: draw xticks without labeling them.
- `set_yticks_blank()`: draw yticks without labeling them.
- `set_xticks_off()`: do not draw and label any xticks.
- `set_yticks_off()`: do not draw and label any yticks.
- `set_minor_xticks_off()`: do not draw any minor xticks.
- `set_minor_yticks_off()`: do not draw any minor yticks.


## Install/uninstall ticks functions

You usually do not need to call these functions. Upon loading the ticks
module, `install_ticks()` is called automatically.

- `install_ticks()`: install functions of the ticks module in matplotlib.
- `uninstall_ticks()`: uninstall all code of the ticks module from matplotlib.
"""

import numpy as np
from fractions import Fraction
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def set_xticks_delta(ax, delta):
    """ Set interval between major xticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    delta: float
        Interval between xticks.
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_yticks_delta(ax, delta):
    """ Set interval between major yticks.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    delta: float
        Interval between yticks.
    """
    ax.yaxis.set_major_locator(ticker.MultipleLocator(delta))


def set_xticks_log(ax, subs=(1.0,), numdecs=4, numticks=None):
    """ Set major ticks on a logarithmic x-axis.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the xticks are set.
    subs: None, 'auto', 'all', or sequence of floats
        Multiples of integer powers of ten, where to place major ticks.
    numdecs: int
        ???
    numticks: int
        Maximum number of ticks placed on the axis.
    """
    ax.set_xscale('log')
    ax.xaxis.set_major_locator(ticker.LogLocator(10.0, subs, numdecs, numticks))


def set_yticks_log(ax, subs=(1.0,), numdecs=4, numticks=None):
    """ Set major ticks on a logarithmic y-axis.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.
    subs: None, 'auto', 'all', or sequence of floats
        Multiples of integer powers of ten, where to place major ticks.
    numdecs: int
        ???
    numticks: int
        Maximum number of ticks placed on the axis.
    """
    ax.set_yscale('log')
    ax.yaxis.set_major_locator(ticker.LogLocator(10.0, subs, numdecs, numticks))


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

    Notes
    -----
    On logarithmic axis you may want to turn off minor ticks, e.g. via
    `ax.set_minor_xticks_off()`.
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

    Notes
    -----
    On logarithmic axis you may want to turn off minor ticks, e.g. via
    `ax.set_minor_yticks_off()`.
    """
    ax.yaxis.set_major_locator(ticker.FixedLocator(locs))
    if isinstance(labels, (tuple, list)):
        ax.yaxis.set_major_formatter(ticker.FixedFormatter(labels))
    else:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labels))


def prefix_formatter(x, pos):
    """ Function formatter used by `set_xticks_prefix()` and `set_yticks_prefix()`.
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
            return u'%g\\,%s' % (x/10**(3*e), prefix)
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
    """ Function formatter used by `set_xticks_fracs()` and `set_yticks_fracs()`.

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
    ax.set_xticks_fracs(denominator, np.pi, '\\pi', ontop)


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
    ax.set_yticks_fracs(denominator, np.pi, '\\pi', ontop)


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

    See also
    --------
    `plottools.axes.common_xtick_labels()`
    """
    ax.xaxis.set_major_formatter(ticker.NullFormatter())


def set_yticks_blank(ax):
    """ Draw yticks without labeling them.

    Parameters
    ----------
    ax: matplotlib axis
        Axis on which the yticks are set.

    See also
    --------
    `plottools.axes.common_ytick_labels()`
    """
    ax.yaxis.set_major_formatter(ticker.NullFormatter())


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


def install_ticks():
    """ Install ticks functions on matplotlib axes.

    This function is also called automatically upon importing the module.

    See also
    --------
    - `uninstall_ticks()`
    """
    if not hasattr(mpl.axes.Axes, 'set_xticks_delta'):
        mpl.axes.Axes.set_xticks_delta = set_xticks_delta
    if not hasattr(mpl.axes.Axes, 'set_yticks_delta'):
        mpl.axes.Axes.set_yticks_delta = set_yticks_delta
    if not hasattr(mpl.axes.Axes, 'set_xticks_log'):
        mpl.axes.Axes.set_xticks_log = set_xticks_log
    if not hasattr(mpl.axes.Axes, 'set_yticks_log'):
        mpl.axes.Axes.set_yticks_log = set_yticks_log
    if not hasattr(mpl.axes.Axes, 'set_xticks_fixed'):
        mpl.axes.Axes.set_xticks_fixed = set_xticks_fixed
    if not hasattr(mpl.axes.Axes, 'set_yticks_fixed'):
        mpl.axes.Axes.set_yticks_fixed = set_yticks_fixed
    if not hasattr(mpl.axes.Axes, 'set_xticks_prefix'):
        mpl.axes.Axes.set_xticks_prefix = set_xticks_prefix
    if not hasattr(mpl.axes.Axes, 'set_yticks_prefix'):
        mpl.axes.Axes.set_yticks_prefix = set_yticks_prefix
    if not hasattr(mpl.axes.Axes, 'set_xticks_fracs'):
        mpl.axes.Axes.set_xticks_fracs = set_xticks_fracs
    if not hasattr(mpl.axes.Axes, 'set_yticks_fracs'):
        mpl.axes.Axes.set_yticks_fracs = set_yticks_fracs
    if not hasattr(mpl.axes.Axes, 'set_xticks_pifracs'):
        mpl.axes.Axes.set_xticks_pifracs = set_xticks_pifracs
    if not hasattr(mpl.axes.Axes, 'set_yticks_pifracs'):
        mpl.axes.Axes.set_yticks_pifracs = set_yticks_pifracs
    if not hasattr(mpl.axes.Axes, 'set_xticks_format'):
        mpl.axes.Axes.set_xticks_format = set_xticks_format
    if not hasattr(mpl.axes.Axes, 'set_yticks_format'):
        mpl.axes.Axes.set_yticks_format = set_yticks_format
    if not hasattr(mpl.axes.Axes, 'set_xticks_blank'):
        mpl.axes.Axes.set_xticks_blank = set_xticks_blank
    if not hasattr(mpl.axes.Axes, 'set_yticks_blank'):
        mpl.axes.Axes.set_yticks_blank = set_yticks_blank
    if not hasattr(mpl.axes.Axes, 'set_xticks_off'):
        mpl.axes.Axes.set_xticks_off = set_xticks_off
    if not hasattr(mpl.axes.Axes, 'set_yticks_off'):
        mpl.axes.Axes.set_yticks_off = set_yticks_off
    if not hasattr(mpl.axes.Axes, 'set_minor_xticks_off'):
        mpl.axes.Axes.set_minor_xticks_off = set_minor_xticks_off
    if not hasattr(mpl.axes.Axes, 'set_minor_yticks_off'):
        mpl.axes.Axes.set_minor_yticks_off = set_minor_yticks_off


def uninstall_ticks():
    """ Uninstall ticks functions from matplotlib axes.

    Call this function to disable anything that was installed by `install_ticks()`.

    See also
    --------
    - `install_ticks()`
    """
    if hasattr(mpl.axes.Axes, 'set_xticks_delta'):
        delattr(mpl.axes.Axes, 'set_xticks_delta')
    if hasattr(mpl.axes.Axes, 'set_yticks_delta'):
        delattr(mpl.axes.Axes, 'set_yticks_delta')
    if hasattr(mpl.axes.Axes, 'set_xticks_log'):
        delattr(mpl.axes.Axes, 'set_xticks_log')
    if hasattr(mpl.axes.Axes, 'set_yticks_log'):
        delattr(mpl.axes.Axes, 'set_yticks_log')
    if hasattr(mpl.axes.Axes, 'set_xticks_fixed'):
        delattr(mpl.axes.Axes, 'set_xticks_fixed')
    if hasattr(mpl.axes.Axes, 'set_yticks_fixed'):
        delattr(mpl.axes.Axes, 'set_yticks_fixed')
    if hasattr(mpl.axes.Axes, 'set_xticks_prefix'):
        delattr(mpl.axes.Axes, 'set_xticks_prefix')
    if hasattr(mpl.axes.Axes, 'set_yticks_prefix'):
        delattr(mpl.axes.Axes, 'set_yticks_prefix')
    if hasattr(mpl.axes.Axes, 'set_xticks_fracs'):
        delattr(mpl.axes.Axes, 'set_xticks_fracs')
    if hasattr(mpl.axes.Axes, 'set_yticks_fracs'):
        delattr(mpl.axes.Axes, 'set_yticks_fracs')
    if hasattr(mpl.axes.Axes, 'set_xticks_pifracs'):
        delattr(mpl.axes.Axes, 'set_xticks_pifracs')
    if hasattr(mpl.axes.Axes, 'set_yticks_pifracs'):
        delattr(mpl.axes.Axes, 'set_yticks_pifracs')
    if hasattr(mpl.axes.Axes, 'set_xticks_format'):
        delattr(mpl.axes.Axes, 'set_xticks_format')
    if hasattr(mpl.axes.Axes, 'set_yticks_format'):
        delattr(mpl.axes.Axes, 'set_yticks_format')
    if hasattr(mpl.axes.Axes, 'set_xticks_blank'):
        delattr(mpl.axes.Axes, 'set_xticks_blank')
    if hasattr(mpl.axes.Axes, 'set_yticks_blank'):
        delattr(mpl.axes.Axes, 'set_yticks_blank')
    if hasattr(mpl.axes.Axes, 'set_xticks_off'):
        delattr(mpl.axes.Axes, 'set_xticks_off')
    if hasattr(mpl.axes.Axes, 'set_yticks_off'):
        delattr(mpl.axes.Axes, 'set_yticks_off')
    if hasattr(mpl.axes.Axes, 'set_minor_xticks_off'):
        delattr(mpl.axes.Axes, 'set_minor_xticks_off')
    if hasattr(mpl.axes.Axes, 'set_minor_yticks_off'):
        delattr(mpl.axes.Axes, 'set_minor_yticks_off')


install_ticks()

    
def demo():
    """ Run a demonstration of the ticks module.
    """
    install_ticks()
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
    
    plt.show()
    uninstall_ticks()


if __name__ == "__main__":
    demo()
