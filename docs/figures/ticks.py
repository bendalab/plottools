import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
import plottools.figure
import plottools.subplots
import plottools.spines
import plottools.ticks

    
def ticks_figures():
    """ Generate figure demonstrating functionality of the ticks module.
    """

    def new_figure():
        plt.rcParams['xtick.direction'] = 'out'
        fig, ax = plt.subplots(cmsize=(10, 1.2))
        fig.subplots_adjust(leftm=2, rightm=2, topm=0, bottomm=2.5)
        ax.set_ylim(0, 1)
        ax.show_spines('b')
        return fig, ax

    def save_fig(fig, name):
        fig.savefig('ticks-' + name + '.png')
        plt.close()
        
    fig, ax = new_figure()
    ax.set_xticks_delta(0.5)
    save_fig(fig, 'delta')

    fig, ax = new_figure()
    ax.set_xticks_format('%04.1f')
    save_fig(fig, 'format')

    fig, ax = new_figure()
    ax.set_xticks_fixed((0, 0.3, 1))
    save_fig(fig, 'fixed')

    fig, ax = new_figure()
    ax.set_xticks_fixed((0, 0.5, 1), ('a', 'b', 'c'))
    save_fig(fig, 'fixedlabels')

    fig, ax = new_figure()
    ax.set_xscale('log')
    ax.set_xlim(1e-6, 1e0)
    ax.set_xticks_prefix()
    save_fig(fig, 'prefix')

    fig, ax = new_figure()
    ax.set_xlim(-1, 1)
    ax.set_xticks_fracs(4)
    save_fig(fig, 'fracs')

    fig, ax = new_figure()
    ax.set_xlim(-np.pi, 2*np.pi)
    ax.set_xticks_pifracs(2)
    save_fig(fig, 'pifracs')

    fig, ax = new_figure()
    ax.set_xlim(0, 4*np.pi/3)
    ax.set_xticks_pifracs(3, True)
    save_fig(fig, 'pifracstop')

    fig, ax = new_figure()
    ax.set_xticks_blank()
    save_fig(fig, 'blank')

    fig, ax = new_figure()
    ax.set_xticks_off()
    save_fig(fig, 'off')
    

if __name__ == "__main__":
    ticks_figures()
