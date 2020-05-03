import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
from plottools.figure import install_figure
import plottools.spines
import plottools.ticks

    
def spines_figures():
    """ Generate figure demonstrating functionality of the spines module.
    """

    def new_figure():
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        fig, axs = plt.subplots(1, 3, figsize=(28, 10))
        fig.subplots_adjust(left=7.5, right=7.5, top=3.5, bottom=3.5, wspace=0.4)
        for ax in axs:
            x = np.linspace(0, 1, 200)
            y = np.sin(2*np.pi*5*x)
            ax.plot(x, y, lw=2)
            ax.set_xlim(0, 1)
            ax.set_xlabel('Time [ms]')
            ax.set_ylim(-1, 1)
            ax.set_ylabel('Voltage [mV]')
        return fig, axs

    def save_fig(fig, name):
        fig.savefig('spines-' + name + '.png')
        plt.close()
        
    install_figure()

    fig, axs = new_figure()
    axs[0].show_spines('lb')
    axs[1].show_spines('bt')
    axs[2].show_spines('tr')
    save_fig(fig, 'show')
    
    

if __name__ == "__main__":
    spines_figures()

