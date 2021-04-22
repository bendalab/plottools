import numpy as np
import matplotlib.pyplot as plt
from plottools.styles import demo as styles_demo
from plottools.colors import demo as colors_demo
from plottools.figure import demo as figure_demo
from plottools.spines import demo as spines_demo
from plottools.ticks import demo as ticks_demo
from plottools.labels import demo as labels_demo
from plottools.labels import uninstall_align_labels
from plottools.arrows import demo as arrows_demo
from plottools.text import demo as text_demo
from plottools.axes import demo as axes_demo
from plottools.insets import demo as insets_demo
from plottools.scalebars import demo as scalebars_demo
from plottools.significance import demo as significance_demo


if __name__ == "__main__":
    print('plottools.styles ...')
    styles_demo()
    uninstall_align_labels()

    print('plottools.colors ...')
    colors_demo()

    print('plottools.figure ...')
    figure_demo()

    print('plottools.spines ...')
    spines_demo()

    print('plottools.ticks ...')
    ticks_demo()

    print('plottools.labels ...')
    labels_demo()

    print('plottools.arrows ...')
    arrows_demo()

    print('plottools.text ...')
    text_demo()

    print('plottools.axes ...')
    axes_demo()
    
    print('plottools.insets ...')
    insets_demo()

    print('plottools.scalebars ...')
    scalebars_demo()

    print('plottools.significance ...')
    significance_demo()

