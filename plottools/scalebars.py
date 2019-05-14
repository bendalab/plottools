"""
# Scalebars

Labeled scale bars.

- `xscalebar()`: horizontal scale bar with label.
- `yscalebar()`: vertical scale bar with label.
- `scalebars()`: horizontal and vertical scale bars with labels.
"""


def xscalebar(ax, x, y, width, wunit=None, wformat=None,
              ha='left', va='bottom', lw=2, capsize=0.0, clw=0.5, **kwargs):
    """ Horizontal scale bar with label.

    Parameter
    ---------
    ax: matplotlib axes
        Axes where to draw the scale bar.
    x: float
        x-coordinate where to draw the scale bar in relative units of the axes.
    y: float
        y-coordinate where to draw the scale bar in relative units of the axes.
    width: float
        Length of the scale bar in units of the data's x-values.
    wunit: string or None
        Optional unit of the data's x-values.
    wformat: string or None
        Optional format string for formatting the label of the scale bar
        or simply a string used for labeling the scale bar.
    ha: 'left', 'right', or 'center'
        Scale bar aligned left, right, or centered to (x, y)
    va: 'top' or 'bottom'
        Label of the scale bar either above or below the scale bar.
    lw: int, float
        Line width of the scale bar.
    capsize: float
        If larger then zero draw cap lines at the ends of the bar.
        The length of the lines is given in points (same unit as linewidth).
    clw: int, float
        Line width of the cap lines.
    kwargs: key-word arguments
        Passed on to ax.text() used to print the scale bar label.
    """
    ax.autoscale(False)
    # ax dimensions:
    pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))[0]
    pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))[0]
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    unitx = xmax - xmin
    unity = ymax - ymin
    dxu = np.abs(unitx)/pixelx
    dyu = np.abs(unity)/pixely
    # transform x, y from relative units to axis units:
    x = xmin + x*unitx
    y = ymin + y*unity
    # bar length:
    if wformat is None:
        wformat = '%.0f'
        if width < 1.0:
            wformat = '%.1f'
    try:
        ls = wformat % width
        width = float(ls)
    except TypeError:
        ls = wformat
    # bar:
    if ha == 'left':
        x0 = x
        x1 = x+width
    elif ha == 'right':
        x0 = x-width
        x1 = x
    else:
        x0 = x-0.5*width
        x1 = x+0.5*width
    lh = ax.plot([x0, x1], [y, y], 'k', lw=lw, solid_capstyle='butt', clip_on=False)
    # get y position of line in figure pixel coordinates:
    ly = np.array(lh[0].get_window_extent(ax.get_figure().canvas.get_renderer()))[0,1]
    if capsize > 0.0:
        dy = capsize*dyu
        ax.plot([x0, x0], [y-dy, y+dy], 'k', lw=clw,
                solid_capstyle='butt', clip_on=False)
        ax.plot([x1, x1], [y-dy, y+dy], 'k', lw=clw,
                solid_capstyle='butt', clip_on=False)
    # label:
    if wunit:
        ls += u'\u2009%s' % wunit
    if va == 'top':
        th = ax.text(0.5*(x0+x1), y, ls, clip_on=False,
                     ha='center', va='bottom', **kwargs)
        # get y coordinate of text bottom in figure pixel coordinates:
        ty = np.array(th.get_window_extent(ax.get_figure().canvas.get_renderer()))[0,1]
        dty = ly+0.5*lw + 2.0 - ty
    else:
        th = ax.text(0.5*(x0+x1), y, ls, clip_on=False,
                     ha='center', va='top', **kwargs)
        # get y coordinate of text bottom in figure pixel coordinates:
        ty = np.array(th.get_window_extent(ax.get_figure().canvas.get_renderer()))[1,1]
        dty = ly-0.5*lw - 2.0 - ty
    th.set_position((0.5*(x0+x1), y+np.abs(unity)*dty/pixely))
    return x0, x1, y

        
