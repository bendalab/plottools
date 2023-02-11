"""
Electrical circuits.

## Axes member functions

- `resistance_h()`: draw a horizontal resistance.
- `resistance_v()`: draw a vertical resistance.
- `resistance()`: draw an arbitrarily rotated resistance.
- `capacitance_h()`: draw a horizontal capacitance.
- `capacitance_v()`: draw a vertical capacitance.
- `battery_h()`: draw a horizontal battery (voltage source).
- `battery_v()`: draw a vertical battery (voltage source).
- `ground()`: draw ground.
- `opamp_l()`: draw an operational amplifier with inputs on the left.
- `opamp_l()`: draw an operational amplifier with inputs on the right.
- `node()`: draw a node connecting lines.
- `connect()`: draw lines directly connecting circuit elements.
- `connect_straight()`: draw straight lines connecting circuit elements.


## Classes

- `class Pos`: x and y coordinate of a circuit element.


## Settings

- `circuits_params()`: set rc settings for circuits.

`matplotlib.rcParams` defined by the circuits module:
```py
circuits.scale: 1
circuits.connectwidth: 1
circuits.linewidth: 2
circuits.color: 'black'
circuits.facecolor: 'white'
circuits.alpha: 1
circuits.zorder: 100
circuits.font: dict()
```


## Install/uninstall circuits functions

You usually do not need to call these functions. Upon loading the circuits
module, `install_circuits()` is called automatically.

- `install_circuits()`: install functions of the circuits module in matplotlib.
- `uninstall_circuits()`: uninstall all code of the circuits module from matplotlib.

"""

import numpy as np
import matplotlib as mpl
import matplotlib.transforms as mpt
import matplotlib.rcsetup as mrc
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from .rcsetup import _validate_fontdict


class Pos(tuple):
    """ x and y coordinate of a circuit element.
    """

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def x(self):
        """ x coordinate of the circuit element.

        Returns
        -------
        x: float
            x-coordinate
        """
        return self[0]

    def y(self):
        """ y coordinate of the circuit element.

        Returns
        -------
        y: float
            y-coordinate
        """
        return self[1]

    def up(self, delta=1):
        """ Increment y coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Increment in data coordinates.

        Returns
        -------
        pos: Pos
            Incremented copy of position of circuit element.
        """
        return Pos(self[0], self[1] + delta)

    def down(self, delta=1):
        """ Decrement y coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Decrement in data coordinates.

        Returns
        -------
        pos: Pos
            Decremented copy of position of circuit element.
        """
        return Pos(self[0], self[1] - delta)

    def left(self, delta=1):
        """ Decrement x coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Decrement in data coordinates.

        Returns
        -------
        pos: Pos
            Decremented copy of position of circuit element.
        """
        return Pos(self[0] - delta, self[1])

    def right(self, delta=1):
        """ Increment x coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Increment in data coordinates.

        Returns
        -------
        pos: Pos
            Incremented copy of position of circuit element.
        """
        return Pos(self[0] + delta, self[1])

    def ups(self, delta=1):
        """ Increment y coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Increment in multiples of circuits scale (rcParam `circuits.scale`).

        Returns
        -------
        pos: Pos
            Incremented copy of position of circuit element.
        """
        return Pos(self[0], self[1] + delta*mpl.rcParams['circuits.scale'])

    def downs(self, delta=1):
        """ Decrement y coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Decrement in multiples of circuits scale (rcParam `circuits.scale`).

        Returns
        -------
        pos: Pos
            Decremented copy of position of circuit element.
        """
        return Pos(self[0], self[1] - delta*mpl.rcParams['circuits.scale'])

    def lefts(self, delta=1):
        """ Decrement x coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Decrement in multiples of circuits scale (rcParam `circuits.scale`).

        Returns
        -------
        pos: Pos
            Decremented copy of position of circuit element.
        """
        return Pos(self[0] - delta*mpl.rcParams['circuits.scale'], self[1])

    def rights(self, delta=1):
        """ Increment x coordinate of position of circuit element.

        Parameters
        ----------
        delta: float
            Increment in multiples of circuits scale (rcParam `circuits.scale`).

        Returns
        -------
        pos: Pos
            Incremented copy of position of circuit element.
        """
        return Pos(self[0] + delta*mpl.rcParams['circuits.scale'], self[1])


