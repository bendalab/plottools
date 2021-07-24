"""
## Functions

- `versions()`: print python, numpy, matplotlib and plottools versions.
"""

import sys
import numpy as np
import matplotlib as mpl
try:
    import pandas as pd
    have_pandas = True
except ImportError:
    have_pandas = False


__pdoc__ = {}
__pdoc__['__version__'] = True
__pdoc__['__year__'] = True

__version__ = '0.9'
""" Version of the plottools package. """

__year__ = '2021'
""" Year of last changes to the plottools package. """


def versions():
    """ Print python, numpy, matplotlib and plottools versions.
    """
    print('python     version: %d.%d.%d' % (sys.version_info[:3]))
    print('numpy      version:', np.__version__)
    if have_pandas:
        print('pandas     version:', pd.__version__)
    print('matplotlib version:', mpl.__version__)
    print('plottools  version:', __version__)


if __name__ == "__main__":
    versions()
