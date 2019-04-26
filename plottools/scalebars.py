"""
# Scalebars

Labeled scale bars.

- `xscalebar()`: horizontal scale bar with label.
- `yscalebar()`: vertical scale bar with label.
- `scalebars()`: horizontal and vertical scale bars with labels.
"""


def xscalebar(ax, x, y, width, wunit=None, wformat=None,
              ha='left', va='bottom', lw=2, capsize=0.0, clw=0.5, fs=10.0):
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
        Optional format string for formatting the label of the scale bar.
    ha: 'left', 'right', or 'center'
        Scale bar aligned left, right, or centered to (x, y)
    va: 'top' or 'bottom'
        Label of the scale bar either above or below the scale bar.
    lw: int, float
        Line width of the scale bar.
    capsize: float
        If larger then zero draw cap lines at the ends of the bar.
        The length of the lines is given in fractions of the fontsize.
    clw: int, float
        Line width of the cap lines.
    fs: float
        Fontsize for scale bar label
    """
    ax.autoscale(False)
    # ax dimensions:
    pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))[0]
    pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))[0]
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    unitx = xmax - xmin
    unity = ymax - ymin
    dxf = fs/pixelx*np.abs(unitx)
    dyf = fs/pixely*np.abs(unity)
    # transform x, y from relative units to axis units:
    x = xmin + x*unitx
    y = ymin + y*unity
    # bar length:
    if wformat is None:
        wformat = '%.0f'
        if width < 1.0:
            wformat = '%.1f'
    ls = wformat % width
    width = float(ls)
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
    ax.plot([x0, x1], [y, y], 'k', lw=lw, solid_capstyle='butt', clip_on=False)
    if capsize > 0.0:
        dy = capsize*dyf
        ax.plot([x0, x0], [y-dy, y+dy], 'k', lw=clw,
                solid_capstyle='butt', clip_on=False)
        ax.plot([x1, x1], [y-dy, y+dy], 'k', lw=clw,
                solid_capstyle='butt', clip_on=False)
    # label:
    if wunit:
        ls += u'\u2009%s' % wunit
    if va == 'top':
        ax.text(0.5*(x0+x1), y+0.2*dyf, ls, clip_on=False,
                ha='center', va='bottom', fontsize=fs)
    else:
        ax.text(0.5*(x0+x1), y-0.5*dyf, ls, clip_on=False,
                ha='center', va='top', fontsize=fs)
    return x0, x1, y

        
def yscalebar(ax, x, y, height, hunit=None, hformat=None,
              ha='left', va='bottom', lw=2, capsize=0.0, clw=0.5, fs=10.0):
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
        Optional format string for formatting the label of the scale bar.
    ha: 'left' or 'right'
        Label of the scale bar either to the left or to the right
        of the scale bar.
    va: 'top', 'bottom', or 'center'
        Scale bar aligned above, below, or centered on (x, y).
    lw: int, float
        Line width of the scale bar.
    capsize: float
        If larger then zero draw cap lines at the ends of the bar.
        The length of the lines is given in fractions of the fontsize.
    clw: int, float
        Line width of the cap lines.
    fs: float
        Fontsize for scale bar label.
    """
    ax.autoscale(False)
    # ax dimensions:
    pixelx = np.abs(np.diff(ax.get_window_extent().get_points()[:,0]))[0]
    pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))[0]
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    unitx = xmax - xmin
    unity = ymax - ymin
    dxf = fs/pixelx*np.abs(unitx)
    dyf = fs/pixely*np.abs(unity)
    # transform x, y from relative units to axis units:
    x = xmin + x*unitx
    y = ymin + y*unity
    # bar length:
    if hformat is None:
        hformat = '%.0f'
        if height < 1.0:
            hformat = '%.1f'
    ls = hformat % height
    width = float(ls)
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
    ax.plot([x, x], [y0, y1], 'k', lw=lw, solid_capstyle='butt', clip_on=False)
    if capsize > 0.0:
        dx = capsize*dxf
        ax.plot([x-dx, x+dx], [y0, y0], 'k', lw=clw, solid_capstyle='butt',
                clip_on=False)
        ax.plot([x-dx, x+dx], [y1, y1], 'k', lw=clw, solid_capstyle='butt',
                clip_on=False)
    # label:
    if hunit:
        ls += u'\u2009%s' % hunit
    if ha == 'right':
        ax.text(x+0.3*dxf, 0.5*(y0+y1), ls, clip_on=False, rotation=90.0,
                ha='left', va='center', fontsize=fs)
    else:
        ax.text(x+0.1*dxf, 0.5*(y0+y1), ls, clip_on=False, rotation=90.0,
                ha='right', va='center', fontsize=fs)
    return x, y0, y1

        
def scalebars(ax, x, y, width, height, wunit=None, hunit=None,
              wformat=None, hformat=None, ha='left', va='bottom',
              lw=2, fs=10.0):
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
        Optional format string for formatting the x-label of the scale bar.
    hformat: string or None
        Optional format string for formatting the y-label of the scale bar.
    ha: 'left' or 'right'
        Scale bars aligned left or right to (x, y).
        Vertical scale bar left or right.
    va: 'top' or 'bottom'
        Scale bars aligned above or below (x, y).
        Horizontal scale bar on top or a the bottom.
    lw: int, float
        Line width of the scale bar.
    fs: float
        Fontsize for scale bar label 
    """
    x0, x1, yy = xscalebar(ax, x, y, width, wunit, wformat, ha, va, lw, 0.0, 1, fs)
    ax.lines.pop()
    xx, y0, y1 = yscalebar(ax, x, y, height, hunit, hformat, ha, va, lw, 0.0, 1, fs)
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
              capsize=0.0, clw=1, fs=10.0)
    draw_anchor(ax, 0.5, 0.3)
    xscalebar(ax, 0.5, 0.3, 1.5, 's', '%.1f', ha='center', va='bottom', lw=4,
              capsize=0.5, clw=1, fs=10.0)
    draw_anchor(ax, 1.0, 0.3)
    xscalebar(ax, 1.0, 0.3, 0.55, 's', ha='right', va='top', lw=2,
              capsize=0.0, clw=1, fs=10.0)

    draw_anchor(ax, 0.3, 0.25)
    yscalebar(ax, 0.3, 0.25, 0.5, '', ha='left', va='bottom', lw=2,
              capsize=0.0, clw=1, fs=10.0)
    draw_anchor(ax, 0.7, 0.35)
    yscalebar(ax, 0.7, 0.35, 0.3, '', ha='right', va='top', lw=2,
              capsize=0.2, clw=1, fs=10.0)

    draw_anchor(ax, 0.1, 0.1)
    scalebars(ax, 0.1, 0.1, 1.2, 0.5, 's', '', '%.1f', ha='left', va='bottom',
              lw=2, fs=10.0)
    draw_anchor(ax, 0.9, 0.1)
    scalebars(ax, 0.9, 0.1, 0.8, 0.7, 's', '', ha='right', va='bottom',
              lw=2, fs=10.0)
    draw_anchor(ax, 0.1, 0.9)
    scalebars(ax, 0.1, 0.9, 1.5, 0.5, 's', '', ha='left', va='top',
              lw=4, fs=10.0)
    draw_anchor(ax, 0.95, 0.9)
    scalebars(ax, 0.95, 0.9, 1.0, 0.5, 's', '', ha='right', va='top',
              lw=4, fs=10.0)
        
    plt.show()

    
