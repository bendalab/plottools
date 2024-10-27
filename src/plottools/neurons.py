"""
Draw sketches of neurons.


## Axes member functions

- `neuron()`: draw a sketch of a neuron.


## Install/uninstall neurons functions

You usually do not need to call these functions. Upon loading the neurons
module, `install_neurons()` is called automatically.

- `install_neurons()`: install functions of the neurons module in matplotlib.
- `uninstall_neurons()`: uninstall all code of the neurons module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def neuron(ax, xy, r, label=None, xytarget=None, synapse='exc',
           adapt=0, xyinput=None, fc='white', ec='black', lw=2,
           **kwargs):
    """Draw a sketch of a neuron.

    The coordinate system should have equal distances in both directions
    for the cell bodies being true circles. That is, you should call
    ```
    ax.set_aspect('equal')
    ```
    or
    ```
    import plottools.axes
    ax.set_ylim_equal()
    ```

    Parameters
    ----------
    ax: matplotlib axes
        Axes into which to draw the neuron.
    xy: tuple of floats
        Coordinates of center of cell body in data coordinates.
    r: float
        Radius of cell body in data coordinates.
    label: string or None
        If not `None`, text to printed inside the cell body.
    xytarget: tuple of floats, sequence of tuple of floats or None
        If not `None`, list of x and y coordinates to which
        connections are drawn.  The coordinates are the centers of the
        target neurons in data coordinates from which the radius `r`
        is subtracted.
    synapse: 'exc', 'inh' or 'arr' or lis thereof
        For each `xytarget` the type of synapse to be drawn:
        excitatory synapse (a triangle), inhibitory synapse (a bar),
        or an arrow.
    adapt: int
        If not zero draw a self-inhibitory circular connection,
        indicating an adaptation current.
        - 1: draw self-inhibition to the side of the top-most connection
          to a target neuron.
        - 2: draw self-inhibition opposite of outgoing connections to
          target neurons.
        - 3: draw self-inhibition on top.
    xyinput: tuple of floats or None
        If not `None`, draw an input arrow originating from the given
        coordinates (in data coordinates).
    fc: matplotlib color specification
        Fill color for the cell body.
    ec: matplotlib color specification
        Edge color for the cell body and line color for all the connections,
        synapses and arrows.
    lw: float
        Line width for the cell body and line color for all the connections,
        synapses and arrows.
    **kwargs: key-word arguments
        Arguments passed on to `ax.text()` for drawing the `label`.

    """
    xy = np.asarray(xy)
    arx = 0.5*r
    ary = 0.4*arx
    # inputs:
    if xyinput is not None:
        xyinput = np.asarray(xyinput)
        rx = 1.2*r
        d = xyinput - xy
        dd = np.sqrt(np.dot(d, d))
        theta = np.arctan2(d[1], d[0])
        tt = mpl.transforms.Affine2D().rotate(theta)
        tt += mpl.transforms.Affine2D().translate(xy[0], xy[1])
        tt += ax.transData
        # input arrow:
        ax.plot((rx, dd), (0.0, 0.0), color=ec, lw=lw, clip_on=False,
                transform=tt)
        ax.plot((rx+arx, rx, rx+arx), (ary, 0.0, -ary), color=ec, lw=lw,
                clip_on=False, transform=tt)
    # targets:
    dm = None
    t = None
    if xytarget is not None and len(xytarget) > 0:
        if not isinstance(xytarget[0], (list, tuple)):
            xytarget = [xytarget]
        if not isinstance(synapse, (list, tuple)):
            synapse = [synapse]*len(xytarget)
        x = 0.5*r
        y = 0.4*x
        ym = None
        dm = np.zeros((len(xytarget), 2))
        for k, (xyt, syn) in enumerate(zip(xytarget, synapse)):
            xyt = np.asarray(xyt)
            d = xyt - xy
            dm[k,:] =  d
            dd = np.sqrt(np.dot(d, d))
            dd -= r
            theta = np.arctan2(d[1], d[0])
            tt = mpl.transforms.Affine2D().rotate(theta)
            tt += mpl.transforms.Affine2D().translate(xy[0], xy[1])
            tt += ax.transData
            if ym is None or ym < d[1]:
                t = tt
                ym = d[1]
            # synapse:
            if 'exc' in syn:
                dd -= x+0.2*r
                ax.plot((dd, dd+x, dd+x, dd), (0.0, -y, y, 0.0),
                        clip_on=False, color=ec, lw=lw, transform=tt)
            elif 'inh' in syn:
                dd -= 0.2*r
                ax.plot((dd, dd), (-y, y), color=ec, lw=lw,
                        clip_on=False, transform=tt)
            elif 'arr' in syn:
                dd -= 0.2*r
                ax.plot((dd-arx, dd, dd-arx), (-ary, 0.0, ary),
                        clip_on=False, color=ec, lw=lw, transform=tt)
            # axon:
            ax.plot((r, dd), (0.0, 0.0), color=ec, lw=lw,
                    clip_on=False, transform=tt)
    # adaptation:
    if adapt > 0:
        ar = 1.5*r
        if adapt == 1 and t is not None:
            t = mpl.transforms.Affine2D().rotate_deg(-30) + t
        elif adapt == 2 and dm is not None:
            dm = np.mean(dm, axis=0)
            theta = np.arctan2(-dm[1], -dm[0]) - 0.5*np.pi
            t = mpl.transforms.Affine2D().rotate(theta)
            t += mpl.transforms.Affine2D().translate(xy[0], xy[1])
            t += ax.transData
        else:
            t = mpl.transforms.Affine2D().translate(xy[0], xy[1])
            t += ax.transData
        ax.add_patch(mpl.patches.Arc((0.0, ar), ar, ar, 0.0, -50.0,
                                     220.0, transform=t,
                                     clip_on=False, color=ec, lw=lw))
        ax.plot([1.15*r, 1.2*r], [-0.35*r, 0.35*r], color=ec, lw=lw,
                clip_on=False,
                transform=mpl.transforms.Affine2D().rotate_deg(120) + t)
    # cell body:
    ax.add_patch(mpl.patches.Circle((xy[0], xy[1]), r, ec='none',
                                    fc=fc, lw=0, clip_on=False))
    ax.add_patch(mpl.patches.Circle((xy[0], xy[1]), r, ec=ec,
                                    fc='none', lw=lw, clip_on=False))
    # label:
    if label:
        figw, _ = ax.get_figure().get_size_inches()
        pw = ax.get_position().width * figw * 72.0
        aw = np.diff(ax.get_xlim())[0]
        fs = 'medium'
        if 'fs' in kwargs:
            fs = kwargs.pop('fs')
            kwargs['fontsize'] = fs
        if 'fontsize' in kwargs:
            fs = kwargs['fontsize']
        fp = mpl.font_manager.FontProperties(size=fs)
        cfs = fp.get_size_in_points()
        cf = cfs*aw/pw
        ax.text(xy[0]-0.03*cf, xy[1]-0.08*cf, label, ha='center',
                va='center', clip_on=False, **kwargs)


def install_neurons():
    """ Install neurons functions on matplotlib axes.

    This function is also called automatically upon importing the module.

    See also
    --------
    uninstall_neurons()
    """
    if not hasattr(mpl.axes.Axes, 'neuron'):
        mpl.axes.Axes.neuron = neuron

        
def uninstall_neurons():
    """ Uninstall neurons functions from matplotlib axes.

    Call this code to disable anything that was installed by `install_neurons()`.

    See also
    --------
    install_neurons()
    """
    if hasattr(mpl.axes.Axes, 'neuron'):
        delattr(mpl.axes.Axes, 'neuron')


install_neurons()
            
    
def demo():
    """ Run a demonstration of the neurons module.
    """
    fig, ax = plt.subplots()
    fig.suptitle('plottools.neurons')
    ax.set_aspect('equal')
    ax.set_xlim(0, 10)
    neuronstyle = dict(ec='gray', lw=1.0, fs='medium')
    neuronA = dict(fc='blue', **neuronstyle)
    neuronB = dict(fc='green', **neuronstyle)
    neuronT = dict(fc='orange', **neuronstyle)
    neuronS = dict(fc='yellow', **neuronstyle)
    neuronR = dict(fc='red', **neuronstyle)
    r = 0.6    # neuron radius
    d = 3.5    # short distance between neurons
    dd = 1.3*d # long distance between neurons
    ad = 0.7*d # input arrow length
    x = 2.5    # position of first neuron
    y = 0.35*d # y-position of two neurons
    yt = 1.8*y # y-position of three neurons
    nt = (x+dd, yt)
    ns = (x+dd, 0)
    nr = (x+dd, -yt)
    ax.neuron((x, y), r, 'L', [nt, ns, nr],
           ['exc', 'exc', 'inh'], 3, (x-ad, y), **neuronA)
    ax.neuron((x, -y), r, 'R', [nt, ns, nr],
           ['inh', 'exc', 'exc'], 3, (x-ad, -y), **neuronB)
    ax.neuron(nt, r, '$-$', (x+dd+d, yt), 'exc', adapt=1, **neuronT)
    ax.neuron(ns, r, '$+$', (x+dd+d, 0), 'exc', adapt=0, **neuronS)
    ax.neuron(nr, r, '$-$', (x+dd+d, -yt), 'exc', adapt=1, **neuronR)
    plt.show()


if __name__ == "__main__":
    demo()
    

