"""
Remove specific artists from an axes.


## Axes member functions

- `remove_lines()`: remove all line artists.
- `remove_markers()`: remove all line artists with markers that are not connected by lines.
- `remove_style()`: remove all line artists that match a style.
- `remove_texts()`: remove text artists.
- `remove_arrows()`: remove arrow, i.e. annotation artists.


## Install/uninstall remove functions

You usually do not need to call the `install_remove()` function. Upon
loading the remove module, `install_remove()` is called automatically.

- `install_remove()`: install functions of the remove module in matplotlib.
- `uninstall_remove()`: uninstall all code of the remove module from matplotlib.
"""

import matplotlib as mpl


def remove_lines(ax):
    """Remove all line artists.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which lines should be removed.
    """
    for line in ax.get_lines():
        line.remove()


def remove_markers(ax):
    """Remove all line artists with markers that are not connected by lines.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which lines should be removed.
    """
    remove_lines = []
    for line in ax.get_lines():
        if line.get_marker() != 'None' and line.get_linestyle() == 'None':
            remove_lines.append(line)
    for line in remove_lines:
        line.remove()


def remove_style(ax, **style):
    """Remove all line artists that match a style.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which lines should be removed.
    style: dict
       Line style (color, linewidth, marker, makeredgecolor, etc.)
    """
    remove_lines = []
    for line in ax.get_lines():
        same = True
        for k in style:
            if k == 'color' and line.get_color() != style[k]:
                same = False
            elif k in ['linestyle', 'ls'] and line.get_linestyle() != style[k]:
                same = False
            elif k in ['linewidth', 'lw'] and line.get_linewidth() != style[k]:
                same = False
            elif k == 'marker' and line.get_marker() != style[k]:
                same = False
            elif k in ['markeredgecolor', 'mec'] and line.get_markeredgecolor() != style[k]:
                same = False
            elif k in ['markeredgewidth', 'mew'] and line.get_markeredgewidth() != style[k]:
                same = False
            elif k in ['markerfacecolor', 'mfc'] and line.get_markerfacecolor() != style[k]:
                same = False
            elif k in ['markersize', 'ms'] and line.get_markersize() != style[k]:
                same = False
            elif k == 'alpha' and line.get_alpha() != style[k]:
                same = False
            elif k == 'zorder' and line.get_zorder() != style[k]:
                same = False
            elif k == 'label' and line.get_label() != style[k]:
                same = False
        if same:
            remove_lines.append(line)
    for line in remove_lines:
        line.remove()


def remove_texts(ax, *indices):
    """Remove text artists.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which texts should be removed.
    indices: list of int or str
       If specified, remove only the text elements at the specified indices
       or with the specified text.
    """
    texts = []
    for i in indices:
        if not isinstance(i, int):
            texts.append(i)
    remove_text = []
    count = 0
    for a in ax.get_children():
        if type(a) is mpl.text.Text:
            if len(indices) == 0 or count in indices or a.get_text() in texts:
                remove_text.append(a)
            count += 1
    for text in remove_text:
        try:
            text.remove()
        except NotImplementedError:
            text.set_visible(False)


def remove_arrows(ax, *indices):
    """Remove arrow, i.e. annotation artists.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which arrows should be removed.
    indices: list of int or str
       If specified, remove only the annotation elements at the specified indices
       or with the specified text.
    """
    texts = []
    for i in indices:
        if not isinstance(i, int):
            texts.append(i)
    remove_text = []
    count = 0
    for a in ax.get_children():
        if isinstance(a, mpl.text.Annotation):
            if len(indices) == 0 or count in indices or a.get_text() in texts:
                remove_text.append(a)
            count += 1
    for text in remove_text:
        try:
            text.remove()
        except NotImplementedError:
            text.set_visible(False)


def install_remove():
    """ Install remove functions on matplotlib axes.
    ```

    This function is also called automatically upon importing the module.

    See also
    --------
    uninstall_remove()
    """
    if not hasattr(mpl.axes.Axes, 'remove_lines'):
        mpl.axes.Axes.remove_lines = remove_lines
    if not hasattr(mpl.axes.Axes, 'remove_markers'):
        mpl.axes.Axes.remove_markers = remove_markers
    if not hasattr(mpl.axes.Axes, 'remove_style'):
        mpl.axes.Axes.remove_style = remove_style
    if not hasattr(mpl.axes.Axes, 'remove_texts'):
        mpl.axes.Axes.remove_texts = remove_texts
    if not hasattr(mpl.axes.Axes, 'remove_arrows'):
        mpl.axes.Axes.remove_arrows = remove_arrows

        
def uninstall_remove():
    """ Uninstall remove functions from matplotlib axes.

    Call this code to disable anything that was installed by `install_remove()`.

    See also
    --------
    install_remove()
    """
    if hasattr(mpl.axes.Axes, 'remove_lines'):
        delattr(mpl.axes.Axes, 'remove_lines')
    if hasattr(mpl.axes.Axes, 'remove_markers'):
        delattr(mpl.axes.Axes, 'remove_markers')
    if hasattr(mpl.axes.Axes, 'remove_style'):
        delattr(mpl.axes.Axes, 'remove_style')
    if hasattr(mpl.axes.Axes, 'remove_texts'):
        delattr(mpl.axes.Axes, 'remove_texts')
    if hasattr(mpl.axes.Axes, 'remove_arrows'):
        delattr(mpl.axes.Axes, 'remove_arrows')


install_remove()

       

