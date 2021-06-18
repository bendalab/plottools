"""
Import all plottool modules and install their functions in matplotlib.


For importing all plottools modules, simply import this module
```py
import plottools.plottools as pt 
```

This also imports all the functions of the modules such they can be used
directly in the `pt` namespace. For example:
```py
light_blue = pt.lighter(pt.palettes['muted']['blue'], 0.4)
```
"""

from .align import install_align, uninstall_align, align_params
from .arrows import install_arrows, uninstall_arrows
from .arrows import arrow_style, generic_arrow_styles, plot_arrowstyles
from .aspect import install_aspect, install_aspect, uninstall_aspect
from .axes import axes_params
from .colors import colors_params, palettes, lighter, darker, gradient, colormap
from .common import install_common, uninstall_common
from .figure import figure_params, latex_include_figures, install_figure, uninstall_figure
from .grid import grid_params
from .insets import install_insets, uninstall_insets
from .labels import labels_params, install_labels, uninstall_labels
from .legend import legend_params, install_legend, uninstall_legend
from .neurons import install_neurons, uninstall_neurons
try:
    from .params import plot_params, paper_style, sketch_style, screen_style
except ImportError:
    pass  # when imported from params module
from .scalebars import scalebar_params, install_scalebars, uninstall_scalebars
from .significance import install_significance, uninstall_significance
from .styles import style, lighter_styles, darker_styles, lighter_darker_styles
from .styles import make_linestyles, make_pointstyles, make_linepointstyles
from .styles import make_fillstyles, plot_styles, generic_styles
from .styles import plot_linestyles, plot_pointstyles, plot_linepointstyles, plot_fillstyles
from .spines import spines_params, install_spines, uninstall_spines
from .subplots import install_subplots, uninstall_subplots
from .tag import tag_params, install_tag, uninstall_tag
from .text import text_params, install_text, uninstall_text
from .ticks import ticks_params, install_ticks, uninstall_ticks
from .version import __version__