def resistance_h(ax, pos, label='', align='above', lw=None,
                 color=None, facecolor=None, alpha=None, zorder=None,
                 **kwargs):
    """ Draw a horizontal resistance.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the resistance bar.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the resistance.
    label: string
        Optional label for the resistance.
    align: 'above', 'below', 'center'
        Position the label above, below or in the center of the resistance.
    lw: float, int
        Linewidth for drawing the outline of the resistance.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the resistance.
        Defaults to `circuits.color` rcParams settings.
    facecolor matplotlib color
        Color for filling the resistance.
        Defaults to `circuits.facecolor` rcParams settings.
    alpha: float
        Alpha value for the face color.
        Defaults to `circuits.alpha` rcParams settings.
    zorder: int
        zorder for the resistance and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posl: Pos
        Coordinates of the left end of the resistance.
    posr: Pos
        Coordinates of the right end of the resistance.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if facecolor is None:
        facecolor = mpl.rcParams['circuits.facecolor']
    if alpha is None:
        alpha = mpl.rcParams['circuits.alpha']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']
    h = 0.5*mpl.rcParams['circuits.scale']
    x, y = pos
    ax.add_patch(Rectangle((x - 0.5*w, y - 0.5*h), w, h,
                           zorder=zorder, edgecolor='none',
                           facecolor=facecolor, alpha=alpha))
    ax.add_patch(Rectangle((x - 0.5*w, y - 0.5*h), w, h,
                           zorder=zorder+1, edgecolor=color,
                           facecolor='none', lw=lw))
    if label:
        if align == 'above':
            yy = 0.8*h
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'bottom'
        elif align == 'below':
            yy = -0.8*h
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'top'
        elif align == 'center':
            yy = 0
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'center'
        else:
            raise ValueError('align must be one of "above", "bottom", or "center"')
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'center'
        ax.text(x, y + yy, label, zorder=zorder+1, **kwargs)
    return Pos(x - 0.5*w, y), Pos(x + 0.5*w, y)


def resistance_v(ax, pos, label='', align='right', lw=None, color=None,
                 facecolor=None, alpha=None, zorder=None, **kwargs):
    """ Draw a vertical resistance.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the resistance.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the resistance.
    label: string
        Optional label for the resistance.
    align: 'left', 'right', 'center'
        Position the label to th left, right or in the center of the resistance.
    lw: float, int
        Linewidth for drawing the outline of the resistance.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the resistance.
        Defaults to `circuits.color` rcParams settings.
    facecolor matplotlib color
        Color for filling the resistance.
        Defaults to `circuits.facecolor` rcParams settings.
    alpha: float
        Alpha value for the face color.
        Defaults to `circuits.alpha` rcParams settings.
    zorder: int
        zorder for the resistance and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posb: Pos
        Coordinates of the bottom end of the resistance.
    post: Pos
        Coordinates of the top end of the resistance.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if facecolor is None:
        facecolor = mpl.rcParams['circuits.facecolor']
    if alpha is None:
        alpha = mpl.rcParams['circuits.alpha']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = 0.5*mpl.rcParams['circuits.scale']
    h = mpl.rcParams['circuits.scale']
    x, y = pos
    ax.add_patch(Rectangle((x - 0.5*w, y - 0.5*h), w, h,
                           zorder=zorder, edgecolor='none',
                           facecolor=facecolor, alpha=alpha))
    ax.add_patch(Rectangle((x - 0.5*w, y - 0.5*h), w, h,
                           zorder=zorder+1, edgecolor=color,
                           facecolor='none', lw=lw))
    if label:
        if align == 'right':
            xx = 0.7*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'left'
        elif align == 'left':
            xx = -0.7*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'right'
        elif align == 'center':
            xx = 0
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'center'
        else:
            raise ValueError('align must be one of "left", "right", or "center"')
        if not 'va' in kwargs and not 'verticalalignment' in kwargs:
            kwargs['va'] = 'center'
        ax.text(x + xx, y, label, zorder=zorder+1, **kwargs)
    return Pos(x, y - 0.5*h), Pos(x, y + 0.5*h)


