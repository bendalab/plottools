import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
import plottools.figure
import plottools.subplots
import plottools.spines
from plottools.scalebars import scalebar_params

    
def scalebars_figures():
    """ Generate figure demonstrating functionality of the scalebars module.
    """

    def draw_sine():
        fig, ax = plt.subplots(cmsize=(10, 6))
        fig.subplots_adjust(leftm=0.1, rightm=4, topm=0.1, bottomm=1.5)
        ax.show_spines('')
        f = 0.5
        x = np.linspace(0.0, 10.0, 200)
        ax.plot(x, np.sin(2.0*np.pi*f*x), lw=2)
        ax.set_xlim(0.0, 10.0)
        ax.set_ylim(-1.1, 1.1)
        return fig, ax

    def new_figure(w ,h):
        fig, ax = plt.subplots(cmsize=(w, h))
        fig.subplots_adjust(leftm=1, rightm=1, topm=1, bottomm=1)
        ax.show_spines('')
        ax.set_xlim(0.0, 10.0)
        ax.set_ylim(0.0, 5.0)
        return fig, ax

    def save_fig(fig, name):
        fig.savefig('scalebars-' + name + '.png')
        plt.close()

    def draw_anchor(ax, x, y):
        ax.plot(x, y, '.r', ms=20, transform=ax.transAxes, clip_on=False)
    
    scalebar_params(format_large='%.0f', format_small='%.1f', lw=3, capsize=0, clw=0.5)
    
    fig, ax = draw_sine()
    ax.scalebars(1.05, 0.0, 2, 1, 's', 'mV', ha='right', va='bottom')
    save_fig(fig, 'scalebars')
    
    fig, ax = draw_sine()
    ax.xscalebar(1.0, 0.0, 2, 's', ha='right', va='bottom')
    save_fig(fig, 'xscalebar')
    
    fig, ax = draw_sine()
    ax.yscalebar(1.05, 0.0, 1, 'mV', ha='right', va='bottom')
    save_fig(fig, 'yscalebar')

    fig, ax = new_figure(10, 3)
    ax.xscalebar(0.0, 0.8, 2, 'mm', ha='left', va='bottom', lw=3)
    ax.xscalebar(0.0, 0.3, 2, 'mm', ha='left', va='bottom', lw=6)
    ax.xscalebar(1.0, 0.8, 2, 'mm', ha='right', va='bottom', lw=4, capsize=4, clw=2)
    ax.xscalebar(1.0, 0.3, 2, 'mm', ha='right', va='bottom', lw=4, capsize=6, clw=1)
    save_fig(fig, 'styles')

    fig, ax = new_figure(10, 3)
    draw_anchor(ax, 0.0, 0.8)
    ax.xscalebar(0.0, 0.8, 2, 's', ha='left', va='top', lw=4)
    draw_anchor(ax, 0.5, 0.8)
    ax.xscalebar(0.5, 0.8, 2, 's', ha='center', va='top', lw=4)
    draw_anchor(ax, 1.0, 0.8)
    ax.xscalebar(1.0, 0.8, 2, 's', ha='right', va='top', lw=4)
    draw_anchor(ax, 0.0, 0.3)
    ax.xscalebar(0.0, 0.3, 2, 's', ha='left', va='bottom', lw=4)
    draw_anchor(ax, 0.5, 0.3)
    ax.xscalebar(0.5, 0.3, 2, 's', ha='center', va='bottom', lw=4)
    draw_anchor(ax, 1.0, 0.3)
    ax.xscalebar(1.0, 0.3, 2, 's', ha='right', va='bottom', lw=4)
    save_fig(fig, 'xpos')

    fig, ax = new_figure(5, 8)
    draw_anchor(ax, 0.3, 1.0)
    ax.yscalebar(0.3, 1.0, 1, 'mV', ha='left', va='top', lw=4)
    draw_anchor(ax, 0.3, 0.5)
    ax.yscalebar(0.3, 0.5, 1, 'mV', ha='left', va='center', lw=4)
    draw_anchor(ax, 0.3, 0.0)
    ax.yscalebar(0.3, 0.0, 1, 'mV', ha='left', va='bottom', lw=4)
    draw_anchor(ax, 0.7, 1.0)
    ax.yscalebar(0.7, 1.0, 1, 'mV', ha='right', va='top', lw=4)
    draw_anchor(ax, 0.7, 0.5)
    ax.yscalebar(0.7, 0.5, 1, 'mV', ha='right', va='center', lw=4)
    draw_anchor(ax, 0.7, 0.0)
    ax.yscalebar(0.7, 0.0, 1, 'mV', ha='right', va='bottom', lw=4)
    save_fig(fig, 'ypos')

    fig, ax = new_figure(10, 7)
    draw_anchor(ax, 0.2, 0.8)
    ax.scalebars(0.2, 0.8, 2, 1, 's', 'mV', ha='left', va='top')
    draw_anchor(ax, 0.8, 0.8)
    ax.scalebars(0.8, 0.8, 2, 1, 's', 'mV', ha='right', va='top')
    draw_anchor(ax, 0.2, 0.1)
    ax.scalebars(0.2, 0.1, 2, 1, 's', 'mV', ha='left', va='bottom')
    draw_anchor(ax, 0.8, 0.1)
    ax.scalebars(0.8, 0.1, 2, 1, 's', 'mV', ha='right', va='bottom')
    save_fig(fig, 'pos')


if __name__ == "__main__":
    scalebars_figures()
