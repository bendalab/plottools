"""
Setting axes appearance.


## Settings

- `axes_params()`: set rc settings for axes.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt


def axes_params(xmargin=None, ymargin=None, zmargin=None, color=None):
    """ Set rc settings for axes.

    Only parameters that are not `None` are updated.

    Parameters
    ----------
    xmargin: float
        Padding added to x-axis limits in fractions of the data interval.
        Sets rcParam `axes.xmargin`.
    ymargin: float
        Padding added to y-axis limits in fractions of the data interval.
        Sets rcParam `axes.ymargin`.
    zmargin: float
        Padding added to z-axis limits in fractions of the data interval.
        Sets rcParam `axes.zmargin`.
    color: matplotlib color or 'none'
        Background color for each subplot.
        Sets rcParam `axes.facecolor`.
        For setting the backround color of a given axes, use
        ```
        ax.set_facecolor(color)
        ```
    """
    if xmargin is not None:
        mpl.rcParams['axes.xmargin'] = xmargin
    if ymargin is not None:
        mpl.rcParams['axes.ymargin'] = ymargin
    if 'axes.zmargin' in mpl.rcParams and zmargin is not None:
        mpl.rcParams['axes.zmargin'] = zmargin
    if color is not None:
        mpl.rcParams['axes.facecolor'] = color


def demo():
    """ Run a demonstration of the axes module.
    """
    axes_params(xmargin=0, ymargin=0)
    fig, ax = plt.subplots()
    fig.suptitle('plottools.axes')
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')
    ax.text(0.1, 0.7, 'axes_params(xmargin=0, ymargin=0)', transform=ax.transAxes)
    plt.show()
        

if __name__ == "__main__":
    demo()