def resistance(ax, pos, angle=0, label='', align='above', lw=None,
               color=None, facecolor=None, alpha=None, zorder=None,
               **kwargs):
    """Draw an arbitrarily rotated resistance.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the resistance bar.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the resistance.
    angle: float
        Rotation angle in degrees.
    label: string
        Optional label for the resistance.
    align: 'above', 'below', 'center'
        Position the label above, below or in the center of the
        non-rotated resistance.
    lw: float, int
        Linewidth for drawing the outline of the resistance.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the resistance.
        Defaults to `circuits.color` rcParams settings.
    facecolor matplotlib color
        Color for filling the resistance.
        Defaults to `circuits.facecolor` rcParams settings.
    alpha: float
        Alpha value for the face color.
        Defaults to `circuits.alpha` rcParams settings.
    zorder: int
        zorder for the resistance and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posl: Pos
        Coordinates of the left end of the resistance.
    posr: Pos
        Coordinates of the right end of the resistance.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if facecolor is None:
        facecolor = mpl.rcParams['circuits.facecolor']
    if alpha is None:
        alpha = mpl.rcParams['circuits.alpha']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']
    h = 0.5*mpl.rcParams['circuits.scale']
    x, y = pos
    transform = mpt.Affine2D().rotate(np.radians(angle)).translate(*pos)
    ax.add_patch(Rectangle((-0.5*w, -0.5*h), w, h,
                           transform=transform + ax.transData,
                           zorder=zorder, edgecolor='none',
                           facecolor=facecolor, alpha=alpha))
    ax.add_patch(Rectangle((-0.5*w, -0.5*h), w, h,
                           transform=transform + ax.transData,
                           zorder=zorder+1, edgecolor=color,
                           facecolor='none', lw=lw))
    if label:
        if align == 'above':
            pos = np.array(((0, 0.8*h),))
        elif align == 'below':
            pos = np.array(((0, -0.8*h),))
        elif align == 'center':
            pos = np.array(((0, 0),))
        else:
            raise ValueError('align must be one of "above", "bottom", or "center"')
        pos = transform.transform(pos)
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'center'
        ax.text(pos[0,0], pos[0,1], label, zorder=zorder+1, **kwargs)
    nodes = np.array(((-0.5*w, 0), (+0.5*w, 0)))
    nodes = transform.transform(nodes)
    return Pos(*nodes[0,:]),  Pos(*nodes[1,:])


def capacitance_h(ax, pos, label='', align='above', lw=None,
                  color=None, zorder=None, **kwargs):
    """ Draw a horizontal capacitance.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the capacitance.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the capacitance.
    label: string
        Optional label for the capacitance.
    align: 'above', 'below'
        Position the label above or below the capacitance.
    lw: float, int
        Linewidth for drawing the outline of the capacitance.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the capacitance.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the capacitance and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posl: Pos
        Coordinates of the left end of the capacitance.
    posr: Pos
        Coordinates of the right end of the capacitance.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']
    h = mpl.rcParams['circuits.scale']*0.8/3
    x, y = pos
    ax.plot([x - 0.5*h, x - 0.5*h], [y - 0.5*w, y + 0.5*w],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x + 0.5*h, x + 0.5*h], [y - 0.5*w, y + 0.5*w],
            zorder=zorder, lw=lw, color=color)
    if label:
        yy = 0
        if align == 'above':
            yy = 0.6*w
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'bottom'
        elif align == 'below':
            yy = -0.6*w
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'top'
        else:
            raise ValueError('align must be one of "above" or "bottom"')
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'center'
        ax.text(x, y + yy, label, zorder=zorder, **kwargs)
    return Pos(x - 0.5*h, y), Pos(x + 0.5*h, y)


def capacitance_v(ax, pos, label='', align='right', lw=None,
                  color=None, zorder=None, **kwargs):
    """ Draw a vertical capacitance.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the capacitance.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the capacitance.
    label: string
        Optional label for the capacitance.
    align: 'left', 'right'
        Position the label to the left or to the right of the capacitance.
    lw: float, int
        Linewidth for drawing the outline of the capacitance.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the capacitance.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the capacitance and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posb: Pos
        Coordinates of the bottom end of the capacitance.
    post: Pos
        Coordinates of the top end of the capacitance.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']
    h = mpl.rcParams['circuits.scale']*0.8/3
    x, y = pos
    ax.plot([x - 0.5*w, x + 0.5*w], [y + 0.5*h, y + 0.5*h],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x - 0.5*w, x + 0.5*w], [y - 0.5*h, y - 0.5*h],
            zorder=zorder, lw=lw, color=color)
    if label:
        if align == 'right':
            xx = 0.6*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'left'
        elif align == 'left':
            xx = -0.6*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'right'
        else:
            raise ValueError('align must be one of "left" or "right"')
        if not 'va' in kwargs and not 'verticalalignment' in kwargs:
            kwargs['va'] = 'center'
        ax.text(x + xx, y, label, zorder=zorder, **kwargs)
    return Pos(x, y - 0.5*h), Pos(x, y + 0.5*h)


def battery_h(ax, pos, label='', align='above', lw=None, color=None,
              zorder=None, **kwargs):
    """ Draw a horizontal battery (voltage source).

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the battery.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the battery.
    label: string
        Optional label for the battery.
    align: 'above', 'below'
        Position the label above or below the battery.
    lw: float, int
        Linewidth for drawing the outline of the battery.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the battery.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the battery and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posl: Pos
        Coordinates of the left end of the battery.
    posr: Pos
        Coordinates of the right end of the battery.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']*4/3
    h = mpl.rcParams['circuits.scale']*0.8/3
    x, y = pos
    ax.plot([x - 0.5*h, x - 0.5*h], [y - 0.5*w, y + 0.5*w],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x + 0.5*h, x + 0.5*h], [y - 0.25*w, y + 0.25*w],
            zorder=zorder, lw=lw, color=color)
    if label:
        yy = 0
        if align == 'above':
            yy = 0.6*w
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'bottom'
        elif align == 'below':
            yy = -0.6*w
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'top'
        else:
            raise ValueError('align must be one of "above" or "bottom"')
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'center'
        ax.text(x, y + yy, label, zorder=zorder, **kwargs)
    return Pos(x - 0.5*h, y), Pos(x + 0.5*h, y)