def yscalebar(ax, x, y, height, hunit=None, hformat=None,
              ha='left', va='bottom', lw=2, capsize=0.0, clw=0.5, **kwargs):
    """ Vertical scale bar with label.

    Parameter
    ---------
    ax: matplotlib axes
        Axes where to draw the scale bar.
    x: float
        x-coordinate where to draw the scale bar in relative units of the axes.
    y: float
        y-coordinate where to draw the scale bar in relative units of the axes.
    height: float
        Length of the scale bar in units of the data's y-values.
    hunit: string
        Unit of the data's y-values.
    hformat: string or None
        Optional format string for formatting the label of the scale bar
        or simply a string used for labeling the scale bar.
    ha: 'left' or 'right'
        Label of the scale bar either to the left or to the right
        of the scale bar.
    va: 'top', 'bottom', or 'center'
        Scale bar aligned above, below, or centered on (x, y).
    lw: int, float
        Line width of the scale bar.
    capsize: float
        If larger then zero draw cap lines at the ends of the bar.
        The length of the lines is given in points (same unit as linewidth).
    clw: int, float
        Line width of the cap lines.
    kwargs: key-word arguments
        Passed on to ax.text() used to print the scale bar label.
    """
    ax.autoscale(False)
    # ax dimensions:
    pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))[0]
    pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))[0]
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    unitx = xmax - xmin
    unity = ymax - ymin
    dxu = np.abs(unitx)/pixelx
    dyu = np.abs(unity)/pixely
    # transform x, y from relative units to axis units:
    x = xmin + x*unitx
    y = ymin + y*unity
    # bar length:
    if hformat is None:
        hformat = '%.0f'
        if height < 1.0:
            hformat = '%.1f'
    try:
        ls = hformat % height
        width = float(ls)
    except TypeError:
        ls = hformat
    # bar:
    if va == 'bottom':
        y0 = y
        y1 = y+height
    elif va == 'top':
        y0 = y-height
        y1 = y
    else:
        y0 = y-0.5*height
        y1 = y+0.5*height
    lh = ax.plot([x, x], [y0, y1], 'k', lw=lw, solid_capstyle='butt', clip_on=False)
    # get x position of line in figure pixel coordinates:
    lx = np.array(lh[0].get_window_extent(ax.get_figure().canvas.get_renderer()))[0,0]
    if capsize > 0.0:
        dx = capsize*dxu
        ax.plot([x-dx, x+dx], [y0, y0], 'k', lw=clw, solid_capstyle='butt',
                clip_on=False)
        ax.plot([x-dx, x+dx], [y1, y1], 'k', lw=clw, solid_capstyle='butt',
                clip_on=False)
    # label:
    if hunit:
        ls += u'\u2009%s' % hunit
    if ha == 'right':
        th = ax.text(x, 0.5*(y0+y1), ls, clip_on=False, rotation=90.0,
                     ha='left', va='center', **kwargs)
        # get x coordinate of text bottom in figure pixel coordinates:
        tx = np.array(th.get_window_extent(ax.get_figure().canvas.get_renderer()))[0,0]
        dtx = lx+0.5*lw + 2.0 - tx
    else:
        th = ax.text(x, 0.5*(y0+y1), ls, clip_on=False, rotation=90.0,
                     ha='right', va='center', **kwargs)
        # get x coordinate of text bottom in figure pixel coordinates:
        tx = np.array(th.get_window_extent(ax.get_figure().canvas.get_renderer()))[1,0]
        dtx = lx-0.5*lw - 1.0 - tx
    th.set_position((x+np.abs(unitx)*dtx/pixelx, 0.5*(y0+y1)))
    return x, y0, y1

        
