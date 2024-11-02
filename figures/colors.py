import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
import plottools.figure
import plottools.subplots
import plottools.spines
from plottools.colors import palettes, lighter, darker, gradient, colormap
from plottools.colors import plot_colors, plot_complementary_colors
from plottools.colors import plot_color_comparison, plot_colormap

    
def colors_figures():
    """ Generate figures displaying the color palettes.
    """
    for key, colors in palettes.items():
        fig, ax = plt.subplots(cmsize=(1+2.2*len(colors), 3.3))
        fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
        ax.show_spines('')
        rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
        recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
        for k, c in enumerate(colors):
            ax.fill(rectx + 1.2*k, recty, color=colors[c])
            ax.text(0.5 + 1.2*k, -0.3, c, ha='center')
            ax.text(0.5 + 1.2*k, -0.6, colors[c], ha='center')
        ax.set_xlim(-0.1, len(colors)*1.2 - 0.1)
        ax.set_ylim(-0.7, 1.02)
        fig.savefig('colors-' + key + '.png')

    
def lighter_figure():
    """ Generate figures demonstrating the lighter() function.
    """
    color = palettes['muted']['blue']
    n = 10
    fig, ax = plt.subplots(cmsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
    ax.show_spines('')
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    for k in range(n+1):
        fac = 1.0-k/float(n)
        ax.fill(rectx + 1.2*k, recty, color=lighter(color, fac))
        ax.text(0.5 + 1.2*k, -0.3, '%.0f%%' % (100*fac), ha='center')
    ax.set_xlim(-0.1, (n+1)*1.2 - 0.1)
    ax.set_ylim(-0.4, 1.02)
    fig.savefig('colors-lighter.png')

    
def darker_figure():
    """ Generate figures demonstrating the darker() function.
    """
    color = palettes['muted']['blue']
    n = 10
    fig, ax = plt.subplots(cmsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
    ax.show_spines('')
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    for k in range(n+1):
        fac = 1.0-k/float(n)
        ax.fill(rectx + 1.2*k, recty, color=darker(color, fac))
        ax.text(0.5 + 1.2*k, -0.3, '%.0f%%' % (100*fac), ha='center')
    ax.set_xlim(-0.1, (n+1)*1.2 - 0.1)
    ax.set_ylim(-0.4, 1.02)
    fig.savefig('colors-darker.png')

    
def gradient_figure():
    """ Generate figures demonstrating the gradient() function.
    """
    c1 = palettes['muted']['blue']
    c2 = palettes['muted']['orange']
    n = 10
    fig, ax = plt.subplots(cmsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
    ax.show_spines('')
    rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
    for k in range(n+1):
        fac = k/float(n)
        ax.fill(rectx + 1.2*k, recty, color=gradient(c1, c2, fac))
        ax.text(0.5 + 1.2*k, -0.3, '%.0f%%' % (100*fac), ha='center')
    ax.set_xlim(-0.1, (n+1)*1.2 - 0.1)
    ax.set_ylim(-0.4, 1.02)
    fig.savefig('colors-gradient.png')

    
def colormap_figure():
    """ Generate a figure demonstrating the colormap() function.
    """
    fig, ax = plt.subplots(cmsize=(20.0, 4.0))
    fig.subplots_adjust(leftm=1.5, rightm=1.5, topm=0, bottomm=2)
    colors = palettes['muted']
    cmcolors = [colors['red'], lighter(colors['orange'], 0.85),
                lighter(colors['yellow'], 0.2), lighter(colors['lightblue'], 0.8),
                colors['blue']]
    cmvalues = [0.0, 0.25, 0.5, 0.8, 1.0]
    colormap('RYB', cmcolors, cmvalues)
    plot_colormap(ax, 'RYB', False)
    fig.savefig('colors-colormap.png')

    
def plotcolors_figure():
    """ Generate a figure demonstrating the plot_colors() function.
    """
    fig, ax = plt.subplots(cmsize=(35.0, 17.0))
    fig.subplots_adjust(leftm=1.5, rightm=1.5, topm=0, bottomm=0)
    ax.show_spines('')
    plot_colors(ax, palettes['muted'], 5)
    fig.savefig('colors-plotcolors.png')

    
def plotcomplementary_figure():
    """ Generate a figure demonstrating the plot_complementary_colors() function.
    """
    fig, ax = plt.subplots(cmsize=(25.0, 6.0))
    fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
    ax.show_spines('')
    plot_complementary_colors(ax, palettes['muted'])
    fig.savefig('colors-plotcomplementary.png')

    
def plotcomparison_figure():
    """ Generate a figure demonstrating the plot_color_comparison() function.
    """
    fig, ax = plt.subplots(cmsize=(35.0, 8.0))
    fig.subplots_adjust(leftm=0, rightm=0, topm=0, bottomm=0)
    ax.show_spines('')
    plot_color_comparison(ax, ('muted', 'vivid', 'plain'))
    fig.savefig('colors-plotcomparison.png')

    
def plotcolormap_figure():
    """ Generate a figure demonstrating the plot_colormap() function.
    """
    fig, ax = plt.subplots(cmsize=(20.0, 8.0))
    fig.subplots_adjust(leftm=1.5, rightm=1.5, topm=2, bottomm=2)
    plot_colormap(ax, 'jet', True)
    fig.savefig('colors-plotcolormap.png')

    
if __name__ == "__main__":
    colors_figures()
    lighter_figure()
    darker_figure()
    gradient_figure()
    colormap_figure()
    plotcolors_figure()
    plotcomplementary_figure()
    plotcomparison_figure()
    plotcolormap_figure()