def battery_v(ax, pos, label='', align='right', lw=None, color=None,
              zorder=None, **kwargs):
    """ Draw a vertical battery (voltage source).

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the battery.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the battery.
    label: string
        Optional label for the battery.
    align: 'left', 'right'
        Position the label to the left or to the right of the battery.
    lw: float, int
        Linewidth for drawing the outline of the battery.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the battery.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the battery and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    posb: Pos
        Coordinates of the bottom end of the battery.
    post: Pos
        Coordinates of the top end of the battery.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']*4/3
    h = mpl.rcParams['circuits.scale']*0.8/3
    x, y = pos
    ax.plot([x - 0.5*w, x + 0.5*w], [y + 0.5*h, y + 0.5*h],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x - 0.25*w, x + 0.25*w], [y - 0.5*h, y - 0.5*h],
            zorder=zorder, lw=lw, color=color)
    if label:
        if align == 'right':
            xx = 0.6*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'left'
        elif align == 'left':
            xx = -0.6*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'right'
        else:
            raise ValueError('align must be one of "left" or "right"')
        if not 'va' in kwargs and not 'verticalalignment' in kwargs:
            kwargs['va'] = 'center'
        ax.text(x + xx, y, label, zorder=zorder, **kwargs)
    return Pos(x, y - 0.5*h), Pos(x, y + 0.5*h)


def ground(ax, pos, label='', align='right', lw=None, color=None,
           zorder=None, **kwargs):
    """ Draw ground.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the battery.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the battery.
    label: string
        Optional label for the battery.
    align: 'left', 'right'
        Position the label to the left or to the right of the ground.
    lw: float, int
        Linewidth for drawing the outline of the battery.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the battery.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the battery and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    pos: Pos
        Coordinates of the top end of ground.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    w = mpl.rcParams['circuits.scale']*0.8
    h = mpl.rcParams['circuits.scale']*0.17
    x, y = pos
    ax.plot([x - 0.5*w, x + 0.5*w], [y + h, y + h],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x - 0.3*w, x + 0.3*w], [y, y],
            zorder=zorder, lw=lw, color=color)
    ax.plot([x - 0.06*w, x + 0.06*w], [y - h, y - h],
            zorder=zorder, lw=lw, color=color)
    if label:
        if align == 'right':
            xx = 0.7*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'left'
        elif align == 'left':
            xx = -0.7*w
            if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
                kwargs['ha'] = 'right'
        else:
            raise ValueError('align must be one of "left" or "right"')
        if not 'va' in kwargs and not 'verticalalignment' in kwargs:
            kwargs['va'] = 'center'
        ax.text(x + xx, y, label, zorder=zorder, **kwargs)
    return Pos(x, y + h)


