"""
Simplify production of publication-quality figures based on matplotlib.
"""

import sys

# avoid double inclusion of plottools modules if called as modules,
# e.g. python -m plottools.text`:
if not '-m' in sys.argv:

    from .version import __version__

# somehow pdoc3 gets confused by this:
#__all__ = ['figure',
#           'colors',
#           'spines',
#           'ticks',
#           'labels',
#           'axes',
#           'text',
#           'arrows',
#           'insets',
#           'scalebars',
#           'significance',
#           'styles']
