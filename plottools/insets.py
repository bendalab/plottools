"""
# Insets

Add insets to an axes.

- `zoomed_inset()`: add an inset for displaying zoomed-in data.
"""

def zoomed_inset(ax, pos, box=None, **kwargs):
    """
    Add an inset for displaying zoomed-in data.

    The limits of the inset are set according to `box`. Additionally
    a frame is drawn around the zooemd-in region.

    Parameters
    ----------
    ax: matplotlib axes
        Axes to which the inset is added.
    pos: list of floats
        Position of the inset in axes coordinates (x0, y0, x1, y1).
    box: list of floats or None
        Zoomed in region in data coordinates (x0, y0, x1, y1).
    kwargs:
        Passed on to plot for plotting the box around the zoomed-in region.

    Returns
    -------
    axi: matplotlib axes
        Axes of the inset.
    pos: list of floats
        Coordinates of the inset in data units of ax (x0, y0, x1, y1).
    """
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x0, y0, width, height = ax.get_position().bounds
    axins = ax.get_figure().add_axes([x0+pos[0]*width, y0+pos[1]*height,
                                      (pos[2]-pos[0])*width,
                                      (pos[3]-pos[1])*height])
    if box is not None:
        axins.set_xlim(box[0], box[2])
        axins.set_ylim(box[1], box[3])
        ax.plot([box[0], box[0], box[2], box[2], box[0]],
                [box[1], box[3], box[3], box[1], box[1]], **kwargs)
    # inbox to data coordinates:
    pos = np.array(pos)
    pos[0::2] *= np.abs(xmax - xmin)
    pos[0::2] += min(xmin, xmax)
    pos[1::2] *= np.abs(ymax - ymin)
    pos[1::2] += min(ymin, ymax)
    return axins, pos
    

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    x = np.arange(-2.0, 5.0, 0.01)
    ax.plot(x, np.sin(2.0*np.pi*4.0*x))
    ax.set_xlim(-2.0, 5.0)
    ax.set_ylim(-1.5, 4.5)
    ax.set_xlabel('Time [s]')
    axi, pos = zoomed_inset(ax, [0.1, 0.6, 0.9, 0.95], [0.0, -1.0, 2.0, 1.0],
                            c='k', lw=1.0)
    axi.plot(x, np.sin(2.0*np.pi*4.0*x))
    ax.plot([0.0, pos[0]], [1.0, pos[1]], c='k', lw=1.0)
    ax.plot([2.0, pos[2]], [1.0, pos[1]], c='k', lw=1.0)
    plt.show()
