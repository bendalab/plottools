"""
# Plot format

Layout settings for a plot figure.

- `plot_format()`: set default plot format.
- `cm_size()`: convert dimensions from cm to inch.
"""

import matplotlib as mpl


def plot_format(fontsize=10.0):
    """ Set default plot format.

    Parameters
    ----------
    fontsize: float
        Fontsize for text in points.
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


def cm_size(width, height):
    """ Convert dimensions from cm to inch.

    Parameters
    ----------
    width: float
        Width of the plot figure in centimeter.
    height: float
        Height of the plot figure in centimeter.

    Returns
    -------
    width: float
        Width of the plot figure in inch.
    height: float
        Height of the plot figure in inch.
    """
    inch_fac = 2.54
    return width/inch_fac, height/inch_fac


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plot_format()
    fig, ax = plt.subplots(figsize=cm_size(16.0, 10.0))
    plt.show()