def scalebars(ax, x, y, width, height, wunit=None, hunit=None,
              wformat=None, hformat=None, ha='left', va='bottom',
              lw=2, **kwargs):
    """ Horizontal and vertical scale bars with labels.

    Parameter
    ---------
    ax: matplotlib axes
        Axes where to draw the scale bar.
    x: float
        x-coordinate where to draw the scale bar in relative units of the axes.
    y: float
        y-coordinate where to draw the scale bar in relative units of the axes.
    width: float
        Length of horizontal scale bar in units of the data.
    height: float
        Length of vertical scale bar in units of the data.
    wunit: string
        Unit of x-values.
    hunit: string
        Unit of y-values.
    wformat: string or None
        Optional format string for formatting the x-label of the scale bar
        or simply a string used for labeling the x scale bar.
    hformat: string or None
        Optional format string for formatting the y-label of the scale bar
        or simply a string used for labeling the y scale bar.
    ha: 'left' or 'right'
        Scale bars aligned left or right to (x, y).
        Vertical scale bar left or right.
    va: 'top' or 'bottom'
        Scale bars aligned above or below (x, y).
        Horizontal scale bar on top or a the bottom.
    lw: int, float
        Line width of the scale bar.
    kwargs: key-word arguments
        Passed on to ax.text() used to print the scale bar labels.
    """
    x0, x1, yy = xscalebar(ax, x, y, width, wunit, wformat, ha, va, lw, 0.0, 1, **kwargs)
    ax.lines.pop()
    xx, y0, y1 = yscalebar(ax, x, y, height, hunit, hformat, ha, va, lw, 0.0, 1, **kwargs)
    ax.lines.pop()
    if x0 == xx:
        if y0 == yy:
            ax.plot([x0, x0, x1], [y1, y0, y0], 'k', lw=lw, solid_capstyle='butt',
                    solid_joinstyle='miter', clip_on=False)
        else:
            ax.plot([x0, x0, x1], [y0, y1, y1], 'k', lw=lw, solid_capstyle='butt',
                    solid_joinstyle='miter', clip_on=False)
    else:
        if y0 == yy:
            ax.plot([x0, x1, x1], [y0, y0, y1], 'k', lw=lw, solid_capstyle='butt',
                    solid_joinstyle='miter', clip_on=False)
        else:
            ax.plot([x0, x1, x1], [y1, y1, y0], 'k', lw=lw, solid_capstyle='butt',
                    solid_joinstyle='miter', clip_on=False)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    def draw_anchor(ax, x, y):
        ax.plot(x, y, '.r', ms=20, transform=ax.transAxes)
    
    fig, ax = plt.subplots()
    x = np.arange(-2.0, 5.0, 0.01)
    ax.plot(x, np.sin(2.0*np.pi*1.0*x))
    ax.set_xlim(-2.0, 5.0)
    ax.set_ylim(-2.5, 1.5)
    ax.set_xlabel('Time [s]')
    
    draw_anchor(ax, 0.0, 0.3)
    xscalebar(ax, 0.0, 0.3, 1.0, 's', ha='left', va='bottom', lw=2,
              capsize=0.0, clw=1)
    draw_anchor(ax, 0.5, 0.3)
    xscalebar(ax, 0.5, 0.3, 1.5, 's', '%.1f', ha='center', va='bottom', lw=4,
              capsize=8, clw=1)
    draw_anchor(ax, 1.0, 0.3)
    xscalebar(ax, 1.0, 0.3, 0.55, 's', ha='right', va='top', lw=2,
              capsize=0.0, clw=1)

    draw_anchor(ax, 0.3, 0.25)
    yscalebar(ax, 0.3, 0.25, 0.5, '', ha='left', va='bottom', lw=2,
              capsize=0.0, clw=1)
    draw_anchor(ax, 0.7, 0.35)
    yscalebar(ax, 0.7, 0.35, 0.3, '', ha='right', va='top', lw=2,
              capsize=4, clw=1)

    draw_anchor(ax, 0.1, 0.1)
    scalebars(ax, 0.1, 0.1, 1.2, 0.5, 's', '', '%.1f', ha='left', va='bottom', lw=2)
    draw_anchor(ax, 0.9, 0.1)
    scalebars(ax, 0.9, 0.1, 0.8, 0.7, 's', '', ha='right', va='bottom', lw=2)
    draw_anchor(ax, 0.1, 0.9)
    scalebars(ax, 0.1, 0.9, 1.5, 0.5, 's', '', ha='left', va='top', lw=4)
    draw_anchor(ax, 0.95, 0.9)
    scalebars(ax, 0.95, 0.9, 1.0, 0.5, 's', '', ha='right', va='top', lw=4)
        
    plt.show()

    
