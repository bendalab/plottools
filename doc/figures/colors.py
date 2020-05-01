import numpy as np
import matplotlib.pyplot as plt
import plottoolspath
from plottools.figure import install_figure
import plottools.spines
from plottools.colors import color_palettes, lighter, darker, gradient

    
def colors_figures():
    """ Generate figures displaying the color palettes.
    """
    install_figure()
    for key, colors in color_palettes.items():
        fig, ax = plt.subplots(figsize=(1+2.2*len(colors), 3))
        fig.subplots_adjust(left=0, right=0, top=0, bottom=0)
        ax.show_spines('')
        rectx = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
        recty = np.array([0.0, 0.0, 1.0, 1.0, 0.0])
        for k, c in enumerate(colors):
            ax.fill(rectx + 1.2*k, recty, color=colors[c])
            ax.text(0.5 + 1.2*k, -0.3, c, ha='center')
        ax.set_xlim(-0.1, len(colors)*1.2 - 0.1)
        ax.set_ylim(-0.4, 1.02)
        fig.savefig('colors-' + key + '.png')

    
def lighter_figure():
    """ Generate figures demonstrating the lighter() function.
    """
    install_figure()
    color = color_palettes['muted']['blue']
    n = 10
    fig, ax = plt.subplots(figsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(left=0, right=0, top=0, bottom=0)
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
    install_figure()
    color = color_palettes['muted']['blue']
    n = 10
    fig, ax = plt.subplots(figsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(left=0, right=0, top=0, bottom=0)
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
    install_figure()
    c1 = color_palettes['muted']['blue']
    c2 = color_palettes['muted']['orange']
    n = 10
    fig, ax = plt.subplots(figsize=(1+2.2*(n+1), 3))
    fig.subplots_adjust(left=0, right=0, top=0, bottom=0)
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


if __name__ == "__main__":
    colors_figures()
    lighter_figure()
    darker_figure()
    gradient_figure()
