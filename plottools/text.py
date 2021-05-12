"""
Enhance textual annotations.


## Enhanced axes member functions

- `text()`: text function with slope parameter and LaTeX support.


## Settings

- `text_params()`: set default parameter for the text module.


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
from .latex import translate_latex_text


def text(ax, x, y, s, *args, slope=None, **kwargs):
    """ Text function with slope parameter and LaTeX support.

    Adds an optional slope parameter that rotates the text to a specified slope.
    Uses `latex.translate_latex_text()` to improve LaTeX mode.

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


def text_params(font_size=None, font_family=None, latex=None, preamble=None):
    """ Set default parameter for the text module.
                  
    Only parameters that are not `None` are updated.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    font_size: float
        Set font size for text in points (rcParam `font.size`).
    font_family: string
        Set name of font to be used (rcParam `font.family`).
    latex: boolean
        Use LaTeX for setting text and enable unicode support
        when set to `True` (rcParam `text.usetex`).
    preamble: sequence of strings
        Lines for the latex preamble (rcParam `text.latex.preamble`).
        For convinience, strings starting with 'p:xxx'
        are translated into '\\usepackage{xxx}', strings starting with
        'p:[yyy]xxx' are translated into '\\usepackage[yyy]{xxx}'.
    """
    if font_size is not None:
        mpl.rcParams['font.size'] = font_size
    if font_family is not None:
        mpl.rcParams['font.family'] = font_family
    if latex is not None:
        mpl.rcParams['text.usetex'] = latex
        if latex:
            """
            mpl.rcParams['font.serif'] = ['Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'Computer Modern Roman']
            mpl.rcParams['font.sans-serif'] = ['Helvetica', 'Avant Garde', 'Computer Modern Sans serif']
            mpl.rcParams['font.cursive'] = ['Zapf Chancery']
            mpl.rcParams['font.monospace'] = ['Courier', 'Computer Modern Typewriter']
            """
            if 'text.latex.unicode' in mpl.rcParams and int(mpl.__version__.split('.')[0]) < 3:
                mpl.rcParams['text.latex.unicode'] = True
    if preamble is not None:
        header = []
        for line in preamble:
            if len(line) > 3:
                if line[:3] == 'p:[':
                    i = line.find(']')
                    if i > 2:
                        line = r'\usepackage[%s]{%s}' % (line[3:i], line[i+1:])
                elif line[:2] == 'p:':
                    line = r'\usepackage{%s}' % line[2:]
            header.append(line)
        mpl.rcParams['text.latex.preamble'] = '\n'.join(header)


def install_text():
    """ Patch the `mpl.axes.Axes.text()` function.

    See also
    --------
    `uninstall_text()`
    """
    if not hasattr(mpl.axes.Axes, '__text_orig_text'):
        mpl.axes.Axes.__text_orig_text = mpl.axes.Axes.text
        mpl.axes.Axes.text = text
    

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

                
install_text()


def demo(usetex=False):
    """ Run a demonstration of the text module.

    Parameters
    ----------
    usetex: bool
        If `True` use LaTeX mode.
    """
    text_params(font_size=12, latex=usetex, preamble=r'\usepackage{SIunits}')
    fig, ax = plt.subplots()
    slope1 = 0.5
    slope2 = 0.2
    x = np.linspace(0, 2, 10)
    ax.plot(x, slope1*x-0.2)
    ax.plot(x, slope2*x+0.1)
    ax.text(1.5, 0.57, 'Steep', slope=slope1)
    ax.text(1.5, 0.4, 'Shallow', slope=slope2)
    ax.text(0.05, 0.7, "ax.text(1, 0.3, 'Steep', slope=0.5)", transform=ax.transAxes)
    ax.text(0.05, 0.6, "ax.text(1, 0.2, 'Shallow', slope=0.2)", transform=ax.transAxes)
    ax.text(0.5, 0.0, 'Italic', fontstyle='italic')
    ax.text(0.5, -0.1, 'Bold', fontweight='bold')
    ax.text(0.8, 0.0, "ax.text(0.7, 0.0, 'Italic', fontstyle='italic')")
    ax.text(0.8, -0.1, "ax.text(0.7, -0.1, 'Bold', fontweight='bold')")
    plt.show()
    

if __name__ == "__main__":
    demo()


