"""
# Significance

Indicating statsitical significance.

- `significance_bar()`: horizontal bar with asterisks indicating significance level.

"""


def significance_bar(ax, p, x0, x1, y, **kwargs):
    """
    A horizontal bar with asterisks indicating significance level.
    
    Plot a horizontal bar from x0 to x1 at height y
    for indicating significance. On top of the bar plot
    asterisks according to the significance value p are drawn.
    If p > 0.05 nothing is plotted.

    Note: call this function AFTER ylim has been set!

    Parameters
    ----------
    ax: matplotlib axes
        Axes to which the inset is added.
    p: float
        Significance level.
    x0: float
        x-coordinate of starting point of significance bar in data units.
    x1: float
        x-coordinate of ending point of significance bar in data units.
    y: float
        y-coordinate of significance bar in data units.
    kwargs: key-word arguments
        Passed on to ax.text() used to print the asterisks.
    """
    if p < 0.001:
        ps = '***'
    elif p < 0.01:
        ps = '**'
    elif p < 0.05:
        ps = '*'
    else:
        return
    height = np.diff(ax.get_ylim())[0]
    dy = 0.03*height
    ax.plot([x0, x0, x1, x1], [y-dy, y, y, y-dy], color='black', lw=1,
            clip_on=False)
    ax.text(0.5*(x0+x1), y-0.2*dy, ps, ha='center', **kwargs)
    

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    x1 = 1.0+0.3*np.random.randn(50)
    x2 = 4.0+0.5*np.random.randn(50)
    ax.boxplot([x1, x2])
    ax.set_xlim(0.5, 2.5)
    ax.set_ylim(0.0, 8)
    significance_bar(ax, 0.002, 1, 2, 6)
    plt.show()
