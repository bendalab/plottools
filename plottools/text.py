"""
Enhance textual annotations.


## Enhanced axes member functions

- `text()`: text function with slope parameter and LaTeX support.
- `legend()`: legend function with LaTeX support.


## Functions

- `translate_latex_text()`: translate text to fit both normal and LaTeX mode.


## Install/uninstall text functions

You usually do not need to call these functions. Upon loading the text
module, `install_text()` is called automatically.

- `install_text()`: install functions of the text module in matplotlib.
- `uninstall_text()`: uninstall all code of the text module from matplotlib.
"""

import types
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def translate_latex_text(s, **kwargs):
    """ Translate text to fit both normal and LaTeX mode.
    
    In LaTeX mode (`text.usetex = True`) translate `fontstyle` and
    `fontweight` arguments to corresponding LaTeX commands. Escape
    special characters '%', '#', '&'.

    In non-LaTeX mode translate '\\,' to thin space, '\\micro' to
    upright micro character.

    Parameters
    ----------
    s: string
        The text.
    kwargs: dict
        Key-word arguments for the text.
    fontstyle: string
        In LaTeX mode, if set to `italic` put text into '\\textit{}' command.
    fontweight: string
        In LaTeX mode, if set to `bold` put text into '\\textbf{}' command.

    Returns
    -------
    s: string
        Translated text.
    kwargs: dict
        Updated and adapted key-word arguments.
    """
    # italics and bold LaTeX font:
    if mpl.rcParams['text.usetex']:
        s = s.replace('%', r'\%')
        s = s.replace('#', r'\#')
        s = s.replace('&', r'\&')
        if 'fontstyle' in kwargs and kwargs['fontstyle'] == 'italic':
            del kwargs['fontstyle']
            s = r'\textit{' + s + r'}'
        if 'fontweight' in kwargs and kwargs['fontweight'] == 'bold':
            del kwargs['fontweight']
            s = r'\textbf{' + s + r'}'
    else:
        s = s.replace(r'\,', u'\u2009')
        s = s.replace(r'\micro{}', u'\u00B5')
        s = s.replace(r'\micro ', u'\u00B5')
        s = s.replace(r'\micro', u'\u00B5')
    return s, kwargs


def text(ax, x, y, s, *args, slope=None, **kwargs):
    """ Text function with slope parameter and LaTeX support.

    Adds an optional slope parameter that rotates the text to a specified slope.
    Uses `translate_latex_text ()` to improve LaTeX mode.

    Parameters
    ----------
    Same as `mpl.axes.Axes.text()`.

    slope: float or None
        Slope to which the text should be rotated. If not otherwise specified set
        `rotation_mode` to 'anchor'.
    """
    s, kwargs = translate_latex_text(s, **kwargs)
    # set text:
    txt = ax.__text_orig_text(x, y, s, *args, **kwargs)
    # align text on slope:
    if slope is not None:

        def __text_set_rotation(self, rotation):
            pass

        def __text_get_rotation(self):
            angle = np.rad2deg(np.arctan2(self.slope, 1.0))
            trans_angle = ax.transData.transform_angles(np.array((angle,)),
                            np.array(self.get_position()).reshape((1, 2)))[0]
            return trans_angle
        
        if 'rotation' in kwargs:
            del kwargs['rotation']
        if 'rotation_mode' not in kwargs:
            kwargs.update({'rotation_mode': 'anchor'})
        txt.slope = slope
        txt.ax = ax
        txt.set_rotation = types.MethodType(__text_set_rotation, txt)
        txt.get_rotation = types.MethodType(__text_get_rotation, txt)
    return txt


def legend(ax, *args, **kwargs):
    """ Legend function with LaTeX support.
    
    Uses `translate_latex_text ()` to improve LaTeX mode of legend
    labels.

    Parameters
    ----------
    Same as `mpl.axes.Axes.legend()`.
    """
    handles, labels = ax.get_legend_handles_labels()
    for k in range(len(labels)):
        labels[k], newkwargs = translate_latex_text(labels[k], **kwargs)
    lgd = ax.__legend_orig_text(handles, labels, *args, **newkwargs)
    return lgd


def install_text():
    """ Patch the `mpl.axes.Axes.text()` and `mpl.axes.Axes.legend()` functions.

    See also
    --------
    `uninstall_text()`
    """
    if not hasattr(mpl.axes.Axes, '__text_orig_text'):
        mpl.axes.Axes.__text_orig_text = mpl.axes.Axes.text
        mpl.axes.Axes.text = text
    if not hasattr(mpl.axes.Axes, '__legend_orig_text'):
        mpl.axes.Axes.__legend_orig_text = mpl.axes.Axes.legend
        mpl.axes.Axes.legend = legend


def uninstall_text():
    """ Uninstall code for text.

    Call this code to disable anything that was installed by `install_text()`.

    See also
    --------
    `install_text()`
    """
    if hasattr(mpl.axes.Axes, '__text_orig_text'):
        mpl.axes.Axes.text = mpl.axes.Axes.__text_orig_text
        delattr(mpl.axes.Axes, '__text_orig_text')
    if hasattr(mpl.axes.Axes, '__legend_orig_text'):
        mpl.axes.Axes.legend = mpl.axes.Axes.__legend_orig_text
        delattr(mpl.axes.Axes, '__legend_orig_text')

                
install_text()


def demo(usetex=False):
    """ Run a demonstration of the text module.

    Parameters
    ----------
    usetex: bool
        If `True` use LaTeX mode.
    """
    mpl.rcParams['text.usetex'] = usetex
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{SIunits}']
    fig, ax = plt.subplots()
    slope1 = 0.5
    slope2 = 0.2
    x = np.linspace(0, 2, 10)
    ax.plot(x, slope1*x-0.2, label='0.2\,\micro m')
    ax.plot(x, slope2*x+0.1, label='whatever')
    ax.text(1.5, 0.57, 'Steep', slope=slope1)
    ax.text(1.5, 0.4, 'Shallow', slope=slope2)
    ax.legend(loc='upper left')
    ax.text(0.05, 0.7, "ax.text(1, 0.3, 'Steep', slope=0.5)", transform=ax.transAxes)
    ax.text(0.05, 0.6, "ax.text(1, 0.2, 'Shallow', slope=0.2)", transform=ax.transAxes)
    ax.text(0.5, 0.0, 'Italic', fontstyle='italic')
    ax.text(0.5, -0.1, 'Bold', fontweight='bold')
    ax.text(0.8, 0.0, "ax.text(0.7, 0.0, 'Italic', fontstyle='italic')")
    ax.text(0.8, -0.1, "ax.text(0.7, -0.1, 'Bold', fontweight='bold')")
    plt.show()
    

if __name__ == "__main__":
    demo()


