import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
from plottools.figure import install_figure
from plottools.spines import install_spines
import plottools.ticks

    
def spines_figures():
    """ Generate figures demonstrating functionality of the spines module.
    """

    def new_figure(fac=0.8, maxx=1, miny=-1, maxy=1, margin='all'):
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        fig, axs = plt.subplots(1, 3, cmsize=(28, 10))
        if margin == 'lb':
            fig.subplots_adjust(leftm=7.5, rightm=1.5, topm=0.5, bottomm=3.5, wspace=0.4)
        else:
            fig.subplots_adjust(leftm=7.5, rightm=7.5, topm=3.5, bottomm=3.5, wspace=0.4)
        for ax in axs:
            x = np.linspace(0, 1.5, 200)
            y = fac*np.sin(2*np.pi*5*x)
            ax.plot(x, y, lw=2)
            ax.set_xlim(0, maxx)
            ax.set_xticks_delta(0.2)
            ax.set_xlabel('Time [ms]')
            ax.set_ylim(miny, maxy)
            ax.set_yticks_delta(0.5)
            ax.set_ylabel('Voltage [mV]')
        return fig, axs

    def save_fig(fig, name):
        fig.savefig('spines-' + name + '.png')
        plt.close()
        
    install_figure()
    install_spines()

    fig, axs = new_figure()
    axs[0].show_spines('lb')
    axs[1].show_spines('bt')
    axs[2].show_spines('tr')
    save_fig(fig, 'show')

    fig, axs = new_figure(0.8, 1.1, -0.95, 0.95, 'lb')
    axs[0].show_spines('lb')
    axs[0].set_spines_bounds('lb', 'full')
    axs[1].show_spines('lb')
    axs[1].set_spines_bounds('lb', 'data')
    axs[2].show_spines('lb')
    axs[2].set_spines_bounds('lb', 'ticks')
    save_fig(fig, 'bounds')

    fig, axs = new_figure(1.0, 1.0, -1, 1, 'lb')
    axs[0].show_spines('lb')
    axs[0].set_spines_outward('lb', 0)
    axs[1].show_spines('lb')
    axs[1].set_spines_outward('lb', 10)
    axs[2].show_spines('lb')
    axs[2].set_spines_outward('lb', -10)
    save_fig(fig, 'outward')
    
    
if __name__ == "__main__":
    spines_figures()

