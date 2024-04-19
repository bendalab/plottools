from src.plottools.align import demo as align_demo
from src.plottools.arrows import demo as arrows_demo
from src.plottools.aspect import demo as aspect_demo
from src.plottools.axes import demo as axes_demo
from src.plottools.circuits import demo as circuits_demo
from src.plottools.colors import demo as colors_demo
from src.plottools.common import demo as common_demo
from src.plottools.figure import demo as figure_demo
from src.plottools.grid import demo as grid_demo
from src.plottools.insets import demo as insets_demo
from src.plottools.labels import demo as labels_demo
from src.plottools.legend import demo as legend_demo
from src.plottools.neurons import demo as neurons_demo
from src.plottools.params import demo as params_demo
from src.plottools.scalebars import demo as scalebars_demo
from src.plottools.significance import demo as significance_demo
from src.plottools.spines import demo as spines_demo
from src.plottools.spines import install_spines, uninstall_spines
from src.plottools.styles import demo as styles_demo
from src.plottools.subplots import demo as subplots_demo
from src.plottools.tag import demo as tag_demo
from src.plottools.text import demo as text_demo
from src.plottools.ticks import demo as ticks_demo
from src.plottools.version import __version__, versions


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
