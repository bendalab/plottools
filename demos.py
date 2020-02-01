import numpy as np
import matplotlib.pyplot as plt
from plottools.axislabels import demo as axislabels_demo
from plottools.insets import demo as insets_demo
from plottools.labelaxes import demo as labelaxes_demo
from plottools.ticks import demo as ticks_demo
from plottools.spines import demo as spines_demo
from plottools.plotformat import demo as plotformat_demo
from plottools.scalebars import demo as scalebars_demo
from plottools.significance import demo as significance_demo


if __name__ == "__main__":

    print('plottools.axislabels ...')
    axislabels_demo()
    
    print('plottools.insets ...')
    insets_demo()

    print('plottools.labelaxes ...')
    labelaxes_demo()

    print('plottools.ticks ...')
    ticks_demo()

    print('plottools.spines ...')
    spines_demo()

    print('plottools.plotformat ...')
    plotformat_demo()

    print('plottools.scalebars ...')
    scalebars_demo()

    print('plottools.significance ...')
    significance_demo()

