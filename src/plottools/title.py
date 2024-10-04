"""
Enhance title text.


## Enhanced axes member functions

- `set_title()`: title with LaTeX support.


## Settings

- `title_params()`: set default parameter for the title module.


## Install/uninstall title functions

You usually do not need to call these functions. Upon loading the title
module, `install_title()` is called automatically.

- `install_title()`: install functions of the title module in matplotlib.
- `uninstall_title()`: uninstall all code of the title module from matplotlib.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from .latex import translate_latex_text


def set_title(ax, label, *args, **kwargs):
    """ Title with LaTeX support.
    
    Uses `latex.translate_latex_text()` to improve LaTeX mode of title.

    Parameters
    ----------
    Same as `mpl.axes.Axes.set_title()`.
    """
    s, kwargs = translate_latex_text(label, **kwargs)
    txt = ax.__set_title_orig_title(s, *args, **kwargs)
    return txt


def title_params(fontsize=None, fontweight=None, location=None,
                 color=None, ypos=None, pad=None,):
    """Set default parameter for the title module.
                  
    Only parameters that are not `None` are updated.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    fontsize: float or string
        Set font size for title. Either the font size in points,
        or a string like 'medium', 'small', 'x-small', 'large', 'x-large'.
        Sets rcParam `axes.titlesize`.
    fontweight: int or string
        Set weight of title font. A numeric value in range 0-1000,
        'ultralight', 'light', 'normal', 'regular', 'book', 'medium',
        'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy',
        'extra bold', 'black'
        Sets rcParam `axes.titleweight`.
    location: string
        Location of the title. One of 'left', 'right', 'center'.
        Sets rcParam `axes.titlelocation`.
    color: matplotlib color
        Color of the title or 'auto'.
        Sets rcParam `axes.titlecolor`.
    ypos: float or 'auto'
        Position title in axes relative units. 'auto' is auto positioning.
        Sets rcParam `axes.titley`.
    pad: float or string
        Pad between axes and title in points.
        Sets rcParam `axes.titlepad`.

    """
    if fontsize is not None:
        mpl.rcParams['axes.titlesize'] = fontsize
    if fontweight is not None:
        mpl.rcParams['axes.titleweight'] = fontweight
    if location is not None:
        mpl.rcParams['axes.titlelocation'] = location
    if color is not None:
        mpl.rcParams['axes.titlecolor'] = color
    if ypos is not None:
        if ypos == 'auto':
            ypos = None
        mpl.rcParams['axes.titley'] = ypos
    if pad is not None:
        mpl.rcParams['axes.titlepad'] = pad


def install_title():
    """ Patch the `mpl.axes.Axes.set_title()` function.

    See also
    --------
    uninstall_title()
    """
    if not hasattr(mpl.axes.Axes, '__set_title_orig_title'):
        mpl.axes.Axes.__set_title_orig_title = mpl.axes.Axes.set_title
        mpl.axes.Axes.set_title = set_title
    

def uninstall_title():
    """Uninstall code for title.

    Call this function to disable anything that was installed by
    `install_title()`.

    See also
    --------
    install_title()

    """
    if hasattr(mpl.axes.Axes, '__set_title_orig_title'):
        mpl.axes.Axes.set_title = mpl.axes.Axes.__set_title_orig_title
        delattr(mpl.axes.Axes, '__set_title_orig_title')

                
install_title()

