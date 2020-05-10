"""
# Text

Enhance textual annotations.

- `install_text()`: patch the mpl.axes.Axes.text() function.
- `uninstall_text()`: uninstall code for text.
"""

import types
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def text(ax, x, y, s, *args, slope=None, **kwargs):
    """ Enhanced text function.

    Adds an optional slope parameter that rotates the text to a specified slope.

    In LaTeX mode (`text.usetex = True`) translate `fontstyle` and
    `fontweight` arguments to corresponding LaTeX commands. Escape
    special characters '%', '#', '&'.

    In non-LaTeX mode translate '\,' to thin space, '\micro' to micro character.

    Parameters
    ----------
    Same as mpl.axes.Axes.text().

    slope: float or None
        Slope to which the text should be rotated. If not otherwise specified set
        `rotation_mode` to 'anchor'.
    fontstyle:
        In LaTeX mode, if set to `italic` put text into `\textit{}` command.
    fontweight:
        In LaTeX mode, if set to `bold` put text into `\textbf{}` command.
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
        s = s.replace(r'\micro', u'\u00B5')
    # set text:
    txt = ax.__text_orig_text(x, y, s, *args, **kwargs)
    # align text on slope:
    if slope is not None:

        def __text_set_rotation(self, rotation):
            pass

        def __text_get_rotation(self):
            angle = np.rad2deg(np.arctan2(self.slope, 1.0))
            trans_angle = self.get_axes().transData.transform_angles(np.array((angle,)),
                                        np.array(self.get_position()).reshape((1, 2)))[0]
            return trans_angle
        
        if 'rotation' in kwargs:
            del kwargs['rotation']
        if 'rotation_mode' not in kwargs:
            kwargs.update({'rotation_mode': 'anchor'})
        txt.slope = slope
        txt.set_rotation = types.MethodType(__text_set_rotation, txt)
        txt.get_rotation = types.MethodType(__text_get_rotation, txt)
    return txt


def install_text():
    """ Patch the mpl.axes.Axes.text() function.

    See also
    --------
    uninstall_figure()
    """
    if not hasattr(mpl.axes.Axes, '__text_orig_text'):
        mpl.axes.Axes.__text_orig_text = mpl.axes.Axes.text
        mpl.axes.Axes.text = text


def uninstall_text():
    """ Uninstall code for text.

    Call this code to disable anything that was installed by install_text().
    """
    if hasattr(mpl.axes.Axes, '__text_orig_text'):
        mpl.axes.Axes.text = mpl.axes.Axes.__text_orig_text
        delattr(mpl.axes.Axes, '__text_orig_text')
        
    
def demo():
    """ Run a demonstration of the text module.
    """
    mpl.rcParams['text.usetex'] = True
    install_text()
    fig, ax = plt.subplots()
    slope1 = 0.5
    slope2 = 0.2
    x = np.linspace(0, 2, 10)
    ax.plot(x, slope1*x-0.2)
    ax.plot(x, slope2*x+0.1)
    ax.text(1.5, 0.57, 'Steep', slope=slope1)
    ax.text(1.5, 0.4, 'Shallow', slope=slope2)
    ax.text(0.05, 0.9, "ax.text(1, 0.3, 'Steep', slope=0.5)", transform=ax.transAxes)
    ax.text(0.05, 0.8, "ax.text(1, 0.2, 'Shallow', slope=0.2)", transform=ax.transAxes)
    ax.text(0.5, 0.0, 'Italic', fontstyle='italic')
    ax.text(0.5, -0.1, 'Bold', fontweight='bold')
    ax.text(0.8, 0.0, "ax.text(0.7, 0.0, 'Italic', fontstyle='italic')")
    ax.text(0.8, -0.1, "ax.text(0.7, -0.1, 'Bold', fontweight='bold')")
    plt.show()
    uninstall_text()
    

if __name__ == "__main__":
    demo()


