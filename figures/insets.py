import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
import plottools.figure
import plottools.subplots
import plottools.insets

    
def insets_figures():
    """ Generate figures demonstrating functionality of the insets module.
    """

    def new_figure():
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        fig, ax = plt.subplots(cmsize=(12, 8))
        fig.subplots_adjust(leftm=6.5, rightm=1.5, topm=0.5, bottomm=3.5)
        x = np.arange(-2.0, 5.0, 0.01)
        y = np.sin(2.0*np.pi*4.0*x)
        ax.plot(x, y)
        ax.set_xlim(-2.0, 5.0)
        ax.set_xlabel('Time [ms]')
        ax.set_ylim(-1.5, 4.5)
        ax.set_ylabel('Voltage [mV]')
        return fig, ax, x, y

    def label_corners(ax):
        ax.text(0.02, 0.02, '1', ha='left', va='bottom', fontweight='bold', transform=ax.transAxes)
        ax.text(0.98, 0.02, '2', ha='right', va='bottom', fontweight='bold', transform=ax.transAxes)
        ax.text(0.98, 0.98, '3', ha='right', va='top', fontweight='bold', transform=ax.transAxes)
        ax.text(0.02, 0.98, '4', ha='left', va='top', fontweight='bold', transform=ax.transAxes)
        
    def save_fig(fig, name):
        fig.savefig('insets-' + name + '.png')
        plt.close()

    fig, ax, _, _ = new_figure()
    axi = ax.inset((0.2, 0.6, 0.9, 0.95))
    x = np.linspace(0, 1, 50)
    axi.plot(x, x**2, 'r')
    save_fig(fig, 'inset')

    fig, ax, x, y = new_figure()
    axi = ax.zoomed_inset((0.2, 0.6, 0.9, 0.95), (0.0, -1.1, 2.0, 1.1),
                          ((4, 1), (3, 2)), lw=0.5)
    axi.plot(x, y)
    label_corners(axi)
    save_fig(fig, 'zoomed_inset')


if __name__ == "__main__":
    insets_figures()