def opamp_l(ax, pos, label='', align='above', lw=None, color=None,
            facecolor=None, alpha=None, zorder=None, **kwargs):
    """ Draw an operational amplifier with inputs on the left.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the opamp.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the opamp.
    label: string
        Optional label for the opamp.
    align: 'above', 'below', 'center'
        Position the label above, below or in the center of the opamp.
    lw: float, int
        Linewidth for drawing the outline of the opamp.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the opamp.
        Defaults to `circuits.color` rcParams settings.
    facecolor matplotlib color
        Color for filling the opamp.
        Defaults to `circuits.facecolor` rcParams settings.
    alpha: float
        Alpha value for the face color.
        Defaults to `circuits.alpha` rcParams settings.
    zorder: int
        zorder for the opamp and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    pospos: Pos
        Coordinates of the positive (upper) input of the opamp.
    posneg: Pos
        Coordinates of the negative (lower) input of the opamp.
    posout: Pos
        Coordinates of the output of the opamp.
    posgnd: Pos
        Coordinates of the ground supply of the opamp.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if facecolor is None:
        facecolor = mpl.rcParams['circuits.facecolor']
    if alpha is None:
        alpha = mpl.rcParams['circuits.alpha']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    a = mpl.rcParams['circuits.scale']*5/3
    r = a/2/np.sqrt(3)
    x, y = pos
    xy = np.array([[x - r, y - 0.5*a], [x - r, y + 0.5*a], [x + 2*r, y]])
    ax.add_patch(Polygon(xy, closed=True,
                         zorder=zorder, edgecolor='none',
                         facecolor=facecolor, alpha=alpha))
    ax.add_patch(Polygon(xy, closed=True,
                         zorder=zorder+1, edgecolor=color,
                         facecolor='none', lw=lw))
    ax.text(x - 0.8*r, y + 0.18*a, '$+$', ha='left', va='center',
            fontsize='x-small', color=color, zorder=zorder+1)
    ax.text(x - 0.8*r, y - 0.25*a, '$-$', ha='left', va='center',
            fontsize='x-small', color=color, zorder=zorder+1)
    if label:
        if align == 'above':
            yy = 1.4*r
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'bottom'
        elif align == 'below':
            yy = -1.4*r
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'top'
        elif align == 'center':
            yy = 0
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'center'
        else:
            raise ValueError('align must be one of "above", "bottom", or "center"')
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'left'
        ax.text(x, y + yy, label, zorder=zorder+1, **kwargs)
    return Pos(x - r, y - 0.2*a), Pos(x - r, y + 0.2*a), Pos(x + 2*r, y), Pos(x, y-1.2*r)


def opamp_r(ax, pos, label='', align='above', lw=None, color=None,
            facecolor=None, alpha=None, zorder=None, **kwargs):
    """ Draw an operational amplifier with inputs on the right.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the opamp.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the opamp.
    label: string
        Optional label for the opamp.
    align: 'above', 'below', 'center'
        Position the label above, below or in the center of the opamp.
    lw: float, int
        Linewidth for drawing the outline of the opamp.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color for the outline of the opamp.
        Defaults to `circuits.color` rcParams settings.
    facecolor matplotlib color
        Color for filling the opamp.
        Defaults to `circuits.facecolor` rcParams settings.
    alpha: float
        Alpha value for the face color.
        Defaults to `circuits.alpha` rcParams settings.
    zorder: int
        zorder for the opamp and the label.
        Defaults to `circuits.zorder` rcParams settings.
    kwargs: key-word arguments
        Passed on to `ax.text()` used to print the label.
        Defaults to `circuits.font` rcParams settings.

    Returns
    -------
    pospos: Pos
        Coordinates of the positive (upper) input of the opamp.
    posneg: Pos
        Coordinates of the negative (lower) input of the opamp.
    posout: Pos
        Coordinates of the output of the opamp.
    posgnd: Pos
        Coordinates of the ground supply of the opamp.

    Raises
    ------
    ValueError:
        Invalid value for `align`.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.linewidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if facecolor is None:
        facecolor = mpl.rcParams['circuits.facecolor']
    if alpha is None:
        alpha = mpl.rcParams['circuits.alpha']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    for k in mpl.rcParams['circuits.font']:
        if not k in kwargs:
            kwargs[k] = mpl.rcParams['circuits.font'][k]
    a = mpl.rcParams['circuits.scale']*5/3
    r = a/2/np.sqrt(3)
    x, y = pos
    xy = np.array([[x + r, y - 0.5*a], [x + r, y + 0.5*a], [x - 2*r, y]])
    ax.add_patch(Polygon(xy, closed=True,
                         zorder=zorder, edgecolor='none',
                         facecolor=facecolor, alpha=alpha))
    ax.add_patch(Polygon(xy, closed=True,
                         zorder=zorder+1, edgecolor=color,
                         facecolor='none', lw=lw))
    ax.text(x + 0.8*r, y + 0.18*a, '$+$', ha='right', va='center',
            fontsize='x-small', color=color, zorder=zorder+1)
    ax.text(x + 0.8*r, y - 0.25*a, '$-$', ha='right', va='center',
            fontsize='x-small', color=color, zorder=zorder+1)
    if label:
        if align == 'above':
            yy = 1.4*r
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'bottom'
        elif align == 'below':
            yy = -1.4*r
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'top'
        elif align == 'center':
            yy = 0
            if not 'va' in kwargs and not 'verticalalignment' in kwargs:
                kwargs['va'] = 'center'
        else:
            raise ValueError('align must be one of "above", "bottom", or "center"')
        if not 'ha' in kwargs and not 'horizontalalignment' in kwargs:
            kwargs['ha'] = 'right'
        ax.text(x, y + yy, label, zorder=zorder+1, **kwargs)
    return Pos(x + r, y - 0.2*a), Pos(x + r, y + 0.2*a), Pos(x - 2*r, y), Pos(x, y-1.2*r)


