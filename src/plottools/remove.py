"""
Remove specific artists from an axes.


## Axes member functions

- `remove_lines()`: remove all line artists without marker.
- `remove_markers()`: remove all line artist with markers that are not connected by lines.


## Install/uninstall remove functions

You usually do not need to call the `install_remove()` function. Upon
loading the remove module, `install_remove()` is called automatically.

- `install_remove()`: install functions of the remove module in matplotlib.
- `uninstall_remove()`: uninstall all code of the remove module from matplotlib.
"""


def remove_lines(ax):
    """Remove all line artists that are lines without a marker.

    Parameters
    ----------
    ax: matplotlib axes
       Axes from which lines should be removed.
    """
    remove_lines = []
    for line in ax.get_lines():
        if line.get_marker() == 'None':
            remove_lines.append(line)
    for line in remove_lines:
        ax.remove(line)


def remove_markers(ax):
    """Remove all line artist with markers that are not connected by lines.

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
        ax.remove(line)


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
        mpl.axes.Axes.remove_lines = remove_markers

        
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


install_remove()

       

