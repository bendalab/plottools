import __main__
from plottools.align import demo as align_demo
from plottools.arrows import demo as arrows_demo
from plottools.aspect import demo as aspect_demo
from plottools.axes import demo as axes_demo
from plottools.circuits import demo as circuits_demo
from plottools.colors import demo as colors_demo
from plottools.common import demo as common_demo
from plottools.figure import demo as figure_demo
from plottools.grid import demo as grid_demo
from plottools.insets import demo as insets_demo
from plottools.labels import demo as labels_demo
from plottools.legend import demo as legend_demo
from plottools.neurons import demo as neurons_demo
from plottools.params import demo as params_demo
from plottools.scalebars import demo as scalebars_demo
from plottools.significance import demo as significance_demo
from plottools.spines import demo as spines_demo
from plottools.spines import install_spines, uninstall_spines
from plottools.styles import demo as styles_demo
from plottools.subplots import demo as subplots_demo
from plottools.tag import demo as tag_demo
from plottools.text import demo as text_demo
from plottools.ticks import demo as ticks_demo
from plottools.version import __version__, versions


if __name__ == "__main__":
    versions()
    print()

    print('plottools.align ...')
    align_demo()
    print()

    print('plottools.arrows ...')
    arrows_demo()
    print()

    print('plottools.aspect ...')
    aspect_demo()
    print()

    print('plottools.axes ...')
    axes_demo()
    print()

    print('plottools.colors ...')
    colors_demo()
    print()

    print('plottools.circuits ...')
    circuits_demo()
    print()

    print('plottools.common ...')
    common_demo()
    print()

    print('plottools.figure ...')
    figure_demo()
    print()

    print('plottools.grid ...')
    grid_demo()
    print()
    
    print('plottools.insets ...')
    insets_demo()
    print()

    print('plottools.labels ...')
    labels_demo()
    print()

    print('plottools.legend ...')
    legend_demo()
    print()

    print('plottools.neurons ...')
    neurons_demo()
    print()

    print('plottools.params ...')
    params_demo()
    print()

    print('plottools.scalebars ...')
    scalebars_demo()
    print()

    print('plottools.significance ...')
    significance_demo()
    print()

    print('plottools.spines ...')
    spines_demo()
    uninstall_spines()
    print()
    
    print('plottools.styles ...')
    styles_demo()
    print()

    print('plottools.subplots ...')
    subplots_demo()
    print()

    print('plottools.tag ...')
    tag_demo()
    print()

    print('plottools.text ...')
    text_demo()
    print()

    print('plottools.ticks ...')
    ticks_demo()
    print()