def node(ax, pos, color=None, zorder=None):
    """ Draw a node connecting lines.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the node.
    pos: Pos or 2-tuple of floats
        x and y-coordinate of position of the center of the node.
    color matplotlib color
        Color of the node.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the node.
        Defaults to `circuits.zorder` rcParams settings.

    Returns
    -------
    pos: Pos
        Coordinates of the node.
    """
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    r = mpl.rcParams['circuits.scale']*0.25/3
    ax.add_patch(Circle(pos, r, zorder=zorder, edgecolor='none',
                        facecolor=color))
    return Pos(pos[0], pos[1])


def connect(ax, nodes, lw=None, color=None, zorder=None):
    """ Draw horizontal and vertical lines connecting circuit elements.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the connections.
    nodes: list of Pos or 2-tuple of floats
        x and y-coordinates of positions that should be connected.
        If an element is `None` then leave a gap between the neighboring nodes.
        Makes only horizontal and vertical connection lines in
        counter-clockwise direction.
    lw: float, int
        Linewidth for drawing the connection lines.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color of the connection lines.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the connection lines.
        Defaults to `circuits.zorder` rcParams settings.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.connectwidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    xs = []
    ys = []
    px = None
    py = None
    for n in nodes:
        if n is None:
            xs.append(np.nan)
            ys.append(np.nan)
            px = None
            py = None
        else:
            x = n[0]
            y = n[1]
            if px is None or x == px or y == py:
                xs.append(x)
                ys.append(y)
            else:
                if (x - px)*(y - py) > 0:
                    xs.extend((x, x))
                    ys.extend((py, y))
                else:
                    xs.extend((px, x))
                    ys.extend((y, y))
            px = x
            py = y
    ax.plot(xs, ys, lw=lw, color=color, zorder=zorder)


def connect_straight(ax, nodes, lw=None, color=None, zorder=None):
    """ Draw straight lines connecting circuit elements.

    Parameters
    ----------
    ax: matplotlib axes
        Axes where to draw the connections.
    nodes: list of Pos or 2-tuple of floats
        x and y-coordinates of positions that should be connected.
        If an element is `None` then leave a gap between the neighboring nodes.
    lw: float, int
        Linewidth for drawing the connection lines.
        Defaults to `circuits.linewidth` rcParams settings.
    color matplotlib color
        Color of the connection lines.
        Defaults to `circuits.color` rcParams settings.
    zorder: int
        zorder for the connection lines.
        Defaults to `circuits.zorder` rcParams settings.
    """
    if lw is None:
        lw = mpl.rcParams['circuits.connectwidth']
    if color is None:
        color = mpl.rcParams['circuits.color']
    if zorder is None:
        zorder = mpl.rcParams['circuits.zorder']
    xs = []
    ys = []
    for n in nodes:
        if n is None:
            xs.append(np.nan)
            ys.append(np.nan)
        else:
            x = n[0]
            y = n[1]
            xs.append(x)
            ys.append(y)
    ax.plot(xs, ys, lw=lw, color=color, zorder=zorder)


def circuits_params(scale=None, connectwidth=None, linewidth=None,
                    color=None, facecolor=None, alpha=None,
                    zorder=None, font=None):
    """Set rc settings for circuits.
                  
    Only parameters that are not `None` are updated.

    Parameters
    ----------
    scale: float
        Size of circuit elements as the height of a vertical resistance
        in x/y coordinate units.
    connectwidth: int, float
        Line width of lines connecting circuit elements.
        Set rcParam `circuits.connectwidth`.
    linewidth: int, float
        Line width used for drawing circuit elements.
        Set rcParam `circuits.linewidth`.
    color: matplotlib color
        Color of the connections and circuit elements.
        Set rcParam `circuits.color`.
    facecolor: matplotlib color
        Face color for closed circuit elements like resistances or opamps.
        Set rcParam `circuits.facecolor`.
    alpha: float
        Alpha value for face color for closed circuit elements like
        resistances or opamps.
        Set rcParam `circuits.alpha`.
    zorder: int
        Zorder for all circuit elements drawn.
        Set rcParam `circuits.zorder`.
    font: dict
        Dictionary with font settings used for labeling circuit elements
        (e.g. fontsize, fontfamiliy, fontstyle, fontweight, bbox, ...).
         Set rcParam `circuits.font`.
    """
    if scale is not None and 'circuits.scale' in mrc._validators:
        mpl.rcParams['circuits.scale'] = scale
    if connectwidth is not None and 'circuits.connectwidth' in mrc._validators:
        mpl.rcParams['circuits.connectwidth'] = connectwidth
    if linewidth is not None and 'circuits.linewidth' in mrc._validators:
        mpl.rcParams['circuits.linewidth'] = linewidth
    if color is not None and 'circuits.color' in mrc._validators:
        mpl.rcParams['circuits.color'] = color
    if facecolor is not None and 'circuits.facecolor' in mrc._validators:
        mpl.rcParams['circuits.facecolor'] = facecolor
    if alpha is not None and 'circuits.alpha' in mrc._validators:
        mpl.rcParams['circuits.alpha'] = alpha
    if zorder is not None and 'circuits.zorder' in mrc._validators:
        mpl.rcParams['circuits.zorder'] = zorder
    if font is not None and 'circuits.font' in mrc._validators:
        mpl.rcParams.update({'circuits.font': font})


def install_circuits():
    """ Install circuits functions on matplotlib axes.

    This function is also called automatically upon importing the module.

    See also
    --------
    uninstall_circuits()
    """
    if not hasattr(mpl.axes.Axes, 'resistance_h'):
        mpl.axes.Axes.resistance_h = resistance_h
    if not hasattr(mpl.axes.Axes, 'resistance_v'):
        mpl.axes.Axes.resistance_v = resistance_v
    if not hasattr(mpl.axes.Axes, 'resistance'):
        mpl.axes.Axes.resistance = resistance
    if not hasattr(mpl.axes.Axes, 'capacitance_h'):
        mpl.axes.Axes.capacitance_h = capacitance_h
    if not hasattr(mpl.axes.Axes, 'capacitance_v'):
        mpl.axes.Axes.capacitance_v = capacitance_v
    if not hasattr(mpl.axes.Axes, 'battery_h'):
        mpl.axes.Axes.battery_h = battery_h
    if not hasattr(mpl.axes.Axes, 'battery_v'):
        mpl.axes.Axes.battery_v = battery_v
    if not hasattr(mpl.axes.Axes, 'ground'):
        mpl.axes.Axes.ground = ground
    if not hasattr(mpl.axes.Axes, 'opamp_l'):
        mpl.axes.Axes.opamp_l = opamp_l
    if not hasattr(mpl.axes.Axes, 'opamp_r'):
        mpl.axes.Axes.opamp_r = opamp_r
    if not hasattr(mpl.axes.Axes, 'node'):
        mpl.axes.Axes.node = node
    if not hasattr(mpl.axes.Axes, 'connect'):
        mpl.axes.Axes.connect = connect
    if not hasattr(mpl.axes.Axes, 'connect_straight'):
        mpl.axes.Axes.connect_straight = connect_straight
    # add circuits parameter to rc configuration:
    if 'circuits.scale' not in mpl.rcParams:
        mrc._validators['circuits.scale'] = mrc.validate_float
        mrc._validators['circuits.connectwidth'] = mrc.validate_float
        mrc._validators['circuits.linewidth'] = mrc.validate_float
        mrc._validators['circuits.color'] = mrc.validate_string
        mrc._validators['circuits.facecolor'] = mrc.validate_string
        mrc._validators['circuits.alpha'] = mrc.validate_float
        mrc._validators['circuits.zorder'] = mrc.validate_float
        mrc._validators['circuits.font'] = _validate_fontdict
        mpl.rcParams.update({'circuits.scale': 1,
                             'circuits.connectwidth': 1,
                             'circuits.linewidth': 2,
                             'circuits.color': 'black',
                             'circuits.facecolor': 'white',
                             'circuits.alpha': 1,
                             'circuits.zorder': 100,
                             'circuits.font': dict()})

        
def uninstall_circuits():
    """ Uninstall circuits functions from matplotlib axes.

    Call this code to disable anything that was installed by `install_circuits()`.

    See also
    --------
    install_circuits()
    """
    if hasattr(mpl.axes.Axes, 'resistance_h'):
        delattr(mpl.axes.Axes, 'resistance_h')
    if hasattr(mpl.axes.Axes, 'resistance_v'):
        delattr(mpl.axes.Axes, 'resistance_v')
    if hasattr(mpl.axes.Axes, 'resistance'):
        delattr(mpl.axes.Axes, 'resistance')
    if hasattr(mpl.axes.Axes, 'capacitance_h'):
        delattr(mpl.axes.Axes, 'capacitance_h')
    if hasattr(mpl.axes.Axes, 'capacitance_v'):
        delattr(mpl.axes.Axes, 'capacitance_v')
    if hasattr(mpl.axes.Axes, 'battery_h'):
        delattr(mpl.axes.Axes, 'battery_h')
    if hasattr(mpl.axes.Axes, 'battery_v'):
        delattr(mpl.axes.Axes, 'battery_v')
    if hasattr(mpl.axes.Axes, 'ground'):
        delattr(mpl.axes.Axes, 'ground')
    if hasattr(mpl.axes.Axes, 'opamp_l'):
        delattr(mpl.axes.Axes, 'opamp_l')
    if hasattr(mpl.axes.Axes, 'opamp_r'):
        delattr(mpl.axes.Axes, 'opamp_r')
    if hasattr(mpl.axes.Axes, 'node'):
        delattr(mpl.axes.Axes, 'node')
    if hasattr(mpl.axes.Axes, 'connect'):
        delattr(mpl.axes.Axes, 'connect')
    if hasattr(mpl.axes.Axes, 'connect_straight'):
        delattr(mpl.axes.Axes, 'connect_straight')
    mrc._validators.pop('circuits.scale', None)
    mrc._validators.pop('circuits.connectwidth', None)
    mrc._validators.pop('circuits.linewidth', None)
    mrc._validators.pop('circuits.color', None)
    mrc._validators.pop('circuits.facecolor', None)
    mrc._validators.pop('circuits.alpha', None)
    mrc._validators.pop('circuits.zorder', None)
    mrc._validators.pop('circuits.font', None)


install_circuits()
            
    
def demo():
    fig, ax = plt.subplots()
    e1b, e1t = ax.battery_v((0, 1), r'$E_1$')
    r1b, r1t = ax.resistance_v((e1t[0], 3), r'$R_1$')
    c1b, c1t = ax.capacitance_v((-2, 2), r'$C_1$')
    ax.connect((e1t, r1b, None, r1t, r1t.ups(0.5), c1t, None,
                c1b, e1b.downs(0.5), e1b))
    e2l, e2r = ax.battery_h((0, -1), r'$E_2$', 'below')
    r2l, r2r = ax.resistance_h((-2, e2l.y()), r'$R_2$', 'below')
    c2l, c2r = ax.capacitance_h((-1, -3), r'$C_2$', 'below')
    ax.connect((e2l, r2r, None, r2l, r2l.lefts(0.5), c2l, None,
                c2r, e2r.rights(0.5), e2r))
    op1n, op1p, op1o, op1g = ax.opamp_l((4, 2), r'$OP1$')
    n1n = ax.node(op1n.lefts(2))
    n1p = ax.node(op1p.lefts(2))
    n1o = ax.node(op1o.rights(1))
    gnd1 = ax.ground(op1g.downs(1), r'$GND_1$')
    ax.connect((op1n, n1n))
    ax.connect((op1p, n1p))
    ax.connect((op1o, n1o))
    ax.connect((op1g, gnd1))
    op2n, op2p, op2o, op2g = ax.opamp_r((4, -2), r'$OP2$')
    n2n = ax.node(op2n.rights(1))
    n2p = ax.node(op2p.rights(1))
    n2o = ax.node(op2o.lefts(2))
    gnd2 = ax.ground(op2g.downs(1), r'$GND_2$', 'left')
    ax.connect((op2n, n2n))
    ax.connect((op2p, n2p))
    ax.connect((op2o, n2o))
    ax.connect((op2g, gnd2))
    ax.set_aspect('equal')
    plt.show()


if __name__ == "__main__":
    demo()
